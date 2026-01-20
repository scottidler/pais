# Slack MCP Research

> Researched: 2026-01-04

---

## Summary

Slack MCP enables AI agents to securely access Slack workspace data through the Model Context Protocol, with official support coming summer 2025 and multiple open-source implementations available now.

---

## Top GitHub Repositories

| Repository | Stars | Description |
|------------|-------|-------------|
| [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) | 1,054 | Most powerful MCP Slack Server - Stdio/SSE/HTTP transports, DMs, stealth mode |
| [tuannvm/slack-mcp-client](https://github.com/tuannvm/slack-mcp-client) | 155 | Slack bot as bridge between Slack and MCP servers |
| [ubie-oss/slack-mcp-server](https://github.com/ubie-oss/slack-mcp-server) | 106 | Simple Slack MCP server |
| [duolingo/slack-mcp](https://github.com/duolingo/slack-mcp) | 6 | OAuth-based multi-user with HTTP transport |

---

## Ideas

- Slack MCP servers let AI agents search messages, files, users, and channels with filtering
- Official Slack MCP server uses OAuth authentication respecting existing workspace permissions
- Community solutions offer "stealth mode" requiring no additional Slack app permissions
- Three transport protocols supported: Stdio (local), SSE (streaming), HTTP (remote)
- Smart history fetching supports time-based (1d, 7d, 1m) or count-based pagination
- Message posting is disabled by default in community servers for safety
- Perplexity and Claude.ai are initial official MCP client partners
- Slack's conversational threads provide rich context for AI agent grounding
- Admin approval required for MCP client integrations in enterprise workspaces
- Browser tokens (xoxc/xoxd) enable operation without creating Slack apps

---

## Insights

- MCP transforms Slack from chat tool to AI-accessible knowledge base with structured queries
- Stealth mode democratizes access but official OAuth provides enterprise-grade security guarantees
- The "read-only by default" pattern prevents accidental message posting by AI agents
- Slack is high-value MCP surface because conversation threads contain actionable context

---

## Available Tools (korotovsky/slack-mcp-server)

| Tool | Description |
|------|-------------|
| conversations_history | Retrieve channel/DM messages with pagination |
| conversations_replies | Fetch thread messages by timestamp |
| conversations_add_message | Post messages (disabled by default) |
| conversations_search_messages | Search with date/user/channel filters |
| channels_list | List channels sorted by type or popularity |

---

## Recommendations

- Use korotovsky/slack-mcp-server for immediate local testing with Claude Code
- Wait for official Slack MCP server (summer 2025) for production enterprise use
- Start with read-only operations before enabling message posting capabilities
- Consider browser tokens for quick prototyping without Slack app setup
- Use SSE transport for remote deployments with streaming responses

---

## One-Sentence Takeaway

Slack MCP bridges AI agents to workspace knowledge through standardized protocol with community solutions available now.

---

## Sources

- https://docs.slack.dev/ai/mcp-server/
- https://github.com/korotovsky/slack-mcp-server
- https://github.com/tuannvm/slack-mcp-client
- https://www.anthropic.com/news/model-context-protocol
- https://slack.com/blog/news/powering-agentic-collaboration
