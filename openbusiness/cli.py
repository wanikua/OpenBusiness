"""OpenBusiness CLI — interactive first-run wizard + analysis runner."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from openbusiness.language import (
    SUPPORTED_OUTPUT_LANGUAGES,
    normalize_output_language,
    output_language_name,
    report_language_warnings,
    ui_text,
)
from openbusiness.llm_clients import config

console = Console()
LLM_PROVIDERS = ("openai", "anthropic", "deepseek")
ANALYSIS_DEPTHS = ("standard", "deep")

CONFIG_UI_TEXT = {
    "en": {
        "current_config": "Current Config",
        "item": "Item",
        "status": "Status",
        "not_set": "[red]not set[/]",
        "configured": "✅ configured",
        "setup_body": (
            "[bold cyan]OpenBusiness Config Wizard[/]\n\n"
            "Config file: [yellow]~/.config/openbusiness/config.toml[/] (0600 permissions)\n"
            "Environment variables always take priority "
            "(OPENBUSINESS_OUTPUT_LANGUAGE / OPENAI_API_KEY / ANTHROPIC_API_KEY / "
            "DEEPSEEK_API_KEY / TAVILY_API_KEY / FIRECRAWL_API_KEY)\n"
        ),
        "reconfigure": "\nReconfigure?",
        "keep_config": "[dim]Keeping existing config unchanged.[/]",
        "choose_provider": "[bold]Choose LLM provider[/]",
        "report_language": "[bold]Report output language[/]",
        "ui_language": "[bold]Interface language / 选择界面语言[/]",
        "api_key_required": "[red]API key is required. Exiting.[/]",
        "evidence_tools_title": "\n[bold]Evidence collection tools (optional — press Enter to skip)[/]",
        "evidence_tools_note": (
            "[dim]Without these keys the pipeline still runs, but more analysis "
            "will rely on model knowledge and be labeled [INFERRED].[/]\n"
        ),
        "tavily_prompt": "Tavily API Key (web search, https://tavily.com): ",
        "firecrawl_prompt": "Firecrawl API Key (page scraping, https://firecrawl.dev): ",
        "saved": "\n[green]✅ Config saved to[/] [yellow]{path}[/]",
        "next_steps": (
            "[bold]Next step: analyze a company[/]\n\n"
            "  [cyan]openbusiness analyze \"Notion\" --domain notion.so[/]\n"
            "  [cyan]openbusiness analyze \"Costco\" --ticker COST[/]\n"
            "  [cyan]openbusiness analyze \"Vercel\" --domain vercel.com[/]\n\n"
            "[dim]Reports are written to ./output/<company>_business_model.md[/]"
        ),
        "default_language_set": "[green]✅ Default report output language set to[/] ",
        "no_config": "[yellow]No config found. Run: [bold]openbusiness config[/][/]",
        "missing_config": "[yellow]⚠️ No config found. Run first: [bold]openbusiness config[/][/]",
        "run_wizard_now": "Run the wizard now?",
        "incomplete_config": "[red]Config is still incomplete. Run: [bold]openbusiness config --reset[/][/]",
    },
    "zh": {
        "current_config": "当前配置",
        "item": "项目",
        "status": "状态",
        "not_set": "[red]未设置[/]",
        "configured": "✅ 已配置",
        "setup_body": (
            "[bold cyan]OpenBusiness 配置向导[/]\n\n"
            "配置文件保存路径: [yellow]~/.config/openbusiness/config.toml[/] (权限 0600)\n"
            "环境变量始终优先生效 "
            "(OPENBUSINESS_OUTPUT_LANGUAGE / OPENAI_API_KEY / ANTHROPIC_API_KEY / "
            "DEEPSEEK_API_KEY / TAVILY_API_KEY / FIRECRAWL_API_KEY)\n"
        ),
        "reconfigure": "\n要重新配置吗?",
        "keep_config": "[dim]保持现有配置不变。[/]",
        "choose_provider": "[bold]选择 LLM 提供方[/]",
        "report_language": "[bold]报告输出语言[/]",
        "ui_language": "[bold]Interface language / 选择界面语言[/]",
        "api_key_required": "[red]API key 必填。退出。[/]",
        "evidence_tools_title": "\n[bold]证据采集工具 (可选 — 直接回车跳过)[/]",
        "evidence_tools_note": (
            "[dim]没有这些 key 不影响运行，但分析会更多依赖 LLM 已有知识 (标 [INFERRED])。[/]\n"
        ),
        "tavily_prompt": "Tavily API Key (Web 搜索, https://tavily.com): ",
        "firecrawl_prompt": "Firecrawl API Key (页面抓取, https://firecrawl.dev): ",
        "saved": "\n[green]✅ 配置已保存到[/] [yellow]{path}[/]",
        "next_steps": (
            "[bold]下一步：分析一家公司[/]\n\n"
            "  [cyan]openbusiness analyze \"Notion\" --domain notion.so[/]\n"
            "  [cyan]openbusiness analyze \"Costco\" --ticker COST[/]\n"
            "  [cyan]openbusiness analyze \"Vercel\" --domain vercel.com[/]\n\n"
            "[dim]报告会输出到 ./output/<company>_business_model.md[/]"
        ),
        "default_language_set": "[green]✅ 默认报告输出语言已设置为[/] ",
        "no_config": "[yellow]未找到配置。运行: [bold]openbusiness config[/][/]",
        "missing_config": "[yellow]⚠️ 未找到配置。请先运行: [bold]openbusiness config[/][/]",
        "run_wizard_now": "现在运行向导吗?",
        "incomplete_config": "[red]配置仍不完整。请运行: [bold]openbusiness config --reset[/][/]",
    },
}


def _config_text(language: str, key: str) -> str:
    return CONFIG_UI_TEXT[normalize_output_language(language)][key]


def _show_current_config(ui_language: str = "zh") -> bool:
    """Show what's already configured. Returns True if anything is configured."""
    if not config.CONFIG_FILE.exists():
        return False

    cfg = config.load_config()
    if not cfg:
        return False

    table = Table(title=_config_text(ui_language, "current_config"), border_style="cyan", show_header=True)
    table.add_column(_config_text(ui_language, "item"), style="bold")
    table.add_column(_config_text(ui_language, "status"))

    provider = cfg.get("provider", "")
    configured = _config_text(ui_language, "configured")
    table.add_row("LLM Provider", provider or _config_text(ui_language, "not_set"))
    table.add_row("OpenAI Key", configured if cfg.get("openai_api_key") else "—")
    table.add_row("Anthropic Key", configured if cfg.get("anthropic_api_key") else "—")
    table.add_row("Tavily Key", configured if cfg.get("tavily_api_key") else "—")
    table.add_row("Firecrawl Key", configured if cfg.get("firecrawl_api_key") else "—")
    table.add_row("Output Language", output_language_name(config.get_output_language()))
    console.print(table)
    return True


