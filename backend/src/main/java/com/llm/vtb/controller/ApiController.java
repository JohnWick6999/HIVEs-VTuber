package com.llm.vtb.controller;

import com.llm.vtb.ai.AiChatSystem;
import com.llm.vtb.config.ConfigManager;
import com.llm.vtb.obs.ObsVtsSystem;
import com.llm.vtb.voice.VoiceApiSystem;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private ConfigManager configManager;

    @Autowired
    private AiChatSystem aiChatSystem;

    @Autowired
    private VoiceApiSystem voiceApiSystem;

    @Autowired
    private ObsVtsSystem obsVtsSystem;

    // 健康检查端点
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "healthy");
        return ResponseEntity.ok(response);
    }

    // 配置管理端点
    @GetMapping("/config")
    public ResponseEntity<Map<String, Object>> getConfig() {
        ConfigManager.Config config = configManager.getConfig();
        Map<String, Object> responseMap = new HashMap<>();

        // 聊天API配置
        Map<String, Object> chatApiMap = new HashMap<>();
        chatApiMap.put("api_key", config.getChat_api().getApi_key());
        chatApiMap.put("base_url", config.getChat_api().getBase_url());
        chatApiMap.put("model", config.getChat_api().getModel());
        chatApiMap.put("temperature", config.getChat_api().getTemperature());
        chatApiMap.put("max_tokens", config.getChat_api().getMax_tokens());
        responseMap.put("chat_api", chatApiMap);

        // 语音API配置
        Map<String, Object> voiceApiMap = new HashMap<>();
        Map<String, Object> ttsMap = new HashMap<>();
        ttsMap.put("api_key", config.getVoice_api().getTts().getApi_key());
        ttsMap.put("base_url", config.getVoice_api().getTts().getBase_url());
        ttsMap.put("voice", config.getVoice_api().getTts().getVoice());
        ttsMap.put("engine", config.getVoice_api().getTts().getEngine());
        voiceApiMap.put("tts", ttsMap);

        Map<String, Object> asrMap = new HashMap<>();
        asrMap.put("api_key", config.getVoice_api().getAsr().getApi_key());
        asrMap.put("base_url", config.getVoice_api().getAsr().getBase_url());
        voiceApiMap.put("asr", asrMap);
        responseMap.put("voice_api", voiceApiMap);

        // OBS API配置
        Map<String, Object> obsApiMap = new HashMap<>();
        ConfigManager.ObsConfig obsConfig = config.getObs();
        String obsWsUrl = "ws://" + obsConfig.getHost() + ":" + obsConfig.getPort();
        obsApiMap.put("ws_url", obsWsUrl);
        obsApiMap.put("password", obsConfig.getPassword());
        responseMap.put("obs_api", obsApiMap);

        // VTS API配置
        Map<String, Object> vtsApiMap = new HashMap<>();
        ConfigManager.VtsConfig vtsConfig = config.getVtuber_studio();
        String vtsWsUrl = "ws://" + vtsConfig.getHost() + ":" + vtsConfig.getPort();
        vtsApiMap.put("ws_url", vtsWsUrl);
        vtsApiMap.put("password", ""); // VTS暂时不支持密码
        responseMap.put("vts_api", vtsApiMap);

        // 图像API配置
        Map<String, Object> imageApiMap = new HashMap<>();
        imageApiMap.put("api_key", config.getImage_api().getApi_key());
        imageApiMap.put("base_url", config.getImage_api().getBase_url());
        responseMap.put("image_api", imageApiMap);

        // 搜索API配置
        Map<String, Object> searchApiMap = new HashMap<>();
        searchApiMap.put("api_key", config.getSearch_api().getApi_key());
        searchApiMap.put("base_url", config.getSearch_api().getBase_url());
        searchApiMap.put("model", config.getSearch_api().getModel());
        responseMap.put("search_api", searchApiMap);

        // 数据库配置
        Map<String, Object> databaseMap = new HashMap<>();
        databaseMap.put("enabled", config.getDatabase().isEnabled());
        databaseMap.put("db_path", config.getDatabase().getDb_path());
        responseMap.put("database", databaseMap);

        // 人格配置
        Map<String, Object> personalityMap = new HashMap<>();
        personalityMap.put("name", config.getPersonality().getName());
        personalityMap.put("description", config.getPersonality().getDescription());
        personalityMap.put("greeting", config.getPersonality().getGreeting());
        personalityMap.put("tone", config.getPersonality().getTone());
        responseMap.put("personality", personalityMap);

        // 软件路径配置
        Map<String, Object> softwarePathsMap = new HashMap<>();
        if (config.getSoftware_paths() != null) {
            softwarePathsMap.put("obs",
                    config.getSoftware_paths().getObs() != null ? config.getSoftware_paths().getObs() : "");
            softwarePathsMap.put("vts",
                    config.getSoftware_paths().getVts() != null ? config.getSoftware_paths().getVts() : "");
        } else {
            softwarePathsMap.put("obs", "");
            softwarePathsMap.put("vts", "");
        }
        responseMap.put("software_paths", softwarePathsMap);

        return ResponseEntity.ok(responseMap);
    }

    @PostMapping("/config")
    public ResponseEntity<Map<String, String>> updateConfig(@RequestBody Map<String, Object> configMap) {
        try {
            System.out.println("接收到配置更新请求:");
            System.out.println("配置数据: " + configMap);

            // 检查是否包含obs_api字段
            if (configMap.containsKey("obs_api")) {
                System.out.println("包含obs_api字段:");
                System.out.println("obs_api数据: " + configMap.get("obs_api"));
            } else {
                System.out.println("不包含obs_api字段");
            }

            // 检查是否包含vts_api字段
            if (configMap.containsKey("vts_api")) {
                System.out.println("包含vts_api字段:");
                System.out.println("vts_api数据: " + configMap.get("vts_api"));
            } else {
                System.out.println("不包含vts_api字段");
            }

            ConfigManager.Config config = configManager.getConfig();

            // 处理聊天API配置
            if (configMap.containsKey("chat_api")) {
                Map<String, Object> chatApiMap = (Map<String, Object>) configMap.get("chat_api");
                ConfigManager.ChatApiConfig chatApiConfig = config.getChat_api();
                if (chatApiMap.containsKey("api_key"))
                    chatApiConfig.setApi_key((String) chatApiMap.get("api_key"));
                if (chatApiMap.containsKey("base_url"))
                    chatApiConfig.setBase_url((String) chatApiMap.get("base_url"));
                if (chatApiMap.containsKey("model"))
                    chatApiConfig.setModel((String) chatApiMap.get("model"));
                if (chatApiMap.containsKey("temperature"))
                    chatApiConfig.setTemperature((double) chatApiMap.get("temperature"));
                if (chatApiMap.containsKey("max_tokens"))
                    chatApiConfig.setMax_tokens((int) chatApiMap.get("max_tokens"));
            }

            // 处理语音API配置
            if (configMap.containsKey("voice_api")) {
                Map<String, Object> voiceApiMap = (Map<String, Object>) configMap.get("voice_api");
                ConfigManager.VoiceApiConfig voiceApiConfig = config.getVoice_api();

                if (voiceApiMap.containsKey("tts")) {
                    Map<String, Object> ttsMap = (Map<String, Object>) voiceApiMap.get("tts");
                    ConfigManager.VoiceApiConfig.TtsConfig ttsConfig = voiceApiConfig.getTts();
                    if (ttsMap.containsKey("api_key"))
                        ttsConfig.setApi_key((String) ttsMap.get("api_key"));
                    if (ttsMap.containsKey("base_url"))
                        ttsConfig.setBase_url((String) ttsMap.get("base_url"));
                    if (ttsMap.containsKey("voice"))
                        ttsConfig.setVoice((String) ttsMap.get("voice"));
                    if (ttsMap.containsKey("engine"))
                        ttsConfig.setEngine((String) ttsMap.get("engine"));
                }

                if (voiceApiMap.containsKey("asr")) {
                    Map<String, Object> asrMap = (Map<String, Object>) voiceApiMap.get("asr");
                    ConfigManager.VoiceApiConfig.AsrConfig asrConfig = voiceApiConfig.getAsr();
                    if (asrMap.containsKey("api_key"))
                        asrConfig.setApi_key((String) asrMap.get("api_key"));
                    if (asrMap.containsKey("base_url"))
                        asrConfig.setBase_url((String) asrMap.get("base_url"));
                }
            }

            // 处理OBS API配置
            if (configMap.containsKey("obs_api")) {
                Map<String, Object> obsApiMap = (Map<String, Object>) configMap.get("obs_api");
                ConfigManager.ObsConfig obsConfig = config.getObs();

                if (obsApiMap.containsKey("ws_url")) {
                    String wsUrl = (String) obsApiMap.get("ws_url");
                    // 解析WebSocket URL，提取host和port
                    if (wsUrl.startsWith("ws://")) {
                        String hostPort = wsUrl.substring(5);
                        int colonIndex = hostPort.lastIndexOf(':');
                        if (colonIndex != -1) {
                            String host = hostPort.substring(0, colonIndex);
                            int port = Integer.parseInt(hostPort.substring(colonIndex + 1));
                            obsConfig.setHost(host);
                            obsConfig.setPort(port);
                        }
                    }
                }

                if (obsApiMap.containsKey("password")) {
                    obsConfig.setPassword((String) obsApiMap.get("password"));
                }

                obsConfig.setEnabled(true);
            }

            // 处理VTS API配置
            if (configMap.containsKey("vts_api")) {
                Map<String, Object> vtsApiMap = (Map<String, Object>) configMap.get("vts_api");
                ConfigManager.VtsConfig vtsConfig = config.getVtuber_studio();

                if (vtsApiMap.containsKey("ws_url")) {
                    String wsUrl = (String) vtsApiMap.get("ws_url");
                    // 解析WebSocket URL，提取host和port
                    if (wsUrl.startsWith("ws://")) {
                        String hostPort = wsUrl.substring(5);
                        int colonIndex = hostPort.lastIndexOf(':');
                        if (colonIndex != -1) {
                            String host = hostPort.substring(0, colonIndex);
                            int port = Integer.parseInt(hostPort.substring(colonIndex + 1));
                            vtsConfig.setHost(host);
                            vtsConfig.setPort(port);
                        }
                    }
                }

                if (vtsApiMap.containsKey("password")) {
                    // 注意：VtsConfig类需要添加password字段
                    // 这里暂时注释，等添加字段后再启用
                    // vtsConfig.setPassword((String) vtsApiMap.get("password"));
                }

                vtsConfig.setEnabled(true);
            }

            // 处理图像API配置
            if (configMap.containsKey("image_api")) {
                Map<String, Object> imageApiMap = (Map<String, Object>) configMap.get("image_api");
                ConfigManager.ImageApiConfig imageApiConfig = config.getImage_api();
                if (imageApiMap.containsKey("api_key")) {
                    imageApiConfig.setApi_key((String) imageApiMap.get("api_key"));
                }
                if (imageApiMap.containsKey("base_url")) {
                    imageApiConfig.setBase_url((String) imageApiMap.get("base_url"));
                }
            }

            // 处理搜索API配置
            if (configMap.containsKey("search_api")) {
                Map<String, Object> searchApiMap = (Map<String, Object>) configMap.get("search_api");
                ConfigManager.SearchApiConfig searchApiConfig = config.getSearch_api();
                if (searchApiMap.containsKey("api_key")) {
                    searchApiConfig.setApi_key((String) searchApiMap.get("api_key"));
                }
                if (searchApiMap.containsKey("base_url")) {
                    searchApiConfig.setBase_url((String) searchApiMap.get("base_url"));
                }
                if (searchApiMap.containsKey("model")) {
                    searchApiConfig.setModel((String) searchApiMap.get("model"));
                }
            }

            // 处理数据库配置
            if (configMap.containsKey("database")) {
                Map<String, Object> databaseMap = (Map<String, Object>) configMap.get("database");
                ConfigManager.DatabaseConfig databaseConfig = config.getDatabase();
                if (databaseMap.containsKey("enabled")) {
                    databaseConfig.setEnabled((boolean) databaseMap.get("enabled"));
                }
                if (databaseMap.containsKey("db_path")) {
                    databaseConfig.setDb_path((String) databaseMap.get("db_path"));
                }
            }

            // 处理人格配置
            if (configMap.containsKey("personality")) {
                Map<String, Object> personalityMap = (Map<String, Object>) configMap.get("personality");
                ConfigManager.PersonalityConfig personalityConfig = config.getPersonality();
                if (personalityMap.containsKey("name")) {
                    personalityConfig.setName((String) personalityMap.get("name"));
                }
                if (personalityMap.containsKey("description")) {
                    personalityConfig.setDescription((String) personalityMap.get("description"));
                }
                if (personalityMap.containsKey("greeting")) {
                    personalityConfig.setGreeting((String) personalityMap.get("greeting"));
                }
                if (personalityMap.containsKey("tone")) {
                    personalityConfig.setTone((String) personalityMap.get("tone"));
                }
            }

            // 处理软件路径配置
            if (configMap.containsKey("software_paths")) {
                Map<String, Object> softwarePathsMap = (Map<String, Object>) configMap.get("software_paths");
                if (config.getSoftware_paths() == null) {
                    config.setSoftware_paths(new ConfigManager.SoftwarePathsConfig());
                }
                ConfigManager.SoftwarePathsConfig softwarePathsConfig = config.getSoftware_paths();
                if (softwarePathsMap.containsKey("obs")) {
                    softwarePathsConfig.setObs((String) softwarePathsMap.get("obs"));
                }
                if (softwarePathsMap.containsKey("vts")) {
                    softwarePathsConfig.setVts((String) softwarePathsMap.get("vts"));
                }
            }

            configManager.setConfig(config);
            configManager.saveConfig();
            Map<String, String> response = new HashMap<>();
            response.put("message", "配置更新成功");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "配置更新失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    // 聊天API端点
    @PostMapping("/chat")
    public ResponseEntity<Map<String, String>> chat(@RequestBody Map<String, String> request) {
        try {
            String userInput = request.get("input");
            if (userInput == null || userInput.isEmpty()) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "输入不能为空");
                return ResponseEntity.badRequest().body(errorResponse);
            }

            // 生成回复
            String response = aiChatSystem.generateResponse(userInput);

            Map<String, String> responseBody = new HashMap<>();
            responseBody.put("response", response);
            return ResponseEntity.ok(responseBody);
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "聊天失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    // 语音API端点
    @PostMapping("/tts")
    public ResponseEntity<Map<String, String>> textToSpeech(@RequestBody Map<String, String> request) {
        try {
            System.out.println("收到TTS请求:");
            System.out.println("- 请求参数: " + request);

            String text = request.get("text");
            String outputFile = request.getOrDefault("output_file", "output.wav");

            System.out.println("- 文本: " + text);
            System.out.println("- 输出文件: " + outputFile);

            if (text == null || text.isEmpty()) {
                System.out.println("TTS请求失败: 文本不能为空");
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "文本不能为空");
                return ResponseEntity.badRequest().body(errorResponse);
            }

            System.out.println("开始调用VoiceApiSystem.textToSpeech...");
            boolean success = voiceApiSystem.textToSpeech(text, outputFile);
            System.out.println("VoiceApiSystem.textToSpeech返回: " + success);

            if (success) {
                System.out.println("TTS请求成功");
                Map<String, String> response = new HashMap<>();
                response.put("message", "TTS成功");
                response.put("file", outputFile);
                return ResponseEntity.ok(response);
            } else {
                System.out.println("TTS请求失败: VoiceApiSystem返回失败");
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "TTS失败");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
            }
        } catch (Exception e) {
            System.out.println("TTS请求异常: " + e.getMessage());
            e.printStackTrace();
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "TTS失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/asr")
    public ResponseEntity<Map<String, String>> speechToText(@RequestBody Map<String, String> request) {
        try {
            String audioFile = request.get("audio_file");
            voiceApiSystem.startRecordingProcess();
            // 模拟录音时间
            Thread.sleep(3000);
            voiceApiSystem.stopRecordingProcess();

            String text = voiceApiSystem.speechToText(audioFile);
            Map<String, String> response = new HashMap<>();
            response.put("text", text);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "ASR失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    // OBS API端点
    @PostMapping("/obs/connect")
    public ResponseEntity<Map<String, String>> connectToObs() {
        boolean success = obsVtsSystem.connectToObs();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "连接OBS成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "连接OBS失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/test")
    public ResponseEntity<Map<String, String>> testObsCmd() {
        boolean success = obsVtsSystem.testObsCmd();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "OBS-CMD测试成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "OBS-CMD测试失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/disconnect")
    public ResponseEntity<Map<String, String>> disconnectFromObs() {
        obsVtsSystem.disconnectFromObs();
        Map<String, String> response = new HashMap<>();
        response.put("message", "断开OBS连接成功");
        return ResponseEntity.ok(response);
    }

    @PostMapping("/obs/recording/start")
    public ResponseEntity<Map<String, String>> startObsRecording() {
        boolean success = obsVtsSystem.startObsRecording();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "开始OBS录制成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "开始OBS录制失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/recording/stop")
    public ResponseEntity<Map<String, String>> stopObsRecording() {
        boolean success = obsVtsSystem.stopObsRecording();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "停止OBS录制成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "停止OBS录制失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/recording/toggle")
    public ResponseEntity<Map<String, String>> toggleObsRecording() {
        boolean success = obsVtsSystem.toggleObsRecording();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "切换OBS录制状态成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "切换OBS录制状态失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/streaming/start")
    public ResponseEntity<Map<String, String>> startObsStreaming() {
        boolean success = obsVtsSystem.startObsStreaming();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "开始OBS推流成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "开始OBS推流失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/streaming/stop")
    public ResponseEntity<Map<String, String>> stopObsStreaming() {
        boolean success = obsVtsSystem.stopObsStreaming();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "停止OBS推流成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "停止OBS推流失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/streaming/toggle")
    public ResponseEntity<Map<String, String>> toggleObsStreaming() {
        boolean success = obsVtsSystem.toggleObsStreaming();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "切换OBS推流状态成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "切换OBS推流状态失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/scene")
    public ResponseEntity<Map<String, String>> setObsScene(@RequestBody Map<String, String> request) {
        try {
            String sceneName = request.get("scene_name");
            if (sceneName == null || sceneName.isEmpty()) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "场景名称不能为空");
                return ResponseEntity.badRequest().body(errorResponse);
            }

            boolean success = obsVtsSystem.setObsScene(sceneName);
            if (success) {
                Map<String, String> response = new HashMap<>();
                response.put("message", "设置OBS场景成功");
                return ResponseEntity.ok(response);
            } else {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "设置OBS场景失败");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
            }
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "设置OBS场景失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/virtual-camera/start")
    public ResponseEntity<Map<String, String>> startVirtualCamera() {
        boolean success = obsVtsSystem.startVirtualCamera();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "启动虚拟摄像头成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "启动虚拟摄像头失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/virtual-camera/stop")
    public ResponseEntity<Map<String, String>> stopVirtualCamera() {
        boolean success = obsVtsSystem.stopVirtualCamera();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "停止虚拟摄像头成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "停止虚拟摄像头失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/virtual-camera/toggle")
    public ResponseEntity<Map<String, String>> toggleVirtualCamera() {
        boolean success = obsVtsSystem.toggleVirtualCamera();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "切换虚拟摄像头状态成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "切换虚拟摄像头状态失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/open")
    public ResponseEntity<Map<String, String>> openObs(@RequestBody Map<String, String> request) {
        String path = request.get("path");
        boolean success = obsVtsSystem.openObs(path);
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "打开OBS成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "打开OBS失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/obs/close")
    public ResponseEntity<Map<String, String>> closeObs() {
        boolean success = obsVtsSystem.closeObs();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "关闭OBS成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "关闭OBS失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    // VTuberStudio API端点
    @PostMapping("/vts/hotkey")
    public ResponseEntity<Map<String, String>> triggerVtsHotkey(@RequestBody Map<String, String> request) {
        try {
            String hotkeyName = request.get("hotkey_name");
            if (hotkeyName == null || hotkeyName.isEmpty()) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "热键名称不能为空");
                return ResponseEntity.badRequest().body(errorResponse);
            }

            boolean success = obsVtsSystem.triggerVtsHotkey(hotkeyName);
            if (success) {
                Map<String, String> response = new HashMap<>();
                response.put("message", "触发VTuberStudio热键成功");
                return ResponseEntity.ok(response);
            } else {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "触发VTuberStudio热键失败");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
            }
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "触发VTuberStudio热键失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/vts/expression")
    public ResponseEntity<Map<String, String>> setVtsExpression(@RequestBody Map<String, String> request) {
        try {
            String expressionName = request.get("expression_name");
            if (expressionName == null || expressionName.isEmpty()) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "表情名称不能为空");
                return ResponseEntity.badRequest().body(errorResponse);
            }

            boolean success = obsVtsSystem.setVtsExpression(expressionName);
            if (success) {
                Map<String, String> response = new HashMap<>();
                response.put("message", "设置VTuberStudio表情成功");
                return ResponseEntity.ok(response);
            } else {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("message", "设置VTuberStudio表情失败");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
            }
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "设置VTuberStudio表情失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/vts/open")
    public ResponseEntity<Map<String, String>> openVts(@RequestBody Map<String, String> request) {
        String path = request.get("path");
        boolean success = obsVtsSystem.openVts(path);
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "打开VTuberStudio成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "打开VTuberStudio失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    @PostMapping("/vts/close")
    public ResponseEntity<Map<String, String>> closeVts() {
        boolean success = obsVtsSystem.closeVts();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "关闭VTuberStudio成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "关闭VTuberStudio失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

    // 状态获取端点
    @GetMapping("/status")
    public ResponseEntity<Map<String, Map<String, Object>>> getStatus() {
        Map<String, Map<String, Object>> response = new HashMap<>();
        response.put("obs", obsVtsSystem.getObsStatus());
        response.put("vts", obsVtsSystem.getVtsStatus());
        return ResponseEntity.ok(response);
    }
}
