package com.llm.vtb.voice;

import com.llm.vtb.config.ConfigManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.sound.sampled.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class VoiceApiSystem {

    @Autowired
    private ConfigManager configManager;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private TargetDataLine targetDataLine;
    private ByteArrayOutputStream byteArrayOutputStream;
    private Thread recordingThread;
    private boolean isRecording = false;

    public boolean textToSpeech(String text, String outputFile) {
        boolean result = false;
        System.out.println("*****************************************************************");
        System.out.println("开始执行textToSpeech方法");
        System.out.println("*****************************************************************");

        try {
            System.out.println("开始文本转语音处理...");
            System.out.println("输入文本: " + text);
            System.out.println("输出文件: " + outputFile);

            // 强制刷新输出流
            System.out.flush();

            ConfigManager.Config config = configManager.getConfig();
            System.out.println("获取配置成功");

            ConfigManager.VoiceApiConfig voiceApiConfig = config.getVoice_api();
            System.out.println("获取语音API配置成功");

            ConfigManager.VoiceApiConfig.TtsConfig ttsConfig = voiceApiConfig.getTts();
            System.out.println("获取TTS配置成功");

            String apiKey = ttsConfig.getApi_key();
            String baseUrl = ttsConfig.getBase_url();
            String voice = ttsConfig.getVoice();
            String engine = ttsConfig.getEngine();

            System.out.println("TTS配置:");
            System.out.println("- API Key: " + (apiKey.isEmpty() ? "空"
                    : apiKey.substring(0, 5) + "..." + apiKey.substring(apiKey.length() - 5)));
            System.out.println("- Base URL: " + (baseUrl.isEmpty() ? "空" : baseUrl));
            System.out.println("- Voice: " + (voice.isEmpty() ? "空" : voice));
            System.out.println("- Engine: " + engine);

            // 强制刷新输出流
            System.out.flush();

            // 如果配置不完整，返回失败
            if (apiKey.isEmpty() || baseUrl.isEmpty() || voice.isEmpty()) {
                System.out.println("TTS配置不完整，返回失败");
                System.out.flush();
                return false;
            }

            // 构建请求数据
            Map<String, Object> requestData = new HashMap<>();
            requestData.put("text", text);
            requestData.put("voice", voice);
            requestData.put("output_format", "wav");
            requestData.put("engine", engine);

            System.out.println("请求数据构建成功: " + requestData);
            System.out.flush();

            // 发送请求到TTS API
            System.out.println("开始发送TTS API请求...");
            System.out.flush();

            byte[] audioData = null;
            try {
                audioData = sendTtsRequest(baseUrl, apiKey, requestData);
                System.out.println("TTS API请求成功，收到音频数据，长度: " + (audioData != null ? audioData.length : 0) + " 字节");
                System.out.flush();
            } catch (Exception e) {
                System.out.println("TTS API请求失败:");
                e.printStackTrace();
                System.out.flush();
                throw e;
            }

            // 保存音频数据到文件
            System.out.println("开始保存音频数据到文件...");
            System.out.flush();

            try {
                saveAudioToFile(audioData, outputFile);
                System.out.println("音频数据保存成功，文件: " + outputFile);
                System.out.flush();
            } catch (Exception e) {
                System.out.println("音频数据保存失败:");
                e.printStackTrace();
                System.out.flush();
                throw e;
            }

            result = true;
            System.out.println("TTS处理成功完成");
            System.out.flush();

        } catch (Exception e) {
            System.out.println("TTS处理异常:");
            e.printStackTrace();
            System.out.flush();
            result = false;
        } finally {
            System.out.println("*****************************************************************");
            System.out.println("TTS处理完成，结果: " + result);
            System.out.println("*****************************************************************");
            System.out.flush();
        }
        return result;
    }

    public String speechToText(String audioFile) {
        try {
            ConfigManager.Config config = configManager.getConfig();
            ConfigManager.VoiceApiConfig.AsrConfig asrConfig = config.getVoice_api().getAsr();

            String apiKey = asrConfig.getApi_key();
            String baseUrl = asrConfig.getBase_url();

            // 如果配置不完整，返回空字符串
            if (apiKey.isEmpty() || baseUrl.isEmpty()) {
                return "请先配置语音识别API参数。";
            }

            // 如果没有提供音频文件，使用默认录制的音频
            if (audioFile == null || audioFile.isEmpty()) {
                audioFile = "recording.wav";
            }

            // 读取音频文件
            byte[] audioData = readAudioFile(audioFile);

            // 发送请求到ASR API
            String response = sendAsrRequest(baseUrl, apiKey, audioData);

            // 解析响应
            return parseAsrResponse(response);
        } catch (Exception e) {
            e.printStackTrace();
            return "语音识别时出错：" + e.getMessage();
        }
    }

    public void startRecording() {
        try {
            AudioFormat format = new AudioFormat(
                    AudioFormat.Encoding.PCM_SIGNED,
                    44100,
                    16,
                    2,
                    4,
                    44100,
                    false);

            DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
            targetDataLine = (TargetDataLine) AudioSystem.getLine(info);
            targetDataLine.open(format);
            targetDataLine.start();

            byteArrayOutputStream = new ByteArrayOutputStream();
            isRecording = true;

            recordingThread = new Thread(() -> {
                byte[] buffer = new byte[1024];
                int bytesRead;

                while (isRecording) {
                    bytesRead = targetDataLine.read(buffer, 0, buffer.length);
                    if (bytesRead > 0) {
                        byteArrayOutputStream.write(buffer, 0, bytesRead);
                    }
                }
            });

            recordingThread.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stopRecording() {
        try {
            isRecording = false;
            if (recordingThread != null) {
                recordingThread.join();
            }

            if (targetDataLine != null) {
                targetDataLine.stop();
                targetDataLine.close();
            }

            // 保存录制的音频
            if (byteArrayOutputStream != null) {
                byte[] audioData = byteArrayOutputStream.toByteArray();
                saveRecordingToFile(audioData, "recording.wav");
                byteArrayOutputStream.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private byte[] sendTtsRequest(String baseUrl, String apiKey, Map<String, Object> requestData) throws Exception {
        System.out.println("开始执行sendTtsRequest方法...");
        System.out.println("Base URL: " + baseUrl);
        System.out.println("API Key: " + apiKey.substring(0, 5) + "..." + apiKey.substring(apiKey.length() - 5));
        System.out.println("Request Data: " + requestData);

        // 构建完整的API端点URL（阿里云DashScope TTS API）
        String apiUrl = baseUrl;
        if (!apiUrl.endsWith("/api/v1/text2speech")) {
            apiUrl = apiUrl + (apiUrl.endsWith("/") ? "" : "/") + "api/v1/text2speech";
        }

        System.out.println("TTS API 端点 URL: " + apiUrl);

        URL url = new URL(apiUrl);
        HttpURLConnection connection = null;
        ByteArrayOutputStream outputStream = null;

        try {
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey);
            connection.setDoOutput(true);
            connection.setConnectTimeout(30000); // 30秒连接超时
            connection.setReadTimeout(30000); // 30秒读取超时

            // 写入请求体
            System.out.println("开始写入请求体...");
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = objectMapper.writeValueAsString(requestData).getBytes(StandardCharsets.UTF_8);
                System.out.println("TTS 请求体: " + new String(input, StandardCharsets.UTF_8));
                os.write(input, 0, input.length);
                os.flush();
            }
            System.out.println("请求体写入成功");

            // 读取响应状态码
            System.out.println("开始读取响应状态码...");
            int responseCode = connection.getResponseCode();
            System.out.println("TTS API 响应状态码: " + responseCode);

            // 读取响应
            System.out.println("开始读取响应数据...");
            outputStream = new ByteArrayOutputStream();
            try (InputStream is = responseCode == HttpURLConnection.HTTP_OK ? connection.getInputStream()
                    : connection.getErrorStream()) {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = is.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }
            }
            System.out.println("响应数据读取成功");

            byte[] responseData = outputStream.toByteArray();
            String responseString = new String(responseData, StandardCharsets.UTF_8);
            System.out.println("TTS API 响应长度: " + responseData.length + " 字节");
            System.out.println("TTS API 响应: " + responseString);

            // 检查响应状态
            if (responseCode != HttpURLConnection.HTTP_OK) {
                System.out.println("TTS API 请求失败，状态码: " + responseCode);
                throw new Exception("TTS API 请求失败: " + responseString);
            }

            System.out.println("TTS API 请求成功，返回音频数据");
            return responseData;

        } catch (Exception e) {
            System.out.println("sendTtsRequest方法异常:");
            e.printStackTrace();
            throw e;
        } finally {
            if (outputStream != null) {
                try {
                    outputStream.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            if (connection != null) {
                connection.disconnect();
                System.out.println("HTTP连接已断开");
            }
        }
    }

    private String sendAsrRequest(String baseUrl, String apiKey, byte[] audioData) throws Exception {
        URL url = new URL(baseUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Authorization", "Bearer " + apiKey);
        connection.setRequestProperty("Content-Type", "audio/wav");
        connection.setDoOutput(true);

        // 写入音频数据
        try (OutputStream os = connection.getOutputStream()) {
            os.write(audioData);
        }

        // 读取响应
        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
        }

        connection.disconnect();
        return response.toString();
    }

    private void saveAudioToFile(byte[] audioData, String outputFile) throws Exception {
        System.out.println("开始执行saveAudioToFile方法...");
        System.out.println("输出文件: " + outputFile);
        System.out.println("音频数据长度: " + (audioData != null ? audioData.length : 0) + " 字节");

        try {
            File output = new File(outputFile);
            System.out.println("文件对象创建成功: " + output.getAbsolutePath());

            File parentDir = output.getParentFile();
            System.out.println("父目录: " + (parentDir != null ? parentDir.getAbsolutePath() : "无"));

            if (parentDir != null && !parentDir.exists()) {
                System.out.println("父目录不存在，创建中...");
                boolean mkdirsResult = parentDir.mkdirs();
                System.out.println("父目录创建结果: " + mkdirsResult);
            }

            try (FileOutputStream fos = new FileOutputStream(output)) {
                System.out.println("文件输出流创建成功，开始写入数据...");
                fos.write(audioData);
                fos.flush();
                System.out.println("音频数据写入成功");
            }

            System.out.println("saveAudioToFile方法执行成功");

        } catch (Exception e) {
            System.out.println("saveAudioToFile方法异常:");
            e.printStackTrace();
            throw e;
        }
    }

    private void saveRecordingToFile(byte[] audioData, String outputFile) throws Exception {
        AudioFormat format = new AudioFormat(
                AudioFormat.Encoding.PCM_SIGNED,
                44100,
                16,
                2,
                4,
                44100,
                false);

        ByteArrayInputStream bais = new ByteArrayInputStream(audioData);
        AudioInputStream ais = new AudioInputStream(bais, format, audioData.length / format.getFrameSize());

        File output = new File(outputFile);
        AudioSystem.write(ais, AudioFileFormat.Type.WAVE, output);

        ais.close();
        bais.close();
    }

    private byte[] readAudioFile(String audioFile) throws Exception {
        File file = new File(audioFile);
        if (!file.exists()) {
            throw new FileNotFoundException("音频文件不存在：" + audioFile);
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                baos.write(buffer, 0, bytesRead);
            }
            return baos.toByteArray();
        }
    }

    private String parseAsrResponse(String response) throws Exception {
        Map<String, Object> responseMap = objectMapper.readValue(response, Map.class);
        if (responseMap.containsKey("text")) {
            return (String) responseMap.get("text");
        }
        return "无法解析语音识别响应。";
    }

    public void startRecordingProcess() {
        startRecording();
    }

    public void stopRecordingProcess() {
        stopRecording();
    }
}
