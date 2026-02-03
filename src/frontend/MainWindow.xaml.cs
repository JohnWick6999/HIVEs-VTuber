using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;

namespace AIVtuberTool
{
    public partial class MainWindow : Window
    {
        private readonly HttpClient _httpClient;
        private const string BackendBaseUrl = "http://localhost:8000";

        public MainWindow()
        {
            InitializeComponent();
            _httpClient = new HttpClient { BaseAddress = new Uri(BackendBaseUrl) };
            InitializeEvents();
            // 简化初始化，避免异步操作阻塞UI
            LoadConfigButton.Content = "加载配置";
            SaveConfigButton.Content = "保存配置";
            ResetConfigButton.Content = "重置配置";
        }

        private void InitializeEvents()
        {
            // 配置管理事件
            LoadConfigButton.Click += LoadConfigButton_Click;
            SaveConfigButton.Click += SaveConfigButton_Click;
            ResetConfigButton.Click += ResetConfigButton_Click;

            // 聊天事件
            SendButton.Click += SendButton_Click;

            // 语音事件
            TtsGenerateButton.Click += TtsGenerateButton_Click;
            AsrStartButton.Click += AsrStartButton_Click;
            AsrStopButton.Click += AsrStopButton_Click;

            // OBS/VTS事件
            ConnectObsButton.Click += ConnectObsButton_Click;
            DisconnectObsButton.Click += DisconnectObsButton_Click;
            ConnectVtsButton.Click += ConnectVtsButton_Click;
            StartRecordingButton.Click += StartRecordingButton_Click;
            StopRecordingButton.Click += StopRecordingButton_Click;
            StartStreamingButton.Click += StartStreamingButton_Click;
            StopStreamingButton.Click += StopStreamingButton_Click;
            SetSceneButton.Click += SetSceneButton_Click;
            TriggerHotkeyButton.Click += TriggerHotkeyButton_Click;
            SetExpressionButton.Click += SetExpressionButton_Click;

            // 系统状态事件
            RefreshStatusButton.Click += RefreshStatusButton_Click;
        }

        private async void LoadConfigButton_Click(object sender, RoutedEventArgs e)
        {
            await LoadConfig();
        }

        private async void SaveConfigButton_Click(object sender, RoutedEventArgs e)
        {
            await SaveConfig();
        }

        private async void ResetConfigButton_Click(object sender, RoutedEventArgs e)
        {
            await ResetConfig();
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            await SendChatMessage();
        }

        private async void TtsGenerateButton_Click(object sender, RoutedEventArgs e)
        {
            await GenerateTts();
        }

        private async void AsrStartButton_Click(object sender, RoutedEventArgs e)
        {
            await StartAsr();
        }

        private void AsrStopButton_Click(object sender, RoutedEventArgs e)
        {
            StopAsr();
        }

        private async void ConnectObsButton_Click(object sender, RoutedEventArgs e)
        {
            await ConnectToObs();
        }

        private async void DisconnectObsButton_Click(object sender, RoutedEventArgs e)
        {
            await DisconnectFromObs();
        }

        private async void ConnectVtsButton_Click(object sender, RoutedEventArgs e)
        {
            await ConnectToVts();
        }

        private async void StartRecordingButton_Click(object sender, RoutedEventArgs e)
        {
            await StartObsRecording();
        }

        private async void StopRecordingButton_Click(object sender, RoutedEventArgs e)
        {
            await StopObsRecording();
        }

        private async void StartStreamingButton_Click(object sender, RoutedEventArgs e)
        {
            await StartObsStreaming();
        }

        private async void StopStreamingButton_Click(object sender, RoutedEventArgs e)
        {
            await StopObsStreaming();
        }

        private async void SetSceneButton_Click(object sender, RoutedEventArgs e)
        {
            await SetObsScene();
        }

        private async void TriggerHotkeyButton_Click(object sender, RoutedEventArgs e)
        {
            await TriggerVtsHotkey();
        }

        private async void SetExpressionButton_Click(object sender, RoutedEventArgs e)
        {
            await SetVtsExpression();
        }

        private async void RefreshStatusButton_Click(object sender, RoutedEventArgs e)
        {
            await RefreshStatus();
        }

