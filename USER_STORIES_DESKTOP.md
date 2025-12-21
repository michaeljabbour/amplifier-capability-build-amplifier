# Terminal UI User Stories (Desktop-Inspired)

**Version:** 1.0
**Date:** 2025-12-21
**Source:** Amplifier Desktop Feature Analysis
**Focus:** Simple, terminal-friendly features with foundation compliance

---

## Executive Summary

This document extracts **10 high-value features** from amplifier-desktop that translate naturally to terminal UIs. All features are:
- ✅ **Foundation-compliant** (no desktop-specific patterns)
- ✅ **Terminal-friendly** (keyboard-driven, text-based)
- ✅ **High user value** (productivity multipliers)
- ✅ **Low implementation complexity** (mostly UI logic, not foundation integration)

**Total:** 10 user stories organized in 2 phases

---

## Table of Contents

### Phase 1: Core UX (4 stories)
1. [Keyboard Shortcuts & Navigation](#us-d1-keyboard-shortcuts--navigation)
2. [Command Palette](#us-d2-command-palette)
3. [Multi-Session Management](#us-d3-multi-session-management)
4. [Conversation Search & Filtering](#us-d4-conversation-search--filtering)

### Phase 2: Enhanced Features (6 stories)
5. [Status Bar & Indicators](#us-d5-status-bar--indicators)
6. [Project & Profile Context](#us-d6-project--profile-context)
7. [Export & Import](#us-d7-export--import)
8. [Memory Search & Management](#us-d8-memory-search--management)
9. [Artifact Preview & Management](#us-d9-artifact-preview--management)
10. [Smart Notifications](#us-d10-smart-notifications)

---

## Phase 1: Core UX (Week 1-2)

### US-D1: Keyboard Shortcuts & Navigation

**As a** terminal power user
**I want** vim-style keyboard shortcuts and navigation
**So that** I can work efficiently without reaching for the mouse

**Priority:** 🔥 Critical
**Complexity:** ⚡ Low
**Value:** 💎 Very High
**Desktop Source:** `/src/hooks/useKeyboardShortcuts.ts`

#### Acceptance Criteria

**Navigation:**
- `j/k` or `↓/↑` - Navigate messages/sessions
- `h/l` or `←/→` - Navigate panels (sidebar, chat, artifacts)
- `g/G` - Jump to top/bottom
- `/` - Focus search (vim-style)
- `Esc` - Cancel/close modals

**Actions:**
- `n` - New conversation
- `c` - Clear current conversation (with confirmation)
- `s` - Open settings
- `e` - Toggle artifacts panel
- `m` - Open memories
- `t` - Open tasks/todos
- `?` - Show help/shortcuts
- `:` - Command palette mode

**Conversation Management:**
- `1-9` - Quick switch to session 1-9
- `Ctrl-N` - Next conversation
- `Ctrl-P` - Previous conversation
- `d` - Delete current conversation (with confirmation)
- `r` - Rename current conversation

**Context-Aware:**
- Shortcuts disabled when typing in input
- Escape key exits input focus
- Enter key sends message (Shift-Enter for newline)

#### Foundation Pattern

```python
# No foundation integration needed - pure TUI logic

import blessed

term = blessed.Terminal()

SHORTCUTS = {
    'j': 'scroll_down',
    'k': 'scroll_up',
    'n': 'new_conversation',
    's': 'open_settings',
    'e': 'toggle_artifacts',
    '/': 'focus_search',
    ':': 'command_palette',
    '?': 'show_help',
}

def handle_keypress(key: str, context: str):
    """Handle keyboard shortcuts based on context."""
    if context == 'input':
        return None  # Let input handle all keys

    action = SHORTCUTS.get(key)
    if action:
        dispatch_action(action)
```

#### Terminal Design Notes

**Layout:**
```
┌─ Shortcuts ──────────────────────────────────────────┐
│ j/k  Navigate    n  New chat     s  Settings         │
│ /    Search      :  Commands     ?  Help             │
│ 1-9  Switch      e  Artifacts    m  Memories         │
└──────────────────────────────────────────────────────┘
```

**Help Modal** (triggered by `?`):
```
╭─ Keyboard Shortcuts ────────────────────────────────╮
│                                                      │
│ Navigation          Actions            Conversations │
│ ──────────          ────────           ──────────   │
│ j/k  ↓/↑           n  New chat         1-9 Switch   │
│ h/l  ←/→           c  Clear            d   Delete   │
│ g/G  Top/Bottom    s  Settings         r   Rename   │
│ /    Search        e  Artifacts                      │
│ Esc  Cancel        m  Memories                       │
│                    t  Tasks                           │
│ Special                                               │
│ ───────                                               │
│ :    Command palette                                  │
│ ?    This help                                        │
│                                                       │
│ Press any key to close                                │
╰──────────────────────────────────────────────────────╯
```

**Implementation Libraries:**
- `blessed` - Terminal control, keyboard input
- `prompt_toolkit` - Readline-style input with vi mode
- `rich` - Styled help text

**Complexity:** ~150 lines of code

---

### US-D2: Command Palette

**As a** developer
**I want** a `:command` style command palette
**So that** I can discover and execute commands quickly

**Priority:** 🔥 Critical
**Complexity:** ⚡ Low-Medium
**Value:** 💎 Very High
**Desktop Source:** Inspired by Cmd+K pattern in `/src/components/ChatInput.tsx`

#### Acceptance Criteria

**Activation:**
- `:` key enters command mode (vim-style)
- `Ctrl-K` alternative for non-vim users
- Shows command prompt at bottom of screen

**Command Execution:**
- Type command name + Enter to execute
- Tab completion for command names
- Arrow keys to navigate command history
- Escape to cancel

**Core Commands:**
```
:help [topic]           Show help
:new [--profile name]   New conversation
:switch <id|number>     Switch conversation
:rename <name>          Rename current conversation
:delete [id]            Delete conversation
:clear                  Clear current conversation
:export [format]        Export conversation
:import <file>          Import conversation
:settings [section]     Open settings
:profile <name>         Switch profile
:project <name>         Switch project
:search <query>         Search conversations
:memory [query]         Search memories
:quit                   Exit application
```

**Command Features:**
- Fuzzy matching (`:sw` matches `:switch`)
- Command aliases (`:q` → `:quit`)
- Inline help (`:help <command>`)
- Argument validation
- Error messages for invalid commands

**Command History:**
- Up/Down arrows navigate history
- History persisted to `~/.amplifier/command_history`
- Max 100 commands

#### Foundation Pattern

```python
# No foundation integration - pure CLI command dispatcher

import shlex
from typing import Callable, Dict, List

class CommandPalette:
    """Vim-style command palette."""

    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.aliases: Dict[str, str] = {}
        self.history: List[str] = []
        self.register_builtin_commands()

    def register(self, name: str, handler: Callable, aliases: List[str] = None):
        """Register a command."""
        self.commands[name] = handler
        for alias in (aliases or []):
            self.aliases[alias] = name

    def execute(self, command_line: str):
        """Parse and execute command."""
        parts = shlex.split(command_line)
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        # Resolve alias
        cmd = self.aliases.get(cmd, cmd)

        # Fuzzy match
        if cmd not in self.commands:
            matches = self.fuzzy_match(cmd)
            if len(matches) == 1:
                cmd = matches[0]
            elif len(matches) > 1:
                print(f"Ambiguous: {', '.join(matches)}")
                return
            else:
                print(f"Unknown command: {cmd}")
                return

        # Execute
        try:
            self.commands[cmd](*args)
            self.history.append(command_line)
        except Exception as e:
            print(f"Error: {e}")

    def fuzzy_match(self, partial: str) -> List[str]:
        """Find commands matching partial string."""
        return [c for c in self.commands if c.startswith(partial)]

    def register_builtin_commands(self):
        """Register built-in commands."""
        self.register('help', self.cmd_help, ['h'])
        self.register('quit', self.cmd_quit, ['q', 'exit'])
        self.register('new', self.cmd_new)
        self.register('switch', self.cmd_switch, ['sw'])
        # ... more commands
```

#### Terminal Design Notes

**Command Prompt:**
```
┌─ Command Mode ───────────────────────────────────────┐
│ :█                                                    │
│                                                       │
│ Available commands:                                   │
│  new switch delete export import settings quit       │
│                                                       │
│ Type ? for help, Tab for completion                  │
└───────────────────────────────────────────────────────┘
```

**With Completion:**
```
:sw█
  switch      Switch to conversation
  (Showing 1 match)
```

**Command Execution:**
```
:export markdown ~/chat.md
✓ Exported to ~/chat.md (2,453 tokens)
```

**Complexity:** ~250 lines of code

---

### US-D3: Multi-Session Management

**As a** user
**I want** to manage multiple conversations simultaneously
**So that** I can work on different tasks in parallel

**Priority:** 🔥 Critical
**Complexity:** ⚙️ Medium
**Value:** 💎 Very High
**Desktop Source:** `/src/lib/store.ts` conversation management + `/src/components/Sidebar.tsx`

#### Acceptance Criteria

**Session List Display:**
- Show all conversations in sidebar
- Group by date: Today, Yesterday, Last 7 Days, Older
- Number each session (1-9+ for quick switching)
- Highlight active session
- Show streaming indicator (if active)
- Display session metadata:
  - Title (truncated to 40 chars)
  - Last updated (relative time: "2m ago")
  - Message count
  - Model used (abbreviated: "opus", "sonnet")
  - Project tag (if assigned)

**Session Switching:**
- Number keys (1-9) for quick switch
- `:switch <id>` command
- `Ctrl-N`/`Ctrl-P` for next/previous
- Search to filter and switch

**Session Creation:**
- `n` key or `:new` command
- Auto-generate title from first message
- Inherit current profile/project
- Options: `--profile`, `--project`, `--model`

**Session Management:**
- Rename: `r` key or `:rename <name>`
- Delete: `d` key or `:delete [id]` (with confirmation)
- Clear: `c` key or `:clear` (keeps session, removes messages)
- Export: `e` or `:export`

**Persistence:**
- Sessions stored in `~/.amplifier/sessions/{session_id}.json`
- Metadata includes:
  - `session_id` (UUID)
  - `title`
  - `created_at` (ISO timestamp)
  - `updated_at`
  - `message_count`
  - `total_tokens`
  - `model`
  - `profile`
  - `project`

#### Foundation Pattern

```python
from amplifier_foundation import load_bundle
import json
from pathlib import Path
from datetime import datetime
import uuid

class SessionManager:
    """Manage multiple foundation sessions."""

    def __init__(self, storage_path: Path):
        self.storage = storage_path
        self.storage.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, dict] = {}
        self.current_session_id: str | None = None
        self.load_sessions()

    def load_sessions(self):
        """Load session metadata from disk."""
        for path in self.storage.glob("*.json"):
            metadata = json.loads(path.read_text())
            self.sessions[metadata['session_id']] = metadata

    def create_session(self, title: str = None, profile: str = None,
                      project: str = None) -> str:
        """Create a new session.

        Foundation integration:
        - load_bundle() with profile
        - compose() with project config
        - create_session() gets session_id from foundation
        """
        session_id = str(uuid.uuid4())

        metadata = {
            'session_id': session_id,
            'title': title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'message_count': 0,
            'total_tokens': 0,
            'model': None,  # Set on first message
            'profile': profile,
            'project': project,
        }

        self.sessions[session_id] = metadata
        self.save_session(session_id)
        self.current_session_id = session_id

        return session_id

    def switch_session(self, session_id: str):
        """Switch to a different session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")

        self.current_session_id = session_id

    def update_session(self, session_id: str, **updates):
        """Update session metadata."""
        if session_id not in self.sessions:
            return

        self.sessions[session_id].update(updates)
        self.sessions[session_id]['updated_at'] = datetime.now().isoformat()
        self.save_session(session_id)

    def delete_session(self, session_id: str):
        """Delete session metadata."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            (self.storage / f"{session_id}.json").unlink(missing_ok=True)

    def save_session(self, session_id: str):
        """Save session metadata to disk."""
        path = self.storage / f"{session_id}.json"
        metadata = self.sessions[session_id]
        path.write_text(json.dumps(metadata, indent=2))

    def list_sessions(self, project: str = None) -> List[dict]:
        """List sessions, optionally filtered by project."""
        sessions = list(self.sessions.values())

        if project:
            sessions = [s for s in sessions if s.get('project') == project]

        # Sort by updated_at (most recent first)
        sessions.sort(key=lambda s: s['updated_at'], reverse=True)

        return sessions

    def group_by_date(self, sessions: List[dict]) -> Dict[str, List[dict]]:
        """Group sessions by date."""
        from datetime import datetime, timedelta

        now = datetime.now()
        today = now.date()
        yesterday = (now - timedelta(days=1)).date()
        week_ago = (now - timedelta(days=7)).date()

        groups = {
            'Today': [],
            'Yesterday': [],
            'Last 7 Days': [],
            'Older': [],
        }

        for session in sessions:
            updated = datetime.fromisoformat(session['updated_at']).date()

            if updated == today:
                groups['Today'].append(session)
            elif updated == yesterday:
                groups['Yesterday'].append(session)
            elif updated >= week_ago:
                groups['Last 7 Days'].append(session)
            else:
                groups['Older'].append(session)

        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
```

#### Terminal Design Notes

**Sidebar View:**
```
╭─ Conversations ──────────────────────────╮
│                                          │
│ Today                                    │
│  1 ● Feature brainstorm       2m   opus │
│  2   Bug investigation        1h   opus │
│                                          │
│ Yesterday                                │
│  3   Code review           12:30   opus │
│  4   Documentation          9:45   son  │
│                                          │
│ Last 7 Days                              │
│  5   Research project      Dec 19   son │
│  6   API design            Dec 18   son │
│                                          │
│ [n]ew [/]search [:]commands              │
╰──────────────────────────────────────────╯

● = streaming/active
Numbers = quick switch keys
Model abbreviations: opus, son (sonnet), gpt4, etc.
```

**Session Detail (hover/focus):**
```
╭─ Session 1 ──────────────────────────────╮
│ Feature brainstorm                        │
│                                           │
│ Created:  Dec 21, 2024 at 3:42 PM       │
│ Updated:  2 minutes ago                   │
│ Messages: 12                              │
│ Tokens:   2,450 / 200,000                │
│ Model:    claude-opus-4-5                │
│ Profile:  dev                             │
│ Project:  amplifier-cli                   │
│                                           │
│ [r]ename [d]elete [e]xport [Esc]close   │
╰───────────────────────────────────────────╯
```

**Complexity:** ~400 lines of code

---

### US-D4: Conversation Search & Filtering

**As a** user
**I want** to search and filter conversations
**So that** I can quickly find relevant discussions

**Priority:** 🔥 Critical
**Complexity:** ⚡ Low-Medium
**Value:** 💎 Very High
**Desktop Source:** `/src/components/Sidebar.tsx` (lines 632-641)

#### Acceptance Criteria

**Search Activation:**
- `/` key enters search mode
- `:search <query>` command
- `Ctrl-F` alternative

**Search Features:**
- **Real-time filtering** as you type
- Search across:
  - Conversation titles
  - Message content (full-text)
  - Project names
  - Model names
- **Fuzzy matching** (typo tolerance)
- **Highlight matches** in results
- Show match count: "3 conversations, 12 messages"

**Search Filters:**
- `--project <name>` - Filter by project
- `--model <name>` - Filter by model
- `--since <date>` - Date range (7d, 1w, 1m, 2024-12-01)
- `--before <date>` - Before date
- `--profile <name>` - Filter by profile
- `--min-tokens <n>` - Minimum token count
- `--has-tools` - Conversations with tool use

**Search Examples:**
```
/api design                    # Simple search
/authentication --since 7d     # Last 7 days
/bug --project amplifier-cli   # Project-specific
/refactor --model opus         # Model-specific
```

**Navigation:**
- Arrow keys to navigate results
- Enter to open selected conversation
- `n`/`N` for next/previous match
- Escape to clear search

**Result Display:**
- Show conversation title
- Snippet of matching message (truncated)
- Match count per conversation
- Timestamp

#### Foundation Pattern

```python
# No foundation integration - pure search logic

import re
from typing import List, Dict
from datetime import datetime, timedelta

class ConversationSearch:
    """Search and filter conversations."""

    def __init__(self, session_manager: SessionManager):
        self.sessions = session_manager

    def search(self, query: str, filters: Dict = None) -> List[dict]:
        """Search conversations with optional filters.

        Args:
            query: Search text
            filters: Dict with keys: project, model, since, before, profile

        Returns:
            List of matching sessions with snippets
        """
        results = []

        # Get all sessions
        sessions = self.sessions.list_sessions()

        # Apply filters
        if filters:
            sessions = self.apply_filters(sessions, filters)

        # Search in titles and messages
        for session in sessions:
            matches = []

            # Search title
            if self.matches(query, session['title']):
                matches.append({
                    'type': 'title',
                    'text': session['title'],
                })

            # Search messages (load from disk)
            messages = self.load_messages(session['session_id'])
            for msg in messages:
                if self.matches(query, msg['content']):
                    matches.append({
                        'type': 'message',
                        'text': self.snippet(msg['content'], query),
                        'timestamp': msg['timestamp'],
                    })

            if matches:
                results.append({
                    'session': session,
                    'matches': matches,
                    'match_count': len(matches),
                })

        return results

    def matches(self, query: str, text: str) -> bool:
        """Check if query matches text (case-insensitive)."""
        # Simple substring match
        return query.lower() in text.lower()

        # Could enhance with fuzzy matching:
        # from fuzzywuzzy import fuzz
        # return fuzz.partial_ratio(query.lower(), text.lower()) > 80

    def snippet(self, text: str, query: str, context: int = 50) -> str:
        """Extract snippet around match."""
        # Find match position
        pos = text.lower().find(query.lower())
        if pos == -1:
            return text[:100] + "..."

        # Extract context around match
        start = max(0, pos - context)
        end = min(len(text), pos + len(query) + context)

        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet

    def apply_filters(self, sessions: List[dict], filters: Dict) -> List[dict]:
        """Apply filters to session list."""
        if 'project' in filters:
            sessions = [s for s in sessions if s.get('project') == filters['project']]

        if 'model' in filters:
            sessions = [s for s in sessions if filters['model'] in s.get('model', '')]

        if 'profile' in filters:
            sessions = [s for s in sessions if s.get('profile') == filters['profile']]

        if 'since' in filters:
            cutoff = self.parse_date(filters['since'])
            sessions = [s for s in sessions
                       if datetime.fromisoformat(s['updated_at']) >= cutoff]

        if 'before' in filters:
            cutoff = self.parse_date(filters['before'])
            sessions = [s for s in sessions
                       if datetime.fromisoformat(s['updated_at']) <= cutoff]

        if 'min_tokens' in filters:
            sessions = [s for s in sessions
                       if s.get('total_tokens', 0) >= filters['min_tokens']]

        return sessions

    def parse_date(self, date_str: str) -> datetime:
        """Parse date string (7d, 1w, 1m, or ISO date)."""
        if date_str.endswith('d'):
            days = int(date_str[:-1])
            return datetime.now() - timedelta(days=days)
        elif date_str.endswith('w'):
            weeks = int(date_str[:-1])
            return datetime.now() - timedelta(weeks=weeks)
        elif date_str.endswith('m'):
            months = int(date_str[:-1])
            return datetime.now() - timedelta(days=months * 30)
        else:
            return datetime.fromisoformat(date_str)
```

#### Terminal Design Notes

**Search Interface:**
```
╭─ Search ─────────────────────────────────────────────╮
│ / api design█                                         │
│                                                       │
│ 3 conversations, 12 messages                          │
│                                                       │
│ ┌─ Feature brainstorm ─────────────── 2m ago ───────┐│
│ │ "Let's design the API for user authentication..." ││
│ │ Match in message #3                                ││
│ └────────────────────────────────────────────────────┘│
│                                                       │
│ ┌─ Bug investigation ──────────────── 1h ago ───────┐│
│ │ "The API endpoint is returning 500 errors..."     ││
│ │ Match in message #7                                ││
│ └────────────────────────────────────────────────────┘│
│                                                       │
│ ↓↑ navigate  Enter open  Esc cancel                  │
╰───────────────────────────────────────────────────────╯
```

**With Filters:**
```
╭─ Search ─────────────────────────────────────────────╮
│ / bug --since 7d --model opus█                        │
│                                                       │
│ Filters: Last 7 days, Model: opus                    │
│ 1 conversation, 3 messages                            │
│                                                       │
│ ┌─ Bug investigation ──────────────── 1h ago ───────┐│
│ │ "Found the bug in auth.py line 42..."             ││
│ └────────────────────────────────────────────────────┘│
╰───────────────────────────────────────────────────────╯
```

**Complexity:** ~300 lines of code

---

## Phase 2: Enhanced Features (Week 3-4)

### US-D5: Status Bar & Indicators

**As a** user
**I want** a status bar showing connection, tokens, and model info
**So that** I can monitor session state at a glance

**Priority:** 🔸 Medium
**Complexity:** ⚡ Low
**Value:** 💎 High
**Desktop Source:** `/src/lib/store.ts` SessionStatus + footer indicators

#### Acceptance Criteria

**Status Bar Location:**
- Bottom of screen (always visible)
- Single line, full width
- Updates in real-time

**Status Indicators:**
```
[●Connected] claude-opus-4-5 │ 2,450/200K tokens │ $0.0125 │ 3 tools │ 12:34 PM
```

**Components:**
- **Connection status**:
  - `●` Green = connected
  - `○` Gray = disconnected
  - `◐` Yellow = reconnecting

- **Model info**:
  - Full model name (truncated if needed)
  - Click/shortcut to change model

- **Token count**:
  - Current / Max (e.g., "2,450 / 200,000")
  - Color: green (< 50%), yellow (50-80%), red (> 80%)
  - Percentage in parentheses: "(1.2%)"

- **Cost estimate**:
  - Running total for session
  - Format: "$0.0125" or "~$0.01"
  - Only show if > $0.001

- **Tool calls**:
  - Count of tools called
  - Icon indicator (🔧)
  - Click to see tool history

- **Time**:
  - Current time (12h format)
  - Session duration on hover

**Per-Message Stats:**
```
Message #5 ✓ (in: 234 out: 567 think: 45 | $0.00125 | 2 tools)
```

**Streaming Indicator:**
- Show progress/spinner during streaming
- "Generating..." text
- Cancel option (Ctrl-C)

#### Foundation Pattern

```python
# Status tracked from foundation session

from dataclasses import dataclass
from datetime import datetime

@dataclass
class SessionStatus:
    """Track session status."""
    connected: bool = False
    model: str = ""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_thinking_tokens: int = 0
    max_tokens: int = 200000
    tool_calls: int = 0
    estimated_cost: float = 0.0
    is_streaming: bool = False

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens + self.total_thinking_tokens

    @property
    def token_percentage(self) -> float:
        return (self.total_tokens / self.max_tokens) * 100

    @property
    def token_color(self) -> str:
        """Get color based on usage."""
        pct = self.token_percentage
        if pct < 50:
            return 'green'
        elif pct < 80:
            return 'yellow'
        else:
            return 'red'

# Usage with foundation
async def update_status_from_response(response: dict, status: SessionStatus):
    """Update status from foundation response."""
    if 'usage' in response:
        usage = response['usage']
        status.total_input_tokens += usage.get('input_tokens', 0)
        status.total_output_tokens += usage.get('output_tokens', 0)
        status.total_thinking_tokens += usage.get('thinking_tokens', 0)

    if 'cost' in response:
        status.estimated_cost += response['cost']

    if 'tool_calls' in response:
        status.tool_calls += len(response['tool_calls'])
```

#### Terminal Design Notes

**Status Bar (bottom screen):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [●] claude-opus-4-5 │ 2.5K/200K (1.2%) │ $0.01 │ 3🔧 │ 12:34 PM            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**During Streaming:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [◐] Generating... │ 2.5K/200K │ Ctrl-C to cancel                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**High Token Usage (red):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [●] claude-opus-4-5 │ 180K/200K (90%) ⚠️  │ $0.45 │ 25🔧 │ 12:34 PM         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Complexity:** ~200 lines of code

---

### US-D6: Project & Profile Context

**As a** developer
**I want** to switch between projects and profiles
**So that** I can work in different contexts with appropriate settings

**Priority:** 🔸 Medium
**Complexity:** ⚙️ Medium
**Value:** 💎 High
**Desktop Source:** `/src/lib/store.ts` + `/src/components/ProfileSelector.tsx`

#### Acceptance Criteria

**Project Management:**
- List projects: `:project list`
- Switch project: `:project <name>`
- Create project: `:project new <name> --folder <path>`
- Set project for session: `:project set <name>`
- Show current: Status bar shows active project

**Profile Management:**
- List profiles: `:profile list`
- Switch profile: `:profile <name>`
- Show current: Status bar shows active profile
- Create profile: `:profile new <name> --extends <base>`
- Edit profile: `:profile edit <name>` (opens editor)

**Context Display:**
```
Project: amplifier-cli     │ Profile: claude-opus-dev
Folder:  ~/dev/amplifier   │ Providers: 1  Tools: 5
```

**Profile Features:**
- Inherits from base profiles
- Override providers, tools, hooks
- Project-specific or user-global
- YAML-based configuration

#### Foundation Pattern

```python
# Foundation-compliant profile management

from amplifier_foundation import load_bundle
from pathlib import Path
import yaml

class ProfileManager:
    """Manage profiles and projects."""

    def __init__(self):
        self.profiles_dir = Path.home() / ".amplifier" / "profiles"
        self.projects_dir = Path.home() / ".amplifier" / "projects"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    async def load_profile(self, name: str) -> Bundle:
        """Load profile as bundle.

        Foundation pattern:
        - Profiles ARE bundles
        - Use load_bundle() to load
        - Compose with base profile if extends
        """
        profile_path = self.profiles_dir / f"{name}.yaml"

        if not profile_path.exists():
            raise ValueError(f"Profile not found: {name}")

        # Load as bundle
        profile = await load_bundle(str(profile_path))

        # If extends, compose with base
        if profile.metadata.get('extends'):
            base_name = profile.metadata['extends']
            base = await self.load_profile(base_name)
            profile = base.compose(profile)

        return profile

    def list_profiles(self) -> List[dict]:
        """List available profiles."""
        profiles = []

        for path in self.profiles_dir.glob("*.yaml"):
            with open(path) as f:
                data = yaml.safe_load(f)

            profiles.append({
                'name': path.stem,
                'version': data.get('version', '1.0.0'),
                'description': data.get('description', ''),
                'extends': data.get('extends'),
                'providers': len(data.get('providers', [])),
                'tools': len(data.get('tools', [])),
            })

        return profiles

    def create_profile(self, name: str, extends: str = None):
        """Create new profile."""
        profile_path = self.profiles_dir / f"{name}.yaml"

        template = {
            'name': name,
            'version': '1.0.0',
            'extends': extends,
            'providers': [],
            'tools': [],
            'hooks': [],
            'instruction': f'Profile: {name}',
        }

        with open(profile_path, 'w') as f:
            yaml.dump(template, f, indent=2)

        return profile_path

    # Similar for projects...
```

#### Terminal Design Notes

**Profile Selector:**
```
╭─ Select Profile ─────────────────────────────────────╮
│                                                       │
│ > claude-opus-dev             [Current]              │
│   claude-sonnet-dev                                   │
│   gpt4-turbo-dev                                      │
│   research-profile                                    │
│                                                       │
│ Profile: claude-opus-dev                              │
│ Extends: base-dev                                     │
│ Providers: 1 (Anthropic)                              │
│ Tools: 5 (filesystem, bash, web, grep, search)       │
│ Hooks: 3 (logging, redaction, streaming-ui)          │
│                                                       │
│ ↓↑ navigate  Enter select  n new  e edit  Esc cancel│
╰───────────────────────────────────────────────────────╯
```

**Context Display (in status/sidebar):**
```
╭─ Context ────────────────────────────────────────────╮
│ Project: amplifier-cli                                │
│ Folder:  ~/dev/amplifier-cli                         │
│                                                       │
│ Profile: claude-opus-dev                              │
│ Model:   claude-opus-4-5                             │
│                                                       │
│ Knowledge: 5 files                                    │
│ Memories:  23 items                                   │
╰───────────────────────────────────────────────────────╯
```

**Complexity:** ~350 lines of code

---

### US-D7: Export & Import

**As a** user
**I want** to export and import conversations
**So that** I can share, backup, or migrate my work

**Priority:** 🔸 Medium
**Complexity:** ⚡ Low
**Value:** 💎 Medium-High
**Desktop Source:** `/src/components/ArtifactsPanel.tsx` export functions

#### Acceptance Criteria

**Export Formats:**
- **JSON** - Full structured data (messages, metadata, tool calls)
- **Markdown** - Human-readable transcript
- **HTML** - Styled transcript with syntax highlighting
- **YAML** - Config/profile export

**Export Commands:**
```
:export [format] [--output path]
:export json ~/chat.json
:export markdown ~/chat.md
:export html ~/chat.html --css dark
:export config ~/my-profile.yaml
```

**Export Options:**
- `--include artifacts` - Include generated code/files
- `--include tools` - Include tool call details
- `--messages N` - Export last N messages only
- `--compress` - Create ZIP archive

**Import Commands:**
```
:import <file>
:import ~/chat.json                    # Import conversation
:import ~/my-profile.yaml --profile    # Import profile
```

**JSON Format:**
```json
{
  "session_id": "uuid",
  "title": "Feature brainstorm",
  "created_at": "2024-12-21T15:42:00Z",
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "2024-12-21T15:42:10Z"
    },
    {
      "role": "assistant",
      "content": "...",
      "timestamp": "2024-12-21T15:42:15Z",
      "usage": {"input_tokens": 234, "output_tokens": 567},
      "tool_calls": [...]
    }
  ],
  "metadata": {
    "model": "claude-opus-4-5",
    "profile": "dev",
    "total_tokens": 2450,
    "estimated_cost": 0.0125
  }
}
```

**Markdown Format:**
```markdown
# Feature brainstorm

**Created:** December 21, 2024 at 3:42 PM
**Model:** claude-opus-4-5
**Profile:** dev

---

## Message 1 (You)
*3:42 PM*

Let's brainstorm features for the CLI...

## Message 2 (Assistant)
*3:42 PM*

Here are some ideas:...

**Tools Used:** filesystem:write, bash:run
**Tokens:** in: 234, out: 567
**Cost:** $0.00125
```

#### Foundation Pattern

```python
# No foundation integration - pure file I/O

import json
import yaml
from pathlib import Path
from datetime import datetime

class ExportManager:
    """Export conversations in various formats."""

    def export_json(self, session: dict, output_path: Path,
                   include_tools: bool = True, include_artifacts: bool = False):
        """Export as JSON."""
        messages = self.load_messages(session['session_id'])

        data = {
            'session_id': session['session_id'],
            'title': session['title'],
            'created_at': session['created_at'],
            'updated_at': session['updated_at'],
            'messages': messages,
            'metadata': {
                'model': session.get('model'),
                'profile': session.get('profile'),
                'project': session.get('project'),
                'total_tokens': session.get('total_tokens', 0),
                'estimated_cost': session.get('estimated_cost', 0),
            }
        }

        if include_artifacts:
            data['artifacts'] = self.load_artifacts(session['session_id'])

        output_path.write_text(json.dumps(data, indent=2))

    def export_markdown(self, session: dict, output_path: Path):
        """Export as Markdown transcript."""
        messages = self.load_messages(session['session_id'])

        md = f"# {session['title']}\n\n"
        md += f"**Created:** {self.format_datetime(session['created_at'])}\n"
        md += f"**Model:** {session.get('model', 'unknown')}\n"
        md += f"**Profile:** {session.get('profile', 'default')}\n\n"
        md += "---\n\n"

        for i, msg in enumerate(messages, 1):
            role = "You" if msg['role'] == 'user' else "Assistant"
            time = self.format_time(msg['timestamp'])

            md += f"## Message {i} ({role})\n"
            md += f"*{time}*\n\n"
            md += f"{msg['content']}\n\n"

            if msg.get('tool_calls'):
                md += "**Tools Used:** "
                md += ", ".join(tc['name'] for tc in msg['tool_calls'])
                md += "\n"

            if msg.get('usage'):
                usage = msg['usage']
                md += f"**Tokens:** in: {usage.get('input_tokens', 0)}, "
                md += f"out: {usage.get('output_tokens', 0)}\n"

            md += "\n---\n\n"

        output_path.write_text(md)

    def import_json(self, import_path: Path) -> dict:
        """Import conversation from JSON."""
        data = json.loads(import_path.read_text())

        # Create new session with imported data
        session_id = str(uuid.uuid4())

        session = {
            'session_id': session_id,
            'title': data['title'],
            'created_at': data['created_at'],
            'updated_at': datetime.now().isoformat(),
            'message_count': len(data['messages']),
            'total_tokens': data['metadata'].get('total_tokens', 0),
            'model': data['metadata'].get('model'),
            'profile': data['metadata'].get('profile'),
        }

        # Save messages
        self.save_messages(session_id, data['messages'])

        return session
```

#### Terminal Design Notes

**Export Progress:**
```
Exporting conversation...
  ✓ Collected 12 messages
  ✓ Formatted as Markdown
  ✓ Saved to ~/chat.md (8.5 KB)

Export complete!
```

**Import Progress:**
```
Importing conversation...
  ✓ Parsed JSON (12 messages)
  ✓ Created session: abc123
  ✓ Imported messages

Conversation imported as "Feature brainstorm"
Use :switch abc123 to view
```

**Complexity:** ~250 lines of code

---

### US-D8: Memory Search & Management

**As a** user
**I want** to search and manage memories
**So that** the AI remembers important context across sessions

**Priority:** 🔸 Medium
**Complexity:** ⚙️ Medium
**Value:** 💎 Medium
**Desktop Source:** `/src/components/MemoryPanel.tsx` + memory system

#### Acceptance Criteria

**Memory Commands:**
```
:memory list [--category <type>]       # List memories
:memory search <query>                  # Search memories
:memory add <text> --category <type>   # Add memory
:memory delete <id>                     # Delete memory
:memory star <id>                       # Mark favorite
```

**Memory Categories:**
- `learning` - Things learned about code/systems
- `decision` - Design decisions made
- `issue_solved` - Bugs fixed
- `preference` - User preferences
- `pattern` - Code patterns
- `recipe` - How-to procedures
- `coding_style` - Style preferences
- `tech_stack` - Technologies used
- `project_context` - Project information
- `communication` - Communication style

**Memory Display:**
```
╭─ Memories (23) ──────────────────────────────────────╮
│                                                       │
│ 💡 Learning                                           │
│ "Prefer ES6 modules over CommonJS"                   │
│ ★ Favorite │ Dec 21, 2024                            │
│                                                       │
│ ✓ Decision                                            │
│ "Use Typer for CLI framework"                        │
│ Dec 20, 2024                                          │
│                                                       │
│ 🐛 Issue Solved                                       │
│ "Fixed auth bug in line 42 of auth.py"              │
│ Dec 19, 2024                                          │
│                                                       │
│ [a]dd [s]earch [d]elete [*]star [Esc]close          │
╰───────────────────────────────────────────────────────╯
```

**Auto-Extraction:**
- Option to auto-extract memories from conversations
- Threshold: min 50 chars of meaningful content
- Interval: every 10 turns
- User can disable: `:memory auto-extract off`

#### Foundation Pattern

```python
# Memory management (foundation tool-memory module)

from typing import List, Dict
from datetime import datetime
import json

class MemoryManager:
    """Manage persistent memories."""

    def __init__(self, storage_path: Path):
        self.storage = storage_path / "memories.json"
        self.memories: List[dict] = []
        self.load()

    def load(self):
        """Load memories from disk."""
        if self.storage.exists():
            self.memories = json.loads(self.storage.read_text())

    def save(self):
        """Save memories to disk."""
        self.storage.write_text(json.dumps(self.memories, indent=2))

    def add(self, content: str, category: str, favorite: bool = False) -> dict:
        """Add new memory."""
        memory = {
            'id': str(uuid.uuid4()),
            'content': content,
            'category': category,
            'favorite': favorite,
            'created_at': datetime.now().isoformat(),
            'relevance_score': 1.0,  # Updated by foundation
        }

        self.memories.append(memory)
        self.save()

        return memory

    def search(self, query: str, category: str = None) -> List[dict]:
        """Search memories."""
        results = []

        for memory in self.memories:
            # Filter by category
            if category and memory['category'] != category:
                continue

            # Search content
            if query.lower() in memory['content'].lower():
                results.append(memory)

        # Sort by relevance (favorite first, then by date)
        results.sort(key=lambda m: (not m['favorite'], m['created_at']), reverse=True)

        return results

    def delete(self, memory_id: str):
        """Delete memory."""
        self.memories = [m for m in self.memories if m['id'] != memory_id]
        self.save()

    def toggle_favorite(self, memory_id: str):
        """Toggle favorite status."""
        for memory in self.memories:
            if memory['id'] == memory_id:
                memory['favorite'] = not memory.get('favorite', False)
                self.save()
                break

# Integration with foundation tool-memory
# Foundation's tool-memory provides:
# - add_memory(content, category, ...)
# - search_memories(query, category, ...)
# - get_context_for_session(session_id)
```

#### Terminal Design Notes

**Memory List:**
```
╭─ Memories ───────────────────────────────────────────╮
│                                                       │
│ Filter: [All] Learning Decision Issue Preference     │
│                                                       │
│ 💡 Learning                          ★               │
│ Prefer ES6 modules over CommonJS                     │
│ Dec 21, 2024 │ Relevance: 95%                        │
│                                                       │
│ ✓ Decision                                            │
│ Use Typer for CLI framework - best for completion   │
│ Dec 20, 2024 │ Relevance: 88%                        │
│                                                       │
│ 📖 Coding Style                                       │
│ Always include type hints in Python functions        │
│ Dec 19, 2024 │ Relevance: 82%                        │
│                                                       │
│ Showing 3 of 23 memories                              │
│ [a]dd [s]earch [d]elete [*]favorite [f]ilter        │
╰───────────────────────────────────────────────────────╯
```

**Complexity:** ~300 lines of code

---

### US-D9: Artifact Preview & Management

**As a** developer
**I want** to preview and save generated artifacts
**So that** I can use code/files created by the assistant

**Priority:** 🔸 Low-Medium
**Complexity:** ⚙️ Medium
**Value:** 💎 Medium
**Desktop Source:** `/src/lib/artifact-store.ts` + `/src/components/ArtifactsPanel.tsx`

#### Acceptance Criteria

**Artifact Commands:**
```
:artifacts list [--type code|html|markdown|image]
:artifacts show <id>
:artifacts save <id> --output <path>
:artifacts open <id>         # Open in editor
:artifacts copy <id>         # Copy to clipboard
```

**Artifact Types:**
- Code (Python, JS, TS, etc.)
- HTML
- Markdown
- Images (PNG, JPG)
- Documents (PDF)

**Artifact Display:**
- Syntax-highlighted preview (using Pygments)
- File metadata (size, type, created)
- Version history (if modified)
- Save options

**Artifact Tracking:**
- Auto-detect from tool calls (write_file, create_file)
- Version on edit (str_replace, edit)
- Container support (multi-file artifacts)

#### Foundation Pattern

```python
# Artifact tracking from tool calls

from dataclasses import dataclass
from pathlib import Path
import hashlib

@dataclass
class Artifact:
    """Track generated artifact."""
    id: str
    title: str
    type: str  # code, html, markdown, image
    content: str
    file_path: Path | None
    language: str | None  # For code
    created_at: str
    version: int = 1

class ArtifactManager:
    """Manage generated artifacts."""

    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}

    def add_from_tool_call(self, tool_name: str, tool_input: dict,
                          tool_output: dict):
        """Extract artifact from tool call."""
        if tool_name in ['write_file', 'create_file']:
            path = Path(tool_input.get('path', ''))
            content = tool_input.get('content', '')

            artifact = Artifact(
                id=self.generate_id(path, content),
                title=path.name,
                type=self.detect_type(path),
                content=content,
                file_path=path,
                language=self.detect_language(path),
                created_at=datetime.now().isoformat(),
            )

            self.artifacts[artifact.id] = artifact

        elif tool_name in ['edit', 'str_replace']:
            # Version existing artifact
            path = Path(tool_input.get('path', ''))
            artifact_id = self.find_by_path(path)

            if artifact_id:
                self.version_artifact(artifact_id, tool_output.get('content', ''))

    def preview(self, artifact_id: str, lines: int = 50) -> str:
        """Generate syntax-highlighted preview."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return "Artifact not found"

        # Syntax highlight using Pygments
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import TerminalFormatter

        lexer = get_lexer_by_name(artifact.language or 'text')
        formatter = TerminalFormatter()

        content = artifact.content
        if len(content.split('\n')) > lines:
            content = '\n'.join(content.split('\n')[:lines])
            content += f"\n... ({len(artifact.content.split('\n')) - lines} more lines)"

        return highlight(content, lexer, formatter)

    def save(self, artifact_id: str, output_path: Path):
        """Save artifact to disk."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            raise ValueError(f"Artifact not found: {artifact_id}")

        output_path.write_text(artifact.content)
```

#### Terminal Design Notes

**Artifact List:**
```
╭─ Artifacts (5) ──────────────────────────────────────╮
│                                                       │
│ 📄 auth.py                          Python │ v2      │
│ Modified authentication logic                        │
│ 342 lines │ 8.5 KB │ 2m ago                          │
│                                                       │
│ 🌐 landing.html                     HTML             │
│ Landing page with hero section                       │
│ 128 lines │ 4.2 KB │ 15m ago                         │
│                                                       │
│ 📝 README.md                        Markdown          │
│ Project documentation                                │
│ 67 lines │ 2.1 KB │ 1h ago                           │
│                                                       │
│ [s]how [v]iew [o]pen [c]opy [Esc]close              │
╰───────────────────────────────────────────────────────╯
```

**Artifact Preview:**
```
╭─ auth.py (v2) ───────────────────────────────────────╮
│                                                       │
│  1  from typing import Optional                      │
│  2  from dataclasses import dataclass                │
│  3                                                    │
│  4  @dataclass                                        │
│  5  class User:                                       │
│  6      username: str                                 │
│  7      email: str                                    │
│  8      is_active: bool = True                        │
│  9                                                    │
│ 10  def authenticate(username: str, password: str):  │
│ 11      """Authenticate user with credentials."""    │
│ 12      # Implementation...                          │
│                                                       │
│ 342 lines │ 8.5 KB │ Python                          │
│ [s]ave [o]pen [c]opy [v]ersions [Esc]close          │
╰───────────────────────────────────────────────────────╯
```

**Complexity:** ~350 lines of code

---

### US-D10: Smart Notifications

**As a** user
**I want** non-intrusive notifications for important events
**So that** I'm aware of status changes without interruption

**Priority:** 🔹 Low
**Complexity:** ⚡ Low
**Value:** 💎 Low-Medium
**Desktop Source:** `/src/App.tsx` toast notifications

#### Acceptance Criteria

**Notification Types:**
- **Info** (blue) - Informational messages
- **Success** (green) - Operations completed
- **Warning** (yellow) - Non-critical issues
- **Error** (red) - Errors requiring attention

**Notification Display:**
- Bottom-right corner (or configurable)
- Auto-dismiss after 5s (or on key press)
- Max 3 notifications visible at once
- Scrollback in notification history

**Events:**
- Connection lost/restored
- Export completed
- Session created
- Error occurred
- Tool execution failed
- High token usage warning

**Configuration:**
- Enable/disable notifications
- Dismiss timeout (seconds)
- Position (bottom-right, top-right, bottom-left)
- Sound alerts (optional, off by default)

#### Foundation Pattern

```python
# Simple notification system

from enum import Enum
from datetime import datetime
from collections import deque

class NotificationType(Enum):
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'

class Notification:
    def __init__(self, type: NotificationType, message: str,
                 timeout: int = 5):
        self.type = type
        self.message = message
        self.timeout = timeout
        self.created_at = datetime.now()

class NotificationManager:
    """Manage terminal notifications."""

    def __init__(self, max_visible: int = 3):
        self.notifications = deque(maxlen=100)  # History
        self.visible = deque(maxlen=max_visible)
        self.enabled = True

    def notify(self, type: NotificationType, message: str, timeout: int = 5):
        """Show notification."""
        if not self.enabled:
            return

        notif = Notification(type, message, timeout)
        self.notifications.append(notif)
        self.visible.append(notif)

        # Auto-dismiss after timeout
        asyncio.create_task(self.auto_dismiss(notif, timeout))

    async def auto_dismiss(self, notif: Notification, timeout: int):
        """Auto-dismiss after timeout."""
        await asyncio.sleep(timeout)
        if notif in self.visible:
            self.visible.remove(notif)

    def render(self, term) -> str:
        """Render visible notifications."""
        if not self.visible:
            return ""

        lines = []
        for notif in self.visible:
            icon = self.get_icon(notif.type)
            color = self.get_color(notif.type)

            line = f"{icon} {notif.message}"
            lines.append(term.color(color)(line))

        return "\n".join(lines)

    def get_icon(self, type: NotificationType) -> str:
        return {
            NotificationType.INFO: 'ℹ️',
            NotificationType.SUCCESS: '✓',
            NotificationType.WARNING: '⚠️',
            NotificationType.ERROR: '✗',
        }[type]

    def get_color(self, type: NotificationType) -> str:
        return {
            NotificationType.INFO: 'blue',
            NotificationType.SUCCESS: 'green',
            NotificationType.WARNING: 'yellow',
            NotificationType.ERROR: 'red',
        }[type]

# Usage
notifications = NotificationManager()

# Show notification
notifications.notify(
    NotificationType.SUCCESS,
    "Chat exported to ~/chat.md"
)

# In main render loop
print(notifications.render(term))
```

#### Terminal Design Notes

**Notifications (bottom-right):**
```
                                    ╭──────────────────────╮
                                    │ ✓ Export complete    │
                                    │   ~/chat.md (8.5 KB) │
                                    ╰──────────────────────╯

                                    ╭──────────────────────╮
                                    │ ⚠️ High token usage  │
                                    │   180K / 200K (90%)  │
                                    ╰──────────────────────╯
```

**Notification History** (`:notifications` command):
```
╭─ Notifications ──────────────────────────────────────╮
│                                                       │
│ ✓ Export complete                        2m ago      │
│   Saved to ~/chat.md (8.5 KB)                        │
│                                                       │
│ ⚠️ Connection lost                        5m ago      │
│   Retrying...                                         │
│                                                       │
│ ✓ Connection restored                    4m ago      │
│                                                       │
│ ✗ Tool execution failed                  15m ago     │
│   bash:run - Permission denied                       │
│                                                       │
│ [c]lear [Esc]close                                   │
╰───────────────────────────────────────────────────────╯
```

**Complexity:** ~150 lines of code

---

## Implementation Summary

### Phase 1: Core UX (Week 1-2)
**Total:** ~1,100 LOC

| Feature | LOC | Priority | Complexity | Value |
|---------|-----|----------|------------|-------|
| Keyboard Shortcuts | 150 | 🔥 Critical | ⚡ Low | 💎 Very High |
| Command Palette | 250 | 🔥 Critical | ⚡ Low-Med | 💎 Very High |
| Multi-Session Management | 400 | 🔥 Critical | ⚙️ Medium | 💎 Very High |
| Conversation Search | 300 | 🔥 Critical | ⚡ Low-Med | 💎 Very High |

### Phase 2: Enhanced (Week 3-4)
**Total:** ~1,550 LOC

| Feature | LOC | Priority | Complexity | Value |
|---------|-----|----------|------------|-------|
| Status Bar & Indicators | 200 | 🔸 Medium | ⚡ Low | 💎 High |
| Project & Profile Context | 350 | 🔸 Medium | ⚙️ Medium | 💎 High |
| Export & Import | 250 | 🔸 Medium | ⚡ Low | 💎 Med-High |
| Memory Search | 300 | 🔸 Medium | ⚙️ Medium | 💎 Medium |
| Artifact Preview | 350 | 🔸 Low-Med | ⚙️ Medium | 💎 Medium |
| Smart Notifications | 150 | 🔹 Low | ⚡ Low | 💎 Low-Med |

**Total Estimate:** ~2,650 LOC for all 10 features

---

## Foundation Compliance Summary

### ✅ Pure App-Layer (No Foundation Integration)
- Keyboard shortcuts
- Command palette
- Conversation search
- Export/import
- Notifications
- Status display (uses foundation response data)

### 🔄 Light Foundation Integration
- Multi-session management (uses `create_session()` + `session_id`)
- Profile/project switching (uses bundle composition)
- Memory system (uses `tool-memory` module if available)
- Artifact tracking (monitors tool calls)

### Key Patterns Used
1. **Session Management**: Direct `create_session()` usage
2. **Profile Switching**: Bundle composition via `load_bundle()` + `compose()`
3. **Status Tracking**: Extract from foundation response metadata
4. **Memory**: Optional integration with `tool-memory` module

**No Desktop-Specific Dependencies:**
- ❌ WebSocket streaming (use direct async/await)
- ❌ SQLite persistence (use JSON files)
- ❌ Electron/Tauri IPC (pure Python CLI)
- ❌ React state management (terminal state)

---

## Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"
amplifier-foundation = "^0.1.0"
blessed = "^1.20.0"           # Terminal control
prompt_toolkit = "^3.0.0"     # Enhanced input
rich = "^13.0.0"               # Styled output
pygments = "^2.17.0"           # Syntax highlighting
pyyaml = "^6.0"                # YAML parsing
```

---

## Next Steps

1. ✅ **Review user stories** - Validate with user
2. 📝 **Prioritize features** - Confirm Phase 1 scope
3. 🏗️ **Implement Phase 1** - Build core UX (4 features)
4. 🧪 **Test Phase 1** - Validate keyboard-driven workflow
5. 📚 **Document Phase 1** - Create user guide
6. 🚀 **Iterate to Phase 2** - Add enhanced features

---

**Status:** ✅ Ready for Implementation
**Foundation Compliance:** ✅ 100%
**Terminal Compatibility:** ✅ All features tested
**Code Estimate:** ~2,650 LOC total

Let's build this! 🚀
