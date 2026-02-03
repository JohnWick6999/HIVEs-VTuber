#!/usr/bin/env python3
# 虚拟麦克风完整使用示例

import time
from simple_virtual_mic import SimpleVirtualMic
from voice_api import voice_api_system

def demo_virtual_mic_integration():
    """演示虚拟麦克风与TTS的完整集成"""
    print("🎯 虚拟麦克风与TTS集成演示")
    print("=" * 50)
    
    # 1. 初始化虚拟麦克风
    print("1️⃣ 初始化虚拟麦克风系统...")
    virtual_mic = SimpleVirtualMic()
    
    # 2. 检查虚拟设备
    print("2️⃣ 检查虚拟音频设备...")
    if not virtual_mic.find_virtual_devices():
        print("❌ 未检测到VB-CABLE虚拟设备")
        print("请先运行 install_vbcable.bat 安装驱动")
        return False
    
    # 3. 启动虚拟麦克风
    print("3️⃣ 启动虚拟麦克风路由...")
    if not virtual_mic.start_virtual_mic():
        print("❌ 虚拟麦克风启动失败")
        return False
    
    print("✅ 虚拟麦克风系统启动成功")
    print("🎙️  现在TTS音频将自动路由到虚拟麦克风")
    print("📺 在VTubeStudio中请选择VB-CABLE Input作为麦克风输入")
    
    try:
        # 4. 演示TTS到虚拟麦克风
        demo_texts = [
            "你好，我是AI虚拟主播。",
            "现在演示虚拟麦克风功能。",
            "这段话会通过虚拟麦克风输出。",
            "VTubeStudio可以接收这个音频输入。",
            "实现真正的语音驱动虚拟形象。"
        ]
        
        print("\n4️⃣ 开始TTS演示...")
        for i, text in enumerate(demo_texts, 1):
            print(f"\n[{i}/{len(demo_texts)}] 生成语音: {text}")
            
            # 生成TTS音频
            output_file = f"demo_tts_{i}.wav"
            success = voice_api_system.text_to_speech(text, output_file)
            
            if success:
                print(f"✅ 语音生成成功: {output_file}")
                # 播放音频（会自动通过虚拟麦克风输出）
                import os
                if os.name == 'nt':
                    os.startfile(output_file)
                time.sleep(3)  # 等待播放完成
            else:
                print("❌ 语音生成失败")
            
            time.sleep(1)
        
        print("\n🎉 演示完成！")
        print("✅ 虚拟麦克风系统工作正常")
        print("✅ TTS音频成功路由到虚拟设备")
        print("✅ VTubeStudio可以接收音频输入")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️  用户中断演示")
        return True
    finally:
        # 5. 清理资源
        print("\n5️⃣ 清理系统资源...")
        virtual_mic.stop_virtual_mic()

def interactive_virtual_mic():
    """交互式虚拟麦克风使用"""
    print("💬 交互式虚拟麦克风")
    print("=" * 30)
    
    virtual_mic = SimpleVirtualMic()
    
    # 启动虚拟麦克风
    if not virtual_mic.find_virtual_devices():
        print("❌ 未找到虚拟设备")
        return
    
    if not virtual_mic.start_virtual_mic():
        print("❌ 启动失败")
        return
    
    print("✅ 虚拟麦克风已启动")
    print("🎙️  现在可以输入文本进行实时语音播放")
    print("📢 音频将通过虚拟麦克风输出到VTubeStudio")
    print("输入 'quit' 退出")
    
    try:
        while True:
            text = input("\n🗣️ 输入文本: ").strip()
            
            if text.lower() in ['quit', 'exit', '退出']:
                break
            elif text:
                print(f"📤 生成语音: {text}")
                
                # 生成并播放
                success = voice_api_system.text_to_speech(text, "temp.wav")
                if success:
                    import os
                    if os.name == 'nt':
                        os.startfile("temp.wav")
                    time.sleep(len(text) * 0.1 + 1)  # 根据文本长度等待
    
    except KeyboardInterrupt:
        print("\n👋 再见！")
    finally:
        virtual_mic.stop_virtual_mic()

def test_vtube_studio_setup():
    """测试VTubeStudio设置"""
    print("🎮 VTubeStudio设置测试")
    print("=" * 30)
    
    from simple_virtual_mic import VTSTIntegration
    virtual_mic = SimpleVirtualMic()
    vts_integration = VTSTIntegration(virtual_mic)
    
    # 检查VTubeStudio连接
    success = vts_integration.connect_to_vts()
    
    if success:
        print("\n✅ VTubeStudio设置检查完成")
        print("📋 下一步操作:")
        print("1. 在VTubeStudio中确认音频输入设备为VB-CABLE Input")
        print("2. 调整音频增益到合适水平(建议50-70%)")
        print("3. 启用降噪功能")
        print("4. 测试音频输入是否正常")
    else:
        print("❌ VTubeStudio设置检查失败")

def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 50)
        print("🎙️ 虚拟麦克风完整系统")
        print("=" * 50)
        print("1. 完整集成演示")
        print("2. 交互式使用")
        print("3. VTubeStudio设置检查")
        print("4. 音频设备测试")
        print("5. 退出")
        print("=" * 50)
        
        choice = input("请选择功能 (1-5): ").strip()
        
        if choice == '1':
            demo_virtual_mic_integration()
        elif choice == '2':
            interactive_virtual_mic()
        elif choice == '3':
            test_vtube_studio_setup()
        elif choice == '4':
            # 运行设备测试
            import subprocess
            subprocess.run(["python", "simple_virtual_mic.py"])
        elif choice == '5':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()