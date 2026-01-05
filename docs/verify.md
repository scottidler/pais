# Plugin Verification

Plugins can define verification checks to ensure they're correctly installed and configured.

## Adding Verification

Add a `verification` section to your `plugin.yaml`:

```yaml
verification:
  guide: install.md           # shown when verification fails
  checks:
    files:
      - src/main.py           # files that must exist
      - config/settings.yaml
    env-vars:
      - MY_API_KEY            # environment variables that must be set
      - DATABASE_URL
    commands:
      - name: python-version
        command: python --version
        expect-exit: 0
        expect-contains: "3.10"
      - name: redis-ping
        command: redis-cli ping
        expect-exit: 0
        expect-contains: PONG
```

## Check Types

### File Checks

Verify required files exist in the plugin directory:

```yaml
checks:
  files:
    - src/main.py
    - SKILL.md
    - config/default.yaml
```

### Environment Variable Checks

Verify environment variables are set:

```yaml
checks:
  env-vars:
    - OPENAI_API_KEY
    - DATABASE_URL
```

### Command Checks

Run commands and verify output:

```yaml
checks:
  commands:
    - name: check-tool        # display name
      command: mytool --version
      expect-exit: 0          # expected exit code (default: 0)
      expect-contains: "1.0"  # string that must appear in stdout
```

## Running Verification

```bash
# Verify a plugin (text output)
pais plugin verify <plugin-name>

# JSON output
pais plugin verify <plugin-name> --format json

# Verify all plugins
pais plugin verify --all
```

## Output

```
Verifying plugin: my-plugin

File Checks:
  ✓ src/main.py
  ✗ config/settings.yaml - File not found

Environment Checks:
  ✓ MY_API_KEY
  ✗ DATABASE_URL - Environment variable not set

Command Checks:
  ✓ python-version
  ✓ redis-ping

Result: FAILED (4/6 checks passed)
```

## Built-in Checks

Even without a `verification` section, PAIS runs basic checks:

- **manifest** - plugin.yaml is valid
- **entry-point** - main entry point exists for the declared language

## Best Practices

1. **Check prerequisites** - verify tools your plugin depends on
2. **Check credentials** - verify API keys are set (without exposing values)
3. **Include a guide** - reference your install.md so users know how to fix failures
4. **Keep checks fast** - avoid long-running commands in verification
