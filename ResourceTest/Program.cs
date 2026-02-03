using System;
using System.Globalization;
using System.Reflection;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("=== 资源加载测试 ===");
        
        // 显示当前文化和UI文化
        Console.WriteLine($"当前UI文化: {CultureInfo.CurrentUICulture.Name}");
        Console.WriteLine($"当前文化: {CultureInfo.CurrentCulture.Name}");
        Console.WriteLine($"系统UI文化: {CultureInfo.InstalledUICulture.Name}");
        
        // 测试资源管理器
        try
        {
            Console.WriteLine("\n--- 测试PresentationFramework资源 ---");
            
            // 获取PresentationFramework程序集
            var frameworkAssembly = Assembly.Load("PresentationFramework, Version=8.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35");
            Console.WriteLine($"找到程序集: {frameworkAssembly.FullName}");
            
            // 创建资源管理器
            var resourceManager = new System.Resources.ResourceManager("PresentationFramework", frameworkAssembly);
            Console.WriteLine("资源管理器创建成功");
            
            // 尝试访问一些资源（这可能会触发我们看到的错误）
            try
            {
                var testResource = resourceManager.GetString("SomeNonExistentResource");
                Console.WriteLine("资源访问测试完成");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"资源访问异常: {ex.GetType().Name}: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"内部异常: {ex.InnerException.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"框架资源测试失败: {ex.Message}");
        }
        
        // 测试Aero2主题资源
        try
        {
            Console.WriteLine("\n--- 测试PresentationFramework.Aero2资源 ---");
            
            var aeroAssembly = Assembly.Load("PresentationFramework.Aero2, Version=8.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35");
            Console.WriteLine($"找到Aero2程序集: {aeroAssembly.FullName}");
            
            var aeroResourceManager = new System.Resources.ResourceManager("PresentationFramework.Aero2", aeroAssembly);
            Console.WriteLine("Aero2资源管理器创建成功");
            
            // 尝试访问中文资源（这应该是失败的）
            string[] culturesToTest = { "zh-CN", "zh-Hans", "zh" };
            
            foreach (var culture in culturesToTest)
            {
                try
                {
                    var cultureInfo = new CultureInfo(culture);
                    var resourceSet = aeroResourceManager.GetResourceSet(cultureInfo, true, false);
                    if (resourceSet != null)
                    {
                        Console.WriteLine($"找到{culture}资源集");
                    }
                    else
                    {
                        Console.WriteLine($"{culture}资源集未找到");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"{culture}资源访问失败: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Aero2资源测试失败: {ex.Message}");
        }
        
        Console.WriteLine("\n=== 测试完成 ===");
        Console.WriteLine("如果上面没有显示'Failed to resolve assembly'错误，则说明修复有效");
        Console.WriteLine("按任意键退出...");
        Console.ReadKey();
    }
}