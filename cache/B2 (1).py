#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 CSV 读取 VOD 文件,转码为多分辨率版本并上传到 Backblaze B2
- 下载原始视频
- 转码为多个分辨率 (1080p, 720p, 480p, 360p)
- 生成 HLS (m3u8) 自适应流
- 上传所有文件到 B2
"""

import csv
import os
import subprocess
import json
import requests
from urllib.parse import urlparse
from datetime import datetime
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from b2sdk.v2.exception import B2Error
import shutil

# ================== 配置区 ==========304========
# Backblaze B2 配置
B2_KEY_ID = "0401003f654f"
B2_APPLICATION_KEY = "0047626fced5bfc6a05b22eb90baf03d4149cf3f00"
B2_BUCKET_NAME = "yzzhenli"
B2_FOLDER = "video"  # 目标文件夹

# CSV 文件路径
CSV_FILE = "vod_files_20251211_224353.csv"

# 本地工作目录
DOWNLOAD_DIR = "./downloads"  # 原始下载
TRANSCODE_DIR = "./transcoded"  # 转码输出
KEEP_ORIGINAL = False  # 是否保留原始下载文件
KEEP_TRANSCODED = True  # 是否保留转码文件

# 转码配置
RESOLUTIONS = {
    "1080p": {"width": 1920, "height": 1080, "bitrate": "5000k", "audio_bitrate": "192k"},
    "720p": {"width": 1280, "height": 720, "bitrate": "3000k", "audio_bitrate": "128k"},
    "480p": {"width": 854, "height": 480, "bitrate": "1500k", "audio_bitrate": "128k"},
    "360p": {"width": 640, "height": 360, "bitrate": "800k", "audio_bitrate": "96k"},
}

# HLS 配置
HLS_SEGMENT_TIME = 10  # 每个 TS 分片的秒数

# 日志文件
LOG_FILE = f"transcode_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# 下载配置
CHUNK_SIZE = 8 * 1024 * 1024
TIMEOUT = 300


# ==========================================

class VideoTranscoder:
    def __init__(self):
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        self.bucket = None

        # 创建工作目录
        for directory in [DOWNLOAD_DIR, TRANSCODE_DIR]:
            os.makedirs(directory, exist_ok=True)

        # 检查 ffmpeg
        if not self.check_ffmpeg():
            raise Exception("ffmpeg 未安装或不在 PATH 中")

    def check_ffmpeg(self):
        """检查 ffmpeg 是否可用"""
        try:
            result = subprocess.run(['ffmpeg', '-version'],
                                    capture_output=True, text=True)
            print("✓ ffmpeg 已就绪\n")
            return True
        except FileNotFoundError:
            print("✗ ffmpeg 未找到")
            print("请安装 ffmpeg: https://ffmpeg.org/download.html")
            return False

    def connect_b2(self):
        """连接到 B2"""
        print(f"正在连接 Backblaze B2...")
        try:
            self.b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
            self.bucket = self.b2_api.get_bucket_by_name(B2_BUCKET_NAME)
            print(f"✓ 已连接到存储桶: {B2_BUCKET_NAME}\n")
            return True
        except B2Error as e:
            print(f"✗ B2 连接失败: {e}")
            return False

    def download_video(self, url, output_path):
        """下载视频文件"""
        try:
            print(f"    下载中...")
            response = requests.get(url, stream=True, timeout=TIMEOUT)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"    ✓ 已下载 ({size_mb:.2f} MB)")
            return True
        except Exception as e:
            print(f"    ✗ 下载失败: {e}")
            return False

    def get_video_info(self, video_path):
        """获取视频信息"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"    警告: 无法获取视频信息: {e}")
            return None

    def transcode_video(self, input_path, output_dir, base_name):
        """转码视频为多个分辨率"""
        print(f"    转码中...")

        # 获取原始视频信息
        video_info = self.get_video_info(input_path)
        original_height = 1080  # 默认值

        if video_info:
            for stream in video_info.get('streams', []):
                if stream.get('codec_type') == 'video':
                    original_height = stream.get('height', 1080)
                    break

        transcoded_files = []

        # 为每个分辨率转码
        for res_name, res_config in RESOLUTIONS.items():
            # 如果原始分辨率小于目标分辨率,跳过
            if original_height < res_config['height']:
                print(f"      跳过 {res_name} (原始分辨率较低)")
                continue

            output_file = os.path.join(output_dir, f"{base_name}_{res_name}.mp4")

            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libx264',  # 视频编码器
                '-preset', 'medium',  # 编码速度 (faster/fast/medium/slow)
                '-crf', '23',  # 质量控制 (18-28, 越小质量越好)
                '-vf', f"scale={res_config['width']}:{res_config['height']}",
                '-b:v', res_config['bitrate'],
                '-maxrate', res_config['bitrate'],
                '-bufsize', str(int(res_config['bitrate'].rstrip('k')) * 2) + 'k',
                '-c:a', 'aac',  # 音频编码器
                '-b:a', res_config['audio_bitrate'],
                '-movflags', '+faststart',  # 优化流媒体播放
                '-y',  # 覆盖输出文件
                output_file
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True)
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"      ✓ {res_name}: {size_mb:.2f} MB")
                transcoded_files.append({
                    'resolution': res_name,
                    'path': output_file,
                    'size': os.path.getsize(output_file)
                })
            except subprocess.CalledProcessError as e:
                print(f"      ✗ {res_name} 转码失败")

        return transcoded_files

    def generate_hls(self, input_path, output_dir, base_name):
        """生成 HLS 自适应流"""
        print(f"    生成 HLS...")

        hls_dir = os.path.join(output_dir, f"{base_name}_hls")
        os.makedirs(hls_dir, exist_ok=True)

        master_playlist = os.path.join(hls_dir, "master.m3u8")

        # 构建 ffmpeg 命令 (多码率 HLS)
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', str(HLS_SEGMENT_TIME),
            '-hls_playlist_type', 'vod',
            '-hls_segment_filename', os.path.join(hls_dir, f'{base_name}_%03d.ts'),
            '-master_pl_name', 'master.m3u8',
            os.path.join(hls_dir, f'{base_name}.m3u8')
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)

            # 统计生成的文件
            hls_files = [f for f in os.listdir(hls_dir) if f.endswith(('.m3u8', '.ts'))]
            print(f"      ✓ HLS 生成完成 ({len(hls_files)} 个文件)")

            return hls_dir, hls_files
        except subprocess.CalledProcessError as e:
            print(f"      ✗ HLS 生成失败")
            return None, []

    def upload_to_b2(self, local_path, b2_path, file_metadata=None):
        """上传单个文件到 B2"""
        try:
            self.bucket.upload_local_file(
                local_file=local_path,
                file_name=b2_path,
                file_info=file_metadata or {}
            )
            return True
        except B2Error as e:
            print(f"      ✗ 上传失败: {e}")
            return False

    def process_video(self, row, video_id):
        """处理单个视频"""
        url = row.get('URL', '').strip()
        name = row.get('Name', '未命名')
        file_id = row.get('FileId', '')

        if not url:
            return False

        original_filename = os.path.basename(urlparse(url).path)
        base_name = os.path.splitext(original_filename)[0]

        # 创建视频专属目录
        video_output_dir = os.path.join(TRANSCODE_DIR, base_name)
        os.makedirs(video_output_dir, exist_ok=True)

        # 下载原始视频
        download_path = os.path.join(DOWNLOAD_DIR, original_filename)

        if not os.path.exists(download_path):
            if not self.download_video(url, download_path):
                return False
        else:
            print(f"    使用本地缓存")

        # 转码为多分辨率
        transcoded_files = self.transcode_video(download_path, video_output_dir, base_name)

        if not transcoded_files:
            print(f"    ✗ 转码失败")
            return False

        # 生成 HLS
        hls_dir, hls_files = self.generate_hls(download_path, video_output_dir, base_name)

        # 上传所有文件
        print(f"    上传到 B2...")

        file_metadata = {
            'original_name': name,
            'file_id': file_id,
            'upload_time': datetime.now().isoformat()
        }

        upload_count = 0

        # 上传转码后的 MP4 文件
        for tf in transcoded_files:
            b2_path = f"{B2_FOLDER}/{base_name}/{os.path.basename(tf['path'])}"
            if self.upload_to_b2(tf['path'], b2_path, file_metadata):
                upload_count += 1

        # 上传 HLS 文件
        if hls_dir and hls_files:
            for hls_file in hls_files:
                local_hls_path = os.path.join(hls_dir, hls_file)
                b2_hls_path = f"{B2_FOLDER}/{base_name}/hls/{hls_file}"
                if self.upload_to_b2(local_hls_path, b2_hls_path, file_metadata):
                    upload_count += 1

        print(f"      ✓ 已上传 {upload_count} 个文件")

        # 清理临时文件
        if not KEEP_ORIGINAL and os.path.exists(download_path):
            os.remove(download_path)

        if not KEEP_TRANSCODED and os.path.exists(video_output_dir):
            shutil.rmtree(video_output_dir)

        return True

    def process_csv(self, csv_file, start_index=1):
        """处理 CSV 文件中的所有视频"""
        # 读取 CSV
        print(f"读取 CSV 文件: {csv_file}")
        rows = []
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            print(f"✓ 读取到 {len(rows)} 条记录")
            print(f"⚠️  将从第 {start_index} 行开始处理\n")
        except Exception as e:
            print(f"✗ 读取 CSV 失败: {e}")
            return

        print("=" * 80)
        print("开始处理视频")
        print("=" * 80)

        success_count = 0
        fail_count = 0
        skip_count = start_index - 1

        with open(LOG_FILE, 'w', encoding='utf-8') as log:
            log.write(f"转码日志 - {datetime.now()}\n")
            log.write(f"从第 {start_index} 行开始处理\n")
            log.write("=" * 80 + "\n\n")

            for i, row in enumerate(rows, 1):
                name = row.get('Name', '未命名')
                url = row.get('URL', '')

                if not url:
                    continue

                # 跳过前面的行
                if i < start_index:
                    continue

                print(f"\n[{i}/{len(rows)}] {name}")

                if self.process_video(row, i):
                    success_count += 1
                    log.write(f"[SUCCESS] [{i}] {name}\n")
                else:
                    fail_count += 1
                    log.write(f"[FAIL] [{i}] {name} - {url}\n")

        # 打印汇总
        print("\n" + "=" * 80)
        print("处理完成")
        print("=" * 80)
        print(f"总计: {len(rows)} 个视频")
        print(f"跳过: {skip_count} (前 {start_index - 1} 行)")
        print(f"成功: {success_count}")
        print(f"失败: {fail_count}")
        print(f"\n下载目录: {DOWNLOAD_DIR}")
        print(f"转码目录: {TRANSCODE_DIR}")
        print(f"日志文件: {LOG_FILE}")


def main():
    print("=" * 80)
    print("VOD 视频转码并上传到 Backblaze B2")
    print("=" * 80)
    print()

    # 检查 CSV 文件
    if not os.path.exists(CSV_FILE):
        print(f"✗ CSV 文件不存在: {CSV_FILE}")
        return

    # 创建转码器
    transcoder = VideoTranscoder()

    # 连接 B2
    if not transcoder.connect_b2():
        return

    # 询问从哪一行开始
    start_line = input("从第几行开始处理? (默认 1，输入 278 从第 278 行开始): ").strip()
    start_index = int(start_line) if start_line.isdigit() else 1

    if start_index > 1:
        print(f"\n✓ 将从第 {start_index} 行开始处理\n")

    # 开始处理
    transcoder.process_csv(CSV_FILE, start_index)


if __name__ == "__main__":
    main()