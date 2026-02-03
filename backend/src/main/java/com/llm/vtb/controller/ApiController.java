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
    public ResponseEntity<ConfigManager.Config> getConfig() {
        return ResponseEntity.ok(configManager.getConfig());
    }

    @PostMapping("/config")
    public ResponseEntity<Map<String, String>> updateConfig(@RequestBody ConfigManager.Config config) {
        try {
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

    // VTuberStudio API端点
    @PostMapping("/vts/connect")
    public ResponseEntity<Map<String, String>> connectToVts() {
        boolean success = obsVtsSystem.connectToVts();
        if (success) {
            Map<String, String> response = new HashMap<>();
            response.put("message", "连接VTuberStudio成功");
            return ResponseEntity.ok(response);
        } else {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", "连接VTuberStudio失败");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }

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

    // 状态获取端点
    @GetMapping("/status")
    public ResponseEntity<Map<String, Map<String, Object>>> getStatus() {
        Map<String, Map<String, Object>> response = new HashMap<>();
        response.put("obs", obsVtsSystem.getObsStatus());
        response.put("vts", obsVtsSystem.getVtsStatus());
        return ResponseEntity.ok(response);
    }
}
