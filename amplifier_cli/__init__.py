"""
Amplifier CLI - Foundation-based command-line interface.

This is a lightweight CLI (~1,500 LOC) built directly on amplifier-foundation,
demonstrating the power of the composable architecture without reimplementation.

Key Features:
- Direct foundation workflow: load_bundle → compose → prepare → create_session
- Bundle composition for configuration
- Agent delegation via spawn()
- Project-scoped configuration
- Session persistence
- Rich terminal UI

Architecture:
- App Layer: CLI commands, config search, session metadata (~1,500 LOC)
- Foundation Layer: Session management, bundles, tools, hooks (~10,000+ LOC)

This achieves 85% code reduction vs amplifier-app-cli by using foundation directly.
"""

__version__ = "0.1.0"

from .app import AmplifierApp
from .config import Config

__all__ = ["AmplifierApp", "Config", "__version__"]
