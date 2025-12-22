# Installation Guide

This guide covers all methods for installing the amplifier-cli-skill in Claude Code and other compatible environments.

## Quick Install (Recommended)

For Claude Code users, install directly from GitHub:

```bash
/plugin install https://github.com/michaeljabbour/amplifier-cli-skill
```

That's it! The skill will be available globally for all your conversations.

## Installation Methods

### Method 1: Plugin Installation (Global)

Install the plugin to make the skill available across all Claude Code conversations:

**Step 1: Open Claude Code**

Launch your Claude Code CLI or web interface.

**Step 2: Install the plugin**

```bash
/plugin install https://github.com/michaeljabbour/amplifier-cli-skill
```

**Step 3: Verify installation**

Ask Claude:
```
What skills are available?
```

You should see `amplifier-cli-skill` in the list.

### Method 2: Local Plugin Directory

If you want to develop or test changes to the skill locally:

**Step 1: Clone the repository**

```bash
cd ~/dev  # or wherever you keep your projects
git clone https://github.com/michaeljabbour/amplifier-cli-skill.git
```

**Step 2: Start Claude Code with plugin directory**

```bash
claude --plugin-dir ~/dev/amplifier-cli-skill
```

**Step 3: Use the skill**

The skill will be available in this session. Any changes you make to the skill files will be reflected immediately.

### Method 3: User Skills Directory (Manual)

Copy the skill directly to your user skills directory:

**Step 1: Create skills directory**

```bash
mkdir -p ~/.claude/skills
```

**Step 2: Clone or copy the skill**

```bash
cd ~/.claude/skills
git clone https://github.com/michaeljabbour/amplifier-cli-skill.git
```

Or copy just the skill contents:

```bash
cp -r /path/to/amplifier-cli-skill/skills/amplifier-cli-skill ~/.claude/skills/
```

**Step 3: Restart Claude Code**

The skill will be loaded automatically on next startup.

## Verification

To verify the skill is working correctly:

1. **Check skill is loaded**
   ```
   What skills are available?
   ```

2. **Test skill activation**
   Ask a question related to Amplifier CLI development:
   ```
   How do I build a CLI application using amplifier-foundation?
   ```

   Claude should use the skill to provide detailed guidance using foundation patterns.

3. **View skill metadata**
   ```
   Show me information about the amplifier-cli-skill
   ```

## Troubleshooting

### Skill not loading

**Problem:** Skill doesn't appear in the skills list.

**Solutions:**
- Ensure SKILL.md exists in `skills/amplifier-cli-skill/SKILL.md`
- Verify YAML frontmatter is properly formatted (no syntax errors)
- Check that the skill name in plugin.json matches the directory name
- Restart Claude Code

### Skill not activating

**Problem:** Skill is listed but doesn't activate for relevant questions.

**Solutions:**
- Check the skill's `description` field in SKILL.md frontmatter
- Ensure your question matches the use cases in the description
- Skills activate automatically based on context - try being more specific
- Use the skill name explicitly: "Using amplifier-cli-skill, how do I..."

### Plugin installation fails

**Problem:** `/plugin install` command fails or shows errors.

**Solutions:**
- Verify you have an active internet connection
- Check that the GitHub repository URL is correct
- Ensure you're using the latest version of Claude Code
- Try Method 2 (local plugin directory) instead

### Files not found

**Problem:** Skill can't find reference files (EXAMPLES.md, HOOKS.md, etc.)

**Solutions:**
- Ensure all files are in the correct locations:
  ```
  skills/amplifier-cli-skill/
  ├── SKILL.md
  └── references/
      ├── EXAMPLES.md
      ├── HOOKS.md
      └── ...
  ```
- If you moved files, update paths in SKILL.md
- Reinstall using one of the methods above

## Uninstallation

To remove the skill:

### If installed via plugin:
```bash
/plugin uninstall amplifier-cli-skill
```

### If installed manually:
```bash
rm -rf ~/.claude/skills/amplifier-cli-skill
```

Then restart Claude Code.

## Updating

To update to the latest version:

### If installed via plugin:
```bash
/plugin update amplifier-cli-skill
```

### If installed manually:
```bash
cd ~/.claude/skills/amplifier-cli-skill
git pull origin main
```

Then restart Claude Code.

## Development

If you want to contribute or modify the skill:

**Step 1: Fork and clone**

```bash
git clone https://github.com/YOUR_USERNAME/amplifier-cli-skill.git
cd amplifier-cli-skill
```

**Step 2: Make changes**

Edit files in `skills/amplifier-cli-skill/`:
- `SKILL.md` - Main skill definition
- `references/` - Supporting documentation

**Step 3: Test locally**

```bash
claude --plugin-dir $(pwd)
```

**Step 4: Submit changes**

Create a pull request to the main repository.

For more details, see [CONTRIBUTING.md](skills/amplifier-cli-skill/references/CONTRIBUTING.md).

## Support

- **Issues:** Report bugs or request features at https://github.com/michaeljabbour/amplifier-cli-skill/issues
- **Discussions:** Ask questions at https://github.com/michaeljabbour/amplifier-cli-skill/discussions
- **Reference Implementation:** See [amplifier-simplecli](https://github.com/michaeljabbour/amplifier-simplecli) for working examples

## Requirements

- Claude Code CLI or compatible environment
- Python 3.10+ (for testing bundle examples)
- uv package manager (optional, for bundle validation)
- Git (for cloning and updating)

## License

This skill is licensed under the MIT License. See [LICENSE](LICENSE) for details.
