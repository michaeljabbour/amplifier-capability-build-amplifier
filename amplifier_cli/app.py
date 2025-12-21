"""
Core AmplifierApp class - Foundation-based application.

This is the heart of the CLI, demonstrating the canonical foundation pattern:
    load_bundle() → compose() → prepare() → create_session() → execute()

Key Principles:
- Direct foundation API usage (no reimplementation)
- Bundle composition for configuration
- Foundation handles session state
- Thin app layer for CLI concerns
"""

from pathlib import Path
from typing import Any, Optional

from amplifier_foundation import Bundle, PreparedBundle, Session, load_bundle

from .config import Config


class AmplifierApp:
    """Foundation-based CLI application.

    Follows the canonical pattern:
        load_bundle() → compose() → prepare() → create_session() → execute()

    The app layer provides:
    - Bundle search paths and composition order
    - Config file discovery
    - Session metadata tracking (not state!)
    - Error message formatting

    Foundation provides:
    - Session management (context, history)
    - Bundle loading (local, git)
    - Module downloading and caching
    - @mention resolution
    - Streaming orchestration
    - Hook system
    - Tool system
    """

    def __init__(self, config: Config):
        """Initialize app with configuration.

        Args:
            config: Application configuration
        """
        self.config = config
        self.session: Optional[Session] = None
        self.prepared: Optional[PreparedBundle] = None

    async def initialize(self) -> None:
        """Initialize app: load → compose → prepare → session.

        This follows the foundation workflow strictly:
        1. Load foundation bundle
        2. Load provider bundle
        3. Load any additional bundles (config, explicit)
        4. Compose all bundles (later wins)
        5. Prepare (downloads modules, resolves @mentions)
        6. Create session

        The composed bundle is the complete configuration.
        Config files ARE bundles, reusing the same mechanism.
        """
        bundles: list[Bundle] = []

        # 1. Load foundation (base layer)
        foundation = await load_bundle(
            "git+https://github.com/microsoft/amplifier-foundation@main"
        )
        bundles.append(foundation)

        # 2. Load provider (required)
        provider = await load_bundle(self.config.provider)
        bundles.append(provider)

        # 3. Load global config if exists (bundles ARE configs!)
        global_config_path = Path.home() / ".amplifier" / "config.yaml"
        if global_config_path.exists():
            global_config = await load_bundle(str(global_config_path))
            bundles.append(global_config)

        # 4. Load project config if exists
        if self.config.project_root:
            from .project import ProjectManager

            manager = ProjectManager()
            project_config_path = manager.find_project_config(self.config.project_root)
            if project_config_path:
                project_config = await load_bundle(str(project_config_path))
                bundles.append(project_config)

        # 5. Load explicit bundles from CLI
        for bundle_path in self.config.get_bundle_paths():
            bundle = await load_bundle(bundle_path)
            bundles.append(bundle)

        # 6. Compose all bundles (later overrides earlier)
        composed = bundles[0]
        for bundle in bundles[1:]:
            composed = composed.compose(bundle)

        # 7. Prepare (downloads modules, resolves @mentions)
        # This is where foundation does heavy lifting:
        # - Downloads git-sourced modules
        # - Caches downloaded modules
        # - Resolves @namespace:path references
        # - Validates module schemas
        self.prepared = await composed.prepare()

        # 8. Create session
        # Foundation manages session state, context window, etc.
        self.session = await self.prepared.create_session()

    async def execute(self, prompt: str) -> str:
        """Execute a prompt against the current session.

        Args:
            prompt: User prompt to execute

        Returns:
            AI response

        Raises:
            RuntimeError: If app not initialized
        """
        if not self.session:
            raise RuntimeError("App not initialized. Call initialize() first.")

        # Foundation handles:
        # - Context management (adding to history)
        # - Streaming orchestration
        # - Hook execution
        # - Tool calling
        # - Response generation
        return await self.session.execute(prompt)

    async def spawn_agent(
        self,
        agent_path: str,
        instruction: str,
        session_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Spawn an agent sub-session.

        Uses foundation's spawn() directly - no wrapper needed!

        Args:
            agent_path: Path to agent bundle (local or git URL)
            instruction: Task instruction for agent
            session_id: Session ID to resume (None = new session)

        Returns:
            dict with:
                - output: Agent's response
                - session_id: Session ID (for resumption)

        Raises:
            RuntimeError: If app not initialized
        """
        if not self.prepared or not self.session:
            raise RuntimeError("App not initialized. Call initialize() first.")

        # Load agent bundle
        agent_bundle = await load_bundle(agent_path)

        # Spawn using foundation
        # Foundation handles:
        # - Session creation/resumption
        # - Context inheritance (compose=True)
        # - W3C trace context propagation
        # - Agent execution
        return await self.prepared.spawn(
            child_bundle=agent_bundle,
            instruction=instruction,
            compose=True,  # Compose with parent (inherits config)
            parent_session=self.session,
            session_id=session_id,  # None = new, or ID to resume
        )

    async def shutdown(self) -> None:
        """Clean up resources.

        Foundation's session.cleanup() handles:
        - Context cleanup
        - Tool cleanup
        - Hook cleanup
        - Resource release
        """
        if self.session:
            await self.session.cleanup()

    async def __aenter__(self) -> "AmplifierApp":
        """Context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Context manager exit."""
        await self.shutdown()


# Example usage
async def example_usage() -> None:
    """Example of using AmplifierApp."""
    import asyncio

    from .config import Config

    # Create config
    config = Config.from_env_and_project()
    config.validate()

    # Use as context manager (recommended)
    async with AmplifierApp(config) as app:
        # Execute prompt
        response = await app.execute("Hello, world!")
        print(response)

        # Multi-turn conversation
        response = await app.execute("What did I just say?")
        print(response)

        # Spawn agent
        result = await app.spawn_agent(
            "./agents/bug-hunter.md", "Find bugs in auth.py"
        )
        print(result["output"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_usage())
