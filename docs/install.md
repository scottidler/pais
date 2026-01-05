# Plugin Installation Guides

Plugins can include an installation guide that helps users set up prerequisites and dependencies.

## Adding an Install Guide

1. Create an `install.md` file in your plugin directory
2. Optionally reference it in `plugin.yaml`:

```yaml
plugin:
  name: my-plugin
  install-guide: install.md  # optional, defaults to install.md
```

## What to Include

A good installation guide covers:

- **Prerequisites** - tools, runtimes, or services required
- **Installation steps** - how to install dependencies
- **Configuration** - environment variables, config files
- **Verification** - how to check the installation worked

## Example install.md

```markdown
# Installing my-plugin

## Prerequisites

- Python 3.10+
- Redis server running locally

## Installation

1. Install Python dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export MY_PLUGIN_API_KEY="your-key-here"
   ```

## Verify

```bash
pais plugin verify my-plugin
```
```

## Viewing Install Guides

```bash
# Show the installation guide for a plugin
pais plugin install-guide <plugin-name>

# JSON output
pais plugin install-guide <plugin-name> --format json
```
