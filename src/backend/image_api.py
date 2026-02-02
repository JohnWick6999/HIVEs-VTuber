import requests
import base64
import os
from typing import Dict, Any
from config import config_manager

class ImageAPISystem:
    """图片识别API系统类"""
    
    def __init__(self):
        """初始化图片识别API系统"""
        self.image_config = config_manager.get_image_api_config()
        # 图片大小限制，避免API调用失败
        self.max_image_size = 10 * 1024 * 1024  # 10MB
    
    def recognize_image(self, image_path: str) -> str:
        """识别图片内容"""
        try:
            api_key = self.image_config.get("api_key")
            base_url = self.image_config.get("base_url")
            
            # 检查图片文件是否存在
            if not os.path.exists(image_path):
                return "图片文件不存在"
            
            # 检查图片大小
            if os.path.getsize(image_path) > self.max_image_size:
                return "图片文件过大"
            
            # 如果没有配置API，返回错误信息
            if not api_key or not base_url:
                return "请配置图片识别API"
            
            # 根据不同的API提供商选择不同的调用方式
            if "gemini" in base_url.lower():
                return self._gemini_image_recognition(api_key, base_url, image_path)
            elif "glm" in base_url.lower():
                return self._glm_image_recognition(api_key, base_url, image_path)
            elif "azure" in base_url.lower():
                return self._azure_image_recognition(api_key, base_url, image_path)
            else:
                # 默认使用通用的图片识别API调用方式
                return self._generic_image_recognition(api_key, base_url, image_path)
        except Exception as e:
            print(f"图片识别失败: {e}")
            return "图片识别失败"
    
    def _gemini_image_recognition(self, api_key: str, base_url: str, image_path: str) -> str:
        """使用Gemini API进行图片识别"""
        try:
            # 读取图片并编码为base64
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "gemini-pro-vision",
                "contents": [
                    {
                        "parts": [
                            {"text": "请描述图片中的内容"},
                            {
                                "inline_data": {
                                    "mime_type": self._get_mime_type(image_path),
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024
                }
            }
            
            # 发送请求
            response = requests.post(
                f"{base_url}/models/gemini-pro-vision:generateContent",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result.get("candidates"):
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return "无法识别图片内容"
            else:
                print(f"Gemini API调用失败: {response.status_code}")
                return f"API调用失败: {response.status_code}"
        except Exception as e:
            print(f"Gemini图片识别失败: {e}")
            return "图片识别失败"
    
    def _glm_image_recognition(self, api_key: str, base_url: str, image_path: str) -> str:
        """使用GLM API进行图片识别"""
        try:
            # 读取图片并编码为base64
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "glm-4v",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "请描述图片中的内容"
                            },
                            {
                                "type": "image",
                                "image": image_base64
                            }
                        ]
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            # 发送请求
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result.get("choices"):
                    return result["choices"][0]["message"]["content"]
                else:
                    return "无法识别图片内容"
            else:
                print(f"GLM API调用失败: {response.status_code}")
                return f"API调用失败: {response.status_code}"
        except Exception as e:
            print(f"GLM图片识别失败: {e}")
            return "图片识别失败"
    
    def _azure_image_recognition(self, api_key: str, base_url: str, image_path: str) -> str:
        """使用Azure Computer Vision API进行图片识别"""
        try:
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/octet-stream"
            }
            
            # 读取图片
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # 发送请求
            response = requests.post(
                f"{base_url}/vision/v3.2/analyze",
                headers=headers,
                data=image_data,
                params={
                    "visualFeatures": "Description,Tags",
                    "language": "zh"
                },
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if "description" in result and "captions" in result["description"]:
                    return result["description"]["captions"][0]["text"]
                else:
                    return "无法识别图片内容"
            else:
                print(f"Azure API调用失败: {response.status_code}")
                return f"API调用失败: {response.status_code}"
        except Exception as e:
            print(f"Azure图片识别失败: {e}")
            return "图片识别失败"
    
    def _generic_image_recognition(self, api_key: str, base_url: str, image_path: str) -> str:
        """通用图片识别API调用方式"""
        try:
            # 读取图片并编码为base64
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "image": image_base64,
                "prompt": "请描述图片中的内容"
            }
            
            # 发送请求
            response = requests.post(
                base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                return result.get("description", "无法识别图片内容")
            else:
                print(f"通用API调用失败: {response.status_code}")
                return f"API调用失败: {response.status_code}"
        except Exception as e:
            print(f"通用图片识别失败: {e}")
            return "图片识别失败"
    
    def _get_mime_type(self, image_path: str) -> str:
        """获取图片的MIME类型"""
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return mime_types.get(ext, "image/jpeg")

# 创建全局图片识别API系统实例
image_api_system = ImageAPISystem()
