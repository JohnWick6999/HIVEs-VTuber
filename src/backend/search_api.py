import requests
from typing import List, Dict
from config import config_manager

class SearchAPISystem:
    """搜索API系统类"""
    
    def __init__(self):
        """初始化搜索API系统"""
        self.search_config = config_manager.get_search_api_config()
        self.model = self.search_config.get("model", "moonshot-v1-8k")
    
    def search(self, query: str) -> str:
        """执行网络搜索"""
        try:
            if not query:
                return "搜索查询不能为空"
            
            api_key = self.search_config.get("api_key")
            base_url = self.search_config.get("base_url")
            
            # 如果没有配置API，返回错误信息
            if not api_key or not base_url:
                return "请配置搜索API"
            
            # 根据不同的API提供商选择不同的调用方式
            if "google" in base_url.lower():
                return self._google_search(api_key, base_url, query)
            elif "bing" in base_url.lower():
                return self._bing_search(api_key, base_url, query)
            elif "kimi" in base_url.lower() or "moonshot" in base_url.lower():
                return self._kimi_search(api_key, base_url, query)
            else:
                # 默认使用通用的搜索API调用方式
                return self._generic_search(api_key, base_url, query)
        except Exception as e:
            return "搜索失败"
    
    def _google_search(self, api_key: str, base_url: str, query: str) -> str:
        """使用Google Search API进行搜索"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "q": query,
                "num": 5,
                "start": 1,
                "gl": "zh",
                "hl": "zh-CN"
            }
            
            # 发送请求
            response = requests.get(
                f"{base_url}/customsearch/v1",
                headers=headers,
                params=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                return self._format_search_results(result)
            else:
                return f"搜索失败: {response.status_code}"
        except Exception as e:
            return "搜索失败"
    
    def _bing_search(self, api_key: str, base_url: str, query: str) -> str:
        """使用Bing Search API进行搜索"""
        try:
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "count": 5,
                "offset": 0,
                "mkt": "zh-CN",
                "safesearch": "Moderate"
            }
            
            # 发送请求
            response = requests.get(
                f"{base_url}/v7.0/search",
                headers=headers,
                params=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                return self._format_bing_results(result)
            else:
                return f"搜索失败: {response.status_code}"
        except Exception as e:
            return "搜索失败"
    
    def _kimi_search(self, api_key: str, base_url: str, query: str) -> str:
        """使用Kimi Search API进行搜索"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": f"请搜索以下内容并返回相关结果: {query}"
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2048
            }
            
            # 发送请求
            response = requests.post(
                f"{base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result.get("choices"):
                    content = result["choices"][0]["message"]["content"]
                    return f"搜索结果:\n{content}"
                else:
                    return "搜索未返回结果"
            else:
                return f"搜索失败: {response.status_code}"
        except Exception as e:
            return "搜索失败"
    
    def _generic_search(self, api_key: str, base_url: str, query: str) -> str:
        """通用搜索API调用方式"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "query": query,
                "limit": 5
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
                return self._format_generic_results(result)
            else:
                return f"搜索失败: {response.status_code}"
        except Exception as e:
            return "搜索失败"
    
    def _format_search_results(self, result: Dict) -> str:
        """格式化Google搜索结果"""
        items = result.get("items", [])
        if not items:
            return "未找到相关结果"
        
        formatted_results = []
        for i, item in enumerate(items[:3], 1):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            formatted_results.append(f"{i}. {title}\n{snippet}\n链接: {link}\n")
        
        return "\n".join(formatted_results)
    
    def _format_bing_results(self, result: Dict) -> str:
        """格式化Bing搜索结果"""
        web_pages = result.get("webPages", {}).get("value", [])
        if not web_pages:
            return "未找到相关结果"
        
        formatted_results = []
        for i, page in enumerate(web_pages[:3], 1):
            name = page.get("name", "")
            snippet = page.get("snippet", "")
            url = page.get("url", "")
            formatted_results.append(f"{i}. {name}\n{snippet}\n链接: {url}\n")
        
        return "\n".join(formatted_results)
    
    def _format_kimi_results(self, result: Dict) -> str:
        """格式化Kimi搜索结果"""
        results = result.get("results", [])
        if not results:
            return "未找到相关结果"
        
        formatted_results = []
        for i, item in enumerate(results[:3], 1):
            title = item.get("title", "")
            content = item.get("content", "")
            url = item.get("url", "")
            formatted_results.append(f"{i}. {title}\n{content}\n链接: {url}\n")
        
        return "\n".join(formatted_results)
    
    def _format_generic_results(self, result: Dict) -> str:
        """格式化通用搜索结果"""
        results = result.get("results", [])
        if not results:
            return "未找到相关结果"
        
        formatted_results = []
        for i, item in enumerate(results[:3], 1):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            formatted_results.append(f"{i}. {title}\n{snippet}\n链接: {link}\n")
        
        return "\n".join(formatted_results)

# 创建全局搜索API系统实例
search_api_system = SearchAPISystem()
