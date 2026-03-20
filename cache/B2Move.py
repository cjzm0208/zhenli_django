import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo

# 1. 填这里（或使用环境变量更安全）
BUCKET_NAME = "yzzhenli"  # 改成你的桶名
APPLICATION_KEY_ID = os.getenv("B2_KEY_ID") or "0401003f654f"
APPLICATION_KEY = os.getenv("B2_APP_KEY") or "0047626fced5bfc6a05b22eb90baf03d4149cf3f00"

# 2. 要移动的年份文件夹
SOURCE_FOLDERS = ["2021-01"]
TARGET_FOLDER = "2021"

# ==================== 下面不用改 ====================
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", APPLICATION_KEY_ID, APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

total_copied = 0
total_deleted = 0

for folder in SOURCE_FOLDERS:
    copied = 0
    deleted = 0
    print(f"\n正在处理文件夹：{folder}/  →  {TARGET_FOLDER}/")

    # 递归列出该文件夹下所有文件
    for file_version, _folder_name in bucket.ls(f"{folder}/", recursive=True):
        old_name = file_version.file_name  # 例如 2021-01/photos/DSC001.jpg
        # 新路径：提取 folder 之后的路径部分
        relative_path = old_name[len(folder)+1:]
        new_name = f"{TARGET_FOLDER}/{relative_path}"

        print(f"  复制 {old_name}  →  {new_name}")
        # 修正：使用 b2_api.copy_file 而不是 bucket.copy_file
        b2_api.copy_file(
            file_id=file_version.id_,
            new_file_name=new_name,
            destination_bucket_id=bucket.id_
        )
        copied += 1

        # 删除原文件（第一次运行建议先注释掉这三行，确认没问题再打开）
        print(f"  删除原文件 {old_name}")
        b2_api.delete_file_version(file_version.id_, old_name)
        deleted += 1

    print(f"✔ {folder} 完成：复制 {copied} 个，删除 {deleted} 个")
    total_copied += copied
    total_deleted += deleted

print(f"\n大功告成！共复制 {total_copied} 个文件，删除 {total_deleted} 个原文件")
print(f"请到 Backblaze Web 控制台确认 {TARGET_FOLDER}/ 已经出现，原 {SOURCE_FOLDERS} 文件夹已经为空")