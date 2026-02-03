import asyncio
import os
from vts_integration import vts_integration

class LLMTTSDriver:
    """LLM语音驱动类，用于将LLM生成的文本转换为语音并驱动VTubeStudio"""
    
    def __init__(self):
        """初始化LLM语音驱动"""
        self.vts = vts_integration
    
    async def generate_and_play(self, text, model_id=None):
        """生成语音并播放，驱动VTubeStudio口型"""
        print(f"\n🎯 处理LLM生成的文本:")
        print(f"📝 文本内容: {text}")
        
        # 生成语音并播放到虚拟声卡
        success = self.vts.text_to_speech_with_lip_sync(text, "llm_output.wav")
        
        if success:
            print("✅ LLM语音驱动成功")
            
            # 如果指定了模型ID，尝试加载模型
            if model_id:
                await self.vts.load_model(model_id)
        else:
            print("❌ LLM语音驱动失败")
        
        return success

async def test_llm_voice_driver():
    """测试LLM语音驱动功能"""
    print("🚀 测试LLM语音驱动功能...")
    
    # 创建LLM语音驱动实例
    driver = LLMTTSDriver()
    
    # 测试文本（模拟LLM生成的回复）
    test_texts = [
        "你好！我是一个由LLM驱动的虚拟主播。今天天气真好，很高兴见到你！",
        "我可以回答你的问题，讲述故事，或者只是陪你聊天。有什么我可以帮助你的吗？",
        "虚拟主播技术结合了AI和实时渲染，能够为观众带来更生动的互动体验。"
    ]
    
    # 逐个测试文本
    for i, text in enumerate(test_texts):
        print(f"\n=== 测试 {i+1}/{len(test_texts)} ===")
        await driver.generate_and_play(text)
        
        # 等待几秒钟，然后测试下一个文本
        if i < len(test_texts) - 1:
            print("⏰ 等待3秒后测试下一个文本...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(test_llm_voice_driver())
