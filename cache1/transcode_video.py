import os
import subprocess
import json
RESOLUTIONS = {
            "1080p": {"width": 1920, "height": 1080, "bitrate": "5000k", "audio_bitrate": "192k"},
            "720p": {"width": 1280, "height": 720, "bitrate": "3000k", "audio_bitrate": "128k"},
            "480p": {"width": 854, "height": 480, "bitrate": "1500k", "audio_bitrate": "128k"},
            "360p": {"width": 640, "height": 360, "bitrate": "800k", "audio_bitrate": "96k"},
        }


def get_video_info(video_path):
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
def generate_hls(input_path, output_dir, base_name):
    HLS_SEGMENT_TIME = 10  # 每个 TS 分片的秒数
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
def transcode_video(input_path, output_dir, base_name):
    """转码视频为多个分辨率"""
    print(f"    转码中...")

    # 获取原始视频信息
    video_info = get_video_info(input_path)
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
            '-preset', 'medium',
            '-crf', '23',
            '-vf', f"scale={res_config['width']}:{res_config['height']}",
            '-b:v', res_config['bitrate'],
            '-maxrate', res_config['bitrate'],
            '-bufsize', str(int(res_config['bitrate'].rstrip('k')) * 2) + 'k',
            '-c:a', 'aac',  # 音频编码器
            '-strict', '-2',  # <--- 关键修改：允许使用实验性的 AAC 编码器
            '-b:a', res_config['audio_bitrate'],
            '-movflags', '+faststart',
            '-y',
            output_file
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"      ✓ {res_name}: {size_mb:.2f} MB")
        transcoded_files.append({
            'resolution': res_name,
            'path': output_file,
            'size': os.path.getsize(output_file)
        })

        if not transcoded_files:
            print(f"    ✗ 转码失败")
            return False

        # 生成 HLS
        hls_dir, hls_files = generate_hls(input_path, output_dir, base_name)
    return transcoded_files

# transcode_video("22-12.mp4", "result", "22-12")
hls_dir, hls_files = generate_hls("22-12.mp4", "result", "22-12")