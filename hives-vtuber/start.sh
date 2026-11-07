#!/usr/bin/env bash
# HIVE's VTuber 一键启动脚本
# 首次运行会自动创建虚拟环境并安装依赖，之后直接启动服务。
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    echo "首次运行：创建虚拟环境并安装依赖..."
    python3 -m venv .venv
    ./.venv/bin/pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
fi

echo "启动 HIVE's VTuber： http://localhost:8000/"
exec ./.venv/bin/python main.py
