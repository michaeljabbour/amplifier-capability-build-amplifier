"""
Configuration management for Amplifier CLI.

Follows foundation principles:
- Environment variables are first-class
- Config files ARE bundles (reuse mechanism)
- Project-scoped configuration via directory search
- Simple dataclass (no complex merging)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Application configuration.

    Configuration sources (in precedence order):
    1. CLI flags (highest)
    2. Environment variables
    3. Project config (.amplifier/config.yaml)
    4. Global config (~/.amplifier/config.yaml)
    5. Defaults (lowest)
    """

    # Core settings
    provider: str = field(
        default_factory=lambda: os.getenv(
            "AMPLIFIER_PROVIDER",
            "./providers/anthropic.yaml"
        )
    )
    bundle: Optional[str] = field(
        default_factory=lambda: os.getenv("AMPLIFIER_BUNDLE")
    )
    bundles: list[str] = field(default_factory=list)  # For multiple --bundle flags

    # Project detection
    project_root: Optional[Path] = None

    # API keys
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY")
    )
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )

    # Observability
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )

    # UI preferences
    no_color: bool = False
    verbose: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls()

    @classmethod
    def from_env_and_project(cls, project_root: Optional[Path] = None) -> "Config":
        """Create config from environment + project detection.

        Args:
            project_root: Override project root (defaults to auto-detection)

        Returns:
            Config instance with project root set
        """
        from .project import ProjectManager

        config = cls()

        # Detect project root if not provided
        if project_root is None:
            manager = ProjectManager()
            project_root = manager.get_project_root()

        config.project_root = project_root
        return config

    def validate(self) -> None:
        """Validate required configuration.

        Raises:
            ValueError: If required config is missing
        """
        # Check if any API key is available
        if not self.anthropic_api_key and not self.openai_api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY or OPENAI_API_KEY "
                "environment variable."
            )

        # Validate provider path exists
        provider_path = Path(self.provider)
        if not provider_path.is_absolute():
            # Try relative to cwd or project root
            if self.project_root:
                provider_path = self.project_root / self.provider

            if not provider_path.exists():
                # Try as git URL (starts with git+)
                if not self.provider.startswith("git+"):
                    raise ValueError(
                        f"Provider not found: {self.provider}\n"
                        f"  Searched: {provider_path}\n"
                        f"  Try: amplifier bundle list"
                    )

    def get_api_key(self, provider_name: str) -> Optional[str]:
        """Get API key for a specific provider.

        Args:
            provider_name: Provider name (e.g., "anthropic", "openai")

        Returns:
            API key if found, None otherwise
        """
        provider_map = {
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
        }
        return provider_map.get(provider_name.lower())

    def get_bundle_paths(self) -> list[str]:
        """Get all bundle paths to load.

        Returns list including:
        - Explicit bundles from --bundle flags
        - Single bundle from --bundle flag or AMPLIFIER_BUNDLE env var

        Returns:
            List of bundle paths to compose
        """
        paths = []

        # Multiple bundles from --bundle flags
        if self.bundles:
            paths.extend(self.bundles)

        # Single bundle from flag or env
        if self.bundle and self.bundle not in paths:
            paths.append(self.bundle)

        return paths

    def __repr__(self) -> str:
        """Safe repr that doesn't show API keys."""
        return (
            f"Config("
            f"provider={self.provider!r}, "
            f"bundle={self.bundle!r}, "
            f"project_root={self.project_root}, "
            f"api_key={'***' if self.anthropic_api_key or self.openai_api_key else 'None'}"
            f")"
        )
