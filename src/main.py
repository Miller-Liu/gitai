from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

from src.agents.orchestrator import OrchestratorAgent

load_dotenv()
app = typer.Typer(help="AI-powered git assistant")
console = Console()

@app.command()
def init():
    """Initialize gitai for this repository."""
    console.print("[purple]Initializing gitai...[/purple]")

@app.command()
def commit():
    """Generate an AI commit message."""
    console.print("[yellow]Coming soon[/yellow]")

@app.command()
def explain():
    """Explain how this codebase works."""
    
    if not Path(".git").exists():
        console.print("[red]Not a git repository.[/red]")
        raise typer.Exit(1)
    
    console.print("[purple]Analyzing codebase...[/purple]")
    agent = OrchestratorAgent()
    result = agent.run("Explain how this codebase works.")
    console.print(result)

@app.command()
def push():
    """Safety scan then push."""
    console.print("[yellow]Coming soon[/yellow]")

@app.command()
def setup():
    """Configure provider and API key."""
    console.print("[yellow]Coming soon[/yellow]")
