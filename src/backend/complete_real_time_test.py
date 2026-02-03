#!/usr/bin/env python3
# 完整的实时语音生成测试

from simple_real_time_tts import SimpleRealTimeTTS
import time

def interactive_real_time_tts():
    """交互式实时TTS测试"""
    print("🎙️ 交互式实时TTS测试")
    print("=" * 50)
    print("输入文本，系统会实时转换为语音播放")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'demo' 运行演示")
    print("=" * 50)
    
    tts = SimpleRealTimeTTS()
    
    def interactive_text_generator():
        """交互式文本生成器"""
        while True:
            try:
                user_input = input("\n🗣️ 请输入文本: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！")
                    break
                elif user_input.lower() == 'demo':
                    # 返回演示文本
                    demo_texts = [
                        "你好，欢迎使用实时TTS系统。",
                        "这个系统可以将文本实时转换为语音。",
                        "每一句话都会立即播放出来。",
                        "非常适合直播和实时互动场景。",
                        "感谢您的使用！"
                    ]
                    for text in demo_texts:
                        yield text
                        time.sleep(2)
                elif user_input:
                    yield user_input
                else:
                    print("⚠️ 请输入有效文本")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
    
    # 开始实时流式播放
    success = tts.stream_tts(interactive_text_generator())
    
    if success:
        print("\n✅ 实时TTS测试完成")
    else:
        print("\n❌ 实时TTS测试失败")

def batch_real_time_test():
    """批量实时TTS测试"""
    print("🧪 批量实时TTS测试")
    print("=" * 30)
    
    tts = SimpleRealTimeTTS()
    
    # 测试文本集合
    test_batches = [
        # 中文测试
        ["你好世界", "欢迎使用实时语音系统", "这是一个测试"],
        # 英文测试  
        ["Hello world", "Welcome to real-time voice system", "This is a test"],
        # 混合测试
        ["AI技术让生活更美好", "Artificial Intelligence makes life better", "科技改变未来"]
    ]
    
    for i, batch in enumerate(test_batches):
        print(f"\n--- 测试批次 {i+1} ---")
        
        def batch_generator():
            for text in batch:
                print(f"📥 发送: {text}")
                yield text
                time.sleep(1)
        
        success = tts.stream_tts(batch_generator())
        if success:
            print(f"✅ 批次 {i+1} 完成")
        else:
            print(f"❌ 批次 {i+1} 失败")
        
        if i < len(test_batches) - 1:
            time.sleep(2)  # 批次间间隔

def performance_test():
    """性能测试"""
    print("⚡ 实时TTS性能测试")
    print("=" * 30)
    
    tts = SimpleRealTimeTTS()
    
    # 生成大量短文本测试响应速度
    def performance_generator():
        import random
        words = ["你好", "测试", "实时", "语音", "系统", "播放", "文本", "转换"]
        
        for i in range(20):  # 20个测试
            # 随机生成1-3个词的句子
            sentence = "".join(random.sample(words, random.randint(1, 3)))
            yield sentence
            time.sleep(0.5)  # 快速发送
    
    start_time = time.time()
    success = tts.stream_tts(performance_generator())
    end_time = time.time()
    
    if success:
        print(f"\n✅ 性能测试完成")
        print(f"⏱️  总耗时: {end_time - start_time:.2f}秒")
        print(f"📊 平均响应: {(end_time - start_time)/20:.3f}秒/条")
    else:
        print("❌ 性能测试失败")

def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 50)
        print("🎙️ 实时TTS测试系统")
        print("=" * 50)
        print("1. 交互式实时TTS")
        print("2. 批量实时TTS测试") 
        print("3. 性能测试")
        print("4. 退出")
        print("=" * 50)
        
        choice = input("请选择功能 (1-4): ").strip()
        
        if choice == '1':
            interactive_real_time_tts()
        elif choice == '2':
            batch_real_time_test()
        elif choice == '3':
            performance_test()
        elif choice == '4':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()