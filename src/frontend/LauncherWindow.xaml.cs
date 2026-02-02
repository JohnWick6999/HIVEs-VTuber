using System;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using System.Windows;

namespace AIVtuberTool
{
    public partial class LauncherWindow : Window
    {
        private readonly HttpClient _httpClient;
        private const string BackendBaseUrl = "http://localhost:8000";

        public LauncherWindow()
        {
            InitializeComponent();
            _httpClient = new HttpClient { BaseAddress = new Uri(BackendBaseUrl) };
            CheckBackendStatus();
            SetupEventHandlers();
        }

        private void SetupEventHandlers()
        {
            LaunchClassicButton.Click += async (s, e) => await LaunchClassicInterface();
            LaunchModernButton.Click += async (s, e) => await LaunchModernInterface();
            LaunchKawaiiButton.Click += async (s, e) => await LaunchKawaiiInterface();
        }

        private async void CheckBackendStatus()
        {
            try
            {
                var response = await _httpClient.GetAsync("/health");
                if (response.IsSuccessStatusCode)
                {
                    BackendStatusText.Text = "🟢 Online";
                    BackendStatusText.Foreground = System.Windows.Media.Brushes.LimeGreen;
                }
                else
                {
                    BackendStatusText.Text = "🔴 Offline";
                    BackendStatusText.Foreground = System.Windows.Media.Brushes.Red;
                }
            }
            catch
            {
                BackendStatusText.Text = "🔴 Offline";
                BackendStatusText.Foreground = System.Windows.Media.Brushes.Red;
            }
        }

        private async Task LaunchClassicInterface()
        {
            try
            {
                // 检查后端是否运行
                var response = await _httpClient.GetAsync("/health");
                if (!response.IsSuccessStatusCode)
                {
                    var result = MessageBox.Show(
                        "后端服务似乎没有运行，是否启动后端服务？", 
                        "启动后端服务", 
                        MessageBoxButton.YesNo, 
                        MessageBoxImage.Question);
                    
                    if (result == MessageBoxResult.Yes)
                    {
                        StartBackendService();
                        await Task.Delay(3000); // 等待后端启动
                    }
                }

                // 关闭启动器并打开经典界面
                Close();
                var classicWindow = new MainWindow();
                classicWindow.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"启动经典界面时出错: {ex.Message}", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LaunchModernInterface()
        {
            try
            {
                // 检查后端是否运行
                var response = await _httpClient.GetAsync("/health");
                if (!response.IsSuccessStatusCode)
                {
                    var result = MessageBox.Show(
                        "后端服务似乎没有运行，是否启动后端服务？", 
                        "启动后端服务", 
                        MessageBoxButton.YesNo, 
                        MessageBoxImage.Question);
                    
                    if (result == MessageBoxResult.Yes)
                    {
                        StartBackendService();
                        await Task.Delay(3000); // 等待后端启动
                    }
                }

                // 关闭启动器并打开现代界面
                Close();
                var modernWindow = new ModernMainWindow();
                modernWindow.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"启动现代界面时出错: {ex.Message}", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LaunchKawaiiInterface()
        {
            try
            {
                // 检查后端是否运行
                var response = await _httpClient.GetAsync("/health");
                if (!response.IsSuccessStatusCode)
                {
                    var result = MessageBox.Show(
                        "后端服务似乎没有运行，是否启动后端服务？", 
                        "启动后端服务", 
                        MessageBoxButton.YesNo, 
                        MessageBoxImage.Question);
                    
                    if (result == MessageBoxResult.Yes)
                    {
                        StartBackendService();
                        await Task.Delay(3000); // 等待后端启动
                    }
                }

                // 关闭启动器并打开萌系界面
                Close();
                var kawaiiWindow = new KawaiiMainWindow();
                kawaiiWindow.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"启动萌系界面时出错: {ex.Message}", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void StartBackendService()
        {
            try
            {
                // 尝试启动后端服务 - 使用绝对路径
                string projectRoot = System.IO.Path.GetDirectoryName(System.IO.Path.GetDirectoryName(System.IO.Path.GetDirectoryName(
                    System.IO.Path.GetDirectoryName(System.IO.Path.GetDirectoryName(System.IO.Directory.GetCurrentDirectory())))));
                string backendPath = System.IO.Path.Combine(projectRoot, "src", "backend");
                
                var startInfo = new ProcessStartInfo
                {
                    FileName = "cmd.exe",
                    Arguments = $"/C cd /d \"{backendPath}\" && python main.py",
                    UseShellExecute = true,
                    CreateNoWindow = false
                };
                
                Process.Start(startInfo);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"启动后端服务失败: {ex.Message}", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}