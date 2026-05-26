#!/usr/bin/env bash
# OpenBusiness installer — checks Python, sets up venv, installs deps, runs config wizard.
set -e

# ── Colors ───────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

say()    { printf "${CYAN}▸${RESET} %s\n" "$1"; }
ok()     { printf "${GREEN}✓${RESET} %s\n" "$1"; }
warn()   { printf "${YELLOW}⚠${RESET} %s\n" "$1"; }
die()    { printf "${RED}✗ %s${RESET}\n" "$1" >&2; exit 1; }
banner() {
  printf "\n${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n"
  printf "${BOLD}${CYAN}  %s${RESET}\n" "$1"
  printf "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}\n\n"
}

# ── Welcome ──────────────────────────────────────────────
banner "🚀 OpenBusiness Installer"
echo "这个脚本会:"
echo "  1. 检查 Python 版本 (需要 3.10+)"
echo "  2. 创建虚拟环境 .venv (可选)"
echo "  3. 安装依赖 (pip install -e .)"
echo "  4. 启动交互式配置向导 (让你输入 API key)"
echo ""

# ── Step 1: Check Python ─────────────────────────────────
banner "1️⃣  检查 Python"

PYTHON_CMD=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    version=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
    major=$("$candidate" -c 'import sys; print(sys.version_info.major)' 2>/dev/null)
    minor=$("$candidate" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
    if [ -n "$major" ] && [ -n "$minor" ] && [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
      PYTHON_CMD="$candidate"
      ok "找到 Python $version ($(command -v $candidate))"
      break
    fi
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  die "未找到 Python 3.10+。请先安装: https://www.python.org/downloads/"
fi

# ── Step 2: Virtualenv (optional) ────────────────────────
banner "2️⃣  虚拟环境"

USE_VENV="y"
if [ -d ".venv" ]; then
  warn ".venv 已存在，将复用"
else
  read -r -p "$(printf "${BOLD}创建虚拟环境 .venv？[Y/n]:${RESET} ")" reply
  USE_VENV="${reply:-y}"
  if [[ "$USE_VENV" =~ ^[Yy]$ ]]; then
    say "创建 .venv ..."
    "$PYTHON_CMD" -m venv .venv || die "创建虚拟环境失败"
    ok ".venv 已创建"
  else
    warn "跳过虚拟环境，将安装到当前 Python 环境"
  fi
fi

# ── Step 3: Activate & install ───────────────────────────
banner "3️⃣  安装依赖"

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  PIP_CMD="pip"
  ok "已激活 .venv"
else
  PIP_CMD="$PYTHON_CMD -m pip"
fi

say "升级 pip / setuptools ..."
$PIP_CMD install --quiet --upgrade pip setuptools 2>&1 | tail -3 || warn "pip/setuptools 升级失败 (可能影响后续，但仍尝试继续)"

say "安装 OpenBusiness 与依赖 (可能需要 1-2 分钟)..."
$PIP_CMD install -e . 2>&1 | tail -5 || die "依赖安装失败"
ok "依赖安装完成"

# ── Step 4: Config wizard ────────────────────────────────
banner "4️⃣  配置向导"

say "启动交互式配置向导，输入你的 API key..."
echo ""

if [ -d ".venv" ]; then
  .venv/bin/openbusiness config
else
  openbusiness config
fi

# ── Step 5: Done ─────────────────────────────────────────
banner "🎉 安装完成"

if [ -d ".venv" ]; then
  echo "${BOLD}使用方式 (每次开新终端要先激活 venv):${RESET}"
  echo ""
  echo "  ${CYAN}source .venv/bin/activate${RESET}"
  echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
else
  echo "${BOLD}使用方式:${RESET}"
  echo ""
  echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
fi

echo ""
echo "查看现有配置:    ${CYAN}openbusiness show${RESET}"
echo "重新配置:        ${CYAN}openbusiness config --reset${RESET}"
echo ""
