import requests
import json
from typing import List, Dict, Any
from config import config_manager
from search_api import SearchAPISystem

class AIChatSystem:
    """AI聊天系统核心类"""
    
    def __init__(self):
        """初始化AI聊天系统"""
        self.chat_history: List[Dict[str, str]] = []
        self.personality = config_manager.get_personality_config()
        # 限制聊天历史长度，避免API调用失败
        self.max_history_length = 20
        # 初始化搜索系统
        self.search_system = SearchAPISystem()
    
    def add_message(self, role: str, content: str) -> None:
        """添加消息到聊天历史"""
        self.chat_history.append({"role": role, "content": content})
        # 限制聊天历史长度
        if len(self.chat_history) > self.max_history_length:
            self.chat_history = self.chat_history[-self.max_history_length:]
    
    def clear_history(self) -> None:
        """清空聊天历史"""
        self.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """获取聊天历史"""
        return self.chat_history
    
    def generate_response(self, user_input: str) -> str:
        """生成AI回复"""
        try:
            # 检查是否需要搜索
            search_needed = self._needs_search(user_input)
            search_results = ""
            
            if search_needed:
                # 使用Kimi执行搜索
                search_results = self.search_system.search(user_input)
                # 完全隐藏搜索结果，不打印任何信息给用户
                pass
            
            # 构建Deepseek的输入，包含用户问题和搜索结果
            if search_results and "搜索失败" not in search_results:
                deepseek_input = f"用户问题: {user_input}\n\n搜索结果:\n{search_results}\n\n请严格基于搜索结果回答用户的问题，不要添加任何搜索结果中没有的信息，保持自然友好的语气。如果搜索结果不完整或有问题，请如实告知用户。"
            else:
                deepseek_input = f"用户问题: {user_input}\n\n请如实告知用户你无法获取实时信息，因为你没有访问互联网的能力。建议用户使用其他方式查询相关信息，保持自然友好的语气。"
            
            # 清空聊天历史，避免重复
            self.chat_history = []
            self.add_message("user", deepseek_input)
            
            # 调用Deepseek API生成最终回复
            response = self._call_chat_api()
            
            return response
        except Exception as e:
            print(f"生成回复失败: {e}")
            return "抱歉，我暂时无法回答你的问题。"
    
    def _needs_search(self, user_input: str) -> bool:
        """判断是否需要搜索"""
        # 关键词列表，包含需要搜索的内容类型
        search_keywords = [
            "天气", "温度", "预报", "新闻", "资讯", "最新", "今天", "明天", "后天",
            "什么", "怎么", "如何", "为什么", "何时", "哪里", "谁", "哪个",
            "查询", "搜索", "查找", "了解", "知道", "想知道", "请问", "帮忙"
        ]
        
        # 检查用户输入是否包含搜索关键词
        user_input_lower = user_input.lower()
        for keyword in search_keywords:
            if keyword in user_input_lower:
                return True
        
        return False
    
    def _call_chat_api(self) -> str:
        """调用聊天API"""
        chat_config = config_manager.get_chat_api_config()
        api_key = chat_config.get("api_key")
        base_url = chat_config.get("base_url")
        model = chat_config.get("model", "gpt-3.5-turbo")
        temperature = chat_config.get("temperature", 0.7)
        max_tokens = chat_config.get("max_tokens", 1024)
        
        # 构建系统消息
        system_message = self._build_system_prompt()
        
        # 构建请求消息
        messages = [
            {"role": "system", "content": system_message}
        ] + self.chat_history
        
        # 根据不同的API提供商选择不同的调用方式
        if "openai" in base_url.lower() or not base_url:
            return self._call_openai_api(api_key, base_url, model, messages, temperature, max_tokens)
        elif "deepseek" in base_url.lower():
            return self._call_deepseek_api(api_key, base_url, model, messages, temperature, max_tokens)
        else:
            # 默认使用OpenAI兼容接口
            return self._call_openai_api(api_key, base_url, model, messages, temperature, max_tokens)
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return f"你是{self.personality.get('name')}，{self.personality.get('description')}。你的性格特点是：{self.personality.get('tone')}。初次见面时的问候语是：{self.personality.get('greeting')}。请保持这个设定与用户交流。"
    
    def _call_openai_api(self, api_key: str, base_url: str, model: str, messages: List[Dict[str, str]], 
                        temperature: float, max_tokens: int) -> str:
        """调用OpenAI API"""
        try:
            import openai
            
            # 配置OpenAI客户端
            openai.api_key = api_key
            if base_url:
                openai.api_base = base_url
            
            # 调用API
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 返回回复内容
            return response.choices[0].message.content
        except ImportError:
            print("OpenAI库未安装")
            return "抱歉，OpenAI库未安装，无法提供服务。"
        except Exception as e:
            print(f"OpenAI API调用失败: {e}")
            return "抱歉，我暂时无法回答你的问题。"
    
    def _call_deepseek_api(self, api_key: str, base_url: str, model: str, messages: List[Dict[str, str]], 
                          temperature: float, max_tokens: int) -> str:
        """调用DeepSeek API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            # 发送请求
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            response_data = response.json()
            if "choices" in response_data and response_data.get("choices"):
                return response_data["choices"][0]["message"]["content"]
            else:
                print(f"DeepSeek API响应错误: {response_data}")
                return "抱歉，我暂时无法回答你的问题。"
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return "抱歉，我暂时无法回答你的问题。"

# 创建全局AI聊天系统实例
ai_chat_system = AIChatSystem()
