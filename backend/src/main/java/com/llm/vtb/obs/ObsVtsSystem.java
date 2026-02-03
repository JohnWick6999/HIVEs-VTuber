package com.llm.vtb.obs;

import com.llm.vtb.config.ConfigManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.net.URI;
import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class ObsVtsSystem {

    @Autowired
    private ConfigManager configManager;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private WebSocketClient obsWebSocketClient;
    private WebSocketClient vtsWebSocketClient;
    private boolean isObsConnected = false;
    private boolean isVtsConnected = false;

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

            // 创建并连接WebSocket客户端
            obsWebSocketClient = new SimpleWebSocketClient(new URI(wsUrl)) {
                @Override
                public void onOpen() {
                    super.onOpen();
                    isObsConnected = true;
                    System.out.println("OBS WebSocket连接成功");
                }

                @Override
                public void onMessage(String message) {
                    super.onMessage(message);
                    System.out.println("收到OBS消息: " + message);
                }

                @Override
                public void onClose(int statusCode, String reason) {
                    super.onClose(statusCode, reason);
                    isObsConnected = false;
                    System.out.println("OBS WebSocket连接关闭: " + reason);
                }

                @Override
                public void onError(Throwable throwable) {
                    super.onError(throwable);
                    isObsConnected = false;
                    System.out.println("OBS WebSocket错误: " + throwable.getMessage());
                }
            };

            obsWebSocketClient.connect();

            // 简单的认证逻辑
            if (!password.isEmpty()) {
                sendObsAuthRequest(password);
            }

            return true;
        } catch (Exception e) {
            e.printStackTrace();
            isObsConnected = false;
            return false;
        }
    }

    public void disconnectFromObs() {
        if (obsWebSocketClient != null && isObsConnected) {
            try {
                obsWebSocketClient.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
            isObsConnected = false;
        }
    }

    public boolean startObsRecording() {
        if (!isObsConnected) {
            return false;
        }
        return sendObsRequest("StartRecord");
    }

    public boolean stopObsRecording() {
        if (!isObsConnected) {
            return false;
        }
        return sendObsRequest("StopRecord");
    }

    public boolean startObsStreaming() {
        if (!isObsConnected) {
            return false;
        }
        return sendObsRequest("StartStream");
    }

    public boolean stopObsStreaming() {
        if (!isObsConnected) {
            return false;
        }
        return sendObsRequest("StopStream");
    }

    public boolean setObsScene(String sceneName) {
        if (!isObsConnected) {
            return false;
        }
        Map<String, Object> data = new HashMap<>();
        data.put("sceneName", sceneName);
        return sendObsRequest("SetCurrentScene", data);
    }

    // VTuberStudio相关方法
    public boolean connectToVts() {
        try {
            ConfigManager.Config config = configManager.getConfig();
            ConfigManager.VtsConfig vtsConfig = config.getVtuber_studio();

            String host = vtsConfig.getHost();
            int port = vtsConfig.getPort();

            // 构建WebSocket连接URL
            String wsUrl = "ws://" + host + ":" + port;

            // 创建并连接WebSocket客户端
            vtsWebSocketClient = new SimpleWebSocketClient(new URI(wsUrl)) {
                @Override
                public void onOpen() {
                    super.onOpen();
                    isVtsConnected = true;
                    System.out.println("VTuberStudio WebSocket连接成功");
                }

                @Override
                public void onMessage(String message) {
                    super.onMessage(message);
                    System.out.println("收到VTuberStudio消息: " + message);
                }

                @Override
                public void onClose(int statusCode, String reason) {
                    super.onClose(statusCode, reason);
                    isVtsConnected = false;
                    System.out.println("VTuberStudio WebSocket连接关闭: " + reason);
                }

                @Override
                public void onError(Throwable throwable) {
                    super.onError(throwable);
                    isVtsConnected = false;
                    System.out.println("VTuberStudio WebSocket错误: " + throwable.getMessage());
                }
            };

            vtsWebSocketClient.connect();
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            isVtsConnected = false;
            return false;
        }
    }

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
    private void sendObsAuthRequest(String password) {
        try {
            Map<String, Object> data = new HashMap<>();
            data.put("auth", password);
            sendObsRequest("Authenticate", data);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private boolean sendObsRequest(String requestType) {
        return sendObsRequest(requestType, new HashMap<>());
    }

    private boolean sendObsRequest(String requestType, Map<String, Object> data) {
        try {
            if (obsWebSocketClient == null || !isObsConnected) {
                return false;
            }

            Map<String, Object> request = new HashMap<>();
            request.put("requestType", requestType);
            request.put("requestId", "" + System.currentTimeMillis());
            request.put("requestData", data);

            obsWebSocketClient.send(objectMapper.writeValueAsString(request));
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    private boolean sendVtsRequest(String requestType, Map<String, Object> data) {
        try {
            if (vtsWebSocketClient == null || !isVtsConnected) {
                return false;
            }

            Map<String, Object> request = new HashMap<>();
            request.put("requestType", requestType);
            request.put("data", data);

            vtsWebSocketClient.send(objectMapper.writeValueAsString(request));
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    // 简单的WebSocketClient接口
    private interface WebSocketClient {
        void connect() throws Exception;

        void send(String message) throws Exception;

        void close() throws Exception;

        void onOpen();

        void onMessage(String message);

        void onClose(int statusCode, String reason);

        void onError(Throwable throwable);
    }

    // 简单的WebSocketClient实现
    private class SimpleWebSocketClient implements WebSocketClient {
        private final URI uri;

        public SimpleWebSocketClient(URI uri) {
            this.uri = uri;
        }

        @Override
        public void connect() throws Exception {
            // 这里应该实现真正的WebSocket连接逻辑
            // 由于简化实现，这里只是模拟连接成功
            System.out.println("连接到WebSocket: " + uri);
            onOpen();
        }

        @Override
        public void send(String message) throws Exception {
            // 这里应该实现真正的消息发送逻辑
            System.out.println("发送WebSocket消息: " + message);
        }

        @Override
        public void close() throws Exception {
            // 这里应该实现真正的连接关闭逻辑
            System.out.println("关闭WebSocket连接: " + uri);
            onClose(1000, "Normal closure");
        }

        @Override
        public void onOpen() {
        }

        @Override
        public void onMessage(String message) {
        }

        @Override
        public void onClose(int statusCode, String reason) {
        }

        @Override
        public void onError(Throwable throwable) {
        }
    }
}
