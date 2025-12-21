"""
Session management commands.

Handles:
- Listing sessions
- Showing session details
- Deleting sessions
- Project-scoped vs global sessions
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ..config import Config
from ..session_manager import SessionManager

app = typer.Typer()
console = Console()


@app.command()
def list(
    project: Optional[str] = typer.Option(
        None, "--project", help="Project root (defaults to current project)"
    ),
    limit: int = typer.Option(20, "--limit", "-n", help="Maximum sessions to show"),
):
    """List recent sessions.

    Shows session history with:
    - Session ID (for resumption)
    - Created timestamp
    - Last prompt
    - Provider used

    Examples:

        # List sessions for current project
        amplifier session list

        # List global sessions
        amplifier session list --project ~

        # Show more sessions
        amplifier session list --limit 50
    """
    try:
        # Get project root
        project_root = _get_project_root(project)

        # Load session manager
        manager = SessionManager(project_root)
        sessions = manager.list_sessions()

        if not sessions:
            console.print("[dim]No sessions found[/dim]")
            if project_root:
                console.print(f"[dim]Project: {project_root}[/dim]")
            return

        # Show session table
        table = Table(title=f"Recent Sessions ({len(sessions[:limit])} shown)")
        table.add_column("Session ID", style="cyan")
        table.add_column("Created", style="dim")
        table.add_column("Last Prompt", style="white")
        table.add_column("Provider", style="magenta")

        for session in sessions[:limit]:
            table.add_row(
                session.get("session_id", "unknown")[:16] + "...",
                session.get("created_at", "unknown")[:19],
                session.get("last_prompt", "N/A")[:40],
                _extract_provider_name(session.get("provider", "unknown")),
            )

        console.print(table)

        if project_root:
            console.print(f"\n[dim]Project: {project_root}[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def show(
    session_id: str = typer.Argument(..., help="Session ID to show"),
    project: Optional[str] = typer.Option(
        None, "--project", help="Project root (defaults to current project)"
    ),
):
    """Show detailed session information.

    Examples:

        # Show session details
        amplifier session show abc123...
    """
    try:
        # Get project root
        project_root = _get_project_root(project)

        # Load session manager
        manager = SessionManager(project_root)
        session = manager.get_session(session_id)

        if not session:
            console.print(f"[yellow]Session not found:[/yellow] {session_id}")
            return

        # Show session details
        console.print(f"\n[bold cyan]Session {session_id}[/bold cyan]\n")
        console.print(f"[bold]Created:[/bold] {session.get('created_at', 'unknown')}")
        console.print(f"[bold]Provider:[/bold] {session.get('provider', 'unknown')}")
        if session.get("project_root"):
            console.print(f"[bold]Project:[/bold] {session['project_root']}")
        console.print(f"\n[bold]Last Prompt:[/bold]\n{session.get('last_prompt', 'N/A')}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def delete(
    session_id: str = typer.Argument(..., help="Session ID to delete"),
    project: Optional[str] = typer.Option(
        None, "--project", help="Project root (defaults to current project)"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a session.

    Examples:

        # Delete session
        amplifier session delete abc123...

        # Delete without confirmation
        amplifier session delete abc123... --force
    """
    try:
        # Get project root
        project_root = _get_project_root(project)

        # Load session manager
        manager = SessionManager(project_root)
        session = manager.get_session(session_id)

        if not session:
            console.print(f"[yellow]Session not found:[/yellow] {session_id}")
            return

        # Confirm deletion
        if not force:
            confirm = typer.confirm(f"Delete session {session_id[:16]}...?")
            if not confirm:
                console.print("[dim]Cancelled[/dim]")
                return

        # Delete session
        manager.delete_session(session_id)
        console.print(f"[green]✓[/green] Deleted session {session_id[:16]}...")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


def _get_project_root(project: Optional[str]) -> Optional[Path]:
    """Get project root from option or auto-detect."""
    if project:
        return Path(project)
    else:
        config = Config.from_env_and_project()
        return config.project_root


def _extract_provider_name(provider_path: str) -> str:
    """Extract provider name from path."""
    # Examples:
    #   ./providers/anthropic.yaml → anthropic
    #   git+https://github.com/.../anthropic → anthropic
    if "/" in provider_path:
        name = provider_path.split("/")[-1]
        return name.replace(".yaml", "").replace(".md", "")
    return provider_path
