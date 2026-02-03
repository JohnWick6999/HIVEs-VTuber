using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Documents;

namespace AIVtuberTool
{
    public partial class ModernMainWindow : Window
    {
        private readonly HttpClient _httpClient;
        private const string BackendBaseUrl = "http://localhost:8000";
        private readonly SolidColorBrush GreenBrush = new SolidColorBrush(Colors.LimeGreen);
        private readonly SolidColorBrush RedBrush = new SolidColorBrush(Colors.Red);
        private readonly SolidColorBrush YellowBrush = new SolidColorBrush(Colors.Yellow);

        public ModernMainWindow()
        {
            InitializeComponent();
            _httpClient = new HttpClient { BaseAddress = new Uri(BackendBaseUrl) };
            InitializeEventHandlers();
            Task.Run(() => LoadInitialData()); // 在后台任务中运行同步方法
        }

        private void InitializeEventHandlers()
        {
            // 导航按钮
            HomeButton.Click += (s, e) => NavigateToPage("Home");
            ChatButton.Click += (s, e) => NavigateToPage("Chat");
            ControlButton.Click += (s, e) => NavigateToPage("Control");
            SettingsButton.Click += (s, e) => NavigateToPage("Settings");
            ExitButton.Click += (s, e) => Close();

            // 功能面板按钮
            ChatPanelButton.Click += (s, e) => SwitchToPanel("Chat");
            VoicePanelButton.Click += (s, e) => SwitchToPanel("Voice");
            MediaPanelButton.Click += (s, e) => SwitchToPanel("Media");
            OBSPanelButton.Click += (s, e) => SwitchToPanel("OBS");
            VTSPanelButton.Click += (s, e) => SwitchToPanel("VTS");
            PersonalityPanelButton.Click += (s, e) => SwitchToPanel("Personality");
            ConfigPanelButton.Click += (s, e) => SwitchToPanel("Config");
            LogsPanelButton.Click += (s, e) => SwitchToPanel("Logs");

            // 聊天功能
            SendMessageButton.Click += async (s, e) => { await SendMessage(); };
            ChatInputTextBox.KeyDown += async (s, e) =>
            {
                if (e.Key == Key.Enter && (Keyboard.Modifiers & ModifierKeys.Shift) == 0)
                {
                    e.Handled = true;
                    await SendMessage();
                }
            };

            // 快捷控制按钮
            StartRecordingButton.Click += async (s, e) => { await StartObsRecording(); };
            StopRecordingButton.Click += async (s, e) => { await StopObsRecording(); };
            StartStreamingButton.Click += async (s, e) => { await StartObsStreaming(); };
            StopStreamingButton.Click += async (s, e) => { await StopObsStreaming(); };
            ConnectOBSButton.Click += async (s, e) => { await ConnectToObs(); };
            ConnectVTSButton.Click += async (s, e) => { await ConnectToVts(); };
            StartASRButton.Click += async (s, e) => { await StartAsr(); };
            StopASRButton.Click += (s, e) => StopAsr();

            // 状态相关
            RefreshConnectionButton.Click += async (s, e) => { await RefreshStatus(); };
        }

        private void LoadInitialData()
        {
            RefreshStatus();
        }

        private void NavigateToPage(string page)
        {
            MessageBox.Show($"导航到 {page} 页面");
        }

        private void SwitchToPanel(string panel)
        {
            MessageBox.Show($"切换到 {panel} 面板");
        }

        private async Task SendMessage()
        {
            var userInput = ChatInputTextBox.Text?.Trim();
            if (string.IsNullOrEmpty(userInput))
            {
                ShowNotification("请输入消息内容", NotificationType.Error);
                return;
            }

            try
            {
                // 添加用户消息到聊天历史
                AddChatMessage("👤 您", userInput, Colors.DodgerBlue);
                ChatInputTextBox.Clear();

                // 发送到后端
                var request = new { input = userInput };
                var response = await _httpClient.PostAsJsonAsync("/api/chat", request);
                
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadFromJsonAsync<ChatResponse>();
                    if (result != null && !string.IsNullOrEmpty(result.response))
                    {
                        AddChatMessage("🤖 Neuro", result.response, Colors.LimeGreen);
                        ShowNotification("消息发送成功", NotificationType.Success);
                    }
                }
                else
                {
                    ShowNotification($"发送失败: {response.StatusCode}", NotificationType.Error);
                    AddChatMessage("❌ 系统", $"错误: {response.StatusCode}", Colors.Red);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"发送失败: {ex.Message}", NotificationType.Error);
                AddChatMessage("❌ 系统", $"异常: {ex.Message}", Colors.Red);
            }
        }

