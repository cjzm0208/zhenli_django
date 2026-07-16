#!/usr/bin/env python3
"""
Backblaze B2 MP3 批量转码脚本
════════════════════════════════════════
功能：
  - 扫描 B2 Bucket 中所有 MP3 文件
  - 跳过已经是 128kbps 的文件
  - 将其他比特率的文件转码为 128kbps（保留 ID3 标签）
  - 上传回原路径，文件名与目录结构完全不变
  - 转码/上传完成后自动清理本地临时文件
  - 所有操作写入 b2_convert.log

依赖安装：
  pip install b2sdk
  # macOS:   brew install ffmpeg
  # Ubuntu:  sudo apt install ffmpeg
"""

import os
import sys
import shutil
import subprocess
import tempfile
import logging
from pathlib import Path

# ════════════════════════════════════════════════
# ★ 填写你的 Backblaze B2 凭据
B2_KEY_ID      = "0401003f654f"   # B2 Application Key ID
B2_APP_KEY     = "0047626fced5bfc6a05b22eb90baf03d4149cf3f00"       # B2 Application Key
B2_BUCKET_NAME = "yzzhenli"           # Bucket 名称

# 可选：只处理某个子目录，留空则处理整个 Bucket
# 例如：B2_FOLDER_PREFIX = "podcasts/2024/"
B2_FOLDER_PREFIX = ""
# ════════════════════════════════════════════════

TARGET_BITRATE = 128  # 目标比特率 kbps
BITRATE_MARGIN = 2  # 容差：127~129 kbps 均视为 128，避免重复转码
TARGET_SAMPLERATE = 44100  # 目标采样率 Hz（44.1kHz）
TEMP_DIR = tempfile.mkdtemp(prefix="b2_mp3_")
DONE_FILE = "b2_done.txt"  # 断点续传记录文件

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("b2_convert.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


# ── 检查系统依赖 ────────────────────────────────
def check_dependencies():
    try:
        import b2sdk  # noqa: F401
    except ImportError:
        log.error("缺少 b2sdk，请运行：pip install b2sdk")
        sys.exit(1)

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            log.error(f"未找到 {tool}，请先安装 ffmpeg")
            sys.exit(1)

    log.info("依赖检查通过 ✓")


# ── 用 ffprobe 读取音频属性 ────────────────────
def get_audio_info(file_path: str) -> dict:
    """返回 {'bitrate': int(kbps), 'samplerate': int(Hz)}，读取失败对应值为 None。"""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=bit_rate,sample_rate",
        "-of", "default=noprint_wrappers=1",
        file_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = {"bitrate": None, "samplerate": None}

    for line in result.stdout.splitlines():
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip()
        if not val.isdigit():
            continue
        if key == "bit_rate":
            info["bitrate"] = int(val) // 1000
        elif key == "sample_rate":
            info["samplerate"] = int(val)

    # 比特率回退：从容器格式层读取
    if info["bitrate"] is None:
        cmd2 = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path,
        ]
        raw = subprocess.run(cmd2, capture_output=True, text=True).stdout.strip()
        if raw.isdigit():
            info["bitrate"] = int(raw) // 1000

    return info


