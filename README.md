# HIVE's VTuber

> 面向各类人群的虚拟主播项目，让开播更有隐私，更加轻松。

本仓库用**分支**区分不同技术路线的实现。各分支彼此独立，目前**没有做代码融合**；本页是分支总览、功能详解与导航。

---

## 一、分支总览

| 分支 | 定位 | 技术栈 | 状态 |
|---|---|---|---|
| [`main`](https://github.com/JohnWick6999/HIVEs-VTuber/tree/main) | 分支导航与项目总览（本页） | Markdown | ✅ 维护中 |
| [`master`](https://github.com/JohnWick6999/HIVEs-VTuber/tree/master) | AI Vtuber Tool：Python 后端 + .NET WPF 桌面端 | Python 3 / C# WPF (.NET 8) | 🧪 早期版本 |
| [`Web_App`](https://github.com/JohnWick6999/HIVEs-VTuber/tree/Web_App) | VSP 控制端（Java + Vue）＋ 数字人 Web 项目 `hives-vtuber/` | Java 17 / Vue 3 / FastAPI | 🚧 进行中 |

克隆与切换：

```bash
git clone https://github.com/JohnWick6999/HIVEs-VTuber.git
cd HIVEs-VTuber

git checkout master      # AI Vtuber Tool（Python + WPF）
git checkout Web_App     # VSP 控制端 + 数字人项目
```

---

## 二、`master` 分支 —— AI Vtuber Tool

### 定位

基于 Shizuku_Nya_Bot 项目的 API 调用方式，结合 AI-Vtuber、Open-LLM-VTuber 的思路，做的一个**初级 AI 主播工具**：
一个桌面端控制台，负责把「大模型对话 + 语音合成 + 直播软件控制」串起来。

### 技术架构

| 层 | 技术 |
|---|---|
| 后端 | Python（`src/backend/`），提供本地 Web 服务供前端调用 |
| 前端 | C# / .NET 8 WPF 桌面应用（`NeuroFrontend/`、`NewFrontend/`） |
| 数据 | SQLite（可选，`database.py`） |
| 外部服务 | 大模型 ChatAPI、TTS / ASR 语音 API、图片识别 API、搜索 API、OBS、VTube Studio |

### 功能模块

**后端（Python）**

1. 配置管理：支持导入各种 API 配置（`data/config.json`）
2. ChatAPI 集成：支持多种大语言模型的对话接口
3. 语音 API 集成：TTS 文本转语音、ASR 语音转文本
4. 图片识别 API 集成
5. 搜索 API 集成
6. SQLite 数据库（可选）
7. OBS 接入：场景 / 录制 / 推流控制
8. VTube Studio 接入：热键、表情、动作控制
9. 本地 Web 服务：供前端界面调用

**前端（.NET WPF）**

1. 配置管理界面
2. 实时交互界面
3. OBS 与 VTube Studio 控制界面
4. 系统监控界面
5. 虚拟麦克风输出（配合 VB-Cable，见 `VIRTUAL_MIC_GUIDE.md`）

### 目录结构

```
master/
├── src/backend/              # Python 后端（main.py、ai_chat_system.py、obs_vts.py 等）
├── NeuroFrontend/            # WPF 前端（新版）
├── NewFrontend/              # WPF 前端（另一版界面）
├── ResourceTest/             # 资源测试用 .NET 工程
├── data/                     # config.json 与语音素材
├── docs/                     # VTB 动作控制、VTube Studio 设置指南
├── start_backend.bat         # 一键启动后端（进入 src/backend 并安装依赖）
├── start_frontend.bat        # 一键构建/启动前端
├── start_virtual_mic.bat     # 虚拟麦克风输出
├── VTB控制中心.bat            # 控制中心入口
├── 一键启动VTB控制.bat         # VTB 动作控制器
├── 一键启动现成VTB方案.bat
├── install_vbcable.bat       # VB-Cable 虚拟声卡安装
├── SYSTEM_TEST_REPORT.md     # 系统测试报告
├── TTS_FIX_REPORT.md         # TTS 问题修复记录
├── VTS_INTEGRATION_CLARIFICATION.md
└── VIRTUAL_MIC_GUIDE.md
```

### 启动方式

```bat
:: 1) 启动 Python 后端（会自动 pip install 依赖）
start_backend.bat

:: 2) 启动 WPF 前端
start_frontend.bat
```

> 注意：部分 `.bat` 脚本里写死了作者的本地路径（如 `D:\Project_LLM_VTB`），在你的机器上运行时需要改成自己的路径。

### 适用场景

想要一个**开箱即用的 Windows 桌面控制台**，把 AI 对话、语音、OBS 和 VTube Studio 串起来做直播，且不介意它是早期版本、需要自己调配置。

---

## 三、`Web_App` 分支 —— VSP 控制端 ＋ 数字人项目

该分支现在包含**两个相互独立的子项目**，放在不同目录、各自运行、暂未融合。

```
Web_App/
├── backend/         # VSP 控制端后端（Java / Spring Boot）
├── frontend/        # VSP 控制端前端（Vue 3 + TypeScript）
├── deploy/          # 前端构建产物
├── OBS-CMD/         # OBS 命令行工具与说明
└── hives-vtuber/    # 数字人（VTuber）Web 项目（FastAPI + 浏览器 wasm 渲染）
```

### 1）VSP 控制端（`backend/` + `frontend/`）

一个带图形界面的 **直播控制台**：在浏览器里完成 AI 对话、语音合成、OBS 控制和 VTube Studio 控制。

| 层 | 技术 |
|---|---|
| 后端 | Java 17、Spring Boot 3.2、Spring Security、JPA + H2、Maven |
| 前端 | Vue 3 + TypeScript + Vite 7 |
| 外部服务 | DeepSeek（对话）、阿里云 DashScope（TTS / ASR）、OBS WebSocket |

**核心功能**

1. **AI 聊天系统**：多轮对话、可配置人设与语气风格
2. **语音功能**：TTS 文本转语音、ASR 语音转文本，支持多种音色
3. **OBS 控制**：连接 / 断开、开始停止录制、开始停止推流、切换场景
4. **VTube Studio 控制**：连接、触发热键、设置表情
5. **配置管理**：可视化配置界面，支持保存与加载、实时生效
6. **界面体验**：响应式布局（手机 / 平板 / 电脑）、明暗模式一键切换

**目录结构**

```
backend/                  # Spring Boot 工程（com.llm.vtb.{ai,config,controller,obs,voice}）
frontend/                 # Vue 3 + Vite 工程
deploy/                   # 构建产物（index.html + assets）
OBS-CMD/                  # obs-cmd.exe 与使用说明
```

**启动方式**

```bash
# 后端（默认 8080）
cd backend && mvn spring-boot:run

# 前端（默认 5173，开发模式）
cd frontend && npm install && npm run dev
```

### 2）数字人项目（`hives-vtuber/`）

一个**浏览器内实时渲染的 AI 数字人**：会说话、有表情、有记忆，同一套核心代码可跑在 Web / Electron / Android / 微信小程序上。

**核心功能**

| 能力 | 说明 |
|---|---|
| 🎭 数字人实时渲染 | 浏览器端 Canvas + WebAssembly 引擎，视频素材 + 驱动数据逐帧合成，无需服务端 GPU |
| 🗣️ 全链路语音对话 | 录音 → 实时 ASR → 大模型流式回复 → TTS 流式合成 → 口型 / 表情驱动 |
| 🧠 长期记忆 | 768 维向量记忆库，长短期记忆融合，支持持久化与跨设备同步 |
| 😊 情感与表情 | 情绪标签驱动表情、语调与肢体动作 |
| 👤 多角色管理 | 形象创建、绑定音色、人设设定、背景切换、删除 |
| 🎙️ 音色克隆 | CosyVoice 音色克隆与腾讯云大模型音色 |
| 📱 多端共用 | Web / Electron / Android / 微信小程序共享同一套核心代码 |

**技术实现**

- 一个形象 = `assets/<avatar_id>/` 下的循环视频 `01.webm` + 驱动数据 `combined_data.json.gz` + 缩略图 + 记忆文件 `memory.bin`
- `web/js/DHLiveMini2.js` 加载内置的 `web/wasm/DHLiveMini2.wasm`（约 5 MB）完成渲染，`web/js/MiniLive.js` 负责取帧与绘制调度
- 对话接口 `POST /chat/chat_stream`（SSE 流式），文本按句切分后立即送 TTS，边合成边播放

**启动方式**

```bash
cd hives-vtuber
./start.sh          # 首次运行自动创建虚拟环境并安装依赖
# 或
pip install -r requirements.txt && python main.py
```

打开 http://localhost:8000/ 即可。

**配置**

| 环境变量 | 必填 | 说明 |
|---|---|---|
| `DASHSCOPE_API_KEY` | 对话必填 | 阿里云百炼 API Key |
| `HIVES_VTUBER_KEY` | 创建形象必填 | 形象平台密钥 |
| `HIVES_VTUBER_PLATFORM_BASE` / `HIVES_VTUBER_ASSET_BASE` / `HIVES_VTUBER_WEB_BASE` | 可选 | 外部服务地址 |

详见 [`hives-vtuber/README_zh.md`](https://github.com/JohnWick6999/HIVEs-VTuber/blob/Web_App/hives-vtuber/README_zh.md)。

---

## 四、怎么选

| 你的需求 | 建议分支 |
|---|---|
| 想要 Windows 桌面控制台，Python + .NET 技术栈 | `master` |
| 想要浏览器里的可视化控制台，Java + Vue 技术栈 | `Web_App`（VSP 控制端） |
| 想要「会说话、有表情、有记忆」的数字人形象本身 | `Web_App` 下的 `hives-vtuber/` |
| 想整体了解项目规划 | 留在 `main`（本页） |

---

## 五、密钥与安全

**本仓库不包含任何 API Key。** 所有分支的配置文件中密钥字段均为空或占位，请自行申请并填入：

- VSP 控制端：`backend/data/config.json` 的 `api_key` 字段，或启动前设置环境变量
- 数字人项目：`DASHSCOPE_API_KEY`、`HIVES_VTUBER_KEY` 等环境变量
- AI Vtuber Tool：`data/config.json` 的 `api_key` 字段

> ⚠️ 请勿把真实密钥提交到 Git。历史提交中若曾出现过密钥，请到对应平台吊销并重新生成。

---

## 六、许可证

- `master`：见分支内说明
- `Web_App`（VSP 控制端）：MIT，见分支 README
- `Web_App/hives-vtuber`（数字人项目）：Apache License 2.0，基于 [MatesX](https://github.com/kleinlee/MatesX) 重构，原始版权归其作者所有

---

**免责声明**：本项目仅供学习和研究使用，请勿用于商业用途；使用时请遵守相关服务提供商的使用条款与法律法规。
