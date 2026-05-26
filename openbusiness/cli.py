"""CLI entry point for OpenBusiness."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="openbusiness",
        description="AI-driven multi-agent business model analysis",
    )
    parser.add_argument("company", help="Company name to analyze (e.g. 'Notion')")
    parser.add_argument("--domain", "-d", default="", help="Company website domain (e.g. 'notion.so')")
    parser.add_argument("--ticker", "-t", default="", help="Stock ticker if public (e.g. 'AAPL')")
    parser.add_argument("--output", "-o", default="output", help="Output directory for reports")
    parser.add_argument("--rounds", "-r", type=int, default=2, help="Number of bull/bear debate rounds")

    args = parser.parse_args()

    console.print(
        Panel.fit(
            f"[bold cyan]OpenBusiness[/] v0.1.0\n"
            f"Target: [bold]{args.company}[/]"
            + (f" ({args.domain})" if args.domain else "")
            + (f" [{args.ticker}]" if args.ticker else ""),
            title="🚀 Business Model Reverse Engineering",
            border_style="cyan",
        )
    )

    from openbusiness.graph.setup import build_graph

    graph = build_graph(debate_rounds=args.rounds)

    initial_state = {
        "company_name": args.company,
        "domain": args.domain or f"{args.company.lower().replace(' ', '')}.com",
        "ticker": args.ticker,
        "traffic_report": "",
        "financial_report": "",
        "competitive_report": "",
        "product_report": "",
        "optimist_argument": "",
        "pessimist_argument": "",
        "debate_round": 0,
        "research_verdict": "",
        "final_report": "",
        "messages": [],
    }

    stages = [
        ("traffic_analyst", "📡 Traffic Analyst — 分析流量与获客渠道"),
        ("financial_analyst", "💰 Financial Analyst — 拆解盈利模式与单体经济"),
        ("competitive_analyst", "⚔️ Competitive Analyst — 波特五力竞争分析"),
        ("product_analyst", "🎯 Product Analyst — 价值主张与护城河"),
        ("optimist", "📈 Optimist — 看多论证"),
        ("pessimist", "📉 Pessimist — 看空论证"),
        ("research_director", "🏛️ Research Director — 辩论裁决"),
        ("strategy_director", "📊 Strategy Director — 生成商业模式画布"),
    ]
    stage_map = {s[0]: s[1] for s in stages}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Starting pipeline...", total=None)

        result = None
        for event in graph.stream(initial_state, stream_mode="updates"):
            for node_name in event:
                label = stage_map.get(node_name, node_name)
                progress.update(task, description=f"[cyan]{label}")
            result = event

    final_state = graph.invoke(initial_state)
    report = final_state.get("final_report", "No report generated.")

    out_dir = Path(args.output)
    out_dir.mkdir(exist_ok=True)
    slug = args.company.lower().replace(" ", "_")
    out_path = out_dir / f"{slug}_business_model.md"
    out_path.write_text(report, encoding="utf-8")

    console.print(f"\n[bold green]✅ 报告已生成:[/] {out_path}")
    console.print(Panel(report[:500] + "\n..." if len(report) > 500 else report, title="Preview"))


if __name__ == "__main__":
    main()
