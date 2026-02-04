<template>
  <div class="app-container" :class="{ 'dark-mode': isDarkMode }">
    <header class="app-header">
      <h1>HIVE's VTuber</h1>
      <div class="status-bar">
        <span :class="{ 'status-healthy': backendStatus === 'healthy' }">
          后端服务: {{ backendStatus === "healthy" ? "运行中" : "未运行" }}
        </span>
        <button class="theme-toggle" @click="toggleDarkMode">
          {{ isDarkMode ? '🌞' : '🌙' }}
        </button>
      </div>
    </header>

    <main class="app-main">
      <nav class="sidebar">
        <ul>
          <li
            @click="activeTab = 'chat'"
            :class="{ active: activeTab === 'chat' }"
          >
            <span class="tab-icon">💬</span>
            <span>聊天</span>
          </li>
          <li
            @click="activeTab = 'voice'"
            :class="{ active: activeTab === 'voice' }"
          >
            <span class="tab-icon">🎤</span>
            <span>语音</span>
          </li>
          <li
            @click="activeTab = 'obs'"
            :class="{ active: activeTab === 'obs' }"
          >
            <span class="tab-icon">📹</span>
            <span>OBS</span>
          </li>
          <li
            @click="activeTab = 'vts'"
            :class="{ active: activeTab === 'vts' }"
          >
            <span class="tab-icon">🎭</span>
            <span>VTuberStudio</span>
          </li>
          <li
            @click="activeTab = 'config'"
            :class="{ active: activeTab === 'config' }"
          >
            <span class="tab-icon">⚙️</span>
            <span>配置</span>
          </li>
          <li class="version-info">
            <span class="tab-icon">📦</span>
            <span>pre-version 0.0.2</span>
          </li>
        </ul>
      </nav>

      <div class="content">
        <div v-if="activeTab === 'chat'" class="tab-content">
          <h2>聊天界面</h2>
          <div class="chat-container">
            <div class="chat-history">
              <div
                v-for="(message, index) in chatHistory"
                :key="index"
                :class="{
                  'user-message': message.role === 'user',
                  'ai-message': message.role === 'assistant',
                }"
              >
                <div class="message-header">
                  <span class="message-sender">{{
                    message.role === "user" ? "用户" : "AI"
                  }}</span>
                  <span class="message-time">{{ message.time }}</span>
                </div>
                <div class="message-content">{{ message.content }}</div>
              </div>
            </div>
            <div class="chat-input">
              <input
                v-model="chatInput"
                type="text"
                placeholder="输入消息..."
                @keyup.enter="sendMessage"
              />
              <button @click="sendMessage">发送</button>
            </div>
            <div class="chat-status">{{ chatStatus }}</div>
          </div>
        </div>

        <div v-if="activeTab === 'voice'" class="tab-content">
          <h2>语音功能</h2>
          <div class="voice-container">
            <div class="tts-section">
              <h3>文本转语音</h3>
              <textarea
                v-model="ttsText"
                placeholder="输入要转换的文本..."
                rows="4"
              ></textarea>
              <button @click="generateTTS">生成语音</button>
              <div class="voice-status">{{ ttsStatus }}</div>
            </div>
            <div class="asr-section">
              <h3>语音转文本</h3>
              <div class="asr-result">{{ asrText }}</div>
              <div class="asr-buttons">
                <button @click="startASR">开始录音</button>
                <button @click="stopASR">停止录音</button>
              </div>
              <div class="voice-status">{{ asrStatus }}</div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'obs'" class="tab-content">
          <h2>OBS控制</h2>
          <div class="obs-container">
            <div class="obs-connection">
              <button @click="startOBSCmd">启动OBS-CMD</button>
              <button @click="openOBS">打开OBS</button>
              <button @click="closeOBS">关闭OBS</button>
            </div>
            <div class="obs-status">{{ obsStatus }}</div>
          </div>
        </div>

        <div v-if="activeTab === 'vts'" class="tab-content">
          <h2>VTuberStudio控制</h2>
          <div class="vts-container">
            <div class="vts-connection">
              <button @click="openVTuberStudio">打开VTuberStudio</button>
              <button @click="closeVTuberStudio">关闭VTuberStudio</button>
            </div>
            <div class="vts-status">{{ vtsStatus }}</div>
          </div>
        </div>

        <div v-if="activeTab === 'config'" class="tab-content">
          <h2>配置管理</h2>
          <div class="config-container">
            <div class="config-buttons">
              <button @click="loadConfig">加载配置</button>
              <button @click="saveConfig">保存配置</button>
              <button @click="resetConfig">重置配置</button>
            </div>
            <div class="config-status">{{ configStatus }}</div>

            <div class="config-sections">
              <div class="config-section">
                <h3>聊天API</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>API Key:</label>
                    <input v-model="config.chat_api.api_key" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Base URL:</label>
                    <input v-model="config.chat_api.base_url" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Model:</label>
                    <input v-model="config.chat_api.model" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Temperature:</label>
                    <input
                      v-model.number="config.chat_api.temperature"
                      type="number"
                      step="0.1"
                    />
                  </div>
                  <div class="field-group">
                    <label>Max Tokens:</label>
                    <input
                      v-model.number="config.chat_api.max_tokens"
                      type="number"
                    />
                  </div>
                </div>
              </div>

              <div class="config-section">
                <h3>语音API</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>TTS API Key:</label>
                    <input v-model="config.voice_api.tts.api_key" type="text" />
                  </div>
                  <div class="field-group">
                    <label>TTS Base URL:</label>
                    <input v-model="config.voice_api.tts.base_url" type="text" />
                  </div>
                  <div class="field-group">
                    <label>TTS Voice:</label>
                    <input v-model="config.voice_api.tts.voice" type="text" />
                  </div>
                  <div class="field-group">
                    <label>TTS Engine:</label>
                    <input v-model="config.voice_api.tts.engine" type="text" />
                  </div>
                  <div class="field-group">
                    <label>ASR API Key:</label>
                    <input v-model="config.voice_api.asr.api_key" type="text" />
                  </div>
                  <div class="field-group">
                    <label>ASR Base URL:</label>
                    <input v-model="config.voice_api.asr.base_url" type="text" />
                  </div>
                </div>
              </div>

              <div class="config-section">
                <h3>图像API</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>API Key:</label>
                    <input v-model="config.image_api.api_key" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Base URL:</label>
                    <input v-model="config.image_api.base_url" type="text" />
                  </div>
                </div>
              </div>

              <div class="config-section">
                <h3>搜索API</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>API Key:</label>
                    <input v-model="config.search_api.api_key" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Base URL:</label>
                    <input v-model="config.search_api.base_url" type="text" />
                  </div>
                  <div class="field-group">
                    <label>Model:</label>
                    <input v-model="config.search_api.model" type="text" />
                  </div>
                </div>
              </div>

              <div class="config-section">
                <h3>数据库配置</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>启用数据库:</label>
                    <input v-model="config.database.enabled" type="checkbox" />
                  </div>
                  <div class="field-group">
                    <label>数据库路径:</label>
                    <input v-model="config.database.db_path" type="text" />
                  </div>
                </div>
              </div>



              <div class="config-section">
                <h3>人格配置</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>名称:</label>
                    <input v-model="config.personality.name" type="text" />
                  </div>
                  <div class="field-group">
                    <label>描述:</label>
                    <input v-model="config.personality.description" type="text" />
                  </div>
                  <div class="field-group">
                    <label>问候语:</label>
                    <input v-model="config.personality.greeting" type="text" />
                  </div>
                  <div class="field-group">
                    <label>语气:</label>
                    <input v-model="config.personality.tone" type="text" />
                  </div>
                </div>
              </div>

              <div class="config-section">
                <h3>软件地址</h3>
                <div class="config-fields">
                  <div class="field-group">
                    <label>OBS软件地址:</label>
                    <input v-model="config.software_paths.obs" type="text" placeholder="例如: C:\Program Files\obs-studio\bin\64bit\obs64.exe" />
                  </div>
                  <div class="field-group">
                    <label>VTS软件地址:</label>
                    <input v-model="config.software_paths.vts" type="text" placeholder="例如: C:\Program Files\VTuber Studio\VTuber Studio.exe" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

