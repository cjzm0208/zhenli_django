import requests
import json

BASE_URL = "https://www.yzzhenli.org"
URL = f"{BASE_URL}/new_app/get_office/"

# 请求参数
payload = {"date": "2026-06-17"}

print(f"正在发送表单请求到: {URL}")

try:
    # 💡 核心修改：使用 data= 替代 json=
    # data= 会以 application/x-www-form-urlencoded 格式发送数据，Django 的 request.POST 就能抓到了
    response = requests.post(URL, data=payload)

    print(f"HTTP 状态码: {response.status_code}")
    if response.status_code == 200:
        res = response.json()
        print("\n返回的 JSON 数据：")
        print(json.dumps(res, indent=4, ensure_ascii=False))
    else:
        print(f"❌ 错误内容:\n{response.text}")

except Exception as e:
    print(f"❌ 发生错误: {e}")