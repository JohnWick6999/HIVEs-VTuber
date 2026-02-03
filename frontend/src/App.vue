<template>
  <div class="app-container">
    <header class="app-header">
      <h1>HIVE's VTuber</h1>
      <div class="status-bar">
        <span :class="{ 'status-healthy': backendStatus === 'healthy' }">
          后端服务: {{ backendStatus === "healthy" ? "运行中" : "未运行" }}
        </span>
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
            <span>pre-version 0.0.1</span>
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
              <button @click="connectOBS">连接OBS</button>
              <button @click="disconnectOBS">断开OBS</button>
              <div class="obs-status">{{ obsStatus }}</div>
            </div>
            <div class="obs-controls">
              <h3>录制控制</h3>
              <button @click="startRecording">开始录制</button>
              <button @click="stopRecording">停止录制</button>
            </div>
            <div class="obs-controls">
              <h3>推流控制</h3>
              <button @click="startStreaming">开始推流</button>
              <button @click="stopStreaming">停止推流</button>
            </div>
            <div class="obs-controls">
              <h3>场景设置</h3>
              <input v-model="obsScene" type="text" placeholder="场景名称" />
              <button @click="setOBSScene">设置场景</button>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'vts'" class="tab-content">
          <h2>VTuberStudio控制</h2>
          <div class="vts-container">
            <div class="vts-connection">
              <button @click="connectVTS">连接VTuberStudio</button>
              <div class="vts-status">{{ vtsStatus }}</div>
            </div>
            <div class="vts-controls">
              <h3>热键触发</h3>
              <input v-model="vtsHotkey" type="text" placeholder="热键名称" />
              <button @click="triggerVTSHotkey">触发热键</button>
            </div>
            <div class="vts-controls">
              <h3>表情设置</h3>
              <input
                v-model="vtsExpression"
                type="text"
                placeholder="表情名称"
              />
              <button @click="setVTSExpression">设置表情</button>
            </div>
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

              <!-- 其他配置部分省略，实际项目中需要完整实现 -->
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
const obsScene = ref("");
const vtsStatus = ref("");
const vtsHotkey = ref("");
const vtsExpression = ref("");
const configStatus = ref("");

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
    },
    asr: {
      api_key: "",
      base_url: "",
    },
  },
  // 其他配置项
});

// API基础URL
const API_BASE_URL = "http://localhost:8080";

// 健康检查
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
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
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
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
    const response = await fetch(`${API_BASE_URL}/api/tts`, {
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
    const response = await fetch(`${API_BASE_URL}/api/asr`, {
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
async function connectOBS() {
  console.log("开始连接OBS...");
  try {
    console.log(`调用API端点: ${API_BASE_URL}/api/obs/connect`);
    const response = await fetch(`${API_BASE_URL}/api/obs/connect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    console.log(`API响应状态: ${response.status}`);
    const data = await response.json();
    console.log(`API响应数据: ${JSON.stringify(data)}`);
    obsStatus.value = "连接OBS成功";
  } catch (error) {
    console.error("连接OBS错误:", error);
    obsStatus.value = "连接OBS失败";
  }
}

async function disconnectOBS() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/disconnect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    obsStatus.value = "断开OBS连接成功";
  } catch (error) {
    obsStatus.value = "断开OBS连接失败";
  }
}

async function startRecording() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/recording/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    obsStatus.value = "开始OBS录制成功";
  } catch (error) {
    obsStatus.value = "开始OBS录制失败";
  }
}

async function stopRecording() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/recording/stop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    obsStatus.value = "停止OBS录制成功";
  } catch (error) {
    obsStatus.value = "停止OBS录制失败";
  }
}

async function startStreaming() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/streaming/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    obsStatus.value = "开始OBS推流成功";
  } catch (error) {
    obsStatus.value = "开始OBS推流失败";
  }
}

async function stopStreaming() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/streaming/stop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    obsStatus.value = "停止OBS推流成功";
  } catch (error) {
    obsStatus.value = "停止OBS推流失败";
  }
}

async function setOBSScene() {
  if (!obsScene.value.trim()) {
    obsStatus.value = "场景名称不能为空";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/obs/scene`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scene_name: obsScene.value }),
    });
    obsStatus.value = "设置OBS场景成功";
  } catch (error) {
    obsStatus.value = "设置OBS场景失败";
  }
}

// VTuberStudio功能
async function connectVTS() {
  console.log("开始连接VTuberStudio...");
  try {
    console.log(`调用API端点: ${API_BASE_URL}/api/vts/connect`);
    const response = await fetch(`${API_BASE_URL}/api/vts/connect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    console.log(`API响应状态: ${response.status}`);
    const data = await response.json();
    console.log(`API响应数据: ${JSON.stringify(data)}`);
    vtsStatus.value = "连接VTuberStudio成功";
  } catch (error) {
    console.error("连接VTuberStudio错误:", error);
    vtsStatus.value = "连接VTuberStudio失败";
  }
}

async function triggerVTSHotkey() {
  if (!vtsHotkey.value.trim()) {
    vtsStatus.value = "热键名称不能为空";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/vts/hotkey`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hotkey_name: vtsHotkey.value }),
    });
    vtsStatus.value = "触发VTuberStudio热键成功";
  } catch (error) {
    vtsStatus.value = "触发VTuberStudio热键失败";
  }
}