        private void AddChatMessage(string sender, string message, Color color)
        {
            var border = new Border
            {
                Margin = new Thickness(5),
                Padding = new Thickness(10),
                Background = new SolidColorBrush(Color.FromArgb(30, color.R, color.G, color.B)),
                CornerRadius = new CornerRadius(8)
            };

            var stackPanel = new StackPanel { Orientation = Orientation.Vertical };

            var headerText = new TextBlock
            {
                Text = sender,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(color),
                Margin = new Thickness(0, 0, 0, 5)
            };

            var messageText = new TextBlock
            {
                Text = $"{message}\n[{DateTime.Now:HH:mm:ss}]",
                TextWrapping = TextWrapping.Wrap,
                Foreground = new SolidColorBrush(Colors.White)
            };

            stackPanel.Children.Add(headerText);
            stackPanel.Children.Add(messageText);
            border.Child = stackPanel;

            ChatHistoryList.Items.Add(border);
            ChatHistoryScrollViewer.ScrollToBottom();
        }

        private async Task RefreshStatus()
        {
            try
            {
                // 检查后端服务状态
                var healthResponse = await _httpClient.GetAsync("/health");
                if (healthResponse.IsSuccessStatusCode)
                {
                    BackendStatusValue.Text = "🟢 运行中";
                    BackendStatusValue.Foreground = GreenBrush;
                    ConnectionStatusText.Text = "🟢 已连接";
                    ConnectionStatusText.Foreground = GreenBrush;
                }
                else
                {
                    BackendStatusValue.Text = "🔴 未运行";
                    BackendStatusValue.Foreground = RedBrush;
                    ConnectionStatusText.Text = "🔴 未连接";
                    ConnectionStatusText.Foreground = RedBrush;
                }

                // 检查系统状态
                var statusResponse = await _httpClient.GetFromJsonAsync<StatusResponse>("/api/status");
                if (statusResponse != null)
                {
                    // OBS 状态
                    if (statusResponse.obs?.connected == true)
                    {
                        OBSStatusValue.Text = "🟢 已连接";
                        OBSStatusValue.Foreground = GreenBrush;
                    }
                    else
                    {
                        OBSStatusValue.Text = "🔴 未连接";
                        OBSStatusValue.Foreground = RedBrush;
                    }

                    // VTS 状态
                    if (statusResponse.vts?.connected == true)
                    {
                        VTSStatusValue.Text = "🟢 已连接";
                        VTSStatusValue.Foreground = GreenBrush;
                    }
                    else
                    {
                        VTSStatusValue.Text = "🔴 未连接";
                        VTSStatusValue.Foreground = RedBrush;
                    }

                    // AI 状态 - 基于后端是否运行来判断
                    if (healthResponse.IsSuccessStatusCode)
                    {
                        AIStatusValue.Text = "🟢 就绪";
                        AIStatusValue.Foreground = GreenBrush;
                    }
                    else
                    {
                        AIStatusValue.Text = "🔴 未就绪";
                        AIStatusValue.Foreground = RedBrush;
                    }
                }

                // 加载配置信息
                await LoadConfigForDisplay();
            }
            catch (Exception ex)
            {
                ShowNotification($"刷新状态失败: {ex.Message}", NotificationType.Error);
            }
        }

        private async Task LoadConfigForDisplay()
        {
            try
            {
                var response = await _httpClient.GetFromJsonAsync<ConfigResponse>("/api/config");
                if (response != null)
                {
                    // 更新人格设定显示
                    CurrentPersonaName.Text = $"人格名称：{response.personality?.name ?? "未设置"}";
                    CurrentPersonaDescription.Text = $"人格描述：{response.personality?.description ?? "未设置"}";
                    CurrentPersonaGreeting.Text = $"问候语：{response.personality?.greeting ?? "未设置"}";
                    CurrentPersonaTone.Text = $"语气：{response.personality?.tone ?? "未设置"}";
                }
            }
            catch (Exception ex)
            {
                // 静默处理配置加载失败
                Console.WriteLine($"配置加载失败: {ex.Message}");
            }
        }

