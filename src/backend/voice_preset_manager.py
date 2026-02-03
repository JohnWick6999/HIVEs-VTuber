#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音色预设管理中心
整合所有音色配置，方便管理和使用
"""

import json
from pathlib import Path

# 导入所有音色配置
from cute_voices import CUTE_VOICES
from official_cute_voices import OFFICIAL_CUTE_VOICES  
from super_cute_voices import SUPER_CUTE_VOICES

class VoicePresetManager:
    """音色预设管理器"""
    
    def __init__(self):
        self.presets = {}
        self._load_all_presets()
    
    def _load_all_presets(self):
        """加载所有音色预设"""
        # 基础可爱音色
        for name, config in CUTE_VOICES.items():
            self.presets[f"基础_{name}"] = {
                "type": "basic",
                "config": config,
                "source": "cute_voices.py"
            }
        
        # 官方参数音色
        for name, config in OFFICIAL_CUTE_VOICES.items():
            self.presets[f"官方_{name}"] = {
                "type": "official",
                "config": config,
                "source": "official_cute_voices.py"
            }
        
        # 超级可爱音色
        for name, config in SUPER_CUTE_VOICES.items():
            self.presets[f"超级_{name}"] = {
                "type": "super",
                "config": config,
                "source": "super_cute_voices.py"
            }
    
    def list_all_presets(self):
        """列出所有音色预设"""
        print("🎭 音色预设大全:")
        print("=" * 60)
        
        # 按类型分组显示
        types = {"basic": "基础音色", "official": "官方音色", "super": "超级音色"}
        
        for type_key, type_name in types.items():
            print(f"\n🌟 {type_name}:")
            print("-" * 40)
            
            for name, preset in self.presets.items():
                if preset["type"] == type_key:
                    config = preset["config"]
                    print(f"  🎤 {name}")
                    print(f"     描述: {config.get('description', '无描述')}")
                    print(f"     音调: {config.get('pitch', 'N/A')}x")
                    print(f"     语速: {config.get('rate', 'N/A')}x")
                    print(f"     音量: {config.get('volume', 'N/A')}")
                    print(f"     来源: {preset['source']}")
                    print()
    
    def get_preset(self, preset_name):
        """获取指定音色预设"""
        return self.presets.get(preset_name)
    
    def search_presets(self, keyword):
        """搜索音色预设"""
        results = {}
        for name, preset in self.presets.items():
            if keyword.lower() in name.lower() or keyword.lower() in preset["config"].get("description", "").lower():
                results[name] = preset
        return results
    
    def export_presets(self, filepath):
        """导出音色预设到文件"""
        export_data = {}
        for name, preset in self.presets.items():
            export_data[name] = {
                "type": preset["type"],
                "config": preset["config"]
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 音色预设已导出到: {filepath}")
    
    def import_presets(self, filepath):
        """从文件导入音色预设"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for name, data in import_data.items():
                if name not in self.presets:  # 避免重复
                    self.presets[name] = {
                        "type": data["type"],
                        "config": data["config"],
                        "source": f"imported_from_{Path(filepath).name}"
                    }
                    imported_count += 1
            
            print(f"✅ 成功导入 {imported_count} 个音色预设")
            return True
        except Exception as e:
            print(f"❌ 导入失败: {e}")
            return False

# 创建全局实例
voice_manager = VoicePresetManager()

def main():
    """主函数 - 音色预设管理界面"""
    print("🎭 音色预设管理中心")
    print("=" * 40)
    
    while True:
        print("\n请选择操作:")
        print("1. 📋 查看所有音色预设")
        print("2. 🔍 搜索音色预设")
        print("3. 📤 导出音色预设")
        print("4. 📥 导入音色预设")
        print("5. 👋 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == "1":
            voice_manager.list_all_presets()
            
        elif choice == "2":
            keyword = input("请输入搜索关键词: ").strip()
            if keyword:
                results = voice_manager.search_presets(keyword)
                if results:
                    print(f"\n🔍 搜索 '{keyword}' 的结果:")
                    print("-" * 30)
                    for name, preset in results.items():
                        print(f"🎤 {name}: {preset['config'].get('description', '无描述')}")
                else:
                    print("❌ 未找到匹配的音色预设")
            else:
                print("❌ 请输入搜索关键词")
                
        elif choice == "3":
            filepath = input("请输入导出文件路径 (默认: voice_presets.json): ").strip()
            if not filepath:
                filepath = "voice_presets.json"
            voice_manager.export_presets(filepath)
            
        elif choice == "4":
            filepath = input("请输入要导入的文件路径: ").strip()
            if filepath and Path(filepath).exists():
                voice_manager.import_presets(filepath)
            else:
                print("❌ 文件不存在")
                
        elif choice == "5":
            print("👋 再见！")
            break
            
        else:
            print("❌ 无效选择，请输入1-5")

if __name__ == "__main__":
    main()