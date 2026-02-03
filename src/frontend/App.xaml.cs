using System.Configuration;
using System.Data;
using System.Windows;
using System.Globalization;
using System.Diagnostics;

namespace AIVtuberTool;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        // 添加资源加载调试信息
        Debug.WriteLine($"Current UI Culture: {CultureInfo.CurrentUICulture}");
        Debug.WriteLine($"Current Culture: {CultureInfo.CurrentCulture}");
        Debug.WriteLine($"Neutral Language: {System.Reflection.Assembly.GetExecutingAssembly().GetName().CultureInfo}");
        
        try
        {
            // 尝试访问PresentationFramework资源
            var frameworkAssembly = typeof(Window).Assembly;
            Debug.WriteLine($"Framework Assembly: {frameworkAssembly.FullName}");
            
            // 这里可能会触发资源加载
            var testWindow = new Window();
            Debug.WriteLine("Window created successfully");
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Resource loading error: {ex}");
        }
        
        // 设置默认主窗口为现代化窗口
        var mainWindow = new LauncherWindow();
        mainWindow.Show();
        
        base.OnStartup(e);
    }
}