package com.llm.vtb.ai;

import com.llm.vtb.config.ConfigManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class AiChatSystem {

    @Autowired
    private ConfigManager configManager;

    private final ObjectMapper objectMapper = new ObjectMapper();

    public String generateResponse(String userInput) {
        try {
            ConfigManager.Config config = configManager.getConfig();
            ConfigManager.ChatApiConfig chatApiConfig = config.getChat_api();

            String apiKey = chatApiConfig.getApi_key();
            String baseUrl = chatApiConfig.getBase_url();
            String model = chatApiConfig.getModel();
            double temperature = chatApiConfig.getTemperature();
            int maxTokens = chatApiConfig.getMax_tokens();

            // 使用默认配置（如果用户未配置）
            if (apiKey.isEmpty()) {
                apiKey = "sk-e4b872b156584ddb932b767be0bbe938"; // 使用原有项目的 DeepSeek API Key
                System.out.println("使用默认 DeepSeek API Key");
            }
            if (baseUrl.isEmpty()) {
                baseUrl = "https://api.deepseek.com"; // 使用原有项目的 DeepSeek API Base URL
                System.out.println("使用默认 DeepSeek API Base URL: " + baseUrl);
            }
            if (model.isEmpty()) {
                model = "deepseek-chat"; // 默认 DeepSeek 模型
                System.out.println("使用默认 DeepSeek 模型: " + model);
            }

            System.out.println("准备调用 AI API: ");
            System.out.println("- Model: " + model);
            System.out.println("- Base URL: " + baseUrl);
            System.out.println("- API Key: " + apiKey.substring(0, 5) + "..." + apiKey.substring(apiKey.length() - 5));
            System.out.println("- User Input: " + userInput);

            // 构建请求数据
            Map<String, Object> requestData = new HashMap<>();
            requestData.put("model", model);
            requestData.put("temperature", temperature);
            requestData.put("max_tokens", maxTokens);

            Map<String, String> systemMessage = new HashMap<>();
            systemMessage.put("role", "system");
            systemMessage.put("content", buildSystemPrompt());

            Map<String, String> userMessage = new HashMap<>();
            userMessage.put("role", "user");
            userMessage.put("content", userInput);

            requestData.put("messages", new Object[] { systemMessage, userMessage });

            // 发送请求到AI API
            System.out.println("发送请求到 AI API...");
            String response = sendApiRequest(baseUrl, apiKey, requestData);
            System.out.println("收到 API 响应: " + response.substring(0, Math.min(200, response.length())) + "...");

            // 解析响应
            String parsedResponse = parseApiResponse(response);
            System.out.println("解析后的响应: " + parsedResponse);
            return parsedResponse;
        } catch (Exception e) {
            System.out.println("AI 聊天 API 调用失败: " + e.getMessage());
            e.printStackTrace();
            return "抱歉，我暂时无法回答你的问题。错误原因: " + e.getMessage();
        }
    }

    private String buildSystemPrompt() {
        ConfigManager.Config config = configManager.getConfig();
        ConfigManager.PersonalityConfig personality = config.getPersonality();

        StringBuilder prompt = new StringBuilder();
        prompt.append("你是一个VTuber助手，名为").append(personality.getName()).append("。\n");
        prompt.append("你的性格特点：").append(personality.getDescription()).append("\n");
        prompt.append("你的语气风格：").append(personality.getTone()).append("\n");
        prompt.append("你的问候语：").append(personality.getGreeting()).append("\n");
        prompt.append("请以友好、活泼的方式与用户交流，回答用户的问题。");

        return prompt.toString();
    }

    private String sendApiRequest(String baseUrl, String apiKey, Map<String, Object> requestData) throws Exception {
        // 构建完整的 API 端点 URL
        String apiUrl = baseUrl;
        if (!apiUrl.endsWith("/chat/completions")) {
            apiUrl = apiUrl + (apiUrl.endsWith("/") ? "" : "/") + "chat/completions";
        }

        System.out.println("API 端点 URL: " + apiUrl);

        URL url = new URL(apiUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Authorization", "Bearer " + apiKey);
        connection.setDoOutput(true);
        connection.setConnectTimeout(30000); // 30秒连接超时
        connection.setReadTimeout(30000); // 30秒读取超时

        // 写入请求体
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = objectMapper.writeValueAsString(requestData).getBytes(StandardCharsets.UTF_8);
            System.out.println("请求体大小: " + input.length + " 字节");
            System.out.println("请求体内容: " + objectMapper.writeValueAsString(requestData));
            os.write(input, 0, input.length);
        }

        // 获取响应状态码
        int responseCode = connection.getResponseCode();
        System.out.println("API 响应状态码: " + responseCode + " " + connection.getResponseMessage());

        // 读取响应
        StringBuilder response = new StringBuilder();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            // 成功响应
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
            }
        } else {
            // 错误响应
            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(connection.getErrorStream(), StandardCharsets.UTF_8))) {
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
            }
            System.out.println("API 错误响应: " + response.toString());
            throw new Exception("API 请求失败，状态码: " + responseCode + "，响应: " + response.toString());
        }

        connection.disconnect();
        return response.toString();
    }

    private String parseApiResponse(String response) throws Exception {
        Map<String, Object> responseMap = objectMapper.readValue(response, Map.class);
        if (responseMap.containsKey("choices")) {
            Object choicesObj = responseMap.get("choices");
            if (choicesObj instanceof java.util.ArrayList) {
                java.util.ArrayList<?> choicesList = (java.util.ArrayList<?>) choicesObj;
                if (!choicesList.isEmpty()) {
                    Object choiceObj = choicesList.get(0);
                    if (choiceObj instanceof Map) {
                        Map<?, ?> choice = (Map<?, ?>) choiceObj;
                        Object messageObj = choice.get("message");
                        if (messageObj instanceof Map) {
                            Map<?, ?> message = (Map<?, ?>) messageObj;
                            Object contentObj = message.get("content");
                            if (contentObj instanceof String) {
                                return (String) contentObj;
                            }
                        }
                    }
                }
            }
        }
        return "无法解析API响应。";
    }
}
