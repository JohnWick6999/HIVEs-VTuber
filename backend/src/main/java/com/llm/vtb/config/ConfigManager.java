package com.llm.vtb.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Component
public class ConfigManager {

    private static final String CONFIG_FILE_PATH = "data/config.json"; // 使用相对于backend目录的路径
    private Config config;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public ConfigManager() {
        loadConfig();
    }

    public void loadConfig() {
        try {
            File configFile = new File(CONFIG_FILE_PATH);
            System.out.println("配置文件路径: " + CONFIG_FILE_PATH);
            System.out.println("配置文件绝对路径: " + configFile.getAbsolutePath());
            System.out.println("配置文件是否存在: " + configFile.exists());

            if (configFile.exists()) {
                System.out.println("配置文件存在，开始读取...");
                config = objectMapper.readValue(configFile, Config.class);
                System.out.println("配置文件读取成功！");
                // 打印部分配置信息进行验证
                System.out.println("- 聊天API Key: " + (config.getChat_api().getApi_key().isEmpty() ? "空"
                        : config.getChat_api().getApi_key().substring(0, 5) + "..."));
                System.out.println("- 语音API Key: " + (config.getVoice_api().getTts().getApi_key().isEmpty() ? "空"
                        : config.getVoice_api().getTts().getApi_key().substring(0, 5) + "..."));
                System.out.println("- 语音API Base URL: " + (config.getVoice_api().getTts().getBase_url().isEmpty() ? "空"
                        : config.getVoice_api().getTts().getBase_url()));
                System.out.println("- 语音API Voice: " + (config.getVoice_api().getTts().getVoice().isEmpty() ? "空"
                        : config.getVoice_api().getTts().getVoice()));
            } else {
                System.out.println("配置文件不存在，创建默认配置...");
                config = createDefaultConfig();
                saveConfig();
                System.out.println("默认配置创建并保存成功！");
            }
        } catch (IOException e) {
            System.out.println("配置文件读取失败: " + e.getMessage());
            e.printStackTrace();
            config = createDefaultConfig();
            System.out.println("使用默认配置！");
        }
    }

