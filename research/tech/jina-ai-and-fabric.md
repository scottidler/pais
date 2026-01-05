---
title: Jina AI and Fabric Integration
date: 2026-01-05
tags:
  - ai
  - search
  - embeddings
  - fabric
  - cli-tools
  - web-scraping
---

# Jina AI and Fabric Integration

## Jina AI

**Jina AI** is a Berlin-based AI company founded in 2020 by Han Xiao, focused on **search AI infrastructure**. They build foundational models and tools for neural/semantic search.

### Core Products

| Product | Purpose |
|---------|---------|
| **Embeddings** | Multimodal & multilingual vector representations |
| **Rerankers** | Improve search result relevance |
| **Reader** | Extract/process content from URLs to clean markdown |
| **Search** | Web search API |
| **Small Language Models** | Lightweight models for search tasks |

### Key Capabilities

- Convert unstructured data into searchable vectors
- Supports text, images, and multilingual content
- Open-source foundations with commercial APIs
- Powers RAG (Retrieval-Augmented Generation) pipelines

### 2025 Acquisition

**Elastic acquired Jina AI in October 2025** for their vector search and RAG capabilities. Han Xiao (Jina CEO) became VP of AI at Elastic. Prior to acquisition, Jina had raised ~$39M from investors including Canaan and SAP.iO.

### Reader API

Convert any URL to clean, LLM-friendly markdown:

```bash
# Simple usage - just prepend r.jina.ai
curl https://r.jina.ai/https://example.com/article

# With API key for higher limits
curl -H "Authorization: Bearer jina_xxx" https://r.jina.ai/https://example.com
```

### Search API

Web search that returns markdown-formatted results:

```bash
curl https://s.jina.ai/what%20is%20RAG
```

---

## Fabric

**Fabric** is Daniel Miessler's open-source AI augmentation framework.

> "AI doesn't have a capabilities problem—it has an integration problem."

Fabric solves this by providing **Patterns**—crowdsourced, battle-tested prompts for specific tasks.

### How It Works

```bash
# Pipe any text through a pattern
cat article.md | fabric -p summarize

# YouTube transcripts
fabric -y "https://youtube.com/watch?v=..." -p extract_wisdom

# Stream output
echo "complex topic" | fabric -p explain_code -s
```

### Key Features

| Feature | Description |
|---------|-------------|
| **234+ Patterns** | Curated prompts for real tasks |
| **Multi-vendor** | OpenAI, Anthropic, Ollama, Google, local models |
| **YouTube integration** | Transcripts, comments, metadata extraction |
| **Contexts & Sessions** | Persistent conversation memory |
| **REST API** | `fabric --serve` for programmatic access |

### Popular Patterns

| Pattern | Use Case |
|---------|----------|
| `extract_wisdom` | Comprehensive extraction from videos/articles |
| `summarize` | Quick summary |
| `improve_prompt` | Make prompts better |
| `create_summary` | Structured key points |
| `analyze_claims` | Fact-check content |
| `write_essay` | Generate essays in your voice |

### Installation

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/danielmiessler/fabric/main/scripts/installer/install.sh | bash

# Or Homebrew
brew install fabric
```

---

## Fabric + Jina Integration

Fabric has **built-in Jina AI support** for web content:

```bash
# Scrape any URL to clean markdown via Jina Reader
fabric -u "https://example.com/article" -p summarize

# Search the web via Jina
fabric -q "What is retrieval augmented generation?" -p summarize
```

The flags:
- `-u, --scrape_url` — Uses Jina AI Reader to convert any webpage to clean markdown
- `-q, --scrape_question` — Uses Jina AI Search to find and retrieve relevant content

This lets you pipe web content directly into any pattern without manual copy-paste.

---

## Jina AI Pricing (Free Tier)

| Feature | Without API Key | With Free API Key |
|---------|-----------------|-------------------|
| **Reader** (`r.jina.ai`) | 20 RPM | 500 RPM |
| **Search** (`s.jina.ai`) | 100 RPM | 1,000 RPM |
| **Free tokens** | — | **10 million tokens** |

### Important Notes

- **Free trial keys = non-commercial only**
- Commercial use requires purchasing tokens
- Tokens are shared across all Jina products (reader, embeddings, reranker)
- Failed requests don't consume tokens
- For personal Fabric use, you'll likely never hit limits

---

## References

- [Jina AI Official Site](https://jina.ai/)
- [Jina Reader API](https://jina.ai/reader/)
- [Fabric GitHub](https://github.com/danielmiessler/fabric)
- [Elastic Acquisition Announcement](https://ir.elastic.co/news/news-details/2025/Elastic-Completes-Acquisition-of-Jina-AI-a-Leader-in-Frontier-Models-for-Multimodal-and-Multilingual-Search/default.aspx)
