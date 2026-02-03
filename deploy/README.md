# HIVE's VTuber 部署说明

## 版本信息
- **版本**: pre-version 0.0.1

## 项目结构

```
deploy/
├── assets/           # 静态资源文件
│   ├── index-C3xwfwBX.css
│   └── index-C_I8sdDQ.js
├── index.html        # 主HTML文件
├── vite.svg          # 图标文件
└── README.md         # 部署说明
```

## 部署步骤

### 1. 后端服务部署

1. 确保已安装 Java 17 或更高版本
2. 确保已安装 Maven 3.9.0 或更高版本
3. 进入后端目录：
   ```bash
   cd d:\Trae_Project\Project_LLM_VTB-VSP\backend
   ```
4. 构建后端项目：
   ```bash
   mvn clean package
   ```
5. 运行后端服务：
   ```bash
   mvn spring-boot:run
   ```

### 2. 前端部署

1. 确保后端服务已启动并运行在 `http://localhost:8080`
2. 方法一：使用本地HTTP服务器
   - 安装 serve 工具：
     ```bash
     npm install -g serve
     ```
   - 进入部署目录：
     ```bash
     cd d:\Trae_Project\Project_LLM_VTB-VSP\deploy
     ```
   - 启动HTTP服务器：
     ```bash
     serve -s
     ```
   - 打开浏览器访问 `http://localhost:3000`

3. 方法二：使用Nginx或Apache
   - 配置Web服务器指向 `deploy` 目录
   - 启动Web服务器
   - 打开浏览器访问对应的URL

## 依赖需求

### 后端依赖

- Java 17+
- Maven 3.9.0+
- Spring Boot 3.2.0+

### 前端依赖

- 现代Web浏览器（Chrome、Firefox、Edge等）
- 可选：serve工具（用于本地部署）

## 配置说明

### 后端配置

- 配置文件路径：`backend/data/config.json`
- 可配置项：
  - OBS连接信息（主机、端口、密码）
  - VTuberStudio连接信息
  - AI API密钥和配置
  - 语音API配置

### 前端配置

- 前端API基础URL：已配置为 `http://localhost:8080`
- 如需修改，请编辑 `src/App.vue` 文件中的 `API_BASE_URL` 变量

## 常见问题

### 1. 前端无法连接到后端

- 检查后端服务是否正在运行
- 检查防火墙是否阻止了端口8080的访问
- 检查前端API_BASE_URL配置是否正确

### 2. OBS连接失败

- 检查OBS是否已安装并运行
- 检查OBS WebSocket插件是否已安装并启用
- 检查OBS连接配置（主机、端口、密码）是否正确

### 3. 语音功能无法使用

- 检查语音API配置是否正确
- 检查API密钥是否有效

## 运行状态

- 后端服务运行在：`http://localhost:8080`
- 前端应用运行在：根据部署方式不同，默认为 `http://localhost:3000` 或配置的Web服务器地址

## 技术栈

- 后端：Spring Boot 3.2.0, Java
- 前端：Vue 3, TypeScript, Vite
- 构建工具：Maven, npm

## 联系信息

如有任何问题，请联系项目维护者。
