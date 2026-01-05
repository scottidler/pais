# Plugin Bundles

Bundles are curated collections of plugins that work well together and can be installed with a single command.

## Bundle Location

Bundles live in `~/.config/pais/bundles/<bundle-name>/`

## Creating a Bundle

```bash
# Scaffold a new bundle
pais bundle new my-bundle

# Or create in a specific location
pais bundle new my-bundle --path /path/to/bundle
```

This creates a `bundle.yaml` manifest:

```yaml
bundle:
  name: my-bundle
  version: 1.0.0
  description: A collection of related plugins
  author: Your Name
  license: MIT
  pais-version: ">=0.2.0"

plugins:
  plugin-one:
    required: true
    description: Core functionality
  plugin-two:
    required: false
    description: Optional enhancement

environment: {}

post-install: []

conflicts: []
```

## Bundle Manifest

### Bundle Metadata

```yaml
bundle:
  name: ai-tools           # bundle name
  version: 1.0.0           # semantic version
  description: AI-powered development tools
  author: Your Name
  license: MIT
  pais-version: ">=0.2.0"  # minimum PAIS version
```

### Plugins

Dict-of-dicts format (name as key):

```yaml
plugins:
  openai:
    required: true
    description: OpenAI API integration
  anthropic:
    required: true
    description: Claude API integration
  ollama:
    required: false
    description: Local LLM support (optional)
```

### Environment Variables

Variables set when bundle is active:

```yaml
environment:
  AI_PROVIDER: openai
  MODEL_DEFAULT: gpt-4
```

### Post-Install Commands

Commands run after all plugins are installed:

```yaml
post-install:
  - command: pais skill index --rebuild
    description: Rebuild skill index
  - command: echo "Bundle installed!"
    description: Completion message
```

### Conflicts

Bundles that cannot be installed together:

```yaml
conflicts:
  - legacy-ai-bundle
  - deprecated-tools
```

## Using Bundles

```bash
# List available bundles
pais bundle list

# Show bundle details
pais bundle show my-bundle

# Install all plugins from a bundle
pais bundle install my-bundle

# Install only required plugins
pais bundle install my-bundle --required-only

# Skip verification after install
pais bundle install my-bundle --skip-verify
```

## Installation Order

Plugins are installed in the order they appear in the manifest. Put dependencies first:

```yaml
plugins:
  core-lib:        # installed first
    required: true
  depends-on-core: # installed second
    required: true
```

## Best Practices

1. **Document purpose** - explain what the bundle provides
2. **Mark optional plugins** - let users skip non-essential plugins
3. **Order dependencies** - install prerequisites first
4. **Version constraints** - specify minimum PAIS version
5. **Avoid conflicts** - declare incompatible bundles
