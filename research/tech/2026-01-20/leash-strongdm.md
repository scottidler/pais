# Leash by StrongDM - Research Summary

**Research Date:** 2026-01-20
**Repository:** [strongdm/leash](https://github.com/strongdm/leash)
**Documentation:** https://leash.strongdm.ai/
**License:** Apache-2.0
**Primary Language:** Go (66%), TypeScript (13.2%), Swift (11.9%)
**Stars:** 269 | **Forks:** 13
**Latest Release:** v1.1.5 (2026-01-12)

---

## What is Leash?

Leash is a **container-based security and governance tool** for AI coding agents. It wraps agents (like Claude Code, Codex, Gemini, Qwen, OpenCode) in containers and monitors their activity in real-time. Users define access control policies using [Cedar](https://docs.cedarpolicy.com/), and Leash enforces them instantly at both the kernel and application layers.

### Core Value Proposition

- **Complete Telemetry**: Captures every filesystem access and network connection
- **Policy-as-Code**: Human-readable Cedar policies that are version-controllable
- **Real-time Enforcement**: Kernel-level blocking via eBPF LSM
- **Secret Protection**: Inject credentials at the boundary without exposing them to agents

---

## Architecture Overview

Leash uses a **two-layer enforcement architecture**:

### Layer 1: Kernel Enforcement (eBPF LSM)

Uses Linux Security Module hooks via eBPF for kernel-level enforcement:

| Hook | Purpose | Policy Action |
|------|---------|---------------|
| `file_open` | File access control | `FileOpen`, `FileOpenReadOnly`, `FileOpenReadWrite` |
| `bprm_check_security` | Process execution | `ProcessExec` |
| `socket_connect` | Network connections | `NetworkConnect` |

**Key advantages over alternatives (seccomp, Landlock, AppArmor/SELinux):**
- Rich context (resolved paths, file modes, cgroup IDs)
- Hot reload without process restart (BPF map updates)
- Cgroup-scoped enforcement (container-specific)
- Ring buffer observability (structured events)

### Layer 2: Application Enforcement (MITM Proxy)

HTTP(S) proxy for L7 inspection and control:

- Hostname-based allow/deny (vs. IP-only at kernel level)
- Header injection (secrets never touch agent container)
- MCP (Model Context Protocol) tool call interception
- TLS interception with dynamic certificate generation

### Container Setup

```
┌─────────────────────────────────────────────────────────┐
│ Host                                                    │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ Leash Manager   │    │ Agent Container             │ │
│  │ (privileged)    │    │ (governed workload)         │ │
│  │                 │    │                             │ │
│  │ - eBPF programs │    │ - AI Agent (claude/codex)   │ │
│  │ - MITM proxy    │◄───│ - Project files mounted     │ │
│  │ - Control UI    │    │ - API keys forwarded        │ │
│  │ - Cedar engine  │    │                             │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│         │                         │                     │
│         └──── /leash (shared) ────┘                     │
│               /leash-private (manager only)             │
└─────────────────────────────────────────────────────────┘
```

---

## Installation

### npm (Recommended)
```bash
npm install -g @strongdm/leash
```

### macOS Homebrew
```bash
brew tap strongdm/tap
brew install --cask leash-app
```

### Binary Download
Available from [GitHub Releases](https://github.com/strongdm/leash/releases)

### Requirements
- Docker, Podman, or OrbStack
- macOS or Linux (WSL supported)

---

## Quick Start

```bash
# Launch Claude Code with Control UI
leash --open claude

# Launch Codex
leash --open codex

# Available agents in default image
leash --open gemini
leash --open qwen
leash --open opencode
```

Control UI available at: `http://localhost:18080`

---

## Policy Language: Cedar

Leash uses [Cedar](https://docs.cedarpolicy.com/) for policy definition. Policies are stored in `/cfg/leash.cedar` and transpiled to Leash IR in memory.

### Supported Actions

| Action | Resources | Purpose |
|--------|-----------|---------|
| `Action::"FileOpen"` | `Dir::"/path/"`, `File::"/path"` | File access |
| `Action::"FileOpenReadOnly"` | `Dir::"/path/"`, `File::"/path"` | Read-only access |
| `Action::"FileOpenReadWrite"` | `Dir::"/path/"`, `File::"/path"` | Write access |
| `Action::"ProcessExec"` | `Dir::"/path/"`, `File::"/path"` | Process execution |
| `Action::"NetworkConnect"` | `Host::"example.com"`, `Host::"*.domain"` | Network egress |
| `Action::"HttpRewrite"` | `Host::"example.com"` | Header injection |
| `Action::"McpCall"` | `MCP::Server::"host"`, `MCP::Tool::"tool"` | MCP tool calls |

### Example Policies

**File Access Control:**
```cedar
// Allow workspace access
permit (principal, action in [Action::"FileOpen", Action::"FileOpenReadWrite"], resource)
when { resource in [ Dir::"/workspace/" ] };

// Protect secrets
forbid (principal, action == Action::"FileOpenReadWrite", resource)
when { resource in [ Dir::"/workspace/secrets/" ] };
```

**Network Policy:**
```cedar
// Allow trusted APIs
permit (principal, action == Action::"NetworkConnect", resource)
when { resource in [ Host::"api.anthropic.com", Host::"*.openai.com" ] };

// Block social media
forbid (principal, action == Action::"NetworkConnect", resource)
when { resource in [ Host::"*.facebook.com", Host::"*.twitter.com" ] };
```

**MCP Tool Control:**
```cedar
// Block dangerous MCP tool
forbid (principal, action == Action::"McpCall", resource == MCP::Tool::"execute-shell")
when { resource in [ MCP::Server::"mcp.example.com" ] };
```

**Secret Injection:**
```cedar
permit (principal, action == Action::"HttpRewrite", resource == Host::"api.internal")
when {
    context.header == "Authorization" &&
    context.value  == "Bearer prod-secret"
};
```

---

## Operational Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Record** | All allowed, all logged | Initial deployment, learning |
| **Shadow** | Policies evaluated, not enforced | Testing new policies |
| **Enforce** | Policies enforced at kernel level | Production governance |

Mode transitions are live (no restart required).

---

## MCP Integration

Leash includes an MCP observer that:
- Intercepts JSON-RPC/SSE traffic to MCP servers
- Parses tool call requests (`tools/call` method)
- Enforces Cedar policies on tool invocations
- Logs all MCP activity to the event stream

**V1 Limitations:**
- Only `forbid` is enforced; `permit` is informational
- Server-level denies block all network connectivity to that host
- Tool-specific denies require both server and tool resources

---

## Configuration

### Config File Location
`~/.config/leash/config.toml`

### Example Configuration
```toml
[leash]
codex = true

[projects."/path/to/project"]
target_image = "ghcr.io/example/dev:latest"

[projects."/path/to/project".volumes]
"~/devtools" = "/workspace/devtools:rw"
```

### CLI Options

| Option | Environment Variable | Purpose |
|--------|---------------------|---------|
| `--image` | `LEASH_TARGET_IMAGE` | Custom agent image |
| `--policy` | `LEASH_POLICY_FILE` | Cedar policy file |
| `--listen` | `LEASH_LISTEN` | Control UI bind address |
| `-v src:dst` | - | Extra bind mounts |
| `-e KEY=val` | - | Environment variables |

### API Key Forwarding

Automatic forwarding based on agent:
- `claude` → `ANTHROPIC_API_KEY`
- `codex` → `OPENAI_API_KEY`
- `gemini` → `GEMINI_API_KEY`
- `qwen` → `DASHSCOPE_API_KEY`

---

## Security Model

### Trust Boundaries

| Component | Trust Level | Role |
|-----------|-------------|------|
| Host | Trusted | Outside governance |
| Leash Manager | Privileged | BPF loader, proxy |
| Agent Container | Untrusted | Governed workload |

### What Leash Prevents

- Unauthorized file access (outside policy scope)
- Unauthorized process execution (shell escapes, privilege escalation)
- Unauthorized network egress (data exfiltration)
- Credential leakage (secrets never touch agent)

### What Leash Does NOT Prevent

- Memory-based attacks (Spectre, Rowhammer)
- Container escape via kernel exploits
- Covert channels (timing, CPU patterns)

### Certificate Security

- Public CA cert in `/leash/ca-cert.pem` (accessible to agent)
- Private CA key in `/leash-private/ca-key.pem` (manager-only, mode 0600)

---

## Performance

| Component | Overhead | Notes |
|-----------|----------|-------|
| eBPF LSM hook | ~100ns | Negligible for syscalls |
| Policy evaluation | O(n) | Max 256 rules, typically <50 |
| Ring buffer submit | ~200ns | Async, non-blocking |
| Proxy TLS handshake | ~1ms | Cached per hostname |
| Proxy forwarding | ~100µs | Memory copy + headers |

**Total overhead:** <1% for typical agent workloads

---

## Control UI Features

Available at `http://localhost:18080`:
- Real-time event stream (WebSocket)
- Policy editor with Monaco (syntax highlighting, autocomplete)
- Policy validation endpoint
- Mode switching (Record/Shadow/Enforce)

### REST API

```bash
# Update policy
curl -X POST -H 'Content-Type: text/plain' \
  --data-binary @policy.cedar \
  http://localhost:18080/api/policies

# Validate policy
curl -X POST -H 'Content-Type: application/json' \
  --data '{"cedar": "..."}' \
  http://localhost:18080/api/policies/validate

# Get completions
curl -X POST -H 'Content-Type: application/json' \
  --data '{"cedar": "...", "cursor": {"line": 1, "column": 33}}' \
  http://localhost:18080/api/policies/complete
```

---

## Use Cases

1. **Enterprise AI Governance**: Control what AI agents can access in development environments
2. **Security Research**: Sandbox AI agents for behavior analysis
3. **Compliance**: Audit trails for AI agent actions
4. **Secret Management**: Inject production credentials without exposing them
5. **Multi-tenant Environments**: Isolate agent workloads per project

---

## Comparison: Why eBPF LSM?

| Feature | Seccomp | Landlock | AppArmor | **eBPF LSM** |
|---------|---------|----------|----------|--------------|
| Context | Syscall args only | Path + FD | Task context | Full kernel objects |
| Hot Reload | No | No | Yes (complex) | **Yes (map updates)** |
| Observability | Audit only | None | External auditd | **Ring buffers** |
| Cgroup Scope | No | No | No | **Yes** |
| Network Control | Yes | No | Yes | **Yes** |
| Read/Write Distinction | No | Limited | Yes | **Yes** |

---

## Future Directions

- Dynamic policy synthesis from Record mode events
- Cross-container policies (east-west traffic)
- Deny-by-default MCP with explicit permits
- Human-in-the-loop approval workflows

---

## Key Resources

- **Repository:** https://github.com/strongdm/leash
- **Documentation:** https://leash.strongdm.ai/
- **Cedar Language:** https://docs.cedarpolicy.com/
- **eBPF LSM Docs:** https://www.kernel.org/doc/html/latest/bpf/prog_lsm.html

---

## Summary

Leash is a sophisticated, defense-in-depth governance tool for AI coding agents. It combines:

1. **Kernel-level enforcement** via eBPF LSM for low-latency, bypassable file/process/network control
2. **Application-layer proxy** for L7 HTTP inspection, hostname enforcement, and secret injection
3. **Cedar policy language** for human-readable, version-controllable access control
4. **MCP integration** for monitoring and controlling AI tool calls
5. **Real-time observability** via WebSocket event streams and a web-based Control UI

The project addresses a real gap in AI agent security: the ability to let agents work autonomously while maintaining guardrails on what they can access, execute, and communicate with. The use of eBPF LSM is particularly well-suited for this use case, providing the combination of performance, flexibility, and observability that alternatives lack.
