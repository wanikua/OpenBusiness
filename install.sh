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

normalize_lang() {
  case "${1:-}" in
    en|EN|english|English|1) printf "en" ;;
    zh|ZH|cn|CN|chinese|Chinese|中文|2) printf "zh" ;;
    *) return 1 ;;
  esac
}

choose_language() {
  if [ -n "${OPENBUSINESS_INSTALL_LANG:-}" ]; then
    INSTALL_LANG="$(normalize_lang "$OPENBUSINESS_INSTALL_LANG")" || die "Unsupported installer language: $OPENBUSINESS_INSTALL_LANG"
    return
  fi

  printf "\n${BOLD}Select installer language / 选择安装语言${RESET}\n"
  while true; do
    read -r -p "$(printf "${BOLD}[1] English  [2] 中文  (en/zh) [zh]: ${RESET}")" reply
    reply="${reply:-zh}"
    INSTALL_LANG="$(normalize_lang "$reply" 2>/dev/null || true)"
    if [ -n "$INSTALL_LANG" ]; then
      break
    fi
    printf "${YELLOW}Please enter en or zh / 请输入 en 或 zh${RESET}\n"
  done
}

is_en() { [ "${INSTALL_LANG:-zh}" = "en" ]; }

choose_language

# ── Welcome ──────────────────────────────────────────────
if is_en; then
  banner "🚀 OpenBusiness Installer"
  echo "This script will:"
  echo "  1. Check Python version (requires 3.10+)"
  echo "  2. Create a .venv virtual environment (optional)"
  echo "  3. Install dependencies (pip install -e .)"
  echo "  4. Start the interactive config wizard for API keys"
  echo ""
else
  banner "🚀 OpenBusiness 安装器"
  echo "这个脚本会:"
  echo "  1. 检查 Python 版本 (需要 3.10+)"
  echo "  2. 创建虚拟环境 .venv (可选)"
  echo "  3. 安装依赖 (pip install -e .)"
  echo "  4. 启动交互式配置向导 (让你输入 API key)"
  echo ""
fi

# ── Step 1: Check Python ─────────────────────────────────
if is_en; then
  banner "1️⃣  Check Python"
else
  banner "1️⃣  检查 Python"
fi

PYTHON_CMD=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    version=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
    major=$("$candidate" -c 'import sys; print(sys.version_info.major)' 2>/dev/null)
    minor=$("$candidate" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
    if [ -n "$major" ] && [ -n "$minor" ] && [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
      PYTHON_CMD="$candidate"
      if is_en; then
        ok "Found Python $version ($(command -v "$candidate"))"
      else
        ok "找到 Python $version ($(command -v "$candidate"))"
      fi
      break
    fi
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  if is_en; then
    die "Python 3.10+ was not found. Install it first: https://www.python.org/downloads/"
  else
    die "未找到 Python 3.10+。请先安装: https://www.python.org/downloads/"
  fi
fi

# ── Step 2: Virtualenv (optional) ────────────────────────
if is_en; then
  banner "2️⃣  Virtual Environment"
else
  banner "2️⃣  虚拟环境"
fi

USE_VENV="y"
if [ -d ".venv" ]; then
  if is_en; then
    warn ".venv already exists; reusing it"
  else
    warn ".venv 已存在，将复用"
  fi
else
  if is_en; then
    read -r -p "$(printf "${BOLD}Create virtual environment .venv? [Y/n]:${RESET} ")" reply
  else
    read -r -p "$(printf "${BOLD}创建虚拟环境 .venv？[Y/n]:${RESET} ")" reply
  fi
  USE_VENV="${reply:-y}"
  if [[ "$USE_VENV" =~ ^[Yy]$ ]]; then
    if is_en; then
      say "Creating .venv ..."
      "$PYTHON_CMD" -m venv .venv || die "Failed to create virtual environment"
      ok ".venv created"
    else
      say "创建 .venv ..."
      "$PYTHON_CMD" -m venv .venv || die "创建虚拟环境失败"
      ok ".venv 已创建"
    fi
  else
    if is_en; then
      warn "Skipping virtual environment; installing into the current Python environment"
    else
      warn "跳过虚拟环境，将安装到当前 Python 环境"
    fi
  fi
fi

# ── Step 3: Activate & install ───────────────────────────
if is_en; then
  banner "3️⃣  Install Dependencies"
else
  banner "3️⃣  安装依赖"
fi

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  PIP_CMD="pip"
  if is_en; then
    ok "Activated .venv"
  else
    ok "已激活 .venv"
  fi
else
  PIP_CMD="$PYTHON_CMD -m pip"
fi

if is_en; then
  say "Upgrading pip / setuptools ..."
  $PIP_CMD install --quiet --upgrade pip setuptools 2>&1 | tail -3 || warn "pip/setuptools upgrade failed; continuing anyway"

  say "Installing OpenBusiness and dependencies (this may take 1-2 minutes)..."
  $PIP_CMD install -e . 2>&1 | tail -5 || die "Dependency installation failed"
  ok "Dependencies installed"
else
  say "升级 pip / setuptools ..."
  $PIP_CMD install --quiet --upgrade pip setuptools 2>&1 | tail -3 || warn "pip/setuptools 升级失败 (可能影响后续，但仍尝试继续)"

  say "安装 OpenBusiness 与依赖 (可能需要 1-2 分钟)..."
  $PIP_CMD install -e . 2>&1 | tail -5 || die "依赖安装失败"
  ok "依赖安装完成"
fi

# ── Step 4: Config wizard ────────────────────────────────
if is_en; then
  banner "4️⃣  Config Wizard"
  say "Starting the interactive config wizard. Enter your API keys..."
else
  banner "4️⃣  配置向导"
  say "启动交互式配置向导，输入你的 API key..."
fi

echo ""

if [ -d ".venv" ]; then
  .venv/bin/openbusiness config --ui-language "$INSTALL_LANG" --language "$INSTALL_LANG"
else
  openbusiness config --ui-language "$INSTALL_LANG" --language "$INSTALL_LANG"
fi

# ── Step 5: Done ─────────────────────────────────────────
if is_en; then
  banner "🎉 Installation Complete"
else
  banner "🎉 安装完成"
fi

if [ -d ".venv" ]; then
  if is_en; then
    echo "${BOLD}Usage (activate the venv whenever you open a new terminal):${RESET}"
    echo ""
    echo "  ${CYAN}source .venv/bin/activate${RESET}"
    echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
  else
    echo "${BOLD}使用方式 (每次开新终端要先激活 venv):${RESET}"
    echo ""
    echo "  ${CYAN}source .venv/bin/activate${RESET}"
    echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
  fi
else
  if is_en; then
    echo "${BOLD}Usage:${RESET}"
    echo ""
    echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
  else
    echo "${BOLD}使用方式:${RESET}"
    echo ""
    echo "  ${CYAN}openbusiness analyze \"Notion\" --domain notion.so${RESET}"
  fi
fi

echo ""
if is_en; then
  echo "Show current config: ${CYAN}openbusiness show${RESET}"
  echo "Reconfigure:         ${CYAN}openbusiness config --reset${RESET}"
else
  echo "查看现有配置:    ${CYAN}openbusiness show${RESET}"
  echo "重新配置:        ${CYAN}openbusiness config --reset${RESET}"
fi
echo ""
