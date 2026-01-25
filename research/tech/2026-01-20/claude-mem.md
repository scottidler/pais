# Claude-Mem - Research Summary

**Research Date:** 2026-01-20
**Repository:** [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
**Documentation:** https://claude-mem.ai / https://docs.claude-mem.ai
**License:** AGPL-3.0
**Primary Language:** TypeScript
**Stars:** 14,678 | **Forks:** 988
**Version:** 6.5.0

---

## What is Claude-Mem?

Claude-Mem is a **persistent memory compression system** built as a plugin for Claude Code. It automatically captures everything Claude does during coding sessions, compresses it with AI (using Claude's Agent SDK), and injects relevant context back into future sessions.

### Core Value Proposition

- **Context Persistence**: Valuable session context survives across sessions instead of being lost
- **Automatic Operation**: No manual intervention required - hooks capture tool usage automatically
- **Semantic Search**: Query your project history with natural language
- **Token Efficiency**: Progressive disclosure pattern provides ~10x token savings

---

## Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Persistent Memory** | Context survives across sessions |
| 📊 **Progressive Disclosure** | Layered memory retrieval with token cost visibility |
| 🔍 **Skill-Based Search** | Query project history with mem-search skill |
| 🖥️ **Web Viewer UI** | Real-time memory stream at http://localhost:37777 |
| 💻 **Claude Desktop Skill** | Search memory from Claude Desktop conversations |
| 🔒 **Privacy Control** | Use `<private>` tags to exclude sensitive content |
| ⚙️ **Context Configuration** | Fine-grained control over context injection |
| 🔗 **Citations** | Reference past observations with IDs |
| 🧪 **Beta Channel** | Experimental features like Endless Mode |

---

## Architecture

### Core Components

1. **5 Lifecycle Hooks** - SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd
2. **Smart Install** - Cached dependency checker (pre-hook script)
3. **Worker Service** - HTTP API on port 37777 with web viewer UI and 10 search endpoints
4. **SQLite Database** - Stores sessions, observations, summaries
5. **mem-search Skill** - Natural language queries with progressive disclosure
6. **Chroma Vector Database** - Hybrid semantic + keyword search

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code Session                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ SessionStart │───▶│ PostToolUse  │───▶│ SessionEnd   │      │
│  │    Hook      │    │    Hook      │    │    Hook      │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Worker Service (port 37777)                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ SQLite DB   │  │ Chroma Vec  │  │ Web Viewer  │      │   │
│  │  │ (sessions,  │  │ (embeddings │  │     UI      │      │   │
│  │  │ observations│  │  search)    │  │             │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Installation

```bash
# In a Claude Code session
> /plugin marketplace add thedotmack/claude-mem
> /plugin install claude-mem
```

Restart Claude Code. Context from previous sessions will automatically appear.

### System Requirements

- **Node.js**: 18.0.0+
- **Claude Code**: Latest version with plugin support
- **Bun**: JavaScript runtime (auto-installed if missing)
- **uv**: Python package manager for vector search (auto-installed if missing)
- **SQLite 3**: For persistent storage (bundled)

---

## MCP Search Tools

Claude-Mem provides 4 MCP tools following a token-efficient **3-layer workflow pattern**:

### The 3-Layer Workflow

1. **`search`** - Get compact index with IDs (~50-100 tokens/result)
2. **`timeline`** - Get chronological context around interesting results
3. **`get_observations`** - Fetch full details ONLY for filtered IDs (~500-1,000 tokens/result)

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `search` | Search memory index with full-text queries, filters by type/date/project |
| `timeline` | Get chronological context around a specific observation or query |
| `get_observations` | Fetch full observation details by IDs (batch multiple IDs) |
| `__IMPORTANT` | Workflow documentation (always visible to Claude) |

### Example Usage

```typescript
// Step 1: Search for index
search(query="authentication bug", type="bugfix", limit=10)

// Step 2: Review index, identify relevant IDs (e.g., #123, #456)

// Step 3: Fetch full details
get_observations(ids=[123, 456])
```

---

## Configuration

Settings stored in `~/.claude-mem/settings.json` (auto-created with defaults).

Configurable options:
- AI model selection
- Worker port (default: 37777)
- Data directory
- Log level
- Context injection settings

---

## Beta Features: Endless Mode

**Endless Mode** is an experimental biomimetic memory architecture for extended sessions. Access via web viewer UI at http://localhost:37777 → Settings.

---

## Related Concept: Smart Forking

From the screenshot, there's community discussion about **"Smart Forking"** - a workflow enhancement:

### How Smart Forking Works

1. Invoke `/fork` command with a description of needed context
2. System runs prompt through an embedding model
3. Conducts cosine similarity search on vectorized session database
4. Returns top 5 relevant chat sessions with summaries (sorted by relevance score)
5. User picks which session to fork from
6. Provides fork command to copy/paste into new session

### Implementation Approach

- Every session transcript auto-loaded into vector database via hooks when session ends
- `/fork` skill runs prompt through embeddings to find most similar sessions
- Enables seamless context transfer between related features/projects

This concept aligns with Claude-Mem's architecture and could be implemented as an additional skill.

---

## Comparison with Similar Tools

| Feature | Claude-Mem | Basic CLAUDE.md | Manual Context |
|---------|------------|-----------------|----------------|
| Automatic Capture | ✅ | ❌ | ❌ |
| Semantic Search | ✅ | ❌ | ❌ |
| Cross-Session Context | ✅ | Limited | ❌ |
| Token Efficiency | ✅ Progressive | ❌ Full file | Variable |
| Privacy Controls | ✅ | ❌ | Manual |
| Web UI | ✅ | ❌ | ❌ |

---

## Documentation Resources

- **[Installation Guide](https://docs.claude-mem.ai/installation)** - Quick start & advanced installation
- **[Usage Guide](https://docs.claude-mem.ai/usage/getting-started)** - How Claude-Mem works automatically
- **[Search Tools](https://docs.claude-mem.ai/usage/search-tools)** - Query your project history
- **[Architecture Overview](https://docs.claude-mem.ai/architecture/overview)** - System components & data flow
- **[Context Engineering](https://docs.claude-mem.ai/context-engineering)** - AI agent context optimization
- **[Configuration](https://docs.claude-mem.ai/configuration)** - Environment variables & settings

---

## Community & Support

- **Official X/Twitter**: [@Claude_Memory](https://x.com/Claude_Memory)
- **Discord**: [Join Discord](https://discord.com/invite/J4wttp9vDu)
- **Issues**: [GitHub Issues](https://github.com/thedotmack/claude-mem/issues)
- **Author**: Alex Newman ([@thedotmack](https://github.com/thedotmack))

---

## Summary

Claude-Mem solves a fundamental problem with AI coding assistants: **context loss between sessions**. By automatically capturing tool usage observations, generating semantic summaries, and making them available to future sessions via hybrid search (SQLite FTS5 + Chroma vector embeddings), it enables Claude to maintain continuity of knowledge about projects.

The architecture is well-designed with:
- **Hooks-based capture** - Non-intrusive, automatic data collection
- **Progressive disclosure** - Token-efficient retrieval pattern
- **Hybrid search** - Combines full-text and semantic search
- **Privacy controls** - `<private>` tags for sensitive content
- **Web UI** - Real-time visibility into memory stream

The project has significant traction (14.6k stars, 988 forks) and active development, indicating strong community adoption.

---

## Note on Token Economics

The project has an associated Solana token ($CMEM) with contract address `2TsmuYUrsctE57VLckZBYEEzdokUF8j8e1GavekWBAGS`. This is a separate crypto project and not required for using the Claude-Mem plugin.
