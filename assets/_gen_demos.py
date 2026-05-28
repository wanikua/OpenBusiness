"""Generate README demo SVGs using rich.Console.save_svg().

Produces:
  assets/demo-terminal.svg   — what running `openbusiness analyze` looks like
  assets/demo-report.svg     — excerpt of the output report (with VERIFIED/INFERRED/MISSING tags)

Run:  python assets/_gen_demos.py
"""
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

OUT = Path(__file__).parent


def render_terminal() -> None:
    console = Console(record=True, width=96, color_system="truecolor")

    console.print()
    console.print("[bold green]$[/] [bold]openbusiness analyze \"Notion\" --domain notion.so[/]")
    console.print()
    console.print(Panel.fit(
        "[bold cyan]OpenBusiness[/] · evidence-driven business model reverse engineering\n"
        "[dim]target:[/] [bold]Notion[/]   [dim]domain:[/] notion.so",
        border_style="cyan",
    ))
    console.print()

    steps = [
        ("🔍", "Evidence Collector",        "Tavily + Firecrawl + SEC EDGAR  ", "done", "12 sources"),
        ("👥", "JTBD Analyst",              "who pays / who uses / what job  ", "done", "3 segments"),
        ("💎", "Value Prop Analyst",        "10x Better test                 ", "done", "5x setup, 2x cost"),
        ("🚀", "GTM Analyst",               "PLG / Sales-led / Community     ", "done", "3 channels"),
        ("💰", "Unit Economics Analyst",    "LTV / CAC / breakeven (pure math)", "done", "LTV/CAC = 1.6x"),
        ("🛡️ ", "Moat Analyst",              "5 moat types + Porter 5F        ", "done", "Narrow, Moderate"),
        ("🧱", "Canvas Synthesizer",        "assemble 9-block canvas         ", "done", "tags preserved"),
        ("🔬", "Assumption Stress Tester",  "which assumptions break canvas  ", "done", "5 high-risk"),
        ("📝", "Finalizer",                  "stitch full report              ", "done", "—"),
    ]

    tbl = Table.grid(padding=(0, 2))
    tbl.add_column()
    tbl.add_column()
    tbl.add_column(style="dim")
    tbl.add_column()
    tbl.add_column(style="dim italic")
    for icon, name, sub, status, hint in steps:
        status_cell = Text("✓ done", style="bold green") if status == "done" else Text(status, style="yellow")
        tbl.add_row(icon, Text(name, style="bold"), sub, status_cell, hint)
    console.print(tbl)

    console.print()
    console.print("[bold green]✅ Report saved[/]  →  [yellow]output/notion_business_model.md[/]")
    console.print("[dim]   289 claims tagged · 🟢 VERIFIED:14  🟡 INFERRED:248  🔴 MISSING:27[/]")
    console.print()

    console.save_svg(str(OUT / "demo-terminal.svg"), title="openbusiness analyze")


def render_report() -> None:
    console = Console(record=True, width=110, color_system="truecolor")

    console.print()
    console.print(Panel.fit(
        "[bold]📊 OpenBusiness Business Model Reverse Engineering Report[/]\n"
        "[dim]Target:[/] [bold cyan]Notion[/]   [dim]Confidence:[/] [yellow]Fragile[/]",
        border_style="cyan",
    ))
    console.print()

    console.print("[bold]💰 Unit Economics Snapshot[/]")
    console.print()
    ue = Table(show_header=True, header_style="bold cyan", border_style="dim")
    ue.add_column("Metric", style="bold")
    ue.add_column("Value")
    ue.add_column("Tag")
    ue.add_row("Blended ARPU",  "$12.00 / month",  "[green]🟢 VERIFIED[/] calculation")
    ue.add_row("Gross Margin",  "80%",             "[yellow]🟡 INFERRED[/] typical SaaS")
    ue.add_row("CAC",           "$150",            "[yellow]🟡 INFERRED[/] PLG blended")
    ue.add_row("Monthly Churn", "4%",              "[yellow]🟡 INFERRED[/] SMB PLG")
    ue.add_row("Lifetime",      "25.0 months",     "[green]🟢 VERIFIED[/] 1 / 0.04")
    ue.add_row("LTV",           "$240.00",         "[green]🟢 VERIFIED[/] $12 × 25 × 0.80")
    ue.add_row("LTV / CAC",     "[bold yellow]1.6x  ⚠ Warning[/]", "[green]🟢 VERIFIED[/] $240 / $150")
    console.print(ue)
    console.print()

    console.print("[bold]🔬 Assumption Stress Test  ·  what breaks the canvas[/]")
    console.print()
    console.print("[bold red]▸ Assumption 1[/]  [bold]4% monthly churn is representative[/]")
    console.print("  [dim]Falsification:[/] If actual churn is 6%, LTV drops to $160, LTV/CAC → [red]1.07x[/] (unsustainable).")
    console.print("                  If churn is 2%, LTV jumps to $480, LTV/CAC → [green]3.2x[/] (healthy).")
    console.print()
    console.print("[bold red]▸ Assumption 2[/]  [bold]Blended ARPU of $12/mo is accurate[/]")
    console.print("  [dim]Falsification:[/] If free users = 80%+, blended ARPU could be $4–6.")
    console.print("                  → LTV/CAC flips [red]below 1.0x[/] — losing money on every acquisition.")
    console.print()

    console.print("[bold]🔴 Missing Data  ·  what we couldn't verify[/]")
    console.print()
    miss = Table.grid(padding=(0, 2))
    miss.add_column(style="red bold")
    miss.add_column()
    miss.add_row("🔴", "Actual ARPU by plan tier  —  [dim]LTV could be very different[/]")
    miss.add_row("🔴", "Actual CAC by channel     —  [dim]enterprise CAC could be $500–$2000+[/]")
    miss.add_row("🔴", "Notion AI adoption rate   —  [dim]key ARPU lever, unverifiable[/]")
    miss.add_row("🔴", "Enterprise revenue mix    —  [dim]blended metrics may be misleading[/]")
    console.print(miss)
    console.print()

    console.save_svg(str(OUT / "demo-report.svg"), title="output/notion_business_model.md")


if __name__ == "__main__":
    render_terminal()
    render_report()
    print(f"Wrote {OUT / 'demo-terminal.svg'}")
    print(f"Wrote {OUT / 'demo-report.svg'}")