// 状态管理
const activeTab = ref("chat");
const backendStatus = ref("");
const chatInput = ref("");
const chatHistory = ref([]);
const chatStatus = ref("");
const ttsText = ref("");
const ttsStatus = ref("");
const asrText = ref("");
const asrStatus = ref("");
const obsStatus = ref("");
const vtsStatus = ref("");
const configStatus = ref("");
const isDarkMode = ref(false);

// 配置数据
const config = ref({
  chat_api: {
    api_key: "",
    base_url: "",
    model: "",
    temperature: 0.7,
    max_tokens: 1024,
  },
  voice_api: {
    tts: {
      api_key: "",
      base_url: "",
      voice: "",
      engine: "qwen",
    },
    asr: {
      api_key: "",
      base_url: "",
    },
  },
  image_api: {
    api_key: "",
    base_url: "",
  },
  search_api: {
    api_key: "",
    base_url: "",
    model: "",
  },
  database: {
    enabled: false,
    db_path: "chat_history.db",
  },
  personality: {
    name: "AI Vtuber",
    description: "一个友好的AI虚拟主播",
    greeting: "你好！我是你的AI虚拟主播，很高兴认识你！",
    tone: "活泼、友好、幽默",
  },
  software_paths: {
    obs: "",
    vts: "",
  },
});

