package com.hives.vtuber

/**
 * HIVE's VTuber - 外部服务配置
 *
 * 应用内加载的 Web 站点地址，集中在此处便于统一替换。
 * 默认值指向原 MatesX 平台托管的站点，可改为你自己的地址（例如局域网内的 http://<host>:8000）。
 */
object Services {
    const val WEB_BASE = "https://www.matesx.com"
}
