package com.llm.vtb.obs;

import com.llm.vtb.config.ConfigManager;
import okhttp3.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.awt.Desktop;
import java.io.File;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

@Component
public class ObsVtsSystem {

    @Autowired
    private ConfigManager configManager;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private WebSocket obsWebSocket;
    private WebSocket vtsWebSocket;
    private boolean isObsConnected = false;
    private boolean isVtsConnected = false;
    private OkHttpClient okHttpClient;
    private String obsCmdPath = "D:\\Trae_Project\\Project_LLM_VTB-VSP\\OBS-CMD\\obs-cmd.exe";

    public ObsVtsSystem() {
        this.okHttpClient = new OkHttpClient.Builder()
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .connectTimeout(10, TimeUnit.SECONDS)
                .build();
    }

    // OBS相关方法
    public boolean connectToObs() {
        try {
            ConfigManager.Config config = configManager.getConfig();
            ConfigManager.ObsConfig obsConfig = config.getObs();

            String host = obsConfig.getHost();
            int port = obsConfig.getPort();
            String password = obsConfig.getPassword();

            // 构建WebSocket连接URL
            String wsUrl = "ws://" + host + ":" + port;

            System.out.println("正在连接OBS WebSocket: " + wsUrl);

            // 创建Request对象
            Request request = new Request.Builder()
                    .url(wsUrl)
                    .build();

            // 创建CountDownLatch用于等待连接结果
            CountDownLatch latch = new CountDownLatch(1);
            boolean[] connectResult = { false };

            // 创建并连接WebSocket客户端
            obsWebSocket = okHttpClient.newWebSocket(request, new WebSocketListener() {
                @Override
                public void onOpen(WebSocket webSocket, Response response) {
                    super.onOpen(webSocket, response);
                    System.out.println("OBS WebSocket连接成功");
                    isObsConnected = true;
                    connectResult[0] = true;

                    latch.countDown();
                }

                @Override
                public void onMessage(WebSocket webSocket, String text) {
                    super.onMessage(webSocket, text);
                    System.out.println("收到OBS消息: " + text);

                    try {
                        // 解析OBS消息
                        Map<String, Object> message = objectMapper.readValue(text, Map.class);

                        // 处理认证挑战
                        if (message.containsKey("d")) {
                            Map<String, Object> data = (Map<String, Object>) message.get("d");
                            if (data.containsKey("authentication")) {
                                Map<String, Object> auth = (Map<String, Object>) data.get("authentication");
                                if (auth.containsKey("challenge") && auth.containsKey("salt")) {
                                    String challenge = (String) auth.get("challenge");
                                    String salt = (String) auth.get("salt");
                                    System.out.println("收到认证挑战，开始处理...");

                                    // 生成认证响应
                                    if (!password.isEmpty()) {
                                        String authResponse = generateAuthResponse(password, salt, challenge);
                                        sendObsAuthResponse(authResponse);
                                    }
                                }
                            }
                        }

                        // 处理认证结果
                        if (message.containsKey("op")) {
                            int op = (int) message.get("op");
                            if (op == 2) { // 认证响应
                                if (message.containsKey("d")) {
                                    Map<String, Object> data = (Map<String, Object>) message.get("d");
                                    if (data.containsKey("authentication")) {
                                        Map<String, Object> auth = (Map<String, Object>) data.get("authentication");
                                        if (auth.containsKey("status")) {
                                            String status = (String) auth.get("status");
                                            if ("ok".equals(status)) {
                                                System.out.println("OBS认证成功");
                                                isObsConnected = true;
                                            } else {
                                                System.out.println("OBS认证失败: " + status);
                                                isObsConnected = false;
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // 处理其他消息
                        if (message.containsKey("op") && message.containsKey("d")) {
                            System.out.println("收到OBS消息 (op: " + message.get("op") + "): " + message.get("d"));
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onClosed(WebSocket webSocket, int code, String reason) {
                    super.onClosed(webSocket, code, reason);
                    isObsConnected = false;
                    System.out.println("OBS WebSocket连接关闭: " + reason);
                }

                @Override
                public void onFailure(WebSocket webSocket, Throwable t, Response response) {
                    super.onFailure(webSocket, t, response);
                    isObsConnected = false;
                    System.out.println("OBS WebSocket错误: " + t.getMessage());
                    latch.countDown();
                }
            });

            // 等待连接结果，最多等待5秒
            latch.await(5, TimeUnit.SECONDS);
            return connectResult[0];
        } catch (Exception e) {
            e.printStackTrace();
            isObsConnected = false;
            return false;
        }
    }

    public void disconnectFromObs() {
        if (obsWebSocket != null && isObsConnected) {
            try {
                obsWebSocket.close(1000, "Normal closure");
                isObsConnected = false;
                System.out.println("OBS WebSocket连接已关闭");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    // 使用obs-cmd的方法
    public boolean testObsCmd() {
        try {
            Process process = executeObsCmdCommand("info");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean startObsRecording() {
        try {
            Process process = executeObsCmdCommand("recording start");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean stopObsRecording() {
        try {
            Process process = executeObsCmdCommand("recording stop");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean toggleObsRecording() {
        try {
            Process process = executeObsCmdCommand("recording toggle");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean startObsStreaming() {
        try {
            Process process = executeObsCmdCommand("streaming start");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean stopObsStreaming() {
        try {
            Process process = executeObsCmdCommand("streaming stop");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean toggleObsStreaming() {
        try {
            Process process = executeObsCmdCommand("streaming toggle");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean setObsScene(String sceneName) {
        try {
            Process process = executeObsCmdCommand("scene switch \"" + sceneName + "\"");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean startVirtualCamera() {
        try {
            Process process = executeObsCmdCommand("virtual-camera start");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean stopVirtualCamera() {
        try {
            Process process = executeObsCmdCommand("virtual-camera stop");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean toggleVirtualCamera() {
        try {
            Process process = executeObsCmdCommand("virtual-camera toggle");
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    // 执行obs-cmd命令的辅助方法
    private Process executeObsCmdCommand(String command) throws IOException {
        ConfigManager.Config config = configManager.getConfig();
        ConfigManager.ObsConfig obsConfig = config.getObs();
        String password = obsConfig.getPassword();

        String fullCommand = obsCmdPath;
        if (!password.isEmpty()) {
            fullCommand += " --websocket obsws://localhost:4455/" + password;
        }
        fullCommand += " " + command;

        System.out.println("执行obs-cmd命令: " + fullCommand);
        return Runtime.getRuntime().exec(fullCommand);
    }

    // VTuberStudio相关方法

    public boolean triggerVtsHotkey(String hotkeyName) {
        if (!isVtsConnected) {
            return false;
        }
        Map<String, Object> data = new HashMap<>();
        data.put("hotkeyName", hotkeyName);
        return sendVtsRequest("TriggerHotkey", data);
    }

    public boolean setVtsExpression(String expressionName) {
        if (!isVtsConnected) {
            return false;
        }
        Map<String, Object> data = new HashMap<>();
        data.put("expressionName", expressionName);
        return sendVtsRequest("SetExpression", data);
    }

    // 状态获取方法
    public Map<String, Object> getObsStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("connected", isObsConnected);
        status.put("enabled", configManager.getConfig().getObs().isEnabled());
        return status;
    }

    public Map<String, Object> getVtsStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("connected", isVtsConnected);
        status.put("enabled", configManager.getConfig().getVtuber_studio().isEnabled());
        return status;
    }

    // 私有辅助方法
    private void sendObsAuthResponse(String authResponse) {
        try {
            // OBS WebSocket v5认证格式 - 确保格式完全正确
            Map<String, Object> request = new HashMap<>();
            Map<String, Object> data = new HashMap<>();
            Map<String, Object> auth = new HashMap<>();

            auth.put("response", authResponse);
            auth.put("rpcVersion", 1);
            auth.put("eventSubscriptions", 0);

            data.put("auth", auth);
            request.put("op", 1); // Identify操作
            request.put("d", data);

            String message = objectMapper.writeValueAsString(request);
            System.out.println("准备发送OBS认证请求: " + message);

            if (obsWebSocket != null) {
                boolean sent = obsWebSocket.send(message);
                System.out.println("OBS认证请求发送结果: " + sent);
            } else {
                System.out.println("OBS WebSocket连接为空，无法发送认证请求");
            }
        } catch (Exception e) {
            System.out.println("发送OBS认证请求时发生错误: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String generateAuthResponse(String password, String salt, String challenge) throws Exception {
        // 步骤1: 对密码和盐进行SHA-256哈希
        String passwordSalt = password + salt;
        byte[] passwordSaltHash = sha256(passwordSalt);

        // 步骤2: 对哈希结果和挑战进行HMAC-SHA256
        // 注意：challenge是Base64编码的，需要先解码
        byte[] challengeBytes = Base64.getDecoder().decode(challenge);
        byte[] hmacResult = hmacSha256(passwordSaltHash, challengeBytes);

        // 步骤3: 对结果进行Base64编码
        return Base64.getEncoder().encodeToString(hmacResult);
    }

    private byte[] sha256(String input) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        return digest.digest(input.getBytes(StandardCharsets.UTF_8));
    }

    private byte[] hmacSha256(byte[] key, byte[] data) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        SecretKeySpec secretKey = new SecretKeySpec(key, "HmacSHA256");
        mac.init(secretKey);
        return mac.doFinal(data);
    }

    private boolean sendObsRequest(String requestType) {
        return sendObsRequest(requestType, new HashMap<>());
    }

    private boolean sendObsRequest(String requestType, Map<String, Object> data) {
        try {
            if (obsWebSocket == null) {
                return false;
            }

            Map<String, Object> request = new HashMap<>();
            request.put("requestType", requestType);
            request.put("requestId", "" + System.currentTimeMillis());
            request.put("requestData", data);

            String message = objectMapper.writeValueAsString(request);
            obsWebSocket.send(message);
            System.out.println("发送OBS请求: " + message);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    private boolean sendVtsRequest(String requestType, Map<String, Object> data) {
        try {
            if (vtsWebSocket == null || !isVtsConnected) {
                return false;
            }

            Map<String, Object> request = new HashMap<>();
            request.put("requestType", requestType);
            request.put("data", data);

            String message = objectMapper.writeValueAsString(request);
            vtsWebSocket.send(message);
            System.out.println("发送VTuberStudio请求: " + message);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    // 打开OBS应用程序
    public boolean openObs(String path) {
        try {
            System.out.println("正在打开OBS...");
            System.out.println("OBS路径: " + path);
            // 尝试打开OBS
            if (path != null && !path.isEmpty()) {
                // 检查路径是否为目录
                File file = new File(path);
                String executablePath = path;
                if (file.isDirectory()) {
                    // 如果是目录，尝试在目录中查找可执行文件
                    File obsExe = new File(file, "obs64.exe");
                    if (obsExe.exists()) {
                        executablePath = obsExe.getAbsolutePath();
                    } else {
                        // 尝试其他可能的可执行文件名
                        File obs32Exe = new File(file, "obs32.exe");
                        if (obs32Exe.exists()) {
                            executablePath = obs32Exe.getAbsolutePath();
                        } else {
                            // 目录中没有找到可执行文件，使用默认命令
                            System.out.println("目录中没有找到OBS可执行文件，使用默认命令");
                            Runtime.getRuntime().exec("cmd.exe /c start obs64.exe");
                            // 等待1秒，确保软件已经启动
                            Thread.sleep(1000);
                            // 尝试将OBS窗口置于最上层
                            bringWindowToFront("OBS");
                            System.out.println("OBS打开命令已执行");
                            return true;
                        }
                    }
                }
                // 直接使用cmd命令打开，确保使用用户配置的路径
                // 使用ProcessBuilder来处理包含空格的路径
                ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", "start", "", executablePath);
                System.out.println("执行命令: " + pb.command());
                pb.start();
            } else {
                // 没有路径，尝试使用默认命令
                System.out.println("没有提供路径，使用默认命令");
                Runtime.getRuntime().exec("cmd.exe /c start obs64.exe");
            }
            // 等待1秒，确保软件已经启动
            Thread.sleep(1000);
            // 尝试将OBS窗口置于最上层
            bringWindowToFront("OBS");
            System.out.println("OBS打开命令已执行");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("打开OBS失败: " + e.getMessage());
            return false;
        }
    }

    // 打开VTuberStudio应用程序
    public boolean openVts(String path) {
        try {
            System.out.println("正在打开VTuberStudio...");
            System.out.println("VTuberStudio路径: " + path);
            // 尝试打开VTuberStudio
            if (path != null && !path.isEmpty()) {
                // 检查路径是否为目录
                File file = new File(path);
                String executablePath = path;
                if (file.isDirectory()) {
                    // 如果是目录，尝试在目录中查找可执行文件
                    File vtsExe = new File(file, "VTuberStudio.exe");
                    if (vtsExe.exists()) {
                        executablePath = vtsExe.getAbsolutePath();
                    } else {
                        // 目录中没有找到可执行文件，使用默认命令
                        System.out.println("目录中没有找到VTuberStudio可执行文件，使用默认命令");
                        Runtime.getRuntime().exec("cmd.exe /c start VTuberStudio.exe");
                        // 等待1秒，确保软件已经启动
                        Thread.sleep(1000);
                        // 尝试将VTuberStudio窗口置于最上层
                        bringWindowToFront("VTuber Studio");
                        System.out.println("VTuberStudio打开命令已执行");
                        return true;
                    }
                }
                // 直接使用cmd命令打开，确保使用用户配置的路径
                // 使用ProcessBuilder来处理包含空格的路径
                ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", "start", "", executablePath);
                System.out.println("执行命令: " + pb.command());
                pb.start();
            } else {
                // 没有路径，尝试使用默认命令
                System.out.println("没有提供路径，使用默认命令");
                Runtime.getRuntime().exec("cmd.exe /c start VTuberStudio.exe");
            }
            // 等待1秒，确保软件已经启动
            Thread.sleep(1000);
            // 尝试将VTuberStudio窗口置于最上层
            bringWindowToFront("VTuber Studio");
            System.out.println("VTuberStudio打开命令已执行");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("打开VTuberStudio失败: " + e.getMessage());
            return false;
        }
    }

    // 将指定标题的窗口置于最上层
    private void bringWindowToFront(String windowTitle) {
        try {
            // 使用PowerShell命令查找并激活窗口
            String powerShellCommand = "Get-Process | Where-Object {$_.MainWindowTitle -like '*" + windowTitle
                    + "*'} | ForEach-Object { $wshell = New-Object -ComObject wscript.shell; $wshell.AppActivate($_.MainWindowTitle) }";
            String command = "powershell.exe -Command " + powerShellCommand;
            System.out.println("执行PowerShell命令: " + command);
            Runtime.getRuntime().exec(command);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("将窗口置于最上层失败: " + e.getMessage());
        }
    }

    public boolean closeObs() {
        try {
            System.out.println("正在关闭OBS...");
            // 使用taskkill命令关闭OBS进程
            Runtime.getRuntime().exec("taskkill /IM obs64.exe /F");
            System.out.println("OBS关闭命令已执行");
            return true;
        } catch (Exception e) {
            System.out.println("关闭OBS时发生错误: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    public boolean closeVts() {
        try {
            System.out.println("正在关闭VTube Studio...");
            // 使用taskkill命令关闭VTube Studio进程
            // 注意：进程名包含空格，需要用引号包围，并且要包含.exe扩展名
            Runtime.getRuntime().exec("taskkill /IM \"VTube Studio.exe\" /F");
            System.out.println("VTube Studio关闭命令已执行");
            return true;
        } catch (Exception e) {
            System.out.println("关闭VTube Studio时发生错误: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
}
