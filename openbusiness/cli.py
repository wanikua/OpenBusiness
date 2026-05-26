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

from openbusiness.llm_clients import config

console = Console()


def _show_current_config() -> bool:
    """Show what's already configured. Returns True if anything is configured."""
    if not config.CONFIG_FILE.exists():
        return False

    cfg = config.load_config()
    if not cfg:
        return False

    table = Table(title="当前配置", border_style="cyan", show_header=True)
    table.add_column("项目", style="bold")
    table.add_column("状态")

    provider = cfg.get("provider", "")
    table.add_row("LLM Provider", provider or "[red]未设置[/]")
    table.add_row("OpenAI Key", "✅ 已配置" if cfg.get("openai_api_key") else "—")
    table.add_row("Anthropic Key", "✅ 已配置" if cfg.get("anthropic_api_key") else "—")
    table.add_row("Tavily Key", "✅ 已配置" if cfg.get("tavily_api_key") else "—")
    table.add_row("Firecrawl Key", "✅ 已配置" if cfg.get("firecrawl_api_key") else "—")
    console.print(table)
    return True


def run_wizard(reset: bool = False) -> None:
    """Interactive first-run config wizard."""
    console.print(
        Panel.fit(
            "[bold cyan]OpenBusiness 配置向导[/]\n\n"
            "配置文件保存路径: [yellow]~/.config/openbusiness/config.toml[/] (权限 0600)\n"
            "环境变量始终优先生效 (OPENAI_API_KEY / ANTHROPIC_API_KEY / TAVILY_API_KEY / FIRECRAWL_API_KEY)\n",
            title="🛠️ Setup",
            border_style="cyan",
        )
    )

    has_config = _show_current_config()
    if has_config and not reset:
        if not Confirm.ask("\n要重新配置吗?", default=False):
            console.print("[dim]保持现有配置不变。[/]")
            _print_next_steps()
            return

    console.print()
    provider = Prompt.ask(
        "[bold]选择 LLM 提供方[/]",
        choices=["openai", "anthropic"],
        default="openai",
    )

    if provider == "openai":
        key = getpass.getpass("OpenAI API Key (sk-...): ").strip()
    else:
        key = getpass.getpass("Anthropic API Key (sk-ant-...): ").strip()

    if not key:
        console.print("[red]API key 必填。退出。[/]")
        sys.exit(1)

    console.print("\n[bold]证据采集工具 (可选 — 直接回车跳过)[/]")
    console.print("[dim]没有这些 key 不影响运行，但分析会更多依赖 LLM 已有知识 (标 [INFERRED])。[/]\n")

    tavily_key = getpass.getpass("Tavily API Key (Web 搜索, https://tavily.com): ").strip()
    firecrawl_key = getpass.getpass("Firecrawl API Key (页面抓取, https://firecrawl.dev): ").strip()

    flat = {"provider": provider}
    if provider == "openai":
        flat["openai_api_key"] = key
    else:
        flat["anthropic_api_key"] = key
    if tavily_key:
        flat["tavily_api_key"] = tavily_key
    if firecrawl_key:
        flat["firecrawl_api_key"] = firecrawl_key

    config.save_config(flat)

    console.print(f"\n[green]✅ 配置已保存到[/] [yellow]{config.CONFIG_FILE}[/]")
    _print_next_steps()


def _print_next_steps() -> None:
    console.print(
        Panel(
            "[bold]下一步：分析一家公司[/]\n\n"
            "  [cyan]openbusiness analyze \"Notion\" --domain notion.so[/]\n"
            "  [cyan]openbusiness analyze \"Costco\" --ticker COST[/]\n"
            "  [cyan]openbusiness analyze \"Vercel\" --domain vercel.com[/]\n\n"
            "[dim]报告会输出到 ./output/<company>_business_model.md[/]",
            title="🚀 Ready",
            border_style="green",
        )
    )


def run_analysis(company: str, domain: str, ticker: str, output_dir: str) -> None:
    """Run the pipeline against a target company."""
    from openbusiness.graph.setup import PIPELINE_STAGES, build_graph

    console.print(
        Panel.fit(
            f"[bold cyan]OpenBusiness[/] v0.1.0\n"
            f"Target: [bold]{company}[/] "
            f"({domain or 'no domain'})" + (f" [{ticker}]" if ticker else ""),
            title="🚀 Business Model Reverse Engineering",
            border_style="cyan",
        )
    )

    graph = build_graph()

    initial_state = {
        "company_name": company,
        "domain": domain or f"{company.lower().replace(' ', '')}.com",
        "ticker": ticker,
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

    final_state = initial_state
    with console.status("[cyan]启动流水线...[/]") as status:
        for event in graph.stream(initial_state, stream_mode="updates"):
            for node_name, node_output in event.items():
                label = stage_labels.get(node_name, node_name)
                status.update(f"[cyan]{label}[/]")
                if isinstance(node_output, dict):
                    final_state = {**final_state, **node_output}

    report = final_state.get("final_report", "")
    if not report:
        console.print("[red]❌ 流水线完成但没有最终报告。检查 API key 与额度。[/]")
        sys.exit(1)

    out = Path(output_dir)
    out.mkdir(exist_ok=True)
    slug = company.lower().replace(" ", "_")
    out_path = out / f"{slug}_business_model.md"
    out_path.write_text(report, encoding="utf-8")

    console.print(f"\n[bold green]✅ 报告已生成:[/] {out_path}")
    preview = report[:800] + "\n..." if len(report) > 800 else report
    console.print(Panel(preview, title="Preview", border_style="green"))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openbusiness",
        description="AI-driven business model reverse engineering",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_config = sub.add_parser("config", help="运行配置向导 (首次使用必须运行)")
    p_config.add_argument("--reset", action="store_true", help="无视现有配置重新输入")

    p_show = sub.add_parser("show", help="显示当前配置 (不显示完整 key)")

    p_analyze = sub.add_parser("analyze", help="分析一家公司的商业模式")
    p_analyze.add_argument("company", help="公司名 (e.g. 'Notion')")
    p_analyze.add_argument("--domain", "-d", default="", help="官网域名 (e.g. notion.so)")
    p_analyze.add_argument("--ticker", "-t", default="", help="美股代码 (e.g. AAPL)")
    p_analyze.add_argument("--output", "-o", default="output", help="报告输出目录")

    args = parser.parse_args()

    if args.cmd == "config":
        run_wizard(reset=args.reset)
        return

    if args.cmd == "show":
        if not _show_current_config():
            console.print("[yellow]未找到配置。运行: [bold]openbusiness config[/][/]")
        return

    if args.cmd == "analyze":
        if not config.is_configured():
            console.print("[yellow]⚠️ 未找到配置。请先运行: [bold]openbusiness config[/][/]")
            if Confirm.ask("现在运行向导吗?", default=True):
                run_wizard()
            else:
                sys.exit(1)
        run_analysis(args.company, args.domain, args.ticker, args.output)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
