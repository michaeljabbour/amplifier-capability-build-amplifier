"""
CLI entry point for Amplifier.

Uses Typer for modern CLI experience:
- Shell completion
- Type validation
- Automatic help generation
- Rich terminal output
"""

import sys
from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .commands import agent, bundle, run, session

# Create Typer app
app = typer.Typer(
    name="amplifier",
    help="Foundation-based CLI for composable AI applications",
    add_completion=True,
    rich_markup_mode="rich",
)

# Add command groups
app.add_typer(run.app, name="run", help="Execute prompts and REPL mode")
app.add_typer(session.app, name="session", help="Session management")
app.add_typer(bundle.app, name="bundle", help="Bundle management")
app.add_typer(agent.app, name="agent", help="Agent management")

# Rich console for output
console = Console()


@app.command()
def version():
    """Show version information."""
    console.print(f"[bold cyan]Amplifier CLI[/bold cyan] v{__version__}")
    console.print("[dim]Foundation-based composable AI applications[/dim]")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colors"),
):
    """
    Amplifier CLI - Foundation-based composable AI applications.

    Built directly on amplifier-foundation with 85% less code than app-cli.

    Quick Start:

        # Execute a prompt
        amplifier run "Hello, world!"

        # Interactive REPL
        amplifier repl

        # Spawn an agent
        amplifier agent run bug-hunter "Find bugs in auth.py"

    Documentation: https://github.com/microsoft/amplifier
    """
    # Store settings in context for commands
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["no_color"] = no_color


def cli_main():
    """Main entry point for CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
