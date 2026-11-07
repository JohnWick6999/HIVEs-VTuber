 # 🌟 HIVE's VTuber — 多端编译（windows、mac、android、小程序）


 ---

 ## 1️⃣ Electron 桌面端编译（支持 Windows 与 macOS）

```bash
cd platform/electron
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
npm config set registry https://registry.npmmirror.com/
npm install electron --save-dev
npm run make
```
 ✅ 编译完成后，生成的安装包位于：

 platform/electron/out/hives-vtuber-win32-x64/ （Windows）

或对应平台架构文件夹（如 macOS 为 hives-vtuber-darwin-arm64/）

> 桌面端加载的站点地址在 `platform/electron/services.js` 中配置（默认指向上游站点，可改为 http://localhost:8000）。

 ---

 ## 2️⃣ Android 移动端编译

 1. 使用 Android Studio 打开 platform/android/ 目录。
 2. 点击菜单栏 Build > Build Bundle(s) / APK(s) > Build APK(s)。

 ✅ 编译完成后，生成的 APK 文件位于：
 platform/android/app/build/outputs/apk/

> 应用包名为 `com.hives.vtuber`，加载的站点地址在 `app/src/main/java/com/hives/vtuber/Services.kt` 中配置。

 ---

 ## 3️⃣ mini-program端编译

代码很简单，请按需编译

> 小程序内嵌的站点地址在 `platform/mini-program/utils/services.js` 中配置。