// API基础URL
const API_BASE_URL = "http://localhost:8080/api";

// 健康检查
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    backendStatus.value = data.status;
  } catch (error) {
    backendStatus.value = "unhealthy";
  }
}

// 聊天功能
async function sendMessage() {
  if (!chatInput.value.trim()) {
    chatStatus.value = "输入不能为空";
    return;
  }

  const userMessage = chatInput.value.trim();
  chatHistory.value.push({
    role: "user",
    content: userMessage,
    time: new Date().toLocaleTimeString(),
  });
  chatInput.value = "";

  try {
    chatStatus.value = "发送中...";
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: userMessage }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      chatStatus.value = `发送失败: ${errorData.error || response.statusText}`;
      return;
    }
    
    const data = await response.json();
    chatHistory.value.push({
      role: "assistant",
      content: data.response,
      time: new Date().toLocaleTimeString(),
    });
    chatStatus.value = "消息发送成功";
  } catch (error) {
    console.error("聊天发送错误:", error);
    chatStatus.value = "网络错误，请检查后端服务是否运行";
  }
}

// 语音功能
async function generateTTS() {
  if (!ttsText.value.trim()) {
    ttsStatus.value = "文本不能为空";
    return;
  }

  try {
    ttsStatus.value = "生成中...";
    const response = await fetch(`${API_BASE_URL}/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: ttsText.value, output_file: "output.wav" }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      ttsStatus.value = `生成失败: ${errorData.error || response.statusText}`;
      return;
    }
    
    const data = await response.json();
    ttsStatus.value = "语音生成成功";
  } catch (error) {
    console.error("语音生成错误:", error);
    ttsStatus.value = "网络错误，请检查后端服务是否运行";
  }
}

async function startASR() {
  try {
    asrStatus.value = "识别中...";
    const response = await fetch(`${API_BASE_URL}/asr`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      asrStatus.value = `识别失败: ${errorData.error || response.statusText}`;
      return;
    }
    
    const data = await response.json();
    asrText.value = data.text;
    asrStatus.value = "语音识别成功";
  } catch (error) {
    console.error("语音识别错误:", error);
    asrStatus.value = "网络错误，请检查后端服务是否运行";
  }
}

function stopASR() {
  asrStatus.value = "录音已停止";
}

// OBS功能
async function startOBSCmd() {
  try {
    obsStatus.value = "启动OBS-CMD...";
    // 这里我们不需要启动obs-cmd进程，因为我们会在每个命令中直接调用它
    // 检查obs-cmd是否可以正常工作
    const testResponse = await fetch(`${API_BASE_URL}/obs/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (testResponse.ok) {
      obsStatus.value = "OBS-CMD启动成功";
    } else {
      obsStatus.value = "OBS-CMD启动失败";
    }
  } catch (error) {
    console.error("启动OBS-CMD错误:", error);
    obsStatus.value = "OBS-CMD启动失败";
  }
}



async function openOBS() {
  try {
    obsStatus.value = "打开OBS...";
    const response = await fetch(`${API_BASE_URL}/obs/open`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: config.value.software_paths.obs }),
    });
    if (response.ok) {
      obsStatus.value = "OBS已打开";
    } else {
      obsStatus.value = "打开OBS失败";
    }
  } catch (error) {
    console.error("打开OBS错误:", error);
    obsStatus.value = "打开OBS失败";
  }
}

