"""
Project detection and isolation.

Provides lightweight project management:
- Auto-detect project root (.git or .amplifier directory)
- Generate stable project IDs
- Per-project session storage
- Config file discovery

This is a thin layer - foundation handles actual session state.
"""

import hashlib
import json
from pathlib import Path
from typing import Optional


class ProjectManager:
    """Lightweight project detection and storage management."""

    def get_project_root(self) -> Path:
        """Find project root by searching for .git or .amplifier directory.

        Searches up the directory tree from current working directory.
        Stops at first .git or .amplifier directory, or at home directory.

        Returns:
            Project root path (may be cwd if no project markers found)
        """
        cwd = Path.cwd()

        # Search up to git root or home
        for parent in [cwd, *cwd.parents]:
            # Check for project markers
            if (parent / ".git").exists() or (parent / ".amplifier").exists():
                return parent

            # Stop at home directory
            if parent == Path.home():
                return cwd

        # No project found, use cwd
        return cwd

    def get_project_id(self, project_root: Path) -> str:
        """Generate stable project ID from path.

        Uses MD5 hash of absolute path for stability across invocations.

        Args:
            project_root: Project root directory

        Returns:
            8-character hex project ID
        """
        return hashlib.md5(str(project_root.resolve()).encode()).hexdigest()[:8]

    def get_project_storage(self, project_root: Path) -> Path:
        """Get project-specific storage directory.

        Storage structure:
            ~/.amplifier/projects/{project_id}/
                sessions/           # Session metadata
                config.yaml         # Symlink to project config (optional)
                project.json        # Project metadata

        Args:
            project_root: Project root directory

        Returns:
            Project storage path (created if doesn't exist)
        """
        project_id = self.get_project_id(project_root)
        storage = Path.home() / ".amplifier" / "projects" / project_id
        storage.mkdir(parents=True, exist_ok=True)

        # Store metadata for project list
        meta_file = storage / "project.json"
        if not meta_file.exists():
            metadata = {
                "project_id": project_id,
                "root_path": str(project_root.resolve()),
                "name": project_root.name,
            }
            meta_file.write_text(json.dumps(metadata, indent=2))

        return storage

    def find_project_config(
        self, project_root: Optional[Path] = None
    ) -> Optional[Path]:
        """Search for project config file.

        Searches for .amplifier/config.yaml starting from project root,
        up to git root or home directory.

        Args:
            project_root: Starting point (defaults to detected project root)

        Returns:
            Path to config file if found, None otherwise
        """
        if project_root is None:
            project_root = self.get_project_root()

        # Search up to git root or home
        for parent in [project_root, *project_root.parents]:
            # Stop at git root
            if (parent / ".git").exists():
                config = parent / ".amplifier" / "config.yaml"
                if config.exists():
                    return config
                return None

            # Check for config
            config = parent / ".amplifier" / "config.yaml"
            if config.exists():
                return config

            # Stop at home
            if parent == Path.home():
                return None

        return None

    def list_projects(self) -> list[dict]:
        """List all known projects.

        Returns:
            List of project metadata dicts with keys:
                - project_id: 8-char hex ID
                - root_path: absolute path to project
                - name: project directory name
        """
        projects_dir = Path.home() / ".amplifier" / "projects"
        if not projects_dir.exists():
            return []

        projects = []
        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            meta_file = project_dir / "project.json"
            if meta_file.exists():
                try:
                    metadata = json.loads(meta_file.read_text())
                    projects.append(metadata)
                except (json.JSONDecodeError, KeyError):
                    # Skip invalid metadata
                    continue

        return sorted(projects, key=lambda p: p.get("name", ""))
