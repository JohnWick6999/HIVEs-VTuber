# HIVE's VTuber (VSP) 项目说明

## 项目概述

HIVE's VTuber (VSP) 是一个集成了AI聊天、语音合成、OBS控制和VTuberStudio控制的综合性工具，旨在为VTuber提供智能化的辅助功能，提升直播体验。

### 版本信息

- **版本**: pre-version 0.0.2

### 仓库结构

本仓库以「互不融合」的方式并存两个独立项目：

| 目录 | 项目 | 说明 |
|---|---|---|
| `backend/` `frontend/` `deploy/` | VSP 控制端（Java + Vue） | AI 聊天、语音、OBS / VTube Studio 控制 |
| [`hives-vtuber/`](hives-vtuber/) | 数字人（Web）项目 | 浏览器内渲染的 VTuber 数字人：会说话、有表情、有记忆，支持 Web / Electron / Android / 小程序 |

两个项目目前相互独立，尚未做代码融合，各自的运行方式见下文。

## 新版本更新 (pre-version 0.0.2)

### 前端功能增强

1. **搜索API配置管理**
   - 修复搜索API配置在前端的显示问题
   - 确保配置能正确加载和保存
   - 完善前端配置界面与后端API的集成

2. **文本转语音功能**
   - 实现完整的文本转语音功能
   - 用户可输入文本并生成语音
   - 集成阿里云DashScope TTS API
   - 提供语音状态反馈和错误处理机制

3. **响应式布局**
   - 完美适配手机、平板、电脑三种设备模式
   - 使用媒体查询实现自适应布局
   - 侧边栏在手机模式下自动调整为水平滚动导航
   - 内容区域根据屏幕尺寸智能调整布局
   - 输入框和按钮在移动端自动优化为全宽显示

4. **明暗模式切换**
   - 支持一键切换明暗模式
   - 平滑的过渡动画效果(0.3秒)
   - 所有页面元素全面适配深色模式
   - 主题切换按钮实时反馈当前状态
   - 包括聊天、语音、OBS、VTuberStudio等所有页面

5. **深色模式UI修复**
   - 修复导航栏高亮颜色错位问题
   - 修复主题切换按钮在深色模式下不可见的问题
   - 修复页面底部出现的意义不明方框
   - 优化深色模式下的视觉体验
   - 确保状态信息容器在空状态下完全透明

## 功能特性

### 核心功能

1. **AI聊天系统**
   - 基于大型语言模型的智能对话
   - 可配置的性格设定和语气风格
   - 支持多轮对话

2. **语音功能**
   - 文本转语音 (TTS)
   - 语音转文本 (ASR)
   - 支持多种语音模型

3. **OBS控制**
   - 连接和断开OBS
   - 开始/停止录制
   - 开始/停止推流
   - 切换场景

4. **VTuberStudio控制**
   - 连接VTuberStudio
   - 触发热键
   - 设置表情

5. **配置管理**
   - 可视化配置界面
   - 支持保存和加载配置
   - 实时配置更新

## 技术栈

### 后端

- **语言**: Java 17
- **框架**: Spring Boot 3.2.0
- **安全**: Spring Security
- **数据**: JPA + H2数据库
- **构建工具**: Maven 3.9.0+

### 前端框架更新

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite 7.x
- **版本**: pre-version 0.0.2
- **特性**:
  - 响应式设计适配多端设备
  - 明暗模式切换
  - 状态管理优化
  - API集成完善

### 第三方服务

- **AI API**: DeepSeek
- **语音API**: 阿里云DashScope
- **WebSocket**: OBS WebSocket

## 项目结构

```
Project_LLM_VTB-VSP/
├── backend/              # 后端Java项目
│   ├── src/              # 源代码
│   │   └── main/java/com/llm/vtb/  # 核心包结构
│   │       ├── ai/       # AI聊天系统
│   │       ├── config/   # 配置管理
│   │       ├── controller/ # API控制器
│   │       ├── obs/      # OBS/VTS控制
│   │       └── voice/     # 语音API系统
│   ├── data/             # 配置文件
│   └── pom.xml           # Maven配置
├── frontend/             # 前端Vue项目
│   ├── src/              # 源代码
│   │   ├── App.vue       # 主应用组件
│   │   ├── main.ts       # 入口文件
│   │   └── style.css     # 全局样式
│   ├── public/           # 静态资源
│   └── package.json      # 依赖配置
├── deploy/               # 构建产物
│   ├── assets/           # 静态资源
│   ├── index.html        # 主HTML文件
│   └── README.md         # 部署说明
├── hives-vtuber/         # 新增：数字人（VTuber）Web 项目，独立运行
└── README.md             # 项目说明
```

## 数字人项目（hives-vtuber/）