def run_wizard(
    reset: bool = False,
    output_language: str | None = None,
    ui_language: str | None = None,
) -> None:
    """Interactive first-run config wizard."""
    ui_language = normalize_output_language(ui_language or output_language or config.get_output_language())
    console.print(
        Panel.fit(
            _config_text(ui_language, "setup_body"),
            title="🛠️ Setup",
            border_style="cyan",
        )
    )

    has_config = _show_current_config(ui_language)
    if has_config and not reset:
        if not Confirm.ask(_config_text(ui_language, "reconfigure"), default=False):
            console.print(_config_text(ui_language, "keep_config"))
            _print_next_steps(ui_language)
            return

    console.print()
    provider = Prompt.ask(
        _config_text(ui_language, "choose_provider"),
        choices=list(LLM_PROVIDERS),
        default="openai",
    )
    language = Prompt.ask(
        _config_text(ui_language, "report_language"),
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        default=normalize_output_language(output_language or config.get_output_language()),
    )

    if provider == "openai":
        key = getpass.getpass("OpenAI API Key (sk-...): ").strip()
    elif provider == "anthropic":
        key = getpass.getpass("Anthropic API Key (sk-ant-...): ").strip()
    else:
        key = getpass.getpass("DeepSeek API Key: ").strip()

    if not key:
        console.print(_config_text(ui_language, "api_key_required"))
        sys.exit(1)

    console.print(_config_text(ui_language, "evidence_tools_title"))
    console.print(_config_text(ui_language, "evidence_tools_note"))

    tavily_key = getpass.getpass(_config_text(ui_language, "tavily_prompt")).strip()
    firecrawl_key = getpass.getpass(_config_text(ui_language, "firecrawl_prompt")).strip()

    flat = {"provider": provider, "output_language": language}
    if provider == "openai":
        flat["openai_api_key"] = key
    elif provider == "anthropic":
        flat["anthropic_api_key"] = key
    else:
        flat["deepseek_api_key"] = key
    if tavily_key:
        flat["tavily_api_key"] = tavily_key
    if firecrawl_key:
        flat["firecrawl_api_key"] = firecrawl_key

    config.save_config(flat)

    console.print(_config_text(ui_language, "saved").format(path=config.CONFIG_FILE))
    _print_next_steps(ui_language)


