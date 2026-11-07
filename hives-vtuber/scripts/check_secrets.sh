#!/usr/bin/env bash
# 密钥扫描脚本：在 commit / push / release 之前运行
#
# 用法:
#   ./scripts/check_secrets.sh            # 扫描当前工作区
#   ./scripts/check_secrets.sh --history  # 额外扫描全部 git 历史
#
# 命中任何规则都会以非 0 退出码结束。

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2

EXCLUDES=(--exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules
          --exclude-dir=__pycache__ --exclude-dir=out --exclude-dir=.gradle)

# 常见真实密钥形态（含明显假值时不会命中）
PATTERNS=(
  'sk-[A-Za-z0-9]{20,}'
  'ghp_[A-Za-z0-9]{20,}'
  'github_pat_[A-Za-z0-9_]{20,}'
  'AKIA[0-9A-Z]{16}'
  'LTAI[0-9A-Za-z]{12,}'
  '(KEY|SECRET|TOKEN|PASSWORD)[A-Za-z0-9_]{0,20}[[:space:]]*[:=][[:space:]]*["'"'"']?[0-9a-f]{32}["'"'"']?'  # 32 位十六进制串（疑似平台密钥）
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  'Authorization:[[:space:]]*Bearer[[:space:]]+[A-Za-z0-9._-]{12,}'
  'x-api-key[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9_-]{16,}'
  '(DASHSCOPE_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|DEEPSEEK_API_KEY|HIVES_VTUBER_KEY)[[:space:]]*=[[:space:]]*["'"'"'][A-Za-z0-9_-]{16,}["'"'"']'
)

status=0

scan_text() {
  local label="$1"; shift
  local hits=0
  for p in "${PATTERNS[@]}"; do
    local out
    out=$(grep -rInEi -e "$p" "${EXCLUDES[@]}" . 2>/dev/null)
    if [ -n "$out" ]; then
      echo "❌ [$label] 命中规则: $p"
      echo "$out" | head -20
      hits=$((hits + 1))
    fi
  done
  if [ "$hits" -eq 0 ]; then
    echo "✅ [$label] 未发现疑似密钥"
  else
    status=1
  fi
}

scan_text "工作区"

if [ "${1:-}" = "--history" ]; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    hist_hits=0
    for p in "${PATTERNS[@]}"; do
      out=$(git log -p --all 2>/dev/null | grep -niE -e "$p" | head -10)
      if [ -n "$out" ]; then
        echo "❌ [历史] 命中规则: $p"
        echo "$out"
        hist_hits=$((hist_hits + 1))
      fi
    done
    if [ "$hist_hits" -eq 0 ]; then
      echo "✅ [历史] 未发现疑似密钥"
    else
      status=1
    fi
  else
    echo "ℹ️  当前目录不是 git 仓库，跳过历史扫描"
  fi
fi

if [ "$status" -ne 0 ]; then
  echo
  echo "扫描未通过：请先移除真实密钥（改为环境变量/占位符），再提交或推送。"
fi

exit "$status"
