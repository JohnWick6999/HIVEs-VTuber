# HIVE's VTuber 数字人 API 接口文档

形象生成服务由外部平台提供，接口地址集中配置在 `utils/services.py` 的 `AVATAR_PLATFORM_BASE`（默认沿用上游平台地址，可替换为你自己的服务）。

## 1. 获取账户信息
说明: 通过密钥获取用户任务信息和余额

接口地址: POST AVATAR_PLATFORM_BASE/api/confirm

请求头:
Content-Type: application/json

请求参数:
```bash
{
    "password": ""
}
```
响应成功示例:
```bash
{
    "tasks": [
        {
            "task_id": "任务ID",
            "status": "任务状态",
            "avatar_url": "数字人缩略图URL",
            "video_url": "生成的视频URL",
            "video_asset_url": "生成的数字人资源URL",
            "errorMessage": "任务出错时的信息"
            "created_time": "创建时间",
            "updated_time": "更新时间",
        }
    ],
    "avatar_balance": "形象余额",
}
```
python代码示例：
```bash
import requests
import json
password = ""
url = AVATAR_PLATFORM_BASE + "/api/confirm"
headers = {
    "Content-Type": "application/json"
}
data = {
    "password": password
}
try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    print(result)
except:
    pass
```

## 2. 上传视频文件接口
说明: 上传文件创建数字人任务，返回任务ID和状态

接口地址: POST AVATAR_PLATFORM_BASE/api/upload

请求格式: multipart/form-data

请求参数:
- key: 用户密钥（必填）
- file: 视频/图片文件（必填，支持mp4/png/jpg格式，最大30MB）
- matting: 是否抠图（布尔值，true/false）
- keepsize: 是否保持分辨率（布尔值，true/false）
- reverse: 是否正反拼接视频来保证无缝循环（布尔值，true/false）
- task_id: 任务ID（选填，若无系统会自动生成唯一ID）

响应成功示例:
```bash
{
    "code": 0,
    "message": "操作成功",
    "data": {
       "avatar_id": avatar_id,
        "new_status": "pending"
    }
}
```

python代码示例：
```bash
import requests

def upload_video(password, file_path, matting=True, keepsize=False, reverse=True):
    url = AVATAR_PLATFORM_BASE + "/api/upload"

    files = {'file': open(file_path, 'rb')}
    data = {
        'key': password,
        'matting': str(matting).lower(),
        'keepsize': str(keepsize).lower(),
        'reverse': str(reverse).lower()
    }
    if callback_url:
        data['callback_url'] = callback_url

    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

# 使用示例
result = upload_video(
    password="your_password",
    file_path="video.mp4",
    matting=True,
)
print(result)
```
## 3. 查询任务状态接口

接口地址: GET AVATAR_PLATFORM_BASE/api/task/{task_id}

请求参数:
- task_id: 任务ID

响应成功示例:
```bash
{
    "task_id": "任务ID",
    "status": "任务状态",
    "avatar_url": "数字人缩略图URL",
    "video_url": "生成的视频URL",
    "video_asset_url": "生成的数字人资源URL",
    "errorMessage": "错误信息",
    "created_time": "创建时间",
    "updated_time": "更新时间"
}
```
python代码示例：
```bash
import requests

def get_task_status(task_id):
    url = f"{AVATAR_PLATFORM_BASE}/api/task/{task_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Query failed: {e}")
        return None

# 使用示例
task_info = get_task_status("your_task_id")
print(task_info)
```