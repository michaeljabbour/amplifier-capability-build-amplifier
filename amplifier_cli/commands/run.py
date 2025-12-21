"""
Run command - Execute prompts and REPL mode.

Handles:
- Single prompt execution
- Interactive REPL with history
- Multi-bundle composition
- Session tracking
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.markdown import Markdown

from ..app import AmplifierApp
from ..config import Config

app = typer.Typer()
console = Console()


@app.command(name="")
def run_prompt(
    prompt: str = typer.Argument(..., help="Prompt to execute"),
    provider: Optional[str] = typer.Option(
        None, "--provider", "-p", help="Provider bundle path"
    ),
    bundle: Optional[list[str]] = typer.Option(
        None, "--bundle", "-b", help="Additional bundle to compose (repeatable)"
    ),
    project: Optional[str] = typer.Option(
        None, "--project", help="Project root path (defaults to auto-detect)"
    ),
):
    """Execute a single prompt.

    Examples:

        # Basic execution
        amplifier run "Hello, world!"

        # With specific provider
        amplifier run --provider ./providers/openai.yaml "prompt"

        # Compose multiple bundles
        amplifier run --bundle base.md --bundle tools.md "prompt"
    """
    asyncio.run(_execute_prompt(prompt, provider, bundle, project))


@app.command()
def repl(
    provider: Optional[str] = typer.Option(
        None, "--provider", "-p", help="Provider bundle path"
    ),
    bundle: Optional[list[str]] = typer.Option(
        None, "--bundle", "-b", help="Additional bundle to compose (repeatable)"
    ),
    project: Optional[str] = typer.Option(
        None, "--project", help="Project root path (defaults to auto-detect)"
    ),
):
    """Start interactive REPL mode.

    REPL features:
    - Multi-line input (Ctrl-J for newlines)
    - Command history (up/down arrows)
    - History search (Ctrl-R)
    - Context preserved across inputs
    - Exit with 'exit', 'quit', or Ctrl-D

    Examples:

        # Start REPL
        amplifier repl

        # REPL with specific provider
        amplifier repl --provider ./providers/openai.yaml
    """
    asyncio.run(_repl_mode(provider, bundle, project))


async def _execute_prompt(
    prompt: str,
    provider: Optional[str],
    bundles: Optional[list[str]],
    project_path: Optional[str],
):
    """Execute a single prompt."""
    try:
        # Create config
        config = _create_config(provider, bundles, project_path)
        config.validate()

        # Initialize app
        async with AmplifierApp(config) as app:
            # Show session info
            console.print(f"[dim]Session: {app.session.session_id}[/dim]")
            console.print(f"[dim]Model: {config.provider}[/dim]\n")

            # Execute prompt
            response = await app.execute(prompt)

            # Render response as markdown
            console.print(Markdown(response))

            # Save session metadata
            await _save_session_metadata(app, config, prompt)

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if console.is_terminal:
            console.print("\n[dim]Tip: Check your API key and provider configuration[/dim]")
        raise typer.Exit(code=1)


async def _repl_mode(
    provider: Optional[str],
    bundles: Optional[list[str]],
    project_path: Optional[str],
):
    """Interactive REPL mode."""
    try:
        # Create config
        config = _create_config(provider, bundles, project_path)
        config.validate()

        # Initialize app (session persists for entire REPL)
        async with AmplifierApp(config) as app:
            # Show welcome message
            console.print("[bold cyan]Amplifier REPL[/bold cyan]")
            console.print(f"[dim]Session: {app.session.session_id}[/dim]")
            console.print(f"[dim]Model: {config.provider}[/dim]")
            console.print("[dim]Commands: 'exit', 'quit', or Ctrl-D to quit[/dim]")
            console.print("[dim]Multi-line: Ctrl-J for newlines[/dim]\n")

            # Setup prompt with history
            history_file = Path.home() / ".amplifier" / "repl_history"
            history_file.parent.mkdir(parents=True, exist_ok=True)

            prompt_session: PromptSession = PromptSession(
                history=FileHistory(str(history_file)),
                multiline=True,
            )

            # REPL loop
            while True:
                try:
                    # Get user input
                    user_input = await prompt_session.prompt_async(">>> ")

                    # Handle exit commands
                    if user_input.strip().lower() in ("exit", "quit"):
                        console.print("[dim]Goodbye![/dim]")
                        break

                    # Skip empty input
                    if not user_input.strip():
                        continue

                    # Execute with foundation
                    response = await app.execute(user_input)

                    # Render response
                    console.print(Markdown(response))
                    console.print()  # Blank line for readability

                except KeyboardInterrupt:
                    # Ctrl-C - just continue
                    console.print("[dim]\nInterrupted. Type 'exit' to quit.[/dim]")
                    continue
                except EOFError:
                    # Ctrl-D - exit gracefully
                    console.print("\n[dim]Goodbye![/dim]")
                    break

            # Save session metadata
            await _save_session_metadata(app, config, "REPL session")

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if console.is_terminal:
            console.print("\n[dim]Tip: Check your API key and provider configuration[/dim]")
        raise typer.Exit(code=1)


def _create_config(
    provider: Optional[str],
    bundles: Optional[list[str]],
    project_path: Optional[str],
) -> Config:
    """Create config from CLI options."""
    # Start with env + project detection
    project_root = Path(project_path) if project_path else None
    config = Config.from_env_and_project(project_root)

    # Override with CLI options
    if provider:
        config.provider = provider
    if bundles:
        config.bundles = list(bundles)

    return config


async def _save_session_metadata(
    app: AmplifierApp, config: Config, last_prompt: str
):
    """Save session metadata for resumption.

    Note: This saves metadata (for user reference), not session state.
    Foundation manages session state during the session lifetime.
    """
    try:
        from ..session_manager import SessionManager

        manager = SessionManager(config.project_root)
        manager.save_session_metadata(
            app.session.session_id,
            {
                "last_prompt": last_prompt[:100],  # Truncate
                "provider": config.provider,
                "project_root": str(config.project_root) if config.project_root else None,
            },
        )
    except Exception:
        # Session metadata is optional, don't fail if it doesn't work
        pass
