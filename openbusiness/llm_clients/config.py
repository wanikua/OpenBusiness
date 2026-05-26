"""Config file management for OpenBusiness CLI.

Storage: ~/.config/openbusiness/config.toml (mode 0600).
Env vars override file values: OPENBUSINESS_PROVIDER, OPENAI_API_KEY,
ANTHROPIC_API_KEY, TAVILY_API_KEY, FIRECRAWL_API_KEY.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Optional

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # type: ignore


CONFIG_DIR = Path(os.environ.get("OPENBUSINESS_CONFIG_DIR", Path.home() / ".config" / "openbusiness"))
CONFIG_FILE = CONFIG_DIR / "config.toml"


def load_config() -> dict:
    """Load config from file (if exists). Env vars take precedence at access time."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def save_config(cfg: dict) -> None:
    """Write config TOML with 0600 perms."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _serialize(value):
        if isinstance(value, str):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        raise TypeError(f"Unsupported config value type: {type(value)}")

    lines = []
    for k, v in cfg.items():
        if isinstance(v, dict):
            lines.append(f"\n[{k}]")
            for sub_k, sub_v in v.items():
                lines.append(f"{sub_k} = {_serialize(sub_v)}")
        else:
            lines.append(f"{k} = {_serialize(v)}")

    CONFIG_FILE.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)


def get(key: str, default: Optional[str] = None) -> Optional[str]:
    """Resolve a config value: env var → config file → default.

    Mapping:
        provider           → OPENBUSINESS_PROVIDER
        openai_api_key     → OPENAI_API_KEY
        anthropic_api_key  → ANTHROPIC_API_KEY
        tavily_api_key     → TAVILY_API_KEY
        firecrawl_api_key  → FIRECRAWL_API_KEY
    """
    env_map = {
        "provider": "OPENBUSINESS_PROVIDER",
        "openai_api_key": "OPENAI_API_KEY",
        "anthropic_api_key": "ANTHROPIC_API_KEY",
        "tavily_api_key": "TAVILY_API_KEY",
        "firecrawl_api_key": "FIRECRAWL_API_KEY",
    }
    env_var = env_map.get(key)
    if env_var:
        env_val = os.environ.get(env_var)
        if env_val:
            return env_val

    cfg = load_config()
    if key in cfg:
        return cfg[key]
    if "llm" in cfg and key in cfg["llm"]:
        return cfg["llm"][key]
    return default


def is_configured() -> bool:
    """True if at least an LLM provider + matching key is available."""
    provider = get("provider")
    if not provider:
        return False
    if provider == "openai":
        return bool(get("openai_api_key"))
    if provider == "anthropic":
        return bool(get("anthropic_api_key"))
    return False


def export_to_env() -> None:
    """Push resolved config values into os.environ so downstream libs find them."""
    for key, env_var in [
        ("openai_api_key", "OPENAI_API_KEY"),
        ("anthropic_api_key", "ANTHROPIC_API_KEY"),
        ("tavily_api_key", "TAVILY_API_KEY"),
        ("firecrawl_api_key", "FIRECRAWL_API_KEY"),
    ]:
        val = get(key)
        if val and not os.environ.get(env_var):
            os.environ[env_var] = val
