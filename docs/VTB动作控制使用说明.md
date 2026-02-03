# VTB角色动作控制方案

## 🎯 方案概述

这是最简单、最稳妥的VTB角色动作控制方案，直接通过VTube Studio API实现。

## 📋 前置条件

1. **安装VTube Studio**
   - 从Steam下载并安装VTube Studio
   - 确保API功能已启用（端口8001）

2. **安装Python依赖**
   ```bash
   pip install pyvts
   ```

## 🚀 快速开始

### 方法一：双击运行（推荐）
```
双击 start_vtb_control.bat 文件
```

### 方法二：命令行运行
```bash
cd D:\Project_LLM_VTB\src\backend
python vtb_interaction.py
```

## 🎮 使用方法

### 基础命令
- `greeting` - 打招呼（挥手+微笑+点头）
- `celebrate` - 庆祝（鼓掌+跳跃+比心）
- `surprise` - 惊讶（惊讶表情+摇头）
- `shy` - 害羞（害羞表情+点头）
- `angry` - 生气（生气表情+摇头）
- `quit` - 退出程序

### 使用示例
```
> greeting
✅ 执行打招呼互动
> celebrate  
✅ 执行庆祝互动
> quit
```

## 🔧 技术说明

### 核心组件
- **vtb_motion_control.py**: 基础控制类
- **vtb_interaction.py**: 互动场景控制器
- **start_vtb_control.bat**: 一键启动脚本

### 工作原理
1. 通过WebSocket连接VTube Studio API
2. 获取当前模型的可用热键列表
3. 根据用户输入触发热键执行对应动作
4. 支持表情、手势、身体动作等多种控制

### 坐标系统
- 屏幕中心为原点(0,0)
- X/Y范围：-1 到 1
- 旋转角度：-180 到 180度

## ⚠️ 注意事项

1. 确保VTube Studio正在运行且API已启用
2. 首次使用需要在VTube Studio中授权插件连接
3. 不同模型的热键名称可能不同
4. 建议在测试环境中先试用

## 🛠️ 扩展功能

如需添加自定义动作：
1. 在VTube Studio中设置新的热键
2. 修改代码中的动作映射表
3. 重启控制器即可使用

## 📞 故障排除

**连接失败**：
- 检查VTube Studio是否运行
- 确认API端口8001未被占用
- 防火墙可能需要放行

**动作无响应**：
- 检查模型是否支持该热键
- 查看VTube Studio日志
- 重新获取热键列表

这个方案简单可靠，无需复杂配置，可直接投入使用！