async function closeOBS() {
  try {
    obsStatus.value = "关闭OBS...";
    const response = await fetch(`${API_BASE_URL}/obs/close`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (response.ok) {
      obsStatus.value = "OBS已关闭";
    } else {
      obsStatus.value = "关闭OBS失败";
    }
  } catch (error) {
    console.error("关闭OBS错误:", error);
    obsStatus.value = "关闭OBS失败";
  }
}

// VTuberStudio功能
async function openVTuberStudio() {
  try {
    vtsStatus.value = "打开VTuberStudio...";
    const response = await fetch(`${API_BASE_URL}/vts/open`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: config.value.software_paths.vts }),
    });
    if (response.ok) {
      vtsStatus.value = "VTuberStudio已打开";
    } else {
      vtsStatus.value = "打开VTuberStudio失败";
    }
  } catch (error) {
    console.error("打开VTuberStudio错误:", error);
    vtsStatus.value = "打开VTuberStudio失败";
  }
}

async function closeVTuberStudio() {
  try {
    vtsStatus.value = "关闭VTuberStudio...";
    const response = await fetch(`${API_BASE_URL}/vts/close`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (response.ok) {
      vtsStatus.value = "VTuberStudio已关闭";
    } else {
      vtsStatus.value = "关闭VTuberStudio失败";
    }
  } catch (error) {
    console.error("关闭VTuberStudio错误:", error);
    vtsStatus.value = "关闭VTuberStudio失败";
  }
}

// 配置功能
async function loadConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/config`);
    const data = await response.json();
    console.log('从后端获取的配置数据:', data);
    
    // 直接更新配置
    if (data.search_api) {
      config.value.search_api = data.search_api;
      console.log('更新搜索API配置:', config.value.search_api);
    }
    if (data.image_api) {
      config.value.image_api = data.image_api;
    }
    if (data.database) {
      config.value.database = data.database;
    }
    if (data.personality) {
      config.value.personality = data.personality;
    }
    if (data.software_paths) {
      config.value.software_paths = data.software_paths;
    }
    if (data.voice_api) {
      config.value.voice_api = data.voice_api;
      console.log('更新语音API配置:', config.value.voice_api);
      console.log('语音API TTS配置:', config.value.voice_api.tts);
    }
    if (data.chat_api) {
      config.value.chat_api = data.chat_api;
    }
    
    configStatus.value = "配置加载成功";
  } catch (error) {
    console.error('加载配置失败:', error);
    configStatus.value = "配置加载失败";
  }
}

async function saveConfig() {
  try {
    console.log("保存配置前的config.value:", config.value);
    console.log("保存配置前的software_paths:", config.value.software_paths);
    
    const response = await fetch(`${API_BASE_URL}/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config.value),
    });
    
    console.log("保存配置的响应状态:", response.status);
    const responseData = await response.json();
    console.log("保存配置的响应数据:", responseData);
    
    configStatus.value = "配置保存成功";
  } catch (error) {
    console.error("保存配置失败:", error);
    configStatus.value = "配置保存失败";
  }
}

async function resetConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    await loadConfig();
    configStatus.value = "配置重置成功";
  } catch (error) {
    configStatus.value = "配置重置失败";
  }
}

// 明暗模式切换
function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value;
}



// 初始化
onMounted(() => {
  checkBackendHealth();
  // 加载配置
  loadConfig();
});
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  font-family: Arial, sans-serif;
  transition: background-color 0.3s ease, color 0.3s ease;
  background-color: #ffffff;
  color: #333333;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.app-container.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.app-container.dark-mode .app-header {
  background-color: #1e1e1e;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.status-bar {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status-healthy {
  color: #27ae60;
}

.theme-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: transform 0.3s ease, background-color 0.3s ease;
  color: white;
}

