"""OpenBusiness CLI — interactive first-run wizard + analysis runner."""

from __future__ import annotations

import argparse
import getpass
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from openbusiness.analysis_run import (
    ANALYSIS_DEPTHS,
    AnalysisRunRequest,
    execute_analysis_run,
    prepare_analysis_run,
)
from openbusiness.language import (
    SUPPORTED_OUTPUT_LANGUAGES,
    normalize_output_language,
    output_language_name,
    ui_text,
)
from openbusiness.llm_clients import config
from openbusiness.profiles import list_analysis_packs, list_report_templates
from openbusiness.stages import stage_labels as build_stage_labels

console = Console()
LLM_PROVIDERS = ("openai", "anthropic", "deepseek")

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
            "(OPENBUSINESS_UI_LANGUAGE / OPENBUSINESS_OUTPUT_LANGUAGE / "
            "OPENAI_API_KEY / ANTHROPIC_API_KEY / "
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
        "default_ui_language_set": "[green]✅ Default interface language set to[/] ",
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
            "(OPENBUSINESS_UI_LANGUAGE / OPENBUSINESS_OUTPUT_LANGUAGE / "
            "OPENAI_API_KEY / ANTHROPIC_API_KEY / "
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
        "default_ui_language_set": "[green]✅ 默认界面语言已设置为[/] ",
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


CLI_HELP_TEXT = {
    "en": {
        "description": "AI-driven business model reverse engineering",
        "config_help": "Run the configuration wizard",
        "config_reset": "Ignore existing config and enter values again",
        "config_language": "Set default report output language: zh or en",
        "config_ui_language": "Set default CLI interface language: zh or en",
        "show_help": "Show current config without revealing full keys",
        "analyze_help": "Analyze one company's business model",
        "company": "Company name (e.g. 'Notion')",
        "domain": "Official company domain (e.g. notion.so)",
        "ticker": "Public-company ticker (e.g. AAPL)",
        "output": "Report output directory",
        "analyze_language": "Report output language: zh or en; overrides config and environment variables",
        "analyze_ui_language": (
            "Run interface language: zh or en; overrides the saved default interface language "
            "and remains separate from report language"
        ),
        "pack": "Analysis pack id. Run `openbusiness packs` to list built-in packs.",
        "pack_file": "Custom analysis pack TOML file.",
        "template": "Report template id. Run `openbusiness templates` to list built-in templates.",
        "template_file": "Custom report template Markdown file with TOML front matter.",
        "depth": "Research depth: standard is faster; deep broadens evidence collection and search depth",
        "packs_help": "List built-in analysis packs",
        "templates_help": "List built-in report templates",
        "id": "ID",
        "name": "Name",
        "description_column": "Description",
        "analysis_pack": "Analysis pack",
        "report_template": "Report template",
        "artifacts_written": "Run artifacts:",
    },
    "zh": {
        "description": "AI 驱动的商业模式逆向工程",
        "config_help": "运行配置向导 (首次使用必须运行)",
        "config_reset": "无视现有配置重新输入",
        "config_language": "设置默认报告输出语言: zh 或 en",
        "config_ui_language": "设置默认 CLI 界面语言: zh 或 en",
        "show_help": "显示当前配置 (不显示完整 key)",
        "analyze_help": "分析一家公司的商业模式",
        "company": "公司名 (e.g. 'Notion')",
        "domain": "官网域名 (e.g. notion.so)",
        "ticker": "美股代码 (e.g. AAPL)",
        "output": "报告输出目录",
        "analyze_language": "报告输出语言: zh 或 en (覆盖配置与环境变量)",
        "analyze_ui_language": "运行界面语言: zh 或 en；覆盖已保存的默认界面语言，与报告输出语言分开",
        "pack": "分析包 ID。运行 `openbusiness packs` 查看内置分析包。",
        "pack_file": "自定义分析包 TOML 文件。",
        "template": "报告模板 ID。运行 `openbusiness templates` 查看内置模板。",
        "template_file": "带 TOML front matter 的自定义报告模板 Markdown 文件。",
        "depth": "分析深度: standard 更快，deep 会增加证据采集范围和搜索深度",
        "packs_help": "列出内置分析包",
        "templates_help": "列出内置报告模板",
        "id": "ID",
        "name": "名称",
        "description_column": "说明",
        "analysis_pack": "分析包",
        "report_template": "报告模板",
        "artifacts_written": "运行产物：",
    },
}


