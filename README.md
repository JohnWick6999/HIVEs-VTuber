# AI Vtuber Tool

基于 Shizuku_Nya_Bot 项目的API调用方法，结合 AI-Vtuber 和 Open-LLM-VTuber 项目的功能，制作的初级AI主播工具。

## 技术架构

- **后端**：Python
- **前端**：dotnet
- **数据库**：SQLite（可选项）

## 功能模块

### 后端模块（Python）
1. **配置管理**：支持导入各种API配置
2. **ChatAPI集成**：支持多种大语言模型
3. **语音API集成**：支持TTS和ASR
4. **图片识别API集成**
5. **搜索API集成**
6. **SQLite数据库**：作为可选项
7. **OBS接入**
8. **VTuberStudio接入**
9. **Web服务**：供前端调用

### 前端模块（dotnet）
1. **配置管理界面**
2. **实时交互界面**
3. **OBS和VTuberStudio控制界面**
4. **系统监控界面**

## 快速开始

### 后端启动
```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python main.py
```

### 前端启动
```bash
# 构建并运行前端
cd AIVtuberTool
dotnet build
dotnet run
```

## 配置说明

配置文件位于 `config.json`，支持以下配置：
- ChatAPI配置（API Key、Base URL等）
- 语音API配置（TTS和ASR）
- 图片识别API配置
- 搜索API配置
- SQLite数据库配置（可选）
- OBS和VTuberStudio配置

## 功能特性

- 支持多种大语言模型
- 支持实时语音交互
- 支持图片识别
- 支持网络搜索
- 支持OBS和VTuberStudio接入
- 可配置的人格设定
- 可选的SQLite数据库存储