.theme-toggle:hover {
  transform: rotate(180deg);
  background-color: rgba(255, 255, 255, 0.1);
}

.theme-toggle:active {
  transform: rotate(180deg) scale(0.9);
}

.app-container.dark-mode .theme-toggle {
  color: #e0e0e0;
  background-color: rgba(255, 255, 255, 0.1);
}

.app-container.dark-mode .theme-toggle:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.app-container.dark-mode .app-main {
  background-color: #1e1e1e;
}

.sidebar {
  width: 200px;
  background-color: #34495e;
  color: white;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: background-color 0.3s ease, width 0.3s ease;
}

.app-container.dark-mode .sidebar {
  background-color: #1e1e1e;
  border-right: 1px solid #333333;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.sidebar li {
  display: flex;
  align-items: center;
  padding: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.sidebar li:hover {
  background-color: #2c3e50;
  transform: translateX(5px);
}

.app-container.dark-mode .sidebar li:hover {
  background-color: #2d2d2d;
  transform: translateX(5px);
}

.sidebar li.active {
  background-color: #3498db;
  transform: none;
}

.app-container.dark-mode .sidebar li.active {
  background-color: #1e3a5f;
  transform: none;
}

.tab-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #f5f5f5;
  transition: background-color 0.3s ease;
}

.app-container.dark-mode .content {
  background-color: #121212;
}