        // OBS 控制方法
        private async Task ConnectToObs()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/connect", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("连接OBS成功", NotificationType.Success);
                    await RefreshStatus();
                }
                else
                {
                    ShowNotification($"连接OBS失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"连接OBS异常: {ex.Message}", NotificationType.Error);
            }
        }

        private async Task StartObsRecording()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/recording/start", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("开始OBS录制成功", NotificationType.Success);
                }
                else
                {
                    ShowNotification($"开始OBS录制失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"开始OBS录制异常: {ex.Message}", NotificationType.Error);
            }
        }

        private async Task StopObsRecording()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/recording/stop", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("停止OBS录制成功", NotificationType.Success);
                }
                else
                {
                    ShowNotification($"停止OBS录制失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"停止OBS录制异常: {ex.Message}", NotificationType.Error);
            }
        }

        private async Task StartObsStreaming()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/streaming/start", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("开始OBS推流成功", NotificationType.Success);
                }
                else
                {
                    ShowNotification($"开始OBS推流失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"开始OBS推流异常: {ex.Message}", NotificationType.Error);
            }
        }

        private async Task StopObsStreaming()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/streaming/stop", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("停止OBS推流成功", NotificationType.Success);
                }
                else
                {
                    ShowNotification($"停止OBS推流失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"停止OBS推流异常: {ex.Message}", NotificationType.Error);
            }
        }

        // VTS 控制方法
        private async Task ConnectToVts()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/vts/connect", new { });
                if (response.IsSuccessStatusCode)
                {
                    ShowNotification("连接VTuberStudio成功", NotificationType.Success);
                    await RefreshStatus();
                }
                else
                {
                    ShowNotification($"连接VTuberStudio失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"连接VTuberStudio异常: {ex.Message}", NotificationType.Error);
            }
        }

        // ASR 方法
        private async Task StartAsr()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/asr", new { });
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadFromJsonAsync<AsrResponse>();
                    if (result != null && !string.IsNullOrEmpty(result.text))
                    {
                        AddChatMessage("🎙️ 语音识别", result.text, Colors.Orange);
                        ShowNotification("语音识别完成", NotificationType.Info);
                    }
                }
                else
                {
                    ShowNotification($"语音识别失败: {response.StatusCode}", NotificationType.Error);
                }
            }
            catch (Exception ex)
            {
                ShowNotification($"语音识别异常: {ex.Message}", NotificationType.Error);
            }
        }

        private void StopAsr()
        {
            ShowNotification("已停止语音识别", NotificationType.Info);
        }

        private void ShowNotification(string message, NotificationType type)
        {
            // 这里可以实现实际的通知系统
            Console.WriteLine($"[{type}] {message}");
        }

        // 数据模型类
        public class ConfigResponse
        {
            public ChatApiConfig? chat_api { get; set; }
            public VoiceApiConfig? voice_api { get; set; }
            public ImageApiConfig? image_api { get; set; }
            public SearchApiConfig? search_api { get; set; }
            public DatabaseConfig? database { get; set; }
            public ObsConfig? obs { get; set; }
            public VtsConfig? vtuber_studio { get; set; }
            public PersonalityConfig? personality { get; set; }
        }

        public class ChatApiConfig
        {
            public string? api_key { get; set; }
            public string? base_url { get; set; }
            public string? model { get; set; }
            public double temperature { get; set; }
            public int max_tokens { get; set; }
        }

        public class VoiceApiConfig
        {
            public TtsConfig? tts { get; set; }
            public AsrConfig? asr { get; set; }
        }

        public class TtsConfig
        {
            public string? api_key { get; set; }
            public string? base_url { get; set; }
            public string? voice { get; set; }
        }

        public class AsrConfig
        {
            public string? api_key { get; set; }
            public string? base_url { get; set; }
        }

        public class ImageApiConfig
        {
            public string? api_key { get; set; }
            public string? base_url { get; set; }
        }

        public class SearchApiConfig
        {
            public string? api_key { get; set; }
            public string? base_url { get; set; }
        }

        public class DatabaseConfig
        {
            public bool enabled { get; set; }
            public string? db_path { get; set; }
        }

        public class ObsConfig
        {
            public bool enabled { get; set; }
            public string? host { get; set; }
            public int port { get; set; }
            public string? password { get; set; }
        }

        public class VtsConfig
        {
            public bool enabled { get; set; }
            public string? host { get; set; }
            public int port { get; set; }
        }

        public class PersonalityConfig
        {
            public string? name { get; set; }
            public string? description { get; set; }
            public string? greeting { get; set; }
            public string? tone { get; set; }
        }

        public class ChatResponse
        {
            public string response { get; set; } = string.Empty;
        }

        public class AsrResponse
        {
            public string text { get; set; } = string.Empty;
        }

        public class StatusResponse
        {
            public ObsStatus obs { get; set; } = new ObsStatus();
            public VtsStatus vts { get; set; } = new VtsStatus();
        }

        public class ObsStatus
        {
            public bool connected { get; set; } = false;
            public bool enabled { get; set; } = false;
        }

        public class VtsStatus
        {
            public bool connected { get; set; } = false;
            public bool enabled { get; set; } = false;
        }
    }
}