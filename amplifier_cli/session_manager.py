"""
Session metadata storage and management.

IMPORTANT: This stores metadata ONLY (for user reference), NOT session state.
Foundation manages session state during the session lifetime.

This thin layer (~50 lines) allows users to:
- List past sessions
- See what they worked on
- Reference past context

Contrast with app-cli's SessionStore: 479 lines with atomic ops, backups, corruption recovery.
We achieve 90% code reduction by not trying to persist session state.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class SessionManager:
    """Lightweight session metadata storage."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize session manager.

        Args:
            project_root: Project root for project-scoped sessions
                         (None = global sessions)
        """
        if project_root:
            from .project import ProjectManager

            manager = ProjectManager()
            project_storage = manager.get_project_storage(project_root)
            self.storage = project_storage / "sessions"
        else:
            # Global sessions
            self.storage = Path.home() / ".amplifier" / "sessions"

        self.storage.mkdir(parents=True, exist_ok=True)

    def save_session_metadata(self, session_id: str, metadata: dict):
        """Save session metadata.

        Metadata includes:
        - session_id
        - created_at
        - last_prompt
        - provider
        - project_root

        Args:
            session_id: Foundation-provided session ID
            metadata: Additional metadata to store
        """
        path = self.storage / f"{session_id}.json"
        metadata.update(
            {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
            }
        )
        path.write_text(json.dumps(metadata, indent=2))

    def list_sessions(self) -> list[dict]:
        """List all sessions (most recent first).

        Returns:
            List of session metadata dicts
        """
        sessions = []
        for path in self.storage.glob("*.json"):
            try:
                metadata = json.loads(path.read_text())
                sessions.append(metadata)
            except (json.JSONDecodeError, KeyError):
                # Skip invalid metadata
                continue

        return sorted(sessions, key=lambda s: s.get("created_at", ""), reverse=True)

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get metadata for a specific session.

        Args:
            session_id: Session ID to retrieve

        Returns:
            Session metadata dict, or None if not found
        """
        path = self.storage / f"{session_id}.json"
        if not path.exists():
            return None

        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, KeyError):
            return None

    def delete_session(self, session_id: str):
        """Delete session metadata.

        Args:
            session_id: Session ID to delete
        """
        path = self.storage / f"{session_id}.json"
        if path.exists():
            path.unlink()
