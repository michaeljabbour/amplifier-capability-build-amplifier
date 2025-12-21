"""
Bundle management commands.

Handles:
- Listing bundles
- Inspecting bundle contents
- Updating git-sourced bundles
- Bundle validation
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from amplifier_foundation import load_bundle

app = typer.Typer()
console = Console()


@app.command()
def list(
    bundles_dir: Optional[str] = typer.Option(
        None, "--dir", help="Bundles directory (defaults to ./bundles and ~/.amplifier/bundles)"
    ),
):
    """List available bundles.

    Shows bundles from:
    - ./bundles/ (project bundles)
    - ./providers/ (provider bundles)
    - ~/.amplifier/bundles/ (global bundles)
    - ~/.amplifier/providers/ (global providers)

    Examples:

        # List all bundles
        amplifier bundle list

        # List bundles from custom directory
        amplifier bundle list --dir ./my-bundles
    """
    try:
        # Determine bundle directories
        if bundles_dir:
            dirs = [Path(bundles_dir)]
        else:
            dirs = [
                Path("./bundles"),
                Path("./providers"),
                Path.home() / ".amplifier" / "bundles",
                Path.home() / ".amplifier" / "providers",
            ]

        # Collect bundles
        bundles = []
        for dir_path in dirs:
            if not dir_path.exists():
                continue

            for bundle_file in list(dir_path.glob("*.md")) + list(dir_path.glob("*.yaml")):
                bundles.append(
                    {
                        "name": bundle_file.stem,
                        "path": str(bundle_file),
                        "type": "provider" if "provider" in dir_path.name else "bundle",
                        "scope": "project" if str(dir_path).startswith(".") else "global",
                    }
                )

        if not bundles:
            console.print("[dim]No bundles found[/dim]")
            console.print("[dim]Create bundles in ./bundles/ or ~/.amplifier/bundles/[/dim]")
            return

        # Show bundle table
        table = Table(title=f"Available Bundles ({len(bundles)})")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Scope", style="dim")
        table.add_column("Path", style="dim")

        for bundle in sorted(bundles, key=lambda b: (b["type"], b["name"])):
            table.add_row(
                bundle["name"], bundle["type"], bundle["scope"], bundle["path"]
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def inspect(
    bundle_path: str = typer.Argument(..., help="Bundle path to inspect"),
):
    """Inspect bundle contents.

    Shows:
    - Bundle metadata (name, version, description)
    - Providers
    - Tools
    - Hooks
    - Agents
    - Instruction (first 200 chars)

    Examples:

        # Inspect local bundle
        amplifier bundle inspect ./bundles/base.md

        # Inspect provider
        amplifier bundle inspect ./providers/anthropic.yaml

        # Inspect git bundle
        amplifier bundle inspect git+https://github.com/org/bundle@main
    """
    asyncio.run(_inspect_bundle(bundle_path))


@app.command()
def update(
    bundle_name: Optional[str] = typer.Argument(
        None, help="Bundle name to update (omit for all)"
    ),
    all: bool = typer.Option(False, "--all", help="Update all git-sourced bundles"),
):
    """Update git-sourced bundles.

    Checks for new commits and refreshes cached bundles.

    Examples:

        # Update specific bundle
        amplifier bundle update my-bundle

        # Update all bundles
        amplifier bundle update --all
    """
    console.print("[dim]Checking for bundle updates...[/dim]")
    console.print(f"[yellow]Not yet implemented[/yellow]")
    console.print("[dim]Coming in Phase 3[/dim]")


async def _inspect_bundle(bundle_path: str):
    """Inspect a bundle and show its contents."""
    try:
        console.print(f"[dim]Loading bundle: {bundle_path}[/dim]\n")

        # Load bundle using foundation
        bundle = await load_bundle(bundle_path)

        # Show metadata
        console.print(f"[bold cyan]{bundle.name}[/bold cyan] v{bundle.version}")
        if bundle.description:
            console.print(f"[dim]{bundle.description}[/dim]\n")

        # Show providers
        if bundle.providers:
            console.print("[bold]Providers:[/bold]")
            for provider in bundle.providers:
                module = provider.get("module", "unknown")
                source = provider.get("source", "built-in")
                console.print(f"  • {module}")
                console.print(f"    [dim]source: {source}[/dim]")

        # Show tools
        if bundle.tools:
            console.print("\n[bold]Tools:[/bold]")
            for tool in bundle.tools:
                module = tool.get("module", "unknown")
                source = tool.get("source", "built-in")
                console.print(f"  • {module}")
                if source != "built-in":
                    console.print(f"    [dim]source: {source}[/dim]")

        # Show hooks
        if bundle.hooks:
            console.print("\n[bold]Hooks:[/bold]")
            for hook in bundle.hooks:
                module = hook.get("module", "unknown")
                source = hook.get("source", "built-in")
                console.print(f"  • {module}")
                if source != "built-in":
                    console.print(f"    [dim]source: {source}[/dim]")

        # Show agents
        if bundle.agents:
            console.print("\n[bold]Agents:[/bold]")
            for agent in bundle.agents:
                name = agent.get("name", "unknown")
                description = agent.get("description", "")
                console.print(f"  • {name}")
                if description:
                    console.print(f"    [dim]{description}[/dim]")

        # Show instruction preview
        if bundle.instruction:
            console.print("\n[bold]Instruction:[/bold]")
            preview = bundle.instruction[:200]
            if len(bundle.instruction) > 200:
                preview += "..."
            console.print(f"[dim]{preview}[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
