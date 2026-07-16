import os
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from b2sdk.v2.exception import B2Error

# ================= 配置参数 =================
BUCKET_NAME = "yzzhenli"
LOCAL_DIR = "/www/Zhenli/static/upload/2026"
REMOTE_PREFIX = "2026"  # 云端的目标文件夹

# Backblaze B2 凭据 (请替换为你的实际信息)
B2_KEY_ID = "0401003f654f"
B2_APPLICATION_KEY = "0047626fced5bfc6a05b22eb90baf03d4149cf3f00"

# 常见图片后缀过滤
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')


# ============================================

def get_b2_bucket():
    """初始化 B2 API 并获取 Bucket 对象"""
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)

    print("正在连接 Backblaze B2...")
    # 授权登录
    b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
    # 获取指定的桶
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)
    return bucket


def upload_images():
    # 1. 检查本地目录
    if not os.path.exists(LOCAL_DIR):
        print(f"❌ 本地目录不存在: {LOCAL_DIR}")
        return

    # 2. 连接 B2
    try:
        bucket = get_b2_bucket()
    except B2Error as e:
        print(f"❌ B2 授权或获取桶失败: {e}")
        return

    print("正在扫描本地图片并开始上传...")

    # 确保本地路径结尾没有斜杠，方便后续计算相对路径
    base_dir = os.path.normpath(LOCAL_DIR)

    success_count = 0
    total_count = 0

    # 3. 递归遍历文件夹
    for root, _, files in os.walk(base_dir):
        for file in files:
            # 过滤图片文件
            if file.lower().endswith(IMAGE_EXTENSIONS):
                total_count += 1
                local_file_path = os.path.join(root, file)

                # 计算相对路径，例如: subdir/image.jpg
                relative_path = os.path.relpath(local_file_path, base_dir)

                # 拼接 B2 上的最终路径，例如: 2026/subdir/image.jpg
                # B2 云端统一使用正斜杠 '/'
                if REMOTE_PREFIX:
                    remote_file_path = os.path.join(REMOTE_PREFIX, relative_path).replace('\\', '/')
                else:
                    remote_file_path = relative_path.replace('\\', '/')

                # 执行上传
                print(f"正在上传 [{total_count}]: {relative_path} -> b2://{BUCKET_NAME}/{remote_file_path}")

                # b2sdk 会自动处理大文件的分块上传以及多线程优化
                bucket.upload_local_file(
                    local_file=local_file_path,
                    file_name=remote_file_path
                )
                success_count += 1

    print("\n--- 上传任务结束 ---")
    print(f"应上传图片数: {total_count}")
    print(f"成功上传数量: {success_count}")
    if success_count < total_count:
        print(f"失败数量: {total_count - success_count}")


if __name__ == "__main__":
    upload_images()