.tab-content {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.app-container.dark-mode .tab-content {
  background-color: #1e1e1e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid #333333;
}

.app-container.dark-mode .tab-content h2 {
  color: #e0e0e0;
}

.tab-content h2 {
  margin-top: 0;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

/* 聊天样式 */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .chat-history {
  background-color: #1e1e1e;
  border-color: #333333;
}

.user-message,
.ai-message {
  margin-bottom: 1rem;
  padding: 0.8rem;
  border-radius: 8px;
  max-width: 80%;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.user-message {
  align-self: flex-end;
  background-color: #e3f2fd;
  margin-left: auto;
}

.app-container.dark-mode .user-message {
  background-color: #1e3a5f;
  color: #e0e0e0;
}

.ai-message {
  align-self: flex-start;
  background-color: #f1f1f1;
}

.app-container.dark-mode .ai-message {
  background-color: #2d2d2d;
  color: #e0e0e0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #333;
  transition: color 0.3s ease;
}

.app-container.dark-mode .message-header {
  color: #aaa;
}

.message-content {
  color: #222;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.app-container.dark-mode .message-content {
  color: #e0e0e0;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.chat-input input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #222;
  background-color: white;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .chat-input input {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #333333;
}

.chat-input button {
  padding: 0.8rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chat-input button:hover {
  background-color: #2980b9;
}

.app-container.dark-mode .chat-input button {
  background-color: #1e3a5f;
}

.app-container.dark-mode .chat-input button:hover {
  background-color: #1a3251;
}

/* 语音样式 */
.voice-container {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.tts-section,
.asr-section {
  flex: 1;
  min-width: 300px;
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .tts-section,
.app-container.dark-mode .asr-section {
  background-color: #1e1e1e;
  border-color: #333333;
}

.tts-section h3,
.asr-section h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.app-container.dark-mode .tts-section h3,
.app-container.dark-mode .asr-section h3 {
  color: #e0e0e0;
}

.tts-section textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 1rem;
  min-height: 100px;
  background-color: white;
  color: #333;
  font-size: 16px;
  box-sizing: border-box;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .tts-section textarea {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #333333;
}

.asr-result {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  min-height: 100px;
  margin-bottom: 1rem;
  background-color: white;
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.app-container.dark-mode .asr-result {
  background-color: #2d2d2d;
  border-color: #333333;
  color: #e0e0e0;
}

.asr-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

/* OBS和VTS样式 */
.obs-container,
.vts-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.obs-connection,
.vts-connection {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.obs-controls,
.vts-controls {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .obs-controls,
.app-container.dark-mode .vts-controls {
  background-color: #1e1e1e;
  border-color: #333333;
}

.obs-controls h3,
.vts-controls h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.app-container.dark-mode .obs-controls h3,
.app-container.dark-mode .vts-controls h3 {
  color: #e0e0e0;
}

.obs-controls input,
.vts-controls input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .obs-controls input,
.app-container.dark-mode .vts-controls input {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #333333;
}

/* 配置样式 */
.config-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.config-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.config-sections {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.config-section {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .config-section {
  background-color: #1e1e1e;
  border-color: #333333;
}

.config-section h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.app-container.dark-mode .config-section h3 {
  color: #e0e0e0;
}

.config-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-group label {
  font-size: 0.9rem;
  color: #555;
  transition: color 0.3s ease;
}

.app-container.dark-mode .field-group label {
  color: #aaa;
}

.field-group input {
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.app-container.dark-mode .field-group input {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #333333;
}

/* 通用按钮样式 */
button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
  background-color: #3498db;
  color: white;
}

button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(1px);
}

.app-container.dark-mode button {
  background-color: #1e3a5f;
}

.app-container.dark-mode button:hover {
  background-color: #1a3251;
}

/* 版本信息样式 */
.version-info {
  margin-top: auto;
  padding-top: 2rem;
  opacity: 0.7;
  font-size: 0.8rem;
  transition: color 0.3s ease;
}

.app-container.dark-mode .version-info {
  color: #aaa;
}

/* 状态样式 */
.chat-status,
.voice-status,
.obs-status,
.vts-status,
.config-status {
  margin-top: 0.5rem;
  padding: 0;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  min-height: 0;
  overflow: hidden;
  background-color: transparent;
  border: none;
  color: transparent;
}

/* 当状态有内容时显示背景和边框 */
.chat-status:not(:empty),
.voice-status:not(:empty),
.obs-status:not(:empty),
.vts-status:not(:empty),
.config-status:not(:empty) {
  padding: 0.5rem;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #333;
}

.app-container.dark-mode .chat-status:not(:empty),
.app-container.dark-mode .voice-status:not(:empty),
.app-container.dark-mode .obs-status:not(:empty),
.app-container.dark-mode .vts-status:not(:empty),
.app-container.dark-mode .config-status:not(:empty) {
  background-color: #1e1e1e;
  color: #e0e0e0;
  border: 1px solid #333333;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  /* 平板模式 */
  .app-header {
    padding: 1rem;
  }
  
  .app-header h1 {
    font-size: 1.2rem;
  }
  
  .content {
    padding: 1.5rem;
  }
  
  .tab-content {
    padding: 1.5rem;
  }
  
  .config-fields {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  /* 手机模式 */
  .app-main {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    padding: 0;
    height: auto;
  }
  
  .sidebar ul {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem 0;
  }
  
  .sidebar li {
    white-space: nowrap;
    padding: 0.8rem 1rem;
    border-radius: 20px;
    margin: 0 0.2rem;
  }
  
  .sidebar li:hover {
    transform: none;
  }
  
  .sidebar li.active {
    transform: none;
  }
  
  .content {
    padding: 1rem;
  }
  
  .tab-content {
    padding: 1rem;
  }
  
  .chat-container {
    height: 400px;
  }
  
  .voice-container {
    flex-direction: column;
  }
  
  .tts-section,
  .asr-section {
    min-width: 100%;
  }
  
  .obs-connection,
  .vts-connection {
    flex-direction: column;
  }
  
  .config-buttons {
    flex-direction: column;
  }
  
  .config-fields {
    grid-template-columns: 1fr;
  }
  
  .theme-toggle {
    font-size: 1.2rem;
    padding: 0.3rem;
  }
}

@media (max-width: 480px) {
  /* 小屏幕手机模式 */
  .app-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .status-bar {
    width: 100%;
    justify-content: space-between;
  }
  
  .chat-input {
    flex-direction: column;
  }
  
  .chat-input button {
    width: 100%;
  }
  
  .asr-buttons {
    flex-direction: column;
  }
  
  .asr-buttons button {
    width: 100%;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-main {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    padding: 0;
  }

  .sidebar ul {
    display: flex;
    overflow-x: auto;
  }

  .sidebar li {
    white-space: nowrap;
  }

  .voice-container {
    grid-template-columns: 1fr;
  }

  .config-fields {
    grid-template-columns: 1fr;
  }
}
</style>