from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

console = Console()

def run():
    if not Path(".git").exists():
        console.print("[red]Not a git repository.[/red]")
        return

    console.print("[purple]Analyzing codebase...[/purple]")

    from src.graphs.graph import run_explain
    result = run_explain()

    console.print(Markdown(result))

    output_path = Path("CODEBASE.md")
    output_path.write_text(result)
    console.print(f"\n[green]✔ Saved to {output_path}[/green]")