def _print_next_steps(ui_language: str = "zh") -> None:
    console.print(
        Panel(
            _config_text(ui_language, "next_steps"),
            title="🚀 Ready",
            border_style="green",
        )
    )


def _choose_analysis_languages(
    output_language: str | None,
    ui_language: str | None,
) -> tuple[str, str]:
    """Choose terminal UI language and report output language separately."""
    if ui_language is None:
        default_ui_language = normalize_output_language(config.get_output_language())
        ui_language = Prompt.ask(
            _config_text(default_ui_language, "ui_language"),
            choices=list(SUPPORTED_OUTPUT_LANGUAGES),
            default=default_ui_language,
        )
    ui_language = normalize_output_language(ui_language)

    if output_language is None:
        output_language = Prompt.ask(
            _config_text(ui_language, "report_language"),
            choices=list(SUPPORTED_OUTPUT_LANGUAGES),
            default=normalize_output_language(config.get_output_language()),
        )
    output_language = normalize_output_language(output_language)

    return output_language, ui_language


def run_analysis(
    company: str,
    domain: str,
    ticker: str,
    output_dir: str,
    output_language: str | None = None,
    analysis_depth: str = "standard",
    ui_language: str | None = None,
) -> None:
    """Run the pipeline against a target company."""
    from openbusiness.graph.setup import PIPELINE_STAGES, build_graph

    try:
        language, ui_language = _choose_analysis_languages(output_language, ui_language)
    except ValueError as exc:
        console.print(f"[red]{exc}[/]")
        sys.exit(2)
    if analysis_depth not in ANALYSIS_DEPTHS:
        console.print(f"[red]Unsupported analysis depth: {analysis_depth!r}[/]")
        sys.exit(2)

    console.print(
        Panel.fit(
            f"[bold cyan]OpenBusiness[/] v0.1.0\n"
            f"{ui_text(ui_language, 'target')}: [bold]{company}[/] "
            f"({domain or ui_text(ui_language, 'no_domain')})" + (f" [{ticker}]" if ticker else "")
            + f"\n{ui_text(ui_language, 'output_language')}: [bold]{output_language_name(language)}[/]"
            + f"\nAnalysis depth: [bold]{analysis_depth}[/]",
            title=f"🚀 {ui_text(ui_language, 'analysis_title')}",
            border_style="cyan",
        )
    )

    graph = build_graph(analysis_depth)

    initial_state = {
        "company_name": company,
        "domain": domain or f"{company.lower().replace(' ', '')}.com",
        "ticker": ticker,
        "output_language": language,
        "analysis_depth": analysis_depth,
        "evidence_pack": "",
        "jtbd_report": "",
        "value_prop_report": "",
        "gtm_report": "",
        "unit_econ_report": "",
        "moat_report": "",
        "canvas_report": "",
        "stress_test_report": "",
        "final_report": "",
        "messages": [],
    }

    stage_labels = dict(PIPELINE_STAGES)
    if ui_language == "zh":
        stage_labels = {
            "evidence_collector": "🔍 证据收集",
            "jtbd_analyst": "👥 客户与待完成任务分析",
            "value_prop_analyst": "💎 价值主张分析",
            "gtm_analyst": "🚀 市场进入分析",
            "unit_econ_analyst": "💰 单体经济分析",
            "moat_analyst": "🛡️ 护城河与竞争分析",
            "synthesizer": "🧱 商业模式合成",
            "stress_tester": "🔬 假设压力测试",
            "finalizer": "📝 报告整理",
        }

    final_state = initial_state
    with console.status(f"[cyan]{ui_text(ui_language, 'starting_pipeline')}[/]") as status:
        for event in graph.stream(initial_state, stream_mode="updates"):
            for node_name, node_output in event.items():
                label = stage_labels.get(node_name, node_name)
                status.update(f"[cyan]{label}[/]")
                if isinstance(node_output, dict):
                    final_state = {**final_state, **node_output}
                console.print(f"[green]✓[/] {label}")

    report = final_state.get("final_report", "")
    if not report:
        console.print(f"[red]❌ {ui_text(ui_language, 'pipeline_no_report')}[/]")
        sys.exit(1)

    out = Path(output_dir)
    out.mkdir(exist_ok=True)
    slug = company.lower().replace(" ", "_")
    out_path = out / f"{slug}_business_model.md"
    out_path.write_text(report, encoding="utf-8")

    warnings = report_language_warnings(report, language)
    if warnings:
        console.print(
            Panel(
                "\n".join(warnings),
                title=ui_text(ui_language, "language_warning_title"),
                border_style="yellow",
            )
        )

    console.print(f"\n[bold green]✅ {ui_text(ui_language, 'report_generated')}[/] {out_path}")
    preview = report[:800] + "\n..." if len(report) > 800 else report
    console.print(Panel(preview, title=ui_text(ui_language, "preview"), border_style="green"))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openbusiness",
        description="AI-driven business model reverse engineering",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_config = sub.add_parser("config", help="运行配置向导 (首次使用必须运行)")
    p_config.add_argument("--reset", action="store_true", help="无视现有配置重新输入")
    p_config.add_argument(
        "--language",
        "-l",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        help="设置默认报告输出语言: zh 或 en",
    )
    p_config.add_argument(
        "--ui-language",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        help="配置向导界面语言: zh 或 en",
    )

    sub.add_parser("show", help="显示当前配置 (不显示完整 key)")

    p_analyze = sub.add_parser("analyze", help="分析一家公司的商业模式")
    p_analyze.add_argument("company", help="公司名 (e.g. 'Notion')")
    p_analyze.add_argument("--domain", "-d", default="", help="官网域名 (e.g. notion.so)")
    p_analyze.add_argument("--ticker", "-t", default="", help="美股代码 (e.g. AAPL)")
    p_analyze.add_argument("--output", "-o", default="output", help="报告输出目录")
    p_analyze.add_argument(
        "--language",
        "-l",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        default=None,
        help="报告输出语言: zh 或 en (覆盖配置与环境变量)",
    )
    p_analyze.add_argument(
        "--ui-language",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        default=None,
        help="运行界面语言: zh 或 en；与报告输出语言分开",
    )
    p_analyze.add_argument(
        "--depth",
        choices=list(ANALYSIS_DEPTHS),
        default="standard",
        help="分析深度: standard 更快，deep 会增加证据采集范围和搜索深度",
    )

    args = parser.parse_args()

    if args.cmd == "config":
        if args.language and not args.reset and not args.ui_language:
            cfg = config.load_config()
            cfg["output_language"] = normalize_output_language(args.language)
            config.save_config(cfg)
            ui_language = normalize_output_language(config.get_output_language())
            console.print(
                _config_text(ui_language, "default_language_set")
                + f"[bold]{output_language_name(args.language)}[/]"
            )
            return
        run_wizard(reset=args.reset, output_language=args.language, ui_language=args.ui_language)
        return

    if args.cmd == "show":
        show_language = normalize_output_language(config.get_output_language())
        if not _show_current_config(show_language):
            console.print(_config_text(show_language, "no_config"))
        return

    if args.cmd == "analyze":
        if not config.is_configured():
            wizard_language = normalize_output_language(args.ui_language or args.language or config.get_output_language())
            console.print(_config_text(wizard_language, "missing_config"))
            if Confirm.ask(_config_text(wizard_language, "run_wizard_now"), default=True):
                run_wizard(ui_language=wizard_language)
                if not config.is_configured():
                    console.print(_config_text(wizard_language, "incomplete_config"))
                    sys.exit(1)
            else:
                sys.exit(1)
        run_analysis(
            args.company,
            args.domain,
            args.ticker,
            args.output,
            args.language,
            args.depth,
            args.ui_language,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