        private async Task LoadConfig()
        {
            try
            {
                var response = await _httpClient.GetFromJsonAsync<ConfigResponse>("/api/config");
                if (response != null)
                {
                    // Chat API
                    ChatApiKeyTextBox.Text = response.chat_api?.api_key ?? "";
                    ChatBaseUrlTextBox.Text = response.chat_api?.base_url ?? "";
                    ChatModelTextBox.Text = response.chat_api?.model ?? "";
                    ChatTemperatureTextBox.Text = response.chat_api != null ? response.chat_api.temperature.ToString() : "";
                    ChatMaxTokensTextBox.Text = response.chat_api != null ? response.chat_api.max_tokens.ToString() : "";

                    // Voice API
                    TtsApiKeyTextBox.Text = response.voice_api?.tts?.api_key ?? "";
                    TtsBaseUrlTextBox.Text = response.voice_api?.tts?.base_url ?? "";
                    TtsVoiceTextBox.Text = response.voice_api?.tts?.voice ?? "";
                    AsrApiKeyTextBox.Text = response.voice_api?.asr?.api_key ?? "";
                    AsrBaseUrlTextBox.Text = response.voice_api?.asr?.base_url ?? "";

                    // Image API
                    ImageApiKeyTextBox.Text = response.image_api?.api_key ?? "";
                    ImageBaseUrlTextBox.Text = response.image_api?.base_url ?? "";

                    // Search API
                    SearchApiKeyTextBox.Text = response.search_api?.api_key ?? "";
                    SearchBaseUrlTextBox.Text = response.search_api?.base_url ?? "";

                    // Database
                    DatabaseEnabledCheckBox.IsChecked = response.database?.enabled ?? false;
                    DatabasePathTextBox.Text = response.database?.db_path ?? "";

                    // OBS
                    ObsEnabledCheckBox.IsChecked = response.obs?.enabled ?? false;
                    ObsHostTextBox.Text = response.obs?.host ?? "";
                    ObsPortTextBox.Text = response.obs != null ? response.obs.port.ToString() : "";
                    ObsPasswordTextBox.Text = response.obs?.password ?? "";

                    // VTuberStudio
                    VtsEnabledCheckBox.IsChecked = response.vtuber_studio?.enabled ?? false;
                    VtsHostTextBox.Text = response.vtuber_studio?.host ?? "";
                    VtsPortTextBox.Text = response.vtuber_studio != null ? response.vtuber_studio.port.ToString() : "";

                    // Personality
                    PersonalityNameTextBox.Text = response.personality?.name ?? "";
                    PersonalityDescriptionTextBox.Text = response.personality?.description ?? "";
                    PersonalityGreetingTextBox.Text = response.personality?.greeting ?? "";
                    PersonalityToneTextBox.Text = response.personality?.tone ?? "";

                    ConfigStatusTextBlock.Text = "配置加载成功";
                }
            }
            catch (Exception ex)
            {
                ConfigStatusTextBlock.Text = $"配置加载失败: {ex.Message}";
                ConfigStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task SaveConfig()
        {
            try
            {
                var config = new ConfigRequest
                {
                    chat_api = new ChatApiConfig
                    {
                        api_key = ChatApiKeyTextBox.Text,
                        base_url = ChatBaseUrlTextBox.Text,
                        model = ChatModelTextBox.Text,
                        temperature = double.TryParse(ChatTemperatureTextBox.Text, out var temp) ? temp : 0.7,
                        max_tokens = int.TryParse(ChatMaxTokensTextBox.Text, out var tokens) ? tokens : 1024
                    },
                    voice_api = new VoiceApiConfig
                    {
                        tts = new TtsConfig
                        {
                            api_key = TtsApiKeyTextBox.Text,
                            base_url = TtsBaseUrlTextBox.Text,
                            voice = TtsVoiceTextBox.Text
                        },
                        asr = new AsrConfig
                        {
                            api_key = AsrApiKeyTextBox.Text,
                            base_url = AsrBaseUrlTextBox.Text
                        }
                    },
                    image_api = new ImageApiConfig
                    {
                        api_key = ImageApiKeyTextBox.Text,
                        base_url = ImageBaseUrlTextBox.Text
                    },
                    search_api = new SearchApiConfig
                    {
                        api_key = SearchApiKeyTextBox.Text,
                        base_url = SearchBaseUrlTextBox.Text
                    },
                    database = new DatabaseConfig
                    {
                        enabled = DatabaseEnabledCheckBox.IsChecked ?? false,
                        db_path = DatabasePathTextBox.Text
                    },
                    obs = new ObsConfig
                    {
                        enabled = ObsEnabledCheckBox.IsChecked ?? false,
                        host = ObsHostTextBox.Text,
                        port = int.TryParse(ObsPortTextBox.Text, out var obsPort) ? obsPort : 4444,
                        password = ObsPasswordTextBox.Text
                    },
                    vtuber_studio = new VtsConfig
                    {
                        enabled = VtsEnabledCheckBox.IsChecked ?? false,
                        host = VtsHostTextBox.Text,
                        port = int.TryParse(VtsPortTextBox.Text, out var vtsPort) ? vtsPort : 8001
                    },
                    personality = new PersonalityConfig
                    {
                        name = PersonalityNameTextBox.Text,
                        description = PersonalityDescriptionTextBox.Text,
                        greeting = PersonalityGreetingTextBox.Text,
                        tone = PersonalityToneTextBox.Text
                    }
                };

                var response = await _httpClient.PostAsJsonAsync("/api/config", config);
                if (response.IsSuccessStatusCode)
                {
                    ConfigStatusTextBlock.Text = "配置保存成功";
                    ConfigStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ConfigStatusTextBlock.Text = $"配置保存失败: {response.StatusCode}";
                    ConfigStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ConfigStatusTextBlock.Text = $"配置保存失败: {ex.Message}";
                ConfigStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task ResetConfig()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/config", new { });
                if (response.IsSuccessStatusCode)
                {
                    await LoadConfig();
                    ConfigStatusTextBlock.Text = "配置重置成功";
                    ConfigStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ConfigStatusTextBlock.Text = $"配置重置失败: {response.StatusCode}";
                    ConfigStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ConfigStatusTextBlock.Text = $"配置重置失败: {ex.Message}";
                ConfigStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task SendChatMessage()
        {
            try
            {
                var userInput = ChatInputTextBox.Text.Trim();
                if (string.IsNullOrEmpty(userInput))
                {
                    ChatStatusTextBlock.Text = "输入不能为空";
                    ChatStatusTextBlock.Foreground = Brushes.Red;
                    return;
                }

                // 添加用户消息到聊天历史
                AddChatMessage("用户", userInput, Brushes.Blue);
                ChatInputTextBox.Clear();

                // 发送到后端
                var request = new { input = userInput };
                var response = await _httpClient.PostAsJsonAsync("/api/chat", request);
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadFromJsonAsync<ChatResponse>();
                    if (result != null && !string.IsNullOrEmpty(result.response))
                    {
                        // 添加AI回复到聊天历史
                        AddChatMessage("AI", result.response, Brushes.Green);
                        ChatStatusTextBlock.Text = "消息发送成功";
                        ChatStatusTextBlock.Foreground = Brushes.Green;
                    }
                }
                else
                {
                    ChatStatusTextBlock.Text = $"消息发送失败: {response.StatusCode}";
                    ChatStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ChatStatusTextBlock.Text = $"消息发送失败: {ex.Message}";
                ChatStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task GenerateTts()
        {
            try
            {
                var text = TtsInputTextBox.Text.Trim();
                if (string.IsNullOrEmpty(text))
                {
                    TtsStatusTextBlock.Text = "文本不能为空";
                    TtsStatusTextBlock.Foreground = Brushes.Red;
                    return;
                }

                var request = new { text, output_file = "output.wav" };
                var response = await _httpClient.PostAsJsonAsync("/api/tts", request);
                if (response.IsSuccessStatusCode)
                {
                    TtsStatusTextBlock.Text = "语音生成成功";
                    TtsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    TtsStatusTextBlock.Text = $"语音生成失败: {response.StatusCode}";
                    TtsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                TtsStatusTextBlock.Text = $"语音生成失败: {ex.Message}";
                TtsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task StartAsr()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/asr", new { });
                if (response.IsSuccessStatusCode)
                {
                    var result = await response.Content.ReadFromJsonAsync<AsrResponse>();
                    if (result != null)
                    {
                        AsrOutputTextBox.Text = result.text;
                        AsrStatusTextBlock.Text = "语音识别成功";
                        AsrStatusTextBlock.Foreground = Brushes.Green;
                    }
                }
                else
                {
                    AsrStatusTextBlock.Text = $"语音识别失败: {response.StatusCode}";
                    AsrStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                AsrStatusTextBlock.Text = $"语音识别失败: {ex.Message}";
                AsrStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private void StopAsr()
        {
            // 实现停止录音的逻辑
            AsrStatusTextBlock.Text = "录音已停止";
            AsrStatusTextBlock.Foreground = Brushes.Green;
        }

        private async Task ConnectToObs()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/connect", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "连接OBS成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"连接OBS失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"连接OBS失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task DisconnectFromObs()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/disconnect", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "断开OBS连接成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"断开OBS连接失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"断开OBS连接失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task ConnectToVts()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/vts/connect", new { });
                if (response.IsSuccessStatusCode)
                {
                    VtsStatusTextBlock.Text = "连接VTuberStudio成功";
                    VtsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    VtsStatusTextBlock.Text = $"连接VTuberStudio失败: {response.StatusCode}";
                    VtsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                VtsStatusTextBlock.Text = $"连接VTuberStudio失败: {ex.Message}";
                VtsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task StartObsRecording()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/recording/start", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "开始OBS录制成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"开始OBS录制失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"开始OBS录制失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task StopObsRecording()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/recording/stop", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "停止OBS录制成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"停止OBS录制失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"停止OBS录制失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task StartObsStreaming()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/streaming/start", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "开始OBS推流成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"开始OBS推流失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"开始OBS推流失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task StopObsStreaming()
        {
            try
            {
                var response = await _httpClient.PostAsJsonAsync("/api/obs/streaming/stop", new { });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "停止OBS推流成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"停止OBS推流失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"停止OBS推流失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task SetObsScene()
        {
            try
            {
                var sceneName = ObsSceneTextBox.Text.Trim();
                if (string.IsNullOrEmpty(sceneName))
                {
                    ObsStatusTextBlock.Text = "场景名称不能为空";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                    return;
                }

                var response = await _httpClient.PostAsJsonAsync("/api/obs/scene", new { scene_name = sceneName });
                if (response.IsSuccessStatusCode)
                {
                    ObsStatusTextBlock.Text = "设置OBS场景成功";
                    ObsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    ObsStatusTextBlock.Text = $"设置OBS场景失败: {response.StatusCode}";
                    ObsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                ObsStatusTextBlock.Text = $"设置OBS场景失败: {ex.Message}";
                ObsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task TriggerVtsHotkey()
        {
            try
            {
                var hotkeyName = VtsHotkeyTextBox.Text.Trim();
                if (string.IsNullOrEmpty(hotkeyName))
                {
                    VtsStatusTextBlock.Text = "热键名称不能为空";
                    VtsStatusTextBlock.Foreground = Brushes.Red;
                    return;
                }

                var response = await _httpClient.PostAsJsonAsync("/api/vts/hotkey", new { hotkey_name = hotkeyName });
                if (response.IsSuccessStatusCode)
                {
                    VtsStatusTextBlock.Text = "触发VTuberStudio热键成功";
                    VtsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    VtsStatusTextBlock.Text = $"触发VTuberStudio热键失败: {response.StatusCode}";
                    VtsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                VtsStatusTextBlock.Text = $"触发VTuberStudio热键失败: {ex.Message}";
                VtsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task SetVtsExpression()
        {
            try
            {
                var expressionName = VtsExpressionTextBox.Text.Trim();
                if (string.IsNullOrEmpty(expressionName))
                {
                    VtsStatusTextBlock.Text = "表情名称不能为空";
                    VtsStatusTextBlock.Foreground = Brushes.Red;
                    return;
                }

                var response = await _httpClient.PostAsJsonAsync("/api/vts/expression", new { expression_name = expressionName });
                if (response.IsSuccessStatusCode)
                {
                    VtsStatusTextBlock.Text = "设置VTuberStudio表情成功";
                    VtsStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    VtsStatusTextBlock.Text = $"设置VTuberStudio表情失败: {response.StatusCode}";
                    VtsStatusTextBlock.Foreground = Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                VtsStatusTextBlock.Text = $"设置VTuberStudio表情失败: {ex.Message}";
                VtsStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private async Task RefreshStatus()
        {
            try
            {
                var healthResponse = await _httpClient.GetFromJsonAsync<HealthResponse>("/health");
                if (healthResponse != null && healthResponse.status == "healthy")
                {
                    BackendStatusTextBlock.Text = "后端服务运行正常";
                    BackendStatusTextBlock.Foreground = Brushes.Green;
                }
                else
                {
                    BackendStatusTextBlock.Text = "后端服务未运行";
                    BackendStatusTextBlock.Foreground = Brushes.Red;
                }

                var statusResponse = await _httpClient.GetFromJsonAsync<StatusResponse>("/api/status");
                if (statusResponse != null)
                {
                    ObsStatusTextBlock.Text = statusResponse.obs?.connected ?? false ? "OBS已连接" : "OBS未连接";
                    ObsStatusTextBlock.Foreground = statusResponse.obs?.connected ?? false ? Brushes.Green : Brushes.Red;
                    VtsStatusTextBlock.Text = statusResponse.vts?.connected ?? false ? "VTuberStudio已连接" : "VTuberStudio未连接";
                    VtsStatusTextBlock.Foreground = statusResponse.vts?.connected ?? false ? Brushes.Green : Brushes.Red;
                }
            }
            catch (Exception ex)
            {
                BackendStatusTextBlock.Text = $"后端服务未运行: {ex.Message}";
                BackendStatusTextBlock.Foreground = Brushes.Red;
            }
        }

        private void AddChatMessage(string sender, string message, Brush color)
        {
            var messageText = new TextBlock
            {
                Text = $"[{DateTime.Now:HH:mm:ss}] {sender}: {message}",
                Foreground = color,
                Margin = new Thickness(5),
                TextWrapping = TextWrapping.Wrap
            };
            ChatHistoryListBox.Items.Add(messageText);
            ChatHistoryListBox.ScrollIntoView(ChatHistoryListBox.Items[ChatHistoryListBox.Items.Count - 1]);
        }

        // 配置相关的类
        public class ConfigResponse
        {
            public ChatApiConfig chat_api { get; set; } = new ChatApiConfig();
            public VoiceApiConfig voice_api { get; set; } = new VoiceApiConfig();
            public ImageApiConfig image_api { get; set; } = new ImageApiConfig();
            public SearchApiConfig search_api { get; set; } = new SearchApiConfig();
            public DatabaseConfig database { get; set; } = new DatabaseConfig();
            public ObsConfig obs { get; set; } = new ObsConfig();
            public VtsConfig vtuber_studio { get; set; } = new VtsConfig();
            public PersonalityConfig personality { get; set; } = new PersonalityConfig();
        }

        public class ConfigRequest
        {
            public ChatApiConfig chat_api { get; set; } = new ChatApiConfig();
            public VoiceApiConfig voice_api { get; set; } = new VoiceApiConfig();
            public ImageApiConfig image_api { get; set; } = new ImageApiConfig();
            public SearchApiConfig search_api { get; set; } = new SearchApiConfig();
            public DatabaseConfig database { get; set; } = new DatabaseConfig();
            public ObsConfig obs { get; set; } = new ObsConfig();
            public VtsConfig vtuber_studio { get; set; } = new VtsConfig();
            public PersonalityConfig personality { get; set; } = new PersonalityConfig();
        }

        public class ChatApiConfig
        {
            public string api_key { get; set; } = string.Empty;
            public string base_url { get; set; } = string.Empty;
            public string model { get; set; } = string.Empty;
            public double temperature { get; set; } = 0.7;
            public int max_tokens { get; set; } = 1000;
        }

        public class VoiceApiConfig
        {
            public TtsConfig tts { get; set; } = new TtsConfig();
            public AsrConfig asr { get; set; } = new AsrConfig();
        }

        public class TtsConfig
        {
            public string api_key { get; set; } = string.Empty;
            public string base_url { get; set; } = string.Empty;
            public string voice { get; set; } = "default";
        }

        public class AsrConfig
        {
            public string api_key { get; set; } = string.Empty;
            public string base_url { get; set; } = string.Empty;
        }

        public class ImageApiConfig
        {
            public string api_key { get; set; } = string.Empty;
            public string base_url { get; set; } = string.Empty;
        }

        public class SearchApiConfig
        {
            public string api_key { get; set; } = string.Empty;
            public string base_url { get; set; } = string.Empty;
        }

        public class DatabaseConfig
        {
            public bool enabled { get; set; } = false;
            public string db_path { get; set; } = string.Empty;
        }

        public class ObsConfig
        {
            public bool enabled { get; set; } = false;
            public string host { get; set; } = string.Empty;
            public int port { get; set; } = 4444;
            public string password { get; set; } = string.Empty;
        }

        public class VtsConfig
        {
            public bool enabled { get; set; } = false;
            public string host { get; set; } = string.Empty;
            public int port { get; set; } = 8001;
        }

        public class PersonalityConfig
        {
            public string name { get; set; } = string.Empty;
            public string description { get; set; } = string.Empty;
            public string greeting { get; set; } = string.Empty;
            public string tone { get; set; } = string.Empty;
        }

        // 响应相关的类
        public class ChatResponse
        {
            public string response { get; set; } = string.Empty;
        }

        public class AsrResponse
        {
            public string text { get; set; } = string.Empty;
        }

        public class HealthResponse
        {
            public string status { get; set; } = string.Empty;
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
