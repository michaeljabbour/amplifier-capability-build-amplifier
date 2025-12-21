"""
Agent management commands.

Handles:
- Spawning agents
- Listing available agents
- Installing agents from git
- Agent library management
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from ..app import AmplifierApp
from ..config import Config

app = typer.Typer()
console = Console()


@app.command(name="run")
def run_agent(
    agent: str = typer.Argument(..., help="Agent name or path"),
    instruction: str = typer.Argument(..., help="Task instruction for agent"),
    provider: Optional[str] = typer.Option(
        None, "--provider", "-p", help="Provider bundle path"
    ),
    resume: Optional[str] = typer.Option(
        None, "--resume", help="Session ID to resume"
    ),
):
    """Spawn an agent to perform a task.

    Agents are specialized bundles with specific capabilities and instructions.
    They can access tools, spawn sub-agents, and maintain conversation history.

    Examples:

        # Run bug hunter agent
        amplifier agent run bug-hunter "Find bugs in auth.py"

        # Resume previous agent session
        amplifier agent run bug-hunter "Continue" --resume abc123...

        # Use custom agent bundle
        amplifier agent run ./agents/code-reviewer.md "Review PR #42"
    """
    asyncio.run(_spawn_agent(agent, instruction, provider, resume))


@app.command()
def list(
    agents_dir: Optional[str] = typer.Option(
        None, "--dir", help="Agents directory (defaults to ./agents)"
    ),
):
    """List available agents.

    Shows agents from:
    - ./agents/ (project agents)
    - ~/.amplifier/agents/ (global agents)

    Examples:

        # List all agents
        amplifier agent list

        # List agents from custom directory
        amplifier agent list --dir ./my-agents
    """
    try:
        # Determine agent directories
        if agents_dir:
            dirs = [Path(agents_dir)]
        else:
            dirs = [
                Path("./agents"),
                Path.home() / ".amplifier" / "agents",
            ]

        # Collect agents
        agents = []
        for dir_path in dirs:
            if not dir_path.exists():
                continue

            for agent_file in dir_path.glob("*.md"):
                agents.append(
                    {
                        "name": agent_file.stem,
                        "path": str(agent_file),
                        "scope": "project" if dir_path == Path("./agents") else "global",
                    }
                )

        if not agents:
            console.print("[dim]No agents found[/dim]")
            console.print("[dim]Create agents in ./agents/ or ~/.amplifier/agents/[/dim]")
            return

        # Show agent table
        table = Table(title=f"Available Agents ({len(agents)})")
        table.add_column("Name", style="cyan")
        table.add_column("Path", style="dim")
        table.add_column("Scope", style="magenta")

        for agent in sorted(agents, key=lambda a: a["name"]):
            table.add_row(agent["name"], agent["path"], agent["scope"])

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def install(
    git_url: str = typer.Argument(..., help="Git URL of agent bundle"),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Agent name (defaults to repo name)"
    ),
):
    """Install an agent from a git repository.

    Examples:

        # Install agent from git
        amplifier agent install git+https://github.com/user/my-agent@main

        # Install with custom name
        amplifier agent install git+https://... --name my-custom-agent
    """
    console.print("[dim]Installing agent from git...[/dim]")
    console.print(f"[yellow]Not yet implemented[/yellow]")
    console.print("[dim]Coming in Phase 5[/dim]")


async def _spawn_agent(
    agent: str,
    instruction: str,
    provider: Optional[str],
    resume_session_id: Optional[str],
):
    """Spawn an agent to perform a task."""
    try:
        # Create config
        config = Config.from_env_and_project()
        if provider:
            config.provider = provider
        config.validate()

        # Resolve agent path
        agent_path = _resolve_agent_path(agent)
        if not agent_path:
            console.print(f"[bold red]Agent not found:[/bold red] {agent}")
            console.print("[dim]Available agents:[/dim]")
            console.print(f"[dim]  - ./agents/{agent}.md[/dim]")
            console.print(f"[dim]  - ~/.amplifier/agents/{agent}.md[/dim]")
            raise typer.Exit(code=1)

        # Initialize app
        async with AmplifierApp(config) as app:
            console.print(f"[dim]Spawning agent: {agent}[/dim]")
            console.print(f"[dim]Task: {instruction}[/dim]\n")

            # Spawn agent
            result = await app.spawn_agent(
                agent_path, instruction, session_id=resume_session_id
            )

            # Show result
            console.print("[bold cyan]Agent Response:[/bold cyan]\n")
            console.print(Markdown(result["output"]))

            # Show session ID for resumption
            console.print(f"\n[dim]Agent Session ID: {result['session_id']}[/dim]")
            console.print(
                f"[dim]Resume with: amplifier agent run {agent} \"...\" "
                f"--resume {result['session_id']}[/dim]"
            )

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


def _resolve_agent_path(agent: str) -> Optional[str]:
    """Resolve agent name to full path.

    Search order:
    1. Exact path (if exists)
    2. ./agents/{agent}.md
    3. ~/.amplifier/agents/{agent}.md

    Args:
        agent: Agent name or path

    Returns:
        Resolved path or None if not found
    """
    # Try exact path
    agent_path = Path(agent)
    if agent_path.exists():
        return str(agent_path)

    # Try project agents
    project_agent = Path("./agents") / f"{agent}.md"
    if project_agent.exists():
        return str(project_agent)

    # Try global agents
    global_agent = Path.home() / ".amplifier" / "agents" / f"{agent}.md"
    if global_agent.exists():
        return str(global_agent)

    return None
