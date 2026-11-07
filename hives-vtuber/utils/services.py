"""HIVE's VTuber - 外部服务配置

说明：
    本项目只包含客户端与轻量应用层实现，数字人形象生成、语音合成等能力
    依赖外部云服务。下面列出的地址是上游公网服务（原 MatesX 平台托管），
    集中放在这里方便统一替换。

    如需接入自己的服务，直接修改默认值，或设置同名环境变量：
        HIVES_VTUBER_PLATFORM_BASE   形象生成平台地址
        HIVES_VTUBER_ASSET_BASE      语音/背景等公共素材地址
        HIVES_VTUBER_WEB_BASE        Web 站点地址
        HIVES_VTUBER_KEY             形象生成平台密钥
"""

import os

# 形象生成平台（上传视频创建数字人 / 查询任务状态）
AVATAR_PLATFORM_BASE = os.getenv("HIVES_VTUBER_PLATFORM_BASE", "https://www.matesx.cn")

# 语音、背景等公共素材的云存储地址
ASSET_BASE = os.getenv("HIVES_VTUBER_ASSET_BASE", "https://matesx.oss-cn-beijing.aliyuncs.com")

# Web 站点地址（桌面端、小程序内嵌页面使用）
WEB_BASE = os.getenv("HIVES_VTUBER_WEB_BASE", "https://www.matesx.com")

# 形象生成平台密钥，请通过环境变量提供你自己的密钥：
#   export HIVES_VTUBER_KEY="your-own-key"
AVATAR_PLATFORM_KEY = os.getenv("HIVES_VTUBER_KEY", "")
