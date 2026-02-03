#!/usr/bin/env python3
# VTS连接诊断和测试工具

import asyncio
import socket
import subprocess
import time
from vts_integration import vts_integration

class VTSConnectionDiagnostic:
    """VTS连接诊断工具"""
    
    def __init__(self):
        self.vts_port = 9001  # VTS默认API端口
        self.host = "localhost"
        
    def check_vts_process(self):
        """检查VTS进程是否运行"""
        print("🔍 检查VTubeStudio进程...")
        
        try:
            import psutil
            
            vts_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'vtuber' in proc.info['name'].lower() or 'vts' in proc.info['name'].lower():
                        vts_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if vts_processes:
                print(f"✅ 发现VTS相关进程: {len(vts_processes)}个")
                for proc in vts_processes:
                    print(f"   PID: {proc['pid']}, 名称: {proc['name']}")
                return True
            else:
                print("❌ 未发现VTS进程")
                return False
                
        except ImportError:
            print("⚠️ 未安装psutil库，跳过进程检查")
            return None
    
    def check_port_availability(self):
        """检查VTS端口是否开放"""
        print(f"🔌 检查端口 {self.vts_port} 可用性...")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.host, self.vts_port))
            sock.close()
            
            if result == 0:
                print(f"✅ 端口 {self.vts_port} 可访问")
                return True
            else:
                print(f"❌ 端口 {self.vts_port} 不可访问")
                return False
                
        except Exception as e:
            print(f"❌ 端口检查失败: {e}")
            return False
    
    def check_firewall(self):
        """检查防火墙设置"""
        print("🛡️ 检查防火墙设置...")
        
        try:
            # 检查Windows防火墙规则
            result = subprocess.run(
                ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                firewall_rules = result.stdout.lower()
                if 'vts' in firewall_rules or 'vtubestudio' in firewall_rules:
                    print("✅ 发现VTS相关防火墙规则")
                    return True
                else:
                    print("⚠️ 未发现VTS防火墙规则")
                    return None
            else:
                print("⚠️ 无法检查防火墙设置")
                return None
                
        except Exception as e:
            print(f"❌ 防火墙检查失败: {e}")
            return None
    
    async def test_vts_api(self):
        """测试VTS API连接"""
        print("📡 测试VTS API连接...")
        
        try:
            # 尝试连接
            success = await vts_integration.connect()
            
            if success:
                print("✅ VTS API连接成功")
                
                # 获取基本信息
                try:
                    status = await vts_integration.get_status()
                    print(f"📊 VTS状态: {status}")
                    
                    current_model = await vts_integration.get_current_model()
                    print(f"🎭 当前模型: {current_model}")
                    
                    return True
                except Exception as e:
                    print(f"⚠️ 获取VTS信息时出错: {e}")
                    return True  # 连接成功就算通过
            else:
                print("❌ VTS API连接失败")
                return False
                
        except Exception as e:
            print(f"❌ VTS API测试异常: {e}")
            return False
    
    def provide_setup_guidance(self):
        """提供设置指导"""
        print("\n🛠️ VTubeStudio设置指导")
        print("=" * 40)
        print("请按以下步骤配置VTS:")
        print()
        print("1. 启动VTubeStudio")
        print("   • 双击VTubeStudio.exe启动程序")
        print("   • 等待程序完全加载")
        print()
        print("2. 启用API服务器")
        print("   • 在VTS中按 F12 打开设置")
        print("   • 选择'Misc'选项卡")
        print("   • 勾选'Enable Access to VTubeStudio API'")
        print("   • 确认端口为9001(默认)")
        print()
        print("3. 配置防火墙(如有需要)")
        print("   • Windows安全中心 → 防火墙")
        print("   • 允许VTubeStudio通过防火墙")
        print()
        print("4. 重启VTS")
        print("   • 完成设置后重启VTubeStudio")
        print("   • 确保API服务器正常运行")
        print()
        print("设置完成后重新运行此测试脚本")
    
    async def run_diagnostic(self):
        """运行完整诊断"""
        print("🔍 VTS连接诊断工具")
        print("=" * 30)
        
        results = {}
        
        # 1. 检查进程
        process_result = self.check_vts_process()
        results['process'] = process_result
        
        # 2. 检查端口
        port_result = self.check_port_availability()
        results['port'] = port_result
        
        # 3. 检查防火墙
        firewall_result = self.check_firewall()
        results['firewall'] = firewall_result
        
        # 4. 测试API连接
        if port_result:  # 只有端口可用才测试API
            api_result = await self.test_vts_api()
            results['api'] = api_result
        else:
            results['api'] = False
        
        # 输出诊断结果
        print("\n" + "=" * 30)
        print("📋 诊断结果:")
        print("=" * 30)
        
        diagnostic_passed = 0
        total_checks = sum(1 for v in results.values() if v is not None)
        
        for check_name, result in results.items():
            if result is None:
                continue
                
            status = "✅" if result else "❌"
            check_labels = {
                'process': 'VTS进程运行',
                'port': 'API端口可用',
                'firewall': '防火墙设置',
                'api': 'API连接测试'
            }
            
            print(f"{status} {check_labels.get(check_name, check_name)}")
            if result:
                diagnostic_passed += 1
        
        print("=" * 30)
        print(f"诊断通过: {diagnostic_passed}/{total_checks}")
        
        # 根据结果提供建议
        if diagnostic_passed == total_checks:
            print("🎉 VTS连接配置完美！")
            print("现在可以正常使用VTS集成功能")
        elif diagnostic_passed >= total_checks * 0.7:
            print("✅ 大部分配置正确")
            print("可能存在轻微问题，但仍可使用")
        else:
            print("⚠️ 配置存在问题")
            self.provide_setup_guidance()
        
        return diagnostic_passed == total_checks

class SimpleVTSTest:
    """简化版VTS测试"""
    
    @staticmethod
    async def quick_test():
        """快速测试VTS基本功能"""
        print("⚡ VTS快速功能测试")
        print("=" * 25)
        
        try:
            # 连接测试
            print("🔌 连接VTS...")
            connected = await vts_integration.connect()
            
            if not connected:
                print("❌ 连接失败")
                return False
            
            print("✅ 连接成功")
            
            # 简单功能测试
            print("🎭 测试基本功能...")
            
            # 获取模型信息
            current_model = await vts_integration.get_current_model()
            print(f"当前模型: {current_model}")
            
            # 测试热键获取
            hotkeys = await vts_integration.get_hotkeys()
            print(f"可用热键: {len(hotkeys)}个")
            
            # 测试表达式获取
            expressions = await vts_integration.get_expressions()
            print(f"可用表情: {len(expressions)}个")
            
            print("✅ 基本功能测试通过")
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False
        finally:
            # 断开连接
            try:
                await vts_integration.disconnect()
                print("🔌 连接已断开")
            except:
                pass

async def main():
    """主函数"""
    print("🤖 VTS集成测试工具")
    print("=" * 25)
    print("选择测试模式:")
    print("1. 完整诊断测试")
    print("2. 快速功能测试")
    print("3. 设置指导")
    print("4. 退出")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == '1':
        diagnostic = VTSConnectionDiagnostic()
        await diagnostic.run_diagnostic()
    elif choice == '2':
        await SimpleVTSTest.quick_test()
    elif choice == '3':
        diagnostic = VTSConnectionDiagnostic()
        diagnostic.provide_setup_guidance()
    elif choice == '4':
        print("👋 再见！")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    asyncio.run(main())