async function setVTSExpression() {
  if (!vtsExpression.value.trim()) {
    vtsStatus.value = "表情名称不能为空";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/vts/expression`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression_name: vtsExpression.value }),
    });
    vtsStatus.value = "设置VTuberStudio表情成功";
  } catch (error) {
    vtsStatus.value = "设置VTuberStudio表情失败";
  }
}

// 配置功能
async function loadConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/config`);
    const data = await response.json();
    config.value = data;
    configStatus.value = "配置加载成功";
  } catch (error) {
    configStatus.value = "配置加载失败";
  }
}

async function saveConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config.value),
    });
    configStatus.value = "配置保存成功";
  } catch (error) {
    configStatus.value = "配置保存失败";
  }
}

async function resetConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/config`, {
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
  height: 100vh;
  font-family: Arial, sans-serif;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.status-bar {
  display: flex;
  gap: 1rem;
}

.status-healthy {
  color: #27ae60;
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background-color: #34495e;
  color: white;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  height: 100%;
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
  transition: background-color 0.2s;
}

.sidebar li:hover {
  background-color: #2c3e50;
}

.sidebar li.active {
  background-color: #3498db;
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
}

.tab-content {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
}

.user-message,
.ai-message {
  margin-bottom: 1rem;
  padding: 0.8rem;
  border-radius: 8px;
  max-width: 80%;
}

.user-message {
  align-self: flex-end;
  background-color: #e3f2fd;
  margin-left: auto;
}

.ai-message {
  align-self: flex-start;
  background-color: #f1f1f1;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #333;
}

.message-content {
  color: #222;
  line-height: 1.4;
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
}

.chat-input button {
  padding: 0.8rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #2980b9;
}

/* 语音样式 */
.voice-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.tts-section,
.asr-section {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.tts-section h3,
.asr-section h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
}

.tts-section textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 1rem;
}

.asr-result {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  min-height: 100px;
  margin-bottom: 1rem;
  background-color: white;
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
}

.obs-controls,
.vts-controls {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.obs-controls h3,
.vts-controls h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
}

.obs-controls input,
.vts-controls input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
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
}

.config-section h3 {
  margin-top: 0;
  color: #34495e;
  margin-bottom: 1rem;
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
}

.field-group input {
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 通用按钮样式 */
button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

button:hover {
  opacity: 0.9;
}

button:active {
  transform: translateY(1px);
}

/* 版本信息样式 */
.version-info {
  margin-top: auto;
  padding-top: 2rem;
  opacity: 0.7;
  font-size: 0.8rem;
}

/* 状态样式 */
.chat-status,
.voice-status,
.obs-status,
.vts-status,
.config-status {
  margin-top: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
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