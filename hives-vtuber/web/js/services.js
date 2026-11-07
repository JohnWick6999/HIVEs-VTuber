// HIVE's VTuber - 外部服务配置
// 说明：数字人形象生成、语音素材等能力依赖外部云服务，地址集中在此处便于统一替换。
// 如需接入自己的服务，修改下面的默认值即可（或参考 utils/services.py 的环境变量）。
window.HIVES_SERVICES = {
    // 公共素材云存储（默认背景等）
    assetBase: "https://matesx.oss-cn-beijing.aliyuncs.com",
    // 语音试听素材目录
    voiceSampleBase: "https://matesx.oss-cn-beijing.aliyuncs.com/audio/public",
    // Web 站点地址
    webBase: "https://www.matesx.com"
};