`hives-vtuber/` 是本仓库新增的**数字人（VTuber）Web 项目**，与原 VSP 控制端相互独立、暂未融合。

### 功能简介

| 能力 | 说明 |
|---|---|
| 🎭 数字人实时渲染 | 浏览器端 Canvas + WebAssembly 引擎，视频素材 + 驱动数据逐帧合成，无需服务端 GPU |
| 🗣️ 全链路语音对话 | 录音 → 实时 ASR → 大模型流式回复 → TTS 流式合成 → 口型 / 表情驱动 |
| 🧠 长期记忆 | 768 维向量记忆库，长短期记忆融合，支持记忆持久化与跨设备同步 |
| 😊 情感与表情 | 情绪标签驱动表情、语调与肢体动作 |
| 👤 多角色管理 | 形象创建、绑定音色、人设设定、背景切换、删除 |
| 🎙️ 音色克隆 | CosyVoice 音色克隆与腾讯云大模型音色 |
| 📱 多端共用 | Web / Electron / Android / 微信小程序共享同一套核心代码 |

### 数字人实现要点

- 一个形象 = `assets/<avatar_id>/` 下的循环视频 `01.webm` + 驱动数据 `combined_data.json.gz` + 缩略图 + 记忆文件 `memory.bin`
- `web/js/DHLiveMini2.js` 加载内置的 `web/wasm/DHLiveMini2.wasm`（约 5MB）完成渲染，`web/js/MiniLive.js` 负责视频取帧与绘制调度
- 对话接口 `POST /chat/chat_stream`（SSE 流式），返回文本按句切分后立即送往 TTS，边合成边播放

### 快速开始

```bash
cd hives-vtuber
./start.sh          # 首次运行自动创建虚拟环境并安装依赖
# 或
pip install -r requirements.txt && python main.py
```

打开 http://localhost:8000/ 即可（自动跳转到形象展示页）。

### 配置（环境变量）

| 变量 | 必填 | 说明 |
|---|---|---|
| `DASHSCOPE_API_KEY` | 对话必填 | 阿里云百炼 API Key |
| `HIVES_VTUBER_KEY` | 创建形象必填 | 形象平台密钥 |
| `HIVES_VTUBER_PLATFORM_BASE` / `HIVES_VTUBER_ASSET_BASE` / `HIVES_VTUBER_WEB_BASE` | 可选 | 外部服务地址 |

> 仓库中不包含任何 API Key，请自行填写；外部服务地址集中在 `hives-vtuber/utils/services.py` 及各端 `services` 配置文件中。

完整说明见 [`hives-vtuber/README_zh.md`](hives-vtuber/README_zh.md)。

## 安装部署

### 前置依赖

- **后端依赖**:
  - Java 17 或更高版本
  - Maven 3.9.0 或更高版本

- **前端依赖**:
  - Node.js 18 或更高版本
  - npm 9 或更高版本

### 后端部署

1. **克隆项目**:

   ```bash
   git clone <repository-url>
   cd Project_LLM_VTB-VSP
   ```

2. **进入后端目录**:

   ```bash
   cd backend
   ```

3. **构建项目**:

   ```bash
   mvn clean package
   ```

4. **运行服务**:

   ```bash
   mvn spring-boot:run
   ```

   后端服务将运行在 `http://localhost:8080`

### 前端部署

#### 方法一：开发模式

1. **进入前端目录**:

   ```bash
   cd frontend
   ```

2. **安装依赖**:

   ```bash
   npm install
   ```

3. **启动开发服务器**:

   ```bash
   npm run dev
   ```

   前端应用将运行在 `http://localhost:5173`

#### 方法二：生产部署

1. **进入前端目录**:

   ```bash
   cd frontend
   ```

2. **安装依赖**:

   ```bash
   npm install
   ```

3. **构建项目**:

   ```bash
   npm run build
   ```

4. **部署静态文件**:
   - 构建产物位于 `frontend/dist` 目录
   - 可将其部署到任何静态文件服务器
   - 推荐使用 `serve` 工具本地部署:
     ```bash
     npm install -g serve
     serve -s dist
     ```

## 配置说明

### 后端配置

后端配置文件位于 `backend/data/config.json`，包含以下配置项：

- **聊天API配置**:
  - API密钥
  - 基础URL
  - 模型选择
  - 温度参数
  - 最大令牌数

- **语音API配置**:
  - TTS配置 (API密钥、基础URL、语音选择)
  - ASR配置 (API密钥、基础URL)

- **OBS配置**:
  - 启用状态
  - 主机地址
  - 端口号
  - 密码

- **VTuberStudio配置**:
  - 启用状态
  - 主机地址
  - 端口号

### 前端配置

前端API基础URL配置位于 `frontend/src/App.vue` 文件中的 `API_BASE_URL` 变量：

