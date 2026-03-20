import requests
from datetime import datetime
import json

# url = "http://127.0.0.1:8000/new_app/index/"           # 如果是完整地址请改成: "https://your-domain.com/new_app/index/"
# url = "https://example.com/new_app/index/"
url = "https://www.yzzhenli.org/new_app/index/"

today = datetime.now().strftime("%Y-%m-%d")
print(today)
data = {
    "date": today
}

response = requests.post(url, data=data,verify=False)   # 表单格式 (application/x-www-form-urlencoded)
response.json()
# 如果后端期待 JSON 格式，就改成下面这行：
# response = requests.post(url, json=data)

print("状态码:", response.status_code)
print("响应文本:",response.json())