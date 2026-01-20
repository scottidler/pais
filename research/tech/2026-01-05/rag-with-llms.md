# RAG (Retrieval Augmented Generation) with LLMs

**Research Date:** 2026-01-05

## Overview

Retrieval Augmented Generation (RAG) is a technique that enhances LLM text generation by incorporating real-time data retrieval from external sources. Unlike traditional models that rely solely on pre-trained knowledge, RAG allows models to search external databases or documents during generation, resulting in more accurate and up-to-date responses.

**Key Benefits:**
- Reduces hallucinations by grounding responses in factual, retrieved data
- Provides up-to-the-minute information without retraining
- Enables source citation for verifiable answers
- More cost-efficient than fine-tuning for many use cases

---

## Top GitHub Repositories

### RAG Frameworks

| Repository | Stars | Description |
|------------|-------|-------------|
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 123.5k | The platform for reliable agents - modular LLM orchestration |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 46.2k | Leading framework for building LLM-powered agents over your data |
| [FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise) | 47.8k | Build AI Agents visually |
| [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | 37k | Local knowledge based LLM RAG and Agent app |
| [truefoundry/cognita](https://github.com/truefoundry/cognita) | 4.3k | RAG Framework for modular, open source production applications |

### RAG Learning Resources

| Repository | Stars | Description |
|------------|-------|-------------|
| [Andrew-Jang/RAGHub](https://github.com/Andrew-Jang/RAGHub) | 1.5k | Community-driven collection of RAG frameworks and resources |
| [mrdbourke/simple-local-rag](https://github.com/mrdbourke/simple-local-rag) | 925 | Build a RAG pipeline from scratch, all running locally |
| [lehoanglong95/rag-all-in-one](https://github.com/lehoanglong95/rag-all-in-one) | 231 | Guide to Building RAG Applications |
| [teilomillet/raggo](https://github.com/teilomillet/raggo) | 202 | Lightweight, production-ready RAG library in Go |

---

## RAG Architecture Types

### 1. Simple RAG
Basic form where the LLM retrieves relevant documents from a static database, then generates output. Works well for small, static databases.

### 2. Simple RAG with Memory
Adds storage to retain information from previous interactions. Better for conversations requiring contextual awareness across multiple queries.

### 3. Agentic RAG
Combines RAG with autonomous agents for complex, multi-turn, tool-augmented tasks. Enables integration with APIs, workflows, and databases.

### 4. Long RAG
Processes longer retrieval units (sections or entire documents) instead of small chunks. Improves retrieval efficiency and preserves context.

### 5. Self-RAG
Self-reflective mechanism that dynamically decides when/how to retrieve information, evaluates relevance, and critiques outputs.

### 6. Corrective RAG
Evaluates retrieved documents and corrects retrieval errors before generation.

### 7. GraphRAG
Uses knowledge graphs to enhance retrieval with entity relationships and semantic connections.

---

## RAG vs Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Purpose** | Add external knowledge on-the-fly | Change model's core behavior/skills |
| **Best for** | Dynamic/changing data, factual grounding | Deep domain knowledge, style control |
| **Cost** | Lower (no retraining) | Higher (compute for training) |
| **Latency** | Higher (retrieval step) | Lower (no retrieval) |
| **Maintenance** | Update knowledge base | Periodic retraining needed |
| **Hallucination** | Reduced (grounded in data) | Can still occur |

### When to Use RAG
- Information changes frequently
- Need source citations
- Large corpus of reliable organizational data
- Regulated industries requiring transparency
- Cost-sensitive deployments

### When to Use Fine-Tuning
- Highly specialized domain tasks
- Need specific tone, format, or style
- Deep internalization of domain patterns required
- Nuance and regulatory compliance critical

### Hybrid Approach
Fine-tune for fluency and tone, layer RAG on top for factual grounding.

---

## Framework Comparison: LangChain vs LlamaIndex

| Aspect | LangChain | LlamaIndex |
|--------|-----------|------------|
| **Stars** | 123k | 46k |
| **Focus** | Multi-step AI workflow orchestration | High-quality retrieval & indexing |
| **Best for** | Agents, chains, tools, pipelines | Document-heavy RAG applications |
| **Learning Curve** | Steeper | Gentler |
| **Integrations** | 50k+ | 150+ data connectors |
| **2025 Highlights** | LangGraph for complex reasoning | 35% retrieval accuracy boost |

### Other Notable Frameworks
- **Haystack** - Open-source NLP framework
- **DSPy** - Programming (not prompting) LLMs
- **Pathway** - Real-time RAG pipelines

### Recommendation
Use **LlamaIndex** for indexing/retrieval, **LangChain** for agents and orchestration. This hybrid approach pairs RAG quality with flexible workflows.

---

## Chunking Strategies

### Core Principles
1. **Semantic coherence** - Each chunk groups related concepts
2. **Contextual preservation** - Enough surrounding info to retain meaning
3. **Size optimization** - Balance between precision and context

### Strategy Types

| Strategy | Best For | Trade-offs |
|----------|----------|------------|
| **Fixed-size** | Simple, predictable docs | May split mid-sentence |
| **Recursive** | General purpose (default) | 85-90% recall, low overhead |
| **Semantic** | Meaning-preserving | Up to 9% recall improvement, costs more |
| **Agentic** | Complex mixed-content | AI-driven, use selectively |

### Best Practices
- **Chunk size**: 400-512 tokens (RecursiveCharacterTextSplitter)
- **Overlap**: 10-20% (50-100 tokens for 500-token chunks)
- **Structured text**: Semantic/recursive chunking
- **Code/technical**: Recursive, language-specific
- **Mixed content**: AI-driven or context-enriched

---

## Vector Database Comparison

| Database | Type | Best For | Strengths |
|----------|------|----------|-----------|
| **Pinecone** | Managed | Production SaaS, minimal ops | <50ms queries, auto-scaling, SOC2/HIPAA |
| **Weaviate** | OSS + Managed | Hybrid search, flexibility | GraphQL API, multi-vector support |
| **Qdrant** | OSS + Managed | Cost-sensitive, edge | Rust performance, powerful filters |
| **Milvus** | OSS | Billion-scale vectors | Industrial-grade distributed |
| **Chroma** | OSS | Prototyping, lightweight | Zero-config, fast start |

### Decision Guide
- **Commercial SaaS, no cluster management**: Pinecone
- **Open-source with hybrid search**: Weaviate or Qdrant
- **Tight budget, mid-scale**: Qdrant/Weaviate
- **Billion-scale with data engineering team**: Milvus
- **Prototyping**: Chroma (have migration path ready)

---

## Production Best Practices

### 1. Data Quality
- Strip boilerplate, normalize text, fix broken encodings
- Don't push raw data directly to vector DB
- Understand your data structure before choosing chunking strategy

### 2. Query Augmentation
- **HyDE (Hypothetical Document Embeddings)**: Generate hypothetical answer, embed it, use for retrieval
- Expand ambiguous queries before retrieval

### 3. Evaluation Metrics
- **NDCG** (Normalized Discounted Cumulative Gain)
- **DCG** (Discounted Cumulative Gain)
- Recall and precision measurements
- End-to-end answer quality

### 4. Key Factors to Optimize
- Language model size
- Prompt design
- Document chunk size
- Knowledge base size
- Retrieval stride
- Query expansion techniques

### 5. Common Failures
Most RAG failures are self-inflicted (data quality, chunking strategy) not database-inflicted.

---

## 2025 Trends

1. **Multi-modal RAG** - Support for image, video, and audio alongside text
2. **Agentic RAG** - Integration with autonomous agents
3. **Self-RAG** - Self-reflective retrieval and generation
4. **GraphRAG** - Knowledge graph enhanced retrieval
5. **Real-time RAG** - Streaming and live data integration

---

## Key Resources

### Documentation & Guides
- [Prompt Engineering Guide - RAG](https://www.promptingguide.ai/research/rag)
- [2025 Guide to RAG - EdenAI](https://www.edenai.co/post/the-2025-guide-to-retrieval-augmented-generation-rag)
- [RAG Architecture Explained - orq.ai](https://orq.ai/blog/rag-architecture)
- [8 RAG Architectures - Humanloop](https://humanloop.com/blog/rag-architectures)

### Best Practices
- [RAG Best Practices - Merge.dev](https://www.merge.dev/blog/rag-best-practices)
- [Six Lessons Building RAG in Production - TDS](https://towardsdatascience.com/six-lessons-learned-building-rag-systems-in-production/)
- [Chunking Strategies - Weaviate](https://weaviate.io/blog/chunking-strategies-for-rag)
- [Best Chunking Strategies 2025 - Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)

### Comparisons
- [RAG vs Fine-Tuning - IBM](https://www.ibm.com/think/topics/rag-vs-fine-tuning)
- [RAG vs Fine-Tuning - Oracle](https://www.oracle.com/artificial-intelligence/generative-ai/retrieval-augmented-generation-rag/rag-fine-tuning/)
- [LangChain vs LlamaIndex - DataCamp](https://www.datacamp.com/blog/langchain-vs-llamaindex)
- [Vector Database Comparison 2025 - Firecrawl](https://www.firecrawl.dev/blog/best-vector-databases-2025)

### Academic
- [Enhancing RAG: Best Practices Study - arXiv](https://arxiv.org/abs/2501.07391)

---

## Summary

RAG is the go-to technique for adding domain knowledge to LLMs without expensive fine-tuning. Success depends on:

1. **Quality data ingestion** - Clean, well-chunked documents
2. **Smart retrieval** - Right vector DB + chunking strategy for your use case
3. **Framework choice** - LlamaIndex for retrieval, LangChain for orchestration
4. **Continuous evaluation** - Measure retrieval quality, not just generation

For most teams starting out: use **RecursiveCharacterTextSplitter** (400-512 tokens, 10-20% overlap), **Qdrant or Weaviate** for the vector store, and **LlamaIndex** for the RAG pipeline. Scale up complexity only when needed.