def _config_text(language: str, key: str) -> str:
    return CONFIG_UI_TEXT[normalize_output_language(language)][key]


def _help_text(language: str, key: str) -> str:
    return CLI_HELP_TEXT[normalize_output_language(language)][key]


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
    configured_ui_language = config.get_ui_language()
    table.add_row("Interface Language", output_language_name(configured_ui_language))
    table.add_row("Output Language", output_language_name(config.get_output_language(default=configured_ui_language)))
    console.print(table)
    return True


def run_wizard(
    reset: bool = False,
    output_language: str | None = None,
    ui_language: str | None = None,
) -> None:
    """Interactive first-run config wizard."""
    ui_language = normalize_output_language(ui_language or config.get_ui_language())
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
        default=normalize_output_language(output_language or ui_language),
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

    flat = {"provider": provider, "ui_language": ui_language, "output_language": language}
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


def _print_profile_table(ui_language: str, title: str, profiles) -> None:
    table = Table(title=title, border_style="cyan", show_header=True)
    table.add_column(_help_text(ui_language, "id"), style="bold")
    table.add_column(_help_text(ui_language, "name"))
    table.add_column(_help_text(ui_language, "description_column"))
    for profile in profiles:
        table.add_row(profile.id, profile.name, profile.description)
    console.print(table)


def run_analysis(
    company: str,
    domain: str,
    ticker: str,
    output_dir: str,
    output_language: str | None = None,
    analysis_depth: str = "standard",
    ui_language: str | None = None,
    pack_name: str = "general",
    pack_file: str | None = None,
    template_name: str = "standard",
    template_file: str | None = None,
) -> None:
    """Run the pipeline against a target company."""
    try:
        prepared = prepare_analysis_run(
            AnalysisRunRequest(
                company=company,
                domain=domain,
                ticker=ticker,
                output_dir=output_dir,
                output_language=output_language,
                ui_language=ui_language,
                analysis_depth=analysis_depth,
                pack_name=pack_name,
                pack_file=pack_file,
                template_name=template_name,
                template_file=template_file,
            )
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/]")
        sys.exit(2)

    console.print(
        Panel.fit(
            f"[bold cyan]OpenBusiness[/] v0.1.0\n"
            f"{ui_text(prepared.ui_language, 'target')}: [bold]{prepared.company}[/] "
            f"({prepared.domain or ui_text(prepared.ui_language, 'no_domain')})"
            + (f" [{prepared.ticker}]" if prepared.ticker else "")
            + f"\n{ui_text(prepared.ui_language, 'output_language')}: "
            f"[bold]{output_language_name(prepared.output_language)}[/]"
            + f"\n{ui_text(prepared.ui_language, 'analysis_depth')}: [bold]{prepared.analysis_depth}[/]"
            + f"\n{_help_text(prepared.ui_language, 'analysis_pack')}: "
            f"[bold]{prepared.analysis_pack.id}[/]"
            + f"\n{_help_text(prepared.ui_language, 'report_template')}: "
            f"[bold]{prepared.report_template.id}[/]",
            title=f"🚀 {ui_text(prepared.ui_language, 'analysis_title')}",
            border_style="cyan",
        )
    )

    labels = build_stage_labels(prepared.ui_language)

    try:
        with console.status(f"[cyan]{ui_text(prepared.ui_language, 'starting_pipeline')}[/]") as status:

            def on_stage_done(node_name: str, _node_output: dict, _final_state: dict) -> None:
                label = labels.get(node_name, node_name)
                status.update(f"[cyan]{label}[/]")
                console.print(f"[green]✓[/] {label}")

            result = execute_analysis_run(prepared, on_stage_done=on_stage_done)
    except RuntimeError:
        console.print(f"[red]❌ {ui_text(prepared.ui_language, 'pipeline_no_report')}[/]")
        sys.exit(1)

    if result.warnings:
        console.print(
            Panel(
                "\n".join(result.warnings),
                title=ui_text(prepared.ui_language, "language_warning_title"),
                border_style="yellow",
            )
        )

    console.print(
        f"\n[bold green]✅ {ui_text(prepared.ui_language, 'report_generated')}[/] "
        f"{result.artifacts.root_report_path}"
    )
    console.print(
        f"[bold green]✅ {_help_text(prepared.ui_language, 'artifacts_written')}[/] "
        f"{result.artifacts.run_dir}"
    )
    preview = result.report[:800] + "\n..." if len(result.report) > 800 else result.report
    console.print(Panel(preview, title=ui_text(prepared.ui_language, "preview"), border_style="green"))


