using System.Configuration;
using System.Data;
using System.Windows;

namespace AIVtuberTool;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        // 设置默认主窗口为现代化窗口
        var mainWindow = new LauncherWindow();
        mainWindow.Show();
        
        base.OnStartup(e);
    }
}