```javascript
// API基础URL
const API_BASE_URL = "http://localhost:8080";
```

## 运行方式

### 完整运行流程

1. **启动后端服务**:

   ```bash
   cd backend
   mvn spring-boot:run
   ```

2. **启动前端应用**:

   ```bash
   cd frontend
   npm run dev
   ```

3. **访问应用**:
   - 打开浏览器访问 `http://localhost:5173`

4. **配置连接**:
   - 在"配置"选项卡中设置OBS和VTuberStudio的连接信息
   - 保存配置

5. **连接外部服务**:
   - 在"OBS"选项卡中点击"连接OBS"
   - 在"VTuberStudio"选项卡中点击"连接VTuberStudio"

6. **使用功能**:
   - 使用"聊天"选项卡与AI交流
   - 使用"语音"选项卡进行语音合成和识别
   - 使用"OBS"选项卡控制录制和推流
   - 使用"VTuberStudio"选项卡控制表情和热键

## 常见问题

### 1. 后端服务启动失败

- **原因**:
  - Java版本不兼容
  - Maven依赖下载失败
  - 端口8080被占用

- **解决方法**:
  - 确保使用Java 17或更高版本
  - 运行 `mvn clean install` 重新下载依赖
  - 检查并关闭占用端口8080的进程

### 2. 前端无法连接到后端

- **原因**:
  - 后端服务未启动
  - API_BASE_URL配置错误
  - CORS配置问题

- **解决方法**:
  - 确保后端服务正在运行
  - 检查 `API_BASE_URL` 是否正确设置为后端服务地址
  - 检查浏览器控制台是否有CORS错误

### 3. OBS连接失败

- **原因**:
  - OBS未安装或未运行
  - OBS WebSocket插件未安装
  - 连接配置错误

- **解决方法**:
  - 确保OBS已安装并运行
  - 安装OBS WebSocket插件
  - 检查OBS配置中的主机、端口和密码是否正确

### 4. 语音功能无法使用

- **原因**:
  - 语音API配置错误
  - API密钥无效
  - 网络连接问题

- **解决方法**:
  - 检查语音API配置是否正确
  - 确保API密钥有效
  - 检查网络连接是否正常

## 开发指南

### 后端开发

1. **添加新API端点**:
   - 在 `ApiController.java` 中添加新的请求处理方法
   - 使用 `@RequestMapping` 或具体的HTTP方法注解

2. **添加新功能模块**:
   - 在 `com.llm.vtb` 包下创建新的包和类
   - 实现核心功能逻辑
   - 在控制器中添加相应的API端点

3. **配置管理**:
   - 在 `ConfigManager.java` 中添加新的配置类
   - 更新配置文件结构

### 前端开发

1. **添加新组件**:
   - 在 `src` 目录下创建新的Vue组件
   - 在 `App.vue` 中导入和使用组件

2. **添加新功能**:
   - 在 `App.vue` 中添加新的功能模块
   - 实现相应的API调用和状态管理

3. **样式修改**:
   - 修改 `style.css` 或组件内的 `<style>` 块

## 测试

### 后端测试

1. **运行单元测试**:

   ```bash
   cd backend
   mvn test
   ```

2. **测试API端点**:
   - 使用Postman或curl测试API端点
   - 例如测试健康检查:
     ```bash
     curl http://localhost:8080/api/health
     ```

### 前端测试

1. **运行构建测试**:

   ```bash
   cd frontend
   npm run build
   ```

2. **手动测试**:
   - 访问前端应用
   - 测试各个功能模块
   - 检查浏览器控制台是否有错误

## 项目维护

### 版本管理

- **后端版本**: 1.0.0-SNAPSHOT
- **前端版本**: pre-version 0.0.2

### 更新日志

#### v1.0.0

- 初始版本
- 实现核心功能
- 集成AI聊天、语音、OBS和VTuberStudio控制

#### pre-version 0.0.2

- 更新前端版本至pre-version 0.0.2
- 修复搜索API配置在前端的显示问题
- 实现文本转语音功能
- 实现响应式布局，适配手机、平板、电脑三种模式
- 添加明暗模式切换功能及平滑切换动画
- 修复深色模式下UI问题
  - 导航栏高亮颜色错位
  - 主题切换按钮不可见
  - 页面底部出现意义不明方框

## 联系信息

如有任何问题或建议，请联系项目维护者：

- **项目地址**: `https://github.com/JohnWick6999/HIVEs-VTuber/tree/Web_App`
- **后端服务**: `http://localhost:8080`
- **前端应用**: `http://localhost:5173`

## 许可证

本项目采用 MIT 许可证。

---

**免责声明**: 本项目仅供学习和研究使用，请勿用于商业用途。使用本项目时，请遵守相关服务提供商的使用条款和法律法规。