def main() -> None:
    cli_language = normalize_output_language(config.get_ui_language())
    parser = argparse.ArgumentParser(
        prog="openbusiness",
        description=_help_text(cli_language, "description"),
    )
    sub = parser.add_subparsers(dest="cmd")

    p_config = sub.add_parser("config", help=_help_text(cli_language, "config_help"))
    p_config.add_argument("--reset", action="store_true", help=_help_text(cli_language, "config_reset"))
    p_config.add_argument(
        "--language",
        "-l",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        help=_help_text(cli_language, "config_language"),
    )
    p_config.add_argument(
        "--ui-language",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        help=_help_text(cli_language, "config_ui_language"),
    )

    sub.add_parser("show", help=_help_text(cli_language, "show_help"))
    sub.add_parser("packs", help=_help_text(cli_language, "packs_help"))
    sub.add_parser("templates", help=_help_text(cli_language, "templates_help"))

    p_analyze = sub.add_parser("analyze", help=_help_text(cli_language, "analyze_help"))
    p_analyze.add_argument("company", help=_help_text(cli_language, "company"))
    p_analyze.add_argument("--domain", "-d", default="", help=_help_text(cli_language, "domain"))
    p_analyze.add_argument("--ticker", "-t", default="", help=_help_text(cli_language, "ticker"))
    p_analyze.add_argument("--output", "-o", default="output", help=_help_text(cli_language, "output"))
    p_analyze.add_argument(
        "--language",
        "-l",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        default=None,
        help=_help_text(cli_language, "analyze_language"),
    )
    p_analyze.add_argument(
        "--ui-language",
        choices=list(SUPPORTED_OUTPUT_LANGUAGES),
        default=None,
        help=_help_text(cli_language, "analyze_ui_language"),
    )
    p_analyze.add_argument(
        "--depth",
        choices=list(ANALYSIS_DEPTHS),
        default="standard",
        help=_help_text(cli_language, "depth"),
    )
    p_analyze.add_argument(
        "--pack",
        default="general",
        help=_help_text(cli_language, "pack"),
    )
    p_analyze.add_argument(
        "--pack-file",
        default=None,
        help=_help_text(cli_language, "pack_file"),
    )
    p_analyze.add_argument(
        "--template",
        default="standard",
        help=_help_text(cli_language, "template"),
    )
    p_analyze.add_argument(
        "--template-file",
        default=None,
        help=_help_text(cli_language, "template_file"),
    )

    args = parser.parse_args()

    if args.cmd == "config":
        if args.language and not args.reset and not args.ui_language:
            cfg = config.load_config()
            cfg["output_language"] = normalize_output_language(args.language)
            config.save_config(cfg)
            ui_language = normalize_output_language(config.get_ui_language())
            console.print(
                _config_text(ui_language, "default_language_set")
                + f"[bold]{output_language_name(args.language)}[/]"
            )
            return
        if args.ui_language and not args.reset and not args.language:
            cfg = config.load_config()
            cfg["ui_language"] = normalize_output_language(args.ui_language)
            cfg["output_language"] = normalize_output_language(args.ui_language)
            config.save_config(cfg)
            ui_language = normalize_output_language(args.ui_language)
            console.print(
                _config_text(ui_language, "default_ui_language_set")
                + f"[bold]{output_language_name(args.ui_language)}[/]"
            )
            return
        run_wizard(reset=args.reset, output_language=args.language, ui_language=args.ui_language)
        return

    if args.cmd == "show":
        show_language = normalize_output_language(config.get_ui_language())
        if not _show_current_config(show_language):
            console.print(_config_text(show_language, "no_config"))
        return

    if args.cmd == "packs":
        _print_profile_table(cli_language, _help_text(cli_language, "packs_help"), list_analysis_packs())
        return

    if args.cmd == "templates":
        _print_profile_table(cli_language, _help_text(cli_language, "templates_help"), list_report_templates())
        return

    if args.cmd == "analyze":
        if not config.is_configured():
            wizard_language = normalize_output_language(args.ui_language or config.get_ui_language())
            console.print(_config_text(wizard_language, "missing_config"))
            if Confirm.ask(_config_text(wizard_language, "run_wizard_now"), default=True):
                run_wizard(output_language=args.language, ui_language=wizard_language)
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
            args.pack,
            args.pack_file,
            args.template,
            args.template_file,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