# ── 转码（128kbps + 44.1kHz）──────────────────
def convert(src: str, dst: str) -> bool:
    """用 ffmpeg 将 src 转为 128kbps / 44100Hz MP3，保留所有 ID3 标签。"""
    cmd = [
        "ffmpeg", "-y",
        "-i", src,
        "-codec:a", "libmp3lame",
        "-b:a", f"{TARGET_BITRATE}k",
        "-ar", str(TARGET_SAMPLERATE),  # 采样率 44100 Hz
        "-map_metadata", "0",  # 保留 ID3 元数据
        "-id3v2_version", "3",  # 兼容性最好的 ID3v2.3
        dst,
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        # 2. 在解码时加上 errors="replace" 或 "ignore"，防止崩溃
        # ffmpeg 的主要信息通常在 stderr 中
        stderr_str = result.stderr.decode('utf-8', errors='replace')
        log.error(f"  ffmpeg 错误:\n{stderr_str[-500:]}")
        return False
    return True


# ── 清理临时文件 ────────────────────────────────
def cleanup(*paths: str):
    for p in paths:
        if p and os.path.isfile(p):
            try:
                os.remove(p)
            except OSError:
                pass


def _mark_done(remote_name: str):
    """将文件名追加到断点续传记录文件。"""
    with open(DONE_FILE, "a", encoding="utf-8") as f:
        f.write(remote_name + "\n")


# ── 主流程 ──────────────────────────────────────
def main():
    check_dependencies()

    from b2sdk.v2 import InMemoryAccountInfo, B2Api

    log.info("正在登录 Backblaze B2 ...")
    info = InMemoryAccountInfo()
    api = B2Api(info)
    api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)
    log.info("登录成功 ✓")

    bucket = api.get_bucket_by_name(B2_BUCKET_NAME)
    log.info(f"已连接 Bucket: {B2_BUCKET_NAME}")

    # ── 列出所有 MP3 ──────────────────────────────
    log.info(f"扫描 MP3 文件（前缀: '{B2_FOLDER_PREFIX or '/'}'）...")
    all_files = [
        fv
        for fv, _ in bucket.ls(
            folder_to_list=B2_FOLDER_PREFIX,
            recursive=True,
            latest_only=True,
        )
        if fv.file_name.lower().endswith(".mp3")
    ]
    total = len(all_files)
    log.info(f"共找到 {total} 个 MP3 文件\n{'─' * 50}")

    # ── 断点续传：读取已完成记录 ─────────────────
    if os.path.exists(DONE_FILE):
        with open(DONE_FILE, encoding="utf-8") as f:
            done_set = set(line.strip() for line in f if line.strip())
        log.info(f"已找到断点记录，跳过 {len(done_set)} 个已处理文件")
    else:
        done_set = set()

    converted = skipped = failed = 0

    for idx, fv in enumerate(all_files, 1):
        remote_name = fv.file_name
        base_name = Path(remote_name).name
        local_dl = os.path.join(TEMP_DIR, f"orig_{idx}_{base_name}")
        local_out = os.path.join(TEMP_DIR, f"conv_{idx}_{base_name}")

        log.info(f"[{idx}/{total}] {remote_name}")

        # 断点续传：已处理过则跳过
        if remote_name in done_set:
            log.info("  → 已处理过，跳过")
            skipped += 1
            continue

        # 1. 下载
        try:
            bucket.download_file_by_name(remote_name).save_to(local_dl)
        except Exception as e:
            log.error(f"  ✗ 下载失败: {e}")
            failed += 1
            cleanup(local_dl)
            continue

        # 2. 检测比特率 + 采样率
        info = get_audio_info(local_dl)
        bitrate = info["bitrate"]
        samplerate = info["samplerate"]

        if bitrate is None:
            log.warning("  ⚠ 无法读取音频信息，已跳过")
            skipped += 1
            cleanup(local_dl)
            continue

        log.info(f"  比特率: {bitrate} kbps  采样率: {samplerate} Hz")

        bitrate_ok = abs(bitrate - TARGET_BITRATE) <= BITRATE_MARGIN
        samplerate_ok = (samplerate == TARGET_SAMPLERATE)

        if bitrate_ok and samplerate_ok:
            log.info(f"  → 已是 {TARGET_BITRATE}kbps / {TARGET_SAMPLERATE}Hz，跳过")
            skipped += 1
            cleanup(local_dl)
            _mark_done(remote_name)
            continue

        reasons = []
        if not bitrate_ok:
            reasons.append(f"{bitrate}kbps → {TARGET_BITRATE}kbps")
        if not samplerate_ok:
            reasons.append(f"{samplerate}Hz → {TARGET_SAMPLERATE}Hz")
        log.info(f"  → 转码: {', '.join(reasons)}")

        # 3. 转码
        if not convert(local_dl, local_out):
            log.error("  ✗ 转码失败，跳过上传")
            failed += 1
            cleanup(local_dl, local_out)
            continue

        # 4. 上传回原路径（文件名不变）
        try:
            bucket.upload_local_file(
                local_file=local_out,
                file_name=remote_name,  # 保持原路径和文件名
                content_type="audio/mpeg",
            )
            log.info(f"  ✓ 上传成功")
            converted += 1
            _mark_done(remote_name)  # 记录已完成
        except Exception as e:
            log.error(f"  ✗ 上传失败: {e}")
            failed += 1
        finally:
            cleanup(local_dl, local_out)

    # 清理临时目录
    try:
        os.rmdir(TEMP_DIR)
    except OSError:
        pass

    # 汇总
    log.info("\n" + "═" * 50)
    log.info("全部完成！")
    log.info(f"  ✓ 转码并上传 : {converted} 个")
    log.info(f"  → 跳过(已128k): {skipped} 个")
    log.info(f"  ✗ 失败        : {failed} 个")
    log.info("详细日志已保存到 b2_convert.log")
    log.info("═" * 50)


if __name__ == "__main__":
    main()