    public void saveConfig() {
        try {
            File configFile = new File(CONFIG_FILE_PATH);
            File parentDir = configFile.getParentFile();
            if (!parentDir.exists()) {
                parentDir.mkdirs();
            }
            objectMapper.writeValue(configFile, config);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private Config createDefaultConfig() {
        Config defaultConfig = new Config();
        defaultConfig.setChat_api(new ChatApiConfig());
        defaultConfig.setVoice_api(new VoiceApiConfig());
        defaultConfig.setImage_api(new ImageApiConfig());
        defaultConfig.setSearch_api(new SearchApiConfig());
        defaultConfig.setDatabase(new DatabaseConfig());
        defaultConfig.setObs(new ObsConfig());
        defaultConfig.setVtuber_studio(new VtsConfig());
        defaultConfig.setPersonality(new PersonalityConfig());
        return defaultConfig;
    }

    public Config getConfig() {
        return config;
    }

    public void setConfig(Config config) {
        this.config = config;
    }

    public static class Config {
        private ChatApiConfig chat_api;
        private VoiceApiConfig voice_api;
        private ImageApiConfig image_api;
        private SearchApiConfig search_api;
        private DatabaseConfig database;
        private ObsConfig obs;
        private VtsConfig vtuber_studio;
        private PersonalityConfig personality;

        public ChatApiConfig getChat_api() {
            return chat_api;
        }

        public void setChat_api(ChatApiConfig chat_api) {
            this.chat_api = chat_api;
        }

        public VoiceApiConfig getVoice_api() {
            return voice_api;
        }

        public void setVoice_api(VoiceApiConfig voice_api) {
            this.voice_api = voice_api;
        }

        public ImageApiConfig getImage_api() {
            return image_api;
        }

        public void setImage_api(ImageApiConfig image_api) {
            this.image_api = image_api;
        }

        public SearchApiConfig getSearch_api() {
            return search_api;
        }

        public void setSearch_api(SearchApiConfig search_api) {
            this.search_api = search_api;
        }

        public DatabaseConfig getDatabase() {
            return database;
        }

        public void setDatabase(DatabaseConfig database) {
            this.database = database;
        }

        public ObsConfig getObs() {
            return obs;
        }

        public void setObs(ObsConfig obs) {
            this.obs = obs;
        }

        public VtsConfig getVtuber_studio() {
            return vtuber_studio;
        }

        public void setVtuber_studio(VtsConfig vtuber_studio) {
            this.vtuber_studio = vtuber_studio;
        }

        public PersonalityConfig getPersonality() {
            return personality;
        }

        public void setPersonality(PersonalityConfig personality) {
            this.personality = personality;
        }
    }

    public static class ChatApiConfig {
        private String api_key = "";
        private String base_url = "";
        private String model = "";
        private double temperature = 0.7;
        private int max_tokens = 1024;

        public String getApi_key() {
            return api_key;
        }

        public void setApi_key(String api_key) {
            this.api_key = api_key;
        }

        public String getBase_url() {
            return base_url;
        }

        public void setBase_url(String base_url) {
            this.base_url = base_url;
        }

        public String getModel() {
            return model;
        }

        public void setModel(String model) {
            this.model = model;
        }

        public double getTemperature() {
            return temperature;
        }

        public void setTemperature(double temperature) {
            this.temperature = temperature;
        }

        public int getMax_tokens() {
            return max_tokens;
        }

        public void setMax_tokens(int max_tokens) {
            this.max_tokens = max_tokens;
        }
    }

    public static class VoiceApiConfig {
        private TtsConfig tts = new TtsConfig();
        private AsrConfig asr = new AsrConfig();

        public static class TtsConfig {
            private String api_key = "";
            private String base_url = "";
            private String voice = "";
            private String engine = "qwen";

            public String getApi_key() {
                return api_key;
            }

            public void setApi_key(String api_key) {
                this.api_key = api_key;
            }

            public String getBase_url() {
                return base_url;
            }

            public void setBase_url(String base_url) {
                this.base_url = base_url;
            }

            public String getVoice() {
                return voice;
            }

            public void setVoice(String voice) {
                this.voice = voice;
            }

            public String getEngine() {
                return engine;
            }

            public void setEngine(String engine) {
                this.engine = engine;
            }
        }

        public static class AsrConfig {
            private String api_key = "";
            private String base_url = "";

            public String getApi_key() {
                return api_key;
            }

            public void setApi_key(String api_key) {
                this.api_key = api_key;
            }

            public String getBase_url() {
                return base_url;
            }

            public void setBase_url(String base_url) {
                this.base_url = base_url;
            }
        }

        public TtsConfig getTts() {
            return tts;
        }

        public void setTts(TtsConfig tts) {
            this.tts = tts;
        }

        public AsrConfig getAsr() {
            return asr;
        }

        public void setAsr(AsrConfig asr) {
            this.asr = asr;
        }
    }

    public static class ImageApiConfig {
        private String api_key = "";
        private String base_url = "";

        public String getApi_key() {
            return api_key;
        }

        public void setApi_key(String api_key) {
            this.api_key = api_key;
        }

        public String getBase_url() {
            return base_url;
        }

        public void setBase_url(String base_url) {
            this.base_url = base_url;
        }
    }

    public static class SearchApiConfig {
        private String api_key = "";
        private String base_url = "";
        private String model = "";

        public String getApi_key() {
            return api_key;
        }

        public void setApi_key(String api_key) {
            this.api_key = api_key;
        }

        public String getBase_url() {
            return base_url;
        }

        public void setBase_url(String base_url) {
            this.base_url = base_url;
        }

        public String getModel() {
            return model;
        }

        public void setModel(String model) {
            this.model = model;
        }
    }

    public static class DatabaseConfig {
        private boolean enabled = false;
        private String db_path = "";

        public boolean isEnabled() {
            return enabled;
        }

        public void setEnabled(boolean enabled) {
            this.enabled = enabled;
        }

        public String getDb_path() {
            return db_path;
        }

        public void setDb_path(String db_path) {
            this.db_path = db_path;
        }
    }

    public static class ObsConfig {
        private boolean enabled = false;
        private String host = "localhost";
        private int port = 4444;
        private String password = "";

        public boolean isEnabled() {
            return enabled;
        }

        public void setEnabled(boolean enabled) {
            this.enabled = enabled;
        }

        public String getHost() {
            return host;
        }

        public void setHost(String host) {
            this.host = host;
        }

        public int getPort() {
            return port;
        }

        public void setPort(int port) {
            this.port = port;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }
    }

    public static class VtsConfig {
        private boolean enabled = false;
        private String host = "localhost";
        private int port = 8001;

        public boolean isEnabled() {
            return enabled;
        }

        public void setEnabled(boolean enabled) {
            this.enabled = enabled;
        }

        public String getHost() {
            return host;
        }

        public void setHost(String host) {
            this.host = host;
        }

        public int getPort() {
            return port;
        }

        public void setPort(int port) {
            this.port = port;
        }
    }

    public static class PersonalityConfig {
        private String name = "";
        private String description = "";
        private String greeting = "";
        private String tone = "";

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }

        public String getGreeting() {
            return greeting;
        }

        public void setGreeting(String greeting) {
            this.greeting = greeting;
        }

        public String getTone() {
            return tone;
        }

        public void setTone(String tone) {
            this.tone = tone;
        }
    }
}
