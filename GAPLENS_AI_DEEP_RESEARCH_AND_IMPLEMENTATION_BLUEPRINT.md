# GAPLENS AI: Deep Research & Technical Product Blueprint
## Build a Winning AI-Powered Information Gap Detection Platform

> **Prepared for:** Shinchan Online Hackathon 2026 by Devengers  
> **Role:** Principal AI/ML Architect + Senior Full-Stack Engineer + AI Research Scientist  
> **Date:** 31 October 2026  
> **Hardware:** Windows 11, 16 GB RAM, NVIDIA RTX 3050 (6 GB VRAM)  
> **Evidence Labels:** `[VERIFIED]` = official source · `[SOURCE-DERIVED]` = from reference docs · `[RESEARCH FINDING]` = external research · `[INFERENCE]` = reasoned deduction · `[HYPOTHESIS]` = strategic judgment · `[UNVERIFIED]` = unconfirmed · `[RECOMMENDATION]` = my advice

---

# 1. Executive Summary

**The decisive answer:** Build **GapLens** — a **web-based AI Research Intelligence & Information Gap Analysis Engine** that accepts a research goal, collects sources via web search APIs, extracts structured claims, detects gaps/contradictions/outdated info, and produces an evidence-linked verification checklist with source traceability.

**Why this wins this specific hackathon:**

1. **Direct problem-statement fit** — The official challenge asks for exactly this: "analyzes information from multiple sources... identifies potential information gaps, conflicting claims, outdated details, unanswered questions... provides evidence with source references and guides users on what to verify next." GapLens implements every bullet.

2. **AI is load-bearing, not decorative** — Remove the AI and you have a static search page. The multi-stage pipeline (goal understanding → dimension generation → query planning → claim extraction → coverage mapping → contradiction detection → freshness analysis → evidence validation → gap prioritization → verification planning) is genuine AI engineering.

3. **Buildable solo in 24 hours** — Uses free-tier APIs (Tavily/Jina for search, Gemini Flash for reasoning, Jina embeddings for dedup), FastAPI + Next.js, SQLite/pgvector, deployed on Vercel + Render. No custom training, no GPU-dependent local inference.

4. **Judging-criteria alignment** — Scores high on *Problem Understanding (15%)*, *Innovation (20%)*, *Working Prototype (25%)*, *Evidence/Accuracy/Transparency (15%)* because every finding traces to a source passage.

5. **Differentiated from generic RAG/chatbot** — Not "chat with PDF" or "summarize search results." It produces a **structured coverage matrix**, **contradiction cards**, **freshness warnings**, and a **prioritized verification checklist** — the exact deliverables the problem statement demands.

**Backup strategy:** If search APIs fail, fall back to user-pasted URLs + Jina Reader extraction. If LLM APIs fail, fall back to deterministic keyword/rule-based gap heuristics + cached demo data.

**First implementation action:** Scaffold repo → FastAPI `/analyze` endpoint → Tavily search + Jina Reader extraction → single LLM call for claim extraction → JSON response → Next.js dashboard rendering.

---

# 2. Official Problem Statement Analysis

## 2.1 Verbatim Requirements (from PDF)

| # | Requirement | Source |
|---|-------------|--------|
| 1 | Web-based platform where user enters topic/question/research goal | PDF p.1 |
| 2 | Way to add/collect relevant source material (user URLs or permitted search results) | PDF p.1 |
| 3 | Structured summary of key information found across selected sources | PDF p.2 |
| 4 | Clear list of potential information gaps and unanswered questions | PDF p.2 |
| 5 | Identification of possible contradictions between sources with references | PDF p.2 |
| 6 | Warnings for potentially outdated/undated information when source dates available | PDF p.2 |
| 7 | Prioritized checklist of items user should verify next | PDF p.2 |
| 8 | Clear dashboard distinguishing sourced information from AI-generated suggestions and uncertainty | PDF p.2 |

## 2.2 Judging Criteria (Official, from PDF)

| Area | Weight | Marks | What Wins |
|------|--------|-------|-----------|
| Problem Understanding & Relevance | 15% | 1.5 | Clear user, real-world usefulness, gap-problem grasp |
| Innovation & Originality | 20% | 2.0 | Beyond ordinary search/summarization/chatbot |
| Working Prototype & Functionality | 25% | 2.5 | Core workflow works end-to-end |
| Technical Implementation | 15% | 1.5 | Web dev quality, data handling, AI integration, reliability |
| Evidence, Accuracy & Transparency | 15% | 1.5 | Findings traceable to sources; uncertainty communicated |
| Presentation & Demo | 10% | 1.0 | Clarity, usability, realistic demonstration |

## 2.3 Judging Guidance (Official)

- Working polished core feature > many incomplete features
- Demo with real or clearly identified sample sources
- AI findings labelled as *potential gaps/signals*, not guaranteed facts
- Judges must inspect source references behind important findings
- Generic chatbot or AI summary alone does **not** satisfy the challenge

## 2.4 Suggested Demo Flow (Official)

> Enter research question → add/retrieve several sources → show extracted information → demonstrate at least one potential gap or conflict → open supporting source references → generate checklist of what user should verify next.

---

# 3. Analysis of Three Reference Documents

## 3.1 Document 1: `SHINCHAN_HACKATHON_WINNING_PROJECT_RESEARCH.md`

**Nature:** Practical, student-facing, RTX-3050-tuned, SIH/Devpost/Imagine Cup patterns  
**Value:** Highest — most ideas explicitly 24–48h scoped; best India-domain thesis  

**Key reusable concepts:**
- Self-correcting RAG (retrieval eval → query rewrite → rerank → faithfulness) — **24h viable if scoped to 2–3 stages**
- Structured output (Pydantic/Outlines/Instructor) — **trivial, high-reliability win**
- Multimodal VLM (Qwen2.5-VL / Florence-2 / Gemini Flash) — **API or small local model**
- Multilingual Indic (Whisper ASR, IndicTrans2, Indic NLP) — **India differentiation**
- Uncertainty/calibration & human-in-the-loop — **yes as trust layer**
- Evaluation-driven dev (baseline + metric) — **cheap, judge-winning**

**What NOT to build (infeasible in 24h):**
- GridArc-µPMU (OPAL-RT/RTDS + Jetson + µPMU)
- PyroCast-AI (WRF-SFIRE supercompute)
- SepsisWave-AI (credentialed MIMIC + proprietary monitors)
- BridgeGuard-AI (sensor rig + bespoke calibration)

## 3.2 Document 2: `2_SHINCHAN_HACKATHON_WINNING_PROJECT_RESEARCH.md`

**Nature:** Research-grade, problem-first, hard domains  
**Value:** Low for build, high for concepts — most need specialized hardware/data  

**Reusable ideas:** Physics-informed constraints, uncertainty/calibration, workflow integration  
**Top overlap:** Crop-disease CV, Construction safety CV, Self-correcting RAG, Code-review agent, Medical document intelligence, LLM security/gateway/eval, Accessibility for visually impaired

## 3.3 Document 3: `ADVANCED_AI_HACKATHON_PROJECT_ROADMAP.md`

**Nature:** Engineering-depth, production-thinking (RAG eval, LLM gateways, security, observability)  
**Value:** Medium-high — best source of differentiating engineering techniques  

**Strongest reusable concepts:** Self-correcting RAG, Structured output, Small language models, Multilingual Indic, Time-series foundation models, LLM gateway, AI security/guardrails, Uncertainty/calibration, Evaluation-driven dev

---

# 4. Refined Product Vision

## 4.1 Product Positioning

> **GapLens — AI Research Intelligence & Information Gap Analysis Engine**  
> *"See what's missing. Verify what matters."*

Not a search engine. Not a summarizer. Not a chatbot. Not ordinary RAG.  
A **structured research workspace** that answers: *What exists? What's missing? What conflicts? What's outdated? What's evidenced? What should I check next?*

## 4.2 Target Users & Workflows

| Persona | Research Goal | Pain Point |
|---------|---------------|------------|
| Scholarship seeker | "What should I verify before applying for Scholarship X?" | Misses renewal conditions, doc requirements, deadline changes |
| College applicant | "What are the actual admission requirements for Program Y?" | Conflicting info across forums, outdated brochures, missing deadlines |
| Startup founder | "What regulations apply to my fintech idea in India?" | Scattered RBI/circular/Gazette sources, version drift |
| Healthcare researcher | "What's the current evidence for Treatment Z?" | Contradictory studies, outdated guidelines, missing populations |
| Policy analyst | "What are the gaps in the new Bill's coverage?" | Cross-referencing amendments, missing stakeholder views |

## 4.3 Core Value Proposition

| Dimension | GapLens Delivers |
|-----------|------------------|
| **Coverage** | Research-dimension matrix: Covered / Partial / Missing / Conflicting / Outdated |
| **Evidence** | Every claim → exact source passage → URL → date → authority signal |
| **Contradictions** | Genuine conflicts highlighted with context (cycle, geography, definition) |
| **Freshness** | Domain-aware freshness (scholarship cycle vs. tech docs vs. regulations) |
| **Actionability** | Prioritized verification checklist with next-step, priority, suggested authority |
| **Trust** | AI suggestions clearly separated from extracted facts; confidence calibrated |

---

# 5. Product Format Decision: Web App vs Extension vs Hybrid

## 5.1 Comparison Matrix

| Criterion | Standalone Web App (Option A) | Browser Extension (Option B) | Hybrid (Option C) |
|-----------|-------------------------------|------------------------------|-------------------|
| **Search Access** | Full via APIs (Tavily/Exa/Jina) | Limited to DOM/scraping | Best of both |
| **Data Collection** | Controlled, reproducible | User's live Google results | Extension collects → App processes |
| **User Experience** | Dedicated research workspace | In-context, side-panel | Flexible |
| **Differentiation** | Full pipeline visible | Lightweight companion | Complex to demo |
| **Technical Complexity** | Medium (API orchestration) | Medium (content scripts, CSP) | High (two surfaces) |
| **Deployment** | Vercel + Render (simple) | Chrome Web Store (review delay) | Both |
| **24h Solo Feasibility** | **High** | Medium (manifest, popup, bg) | Low |
| **Future Scalability** | High (API-first) | Limited by browser APIs | High |
| **Demo Impact** | **High — full dashboard** | Medium — side panel | High but risky |

## 5.2 Definitive Recommendation: **Option A — Standalone Web Application**

**Rationale:**
1. **Judges evaluate via submitted GitHub + optional live link** — a deployed web app is immediately accessible; an extension requires installation.
2. **Search APIs (Tavily, Exa, Jina) give better results than scraping Google SERPs** — cleaner content, structured highlights, no CAPTCHA/blocking risk.
3. **Full dashboard UX** — coverage matrix, contradiction cards, checklist — needs screen real estate; extension side-panel is cramped.
4. **24-hour solo reality** — one codebase, one deploy, one demo flow. Extension adds manifest V3, content-script debugging, CSP issues.
5. **Future-proof** — API-first architecture extends to CLI, MCP server, mobile PWA later.

**Hybrid concession:** Add a "Paste URLs" tab so users can manually add sources from their browser — captures Option B's benefit without the extension complexity.

---

# 6. User Personas & Real-World Workflows

## 6.1 Primary Persona: "Priya — Scholarship Seeker"
- **Goal:** Apply for "Central Sector Scholarship 2026"
- **Workflow:** Enters goal → GapLens searches → finds 8 sources → extracts 23 claims → coverage matrix shows "Renewal conditions: NOT FOUND", "Income certificate format: CONFLICTING (2 sources differ)" → checklist prioritizes "Verify renewal on NSP portal" + "Confirm income cert format with college nodal officer"
- **Outcome:** Submits complete application; avoids rejection for missing renewal undertaking

## 6.2 Secondary Persona: "Rohit — Startup Founder"
- **Goal:** "RBI regulations for account aggregator license"
- **Workflow:** Pastes 3 RBI circular URLs + adds search → GapLens detects "Net-worth requirement: OUTDATED (2022 circular superseded by 2024 amendment)" → flags "Fit & proper criteria: PARTIAL (only director criteria found, not shareholder)" → checklist says "Read Master Direction 2024 Section 4.2" + "Consult CA for net-worth calc"
- **Outcome:** Saves weeks of compliance missteps

## 6.3 Tertiary Persona: "Dr. Mehta — Medical Researcher"
- **Goal:** "Current guideline for Drug X in Condition Y"
- **Workflow:** Searches → 12 sources (ICMR, FDA, EMA, PubMed, pharma sites) → contradiction: "Dosage: ICMR 2023 says 50mg, Pharma site says 75mg" → freshness: "EMA guideline 2021, FDA 2024" → checklist: "Use FDA 2024 dosing; verify ICMR update status"
- **Outcome:** Protocol uses latest evidence; ethics committee approves faster

---

# 7. Competitive Landscape

## 7.1 Direct Competitors (AI Research Assistants)

| Product | Search | Evidence | Contradiction | Gaps | Freshness | Customization | Sessions |
|---------|--------|----------|---------------|------|-----------|---------------|----------|
| **Perplexity** | ✅ | Citations | ❌ | ❌ | ⚠️ | ❌ | ✅ |
| **Gemini Deep Research** | ✅ | Citations | ⚠️ | ⚠️ | ⚠️ | ❌ | ✅ |
| **ChatGPT Deep Research** | ✅ | Citations | ⚠️ | ⚠️ | ⚠️ | ❌ | ✅ |
| **Elicit** | Academic only | ✅ | ❌ | ⚠️ | ✅ | ⚠️ | ✅ |
| **Consensus** | Academic only | ✅ | ✅ (meter) | ❌ | ✅ | ❌ | ✅ |
| **Genspark** | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ❌ | ✅ |
| **GapLens (ours)** | ✅ | **Claim-level** | **Context-aware** | **Dimension-based** | **Domain-aware** | **User-defined** | ✅ |

## 7.2 Feature Gap Analysis

| Underserved Workflow | Current Tools Fail Because | GapLens Solves By |
|----------------------|----------------------------|-------------------|
| **Scholarship/admissions verification** | Generic search; no dimension template | User-defined dimensions + checklist |
| **Regulatory compliance tracking** | No version/date awareness | Freshness engine + amendment tracking |
| **Cross-source contradiction resolution** | Treat all differences as conflicts | Context-aware contradiction classification |
| **Evidence traceability for decisions** | Citations only at paragraph level | Claim → passage → source → date chain |
| **Actionable next steps** | Stop at summary | Prioritized verification checklist |

## 7.3 Differentiation Statement

> **GapLens is not "better search" — it's "structured gap analysis."**  
> Competitors answer "what did I find?" GapLens answers "what am I missing, what conflicts, what's stale, and what do I do next?" — with evidence for every claim.

---

# 8. Search Infrastructure Deep Dive

## 8.1 Functional Separation

| Function | Description | Why It Matters |
|----------|-------------|----------------|
| **Search Discovery** | Query → ranked URLs + snippets | Finds relevant sources |
| **Page Crawling** | Fetch HTML/JS-rendered page | Accesses full content |
| **Content Extraction** | HTML → clean Markdown/text | LLM-ready input |
| **Semantic Retrieval** | Embeddings + vector search | Finds relevant passages |
| **Metadata Extraction** | Date, author, site type, authority | Freshness + credibility |
| **Evidence Passage Retrieval** | Exact spans for citations | Traceability |

## 8.2 Provider Comparison (Current as of Oct 2026)

| Provider | Search | Crawl | Extract | Semantic | Metadata | Free Tier | Pricing (indicative) | Best For |
|----------|--------|-------|---------|----------|----------|-----------|---------------------|----------|
| **Tavily** | ✅ Neural/Keyword | ✅ | ✅ Chunked | ❌ | Title, date, favicon | 1,000 req/mo | $0.005/search (lite) | Primary search + extract |
| **Exa** | ✅ Neural (auto/lite/deep) | ✅ | ✅ Highlights/text/summary | ❌ | Published date, category | 1,000 req/mo | $0.007/search (auto) | Deep research, structured output |
| **Jina Reader** | ✅ s.jina.ai (SERP) | ✅ r.jina.ai | ✅ Markdown + OCR | ✅ Embeddings API | Title, timestamp | 100 RPM search, 500 RPM extract | Token-based (~$0.50/MTok) | Extraction + embeddings + rerank |
| **Firecrawl** | ✅ Search (2 cred/10) | ✅ Crawl/Map | ✅ Markdown/JSON | ❌ | Basic | 1,000 cred/mo | $19/mo (5k cred) | Heavy crawl/scrape needs |
| **SerpAPI** | ✅ Google/Bing/DuckDuckGo | ❌ | ❌ (raw HTML) | ❌ | Rich SERP features | 250/mo | $25/mo (1k) | When Google results specifically needed |
| **Brave Search** | ✅ Independent index | ❌ | ❌ | ❌ | Basic | 2,000/mo | $3/1k req | Privacy-focused, independent index |

## 8.3 Selected Stack

| Role | Provider | Reason |
|------|----------|--------|
| **Primary Search + Extract** | **Tavily** | Fast (180ms p50), built-in extraction, highlights, generous free tier, agent-optimized |
| **Backup Search** | **Exa (lite)** | Different index, structured output schema, deep search if needed |
| **Primary Extraction** | **Jina Reader (r.jina.ai)** | Best Markdown quality, OCR for PDFs, image captions, 500 RPM free |
| **Backup Extraction** | **Firecrawl Scrape** | Handles JS-heavy sites, JSON output schema |
| **Embeddings** | **Jina Embeddings v3** | 1024-dim, multilingual, 500 RPM free, SOTA on MTEB |
| **Reranking** | **Jina Reranker v2** | Cross-encoder, 500 RPM free, improves retrieval precision |

## 8.4 API Integration Patterns

### Tavily Search → Extract Flow
```python
# 1. Search
results = tavily.search(query="scholarship renewal conditions 2026", 
                        search_depth="advanced",
                        max_results=10,
                        include_answer=False)

# 2. Extract full content for top URLs
urls = [r.url for r in results.results[:8]]
extracted = tavily.extract(urls=urls, include_images=False)
# Returns: [{url, raw_content, extracted_content}]
```

### Jina Reader Extraction (for any URL)
```python
# Simple GET - no API key needed for basic usage
async with httpx.AsyncClient() as client:
    resp = await client.get("https://r.jina.ai/http://example.com/page")
    markdown = resp.text  # Clean LLM-ready content
```

### Jina Search (SERP)
```python
# GET https://s.jina.ai/?q=query
async with httpx.AsyncClient() as client:
    resp = await client.get("https://s.jina.ai/", params={"q": "RBI account aggregator 2024"})
    # Returns top 5 results with title, url, content
```

## 8.5 Search Query Planning Strategy

| Stage | Technique | Implementation |
|-------|-----------|----------------|
| **Initial broad** | User goal → 3-5 diverse queries | LLM expands: "scholarship X" → ["eligibility", "documents", "deadline", "renewal", "contact"] |
| **Gap-driven** | Coverage matrix gaps → targeted queries | If "renewal" missing → "scholarship X renewal conditions site:gov.in" |
| **Contradiction-driven** | Conflicting claims → verification queries | If deadline differs → "scholarship X 2026 deadline official notification" |
| **Freshness-driven** | Undated/old sources → recency queries | "scholarship X 2025 2026 latest notification" |
| **Authority-driven** | Low-authority sources → primary source queries | "scholarship X site:scholarships.gov.in OR site:nsp.gov.in" |

---

# 9. LLM and AI Model Selection

## 9.1 Model Comparison (Oct 2026)

| Model | Provider | Context | Reasoning | Structured Out | Multilingual | Cost/MTok (In/Out) | Latency | Best Role |
|-------|----------|---------|-----------|----------------|--------------|-------------------|---------|-----------|
| **Gemini 1.5 Flash** | Google | 1M | ✅ | ✅ JSON Schema | ✅ 100+ | Free tier / $0.075/$0.30 | ~1s | **Primary reasoning** |
| **Gemini 1.5 Pro** | Google | 2M | ✅✅ | ✅ | ✅ | $1.25/$5.00 | ~3s | Complex reasoning fallback |
| **GPT-4o-mini** | OpenAI | 128K | ✅ | ✅ JSON Schema | ✅ | $0.15/$0.60 | ~1.5s | Backup reasoning |
| **GPT-4o** | OpenAI | 128K | ✅✅ | ✅ | ✅ | $5/$15 | ~2s | High-stakes fallback |
| **Claude 3.5 Sonnet** | Anthropic | 200K | ✅✅ | ✅ | ✅ | $3/$15 | ~2s | Nuanced analysis |
| **Claude 3.5 Haiku** | Anthropic | 200K | ✅ | ✅ | ✅ | $0.25/$1.25 | ~0.8s | Fast extraction |
| **Llama 3.1 8B (Groq)** | Groq | 128K | ✅ | ✅ | ✅ | ~$0.05/$0.08 | ~0.3s | Ultra-fast extraction |
| **Qwen2.5-7B (Groq)** | Groq | 128K | ✅ | ✅ | ✅✅ | ~$0.05/$0.08 | ~0.3s | Multilingual extraction |

## 9.2 Definitive Model Assignments

| Role | Model | Provider | Why |
|------|-------|----------|-----|
| **Primary Reasoning** (goal understanding, dimension gen, contradiction analysis, gap prioritization, checklist) | **Gemini 1.5 Flash** | Google AI Studio | 1M context, free tier, strong reasoning, JSON schema, multilingual |
| **Fast Extraction** (claim extraction, entity normalization, date parsing) | **Llama 3.1 8B / Qwen2.5-7B** | Groq | Sub-second, structured output, free tier on Groq |
| **Embeddings** | **Jina Embeddings v3** | Jina AI | 1024-dim, multilingual, 8K context, 500 RPM free |
| **Reranking** | **Jina Reranker v2** | Jina AI | Cross-encoder precision, 500 RPM free |
| **OCR/Document** | **Jina Reader (jina-ocr-v1)** | Jina AI | Handles PDFs, tables, images in extraction |

## 9.3 Provider Abstraction Layer

```python
# llm/providers.py
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Type, TypeVar

T = TypeVar('T', bound=BaseModel)

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, response_model: Type[T] = None) -> T | str: ...
    
    @abstractmethod
    async def extract_structured(self, text: str, schema: Type[T]) -> T: ...

class GeminiProvider(LLMProvider):
    def __init__(self, model: str = "gemini-1.5-flash"):
        self.client = genai.GenerativeModel(model)
    
    async def complete(self, prompt: str, response_model: Type[T] = None):
        if response_model:
            # Use JSON schema via generation_config
            schema = response_model.model_json_schema()
            config = {"response_mime_type": "application/json", "response_schema": schema}
            resp = await self.client.generate_content_async(prompt, generation_config=config)
            return response_model.model_validate_json(resp.text)
        return (await self.client.generate_content_async(prompt)).text

class GroqProvider(LLMProvider):
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.client = AsyncGroq()
        self.model = model
    
    async def extract_structured(self, text: str, schema: Type[T]) -> T:
        # Use JSON mode with schema in prompt
        prompt = f"Extract per schema: {schema.model_json_schema()}\n\nText:\n{text}"
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )
        return schema.model_validate_json(resp.choices[0].message.content)
```

## 9.4 Cost Estimate per Research Session

| Component | Calls | Tokens (In/Out) | Cost (Flash) | Cost (Groq) |
|-----------|-------|-----------------|--------------|-------------|
| Goal understanding | 1 | 2K/1K | $0.0002 | - |
| Dimension generation | 1 | 3K/2K | $0.0004 | - |
| Query planning | 1 | 2K/1K | $0.0002 | - |
| Claim extraction (8 sources) | 8 | 15K/8K | - | $0.0018 |
| Contradiction analysis | 1 | 10K/3K | $0.0010 | - |
| Freshness analysis | 1 | 5K/2K | $0.0004 | - |
| Gap prioritization | 1 | 8K/3K | $0.0008 | - |
| Checklist generation | 1 | 5K/2K | $0.0005 | - |
| **Total** | **15** | **~50K/22K** | **~$0.0035** | **~$0.002** |

**Estimated cost: <$0.01 per session** — well within free tiers.

---

# 10. Core Information Gap Detection Algorithms

## 10.1 Pipeline Overview (11 Stages)

```
User Goal
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 1: Research Goal Understanding │
│  → Main objective, scope, entities, │
│    time period, geography, constraints│
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 2: Research Dimension Generation │
│  → Dynamic framework (eligibility,  │
│    deadline, docs, renewal, contact)│
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 3: Search Query Planning       │
│  → 5-15 targeted queries per dim.   │
│  → Iterative: gap-driven expansion  │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 4: Source Processing           │
│  → Search → Extract → Clean → Chunk │
│  → Preserve URL, metadata, dates    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 5: Claim Extraction            │
│  → Passages → Structured Claims     │
│  → Claim: {text, dimension, source, │
│     excerpt, date, confidence}      │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 6: Coverage Mapping            │
│  → Matrix: Dimension × Claim Status │
│  → Covered / Partial / Missing /    │
│     Conflicting / Outdated / Weak   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 7: Contradiction Detection     │
│  → Cluster claims by (entity, attr, │
│    time, context) → Compare →       │
│    Classify: Genuine / Contextual   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 8: Freshness Analysis          │
│  → Pub date, modified, retrieval,   │
│    validity period → Classification │
│  → Domain-aware thresholds          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 9: Evidence Validation         │
│  → Direct vs indirect evidence      │
│  → Unsupported AI claims flagged    │
│  → Source authority weighting       │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 10: Gap Prioritization         │
│  → Score: Importance × Impact ×     │
│     EvidenceDeficit × Uncertainty   │
│    × TimeSensitivity                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Stage 11: Verification Planning      │
│  → Action cards: {dimension, status,│
│     priority, reason, evidence,     │
│     next_action, authority}         │
└─────────────────────────────────────┘
```

## 10.2 Stage 1: Research Goal Understanding

**Input:** User query (e.g., "What should I verify before applying for Scholarship X?")  
**Output:** Structured `ResearchGoal` object

```python
class ResearchGoal(BaseModel):
    main_objective: str
    scope: List[str]           # ["eligibility", "documents", "deadline", ...]
    entities: List[Entity]     # {name: "Scholarship X", type: "scholarship"}
    time_period: TimePeriod    # {start: "2026-01-01", end: "2026-12-31", cycle: "2026-27"}
    geography: List[str]       # ["India", "Central Government"]
    constraints: List[str]     # ["income < 8L", "first-year student"]
    expected_answer_types: List[str]  # ["checklist", "deadline", "document list"]
```

**Technique:** Single LLM call with JSON schema + few-shot examples.  
**Fallback:** Keyword/rule-based NER for entities + heuristic scope detection.

## 10.3 Stage 2: Research Dimension Generation

**Input:** `ResearchGoal`  
**Output:** `List[ResearchDimension]`

```python
class ResearchDimension(BaseModel):
    id: str                    # "eligibility", "deadline", "documents"
    name: str                  # "Eligibility Criteria"
    description: str           # "Who can apply, income limits, categories"
    importance: int            # 1-5 (user goal dependent)
    expected_evidence_types: List[str]  # ["official notification", "FAQ", "portal"]
    verification_authorities: List[str] # ["NSP portal", "Ministry website"]
    user_defined: bool         # True if user added custom dimension
```

**Technique:** LLM generates dimensions from goal + domain templates.  
**Domain Templates** (pre-defined, user-extensible):
- Scholarship: eligibility, income, academics, documents, deadline, process, renewal, benefits, contact
- Admission: eligibility, cutoff, dates, documents, fees, reservation, hostel, contact
- Regulation: scope, definitions, requirements, penalties, timeline, authority, amendments
- Medical: indication, dosage, contraindications, side-effects, evidence-grade, guidelines

**User Customization:** UI allows add/remove/rename dimensions before search.

## 10.4 Stage 3: Search Query Planning

**Input:** `ResearchGoal` + `List[ResearchDimension]`  
**Output:** `List[SearchQuery]`

```python
class SearchQuery(BaseModel):
    query: str
    target_dimensions: List[str]
    query_type: Literal["broad", "targeted", "verification", "authority", "recency"]
    priority: int
    source_preferences: List[str]  # ["official", "news", "academic", "forum"]
```

**Algorithm:**
1. **Broad queries** (1-2): General topic + goal
2. **Dimension-targeted** (3-5 per dim): Dimension-specific keywords + entity names
3. **Authority-biased** (1-2): `site:gov.in OR site:nsp.gov.in OR site:official`
4. **Recency-biased** (1-2): `2025..2026` date filters
5. **Gap-driven** (iterative): After Stage 6, generate queries for Missing/Conflicting dims

**Deduplication:** Embedding-based query similarity (cosine > 0.85 → merge).

## 10.5 Stage 4: Source Processing

```python
class Source(BaseModel):
    url: HttpUrl
    title: str
    domain: str
    source_type: Literal["official", "news", "academic", "forum", "commercial", "unknown"]
    publication_date: datetime | None
    last_modified: datetime | None
    retrieval_date: datetime = Field(default_factory=datetime.utcnow)
    authority_score: float  # 0-1 (domain reputation, HTTPS, gov/edu TLD)
    relevance_score: float  # 0-1 (semantic similarity to queries)
    content: str            # Clean markdown from Jina Reader
    chunks: List[Chunk]     # 500-token overlapping chunks
```

**Pipeline:**
1. Tavily search → top 15 URLs
2. Parallel Jina Reader extraction (max 10 concurrent)
3. Filter: content > 500 chars, relevance > 0.3
4. Chunk: 500 tokens, 100 overlap, preserve chunk→source mapping
5. Embed chunks (Jina v3) → store in vector DB

## 10.6 Stage 5: Claim Extraction

**Input:** Source chunks  
**Output:** `List[Claim]`

```python
class Claim(BaseModel):
    id: str
    text: str                    # Normalized claim statement
    dimension_id: str            # Links to ResearchDimension
    source_id: str               # Links to Source
    excerpt: str                 # Exact supporting passage (≤300 chars)
    chunk_ids: List[str]         # Provenance
    claim_type: Literal["fact", "requirement", "deadline", "condition", "procedure", "contact", "other"]
    entity: str                  # "income limit", "application deadline"
    attribute: str               # "maximum", "date", "list"
    value: str                   # "8 lakh", "31 Oct 2026", ["Aadhaar", "Income Cert"]
    date_context: DateContext    # {stated_date, validity_period, cycle}
    confidence: float            # 0-1 (extraction confidence)
    evidence_status: Literal["direct", "indirect", "inferred", "unsupported"]
```

**Extraction Prompt Strategy:**
```
Extract ALL factual claims from this text about [dimension].
For each claim output JSON with: text, entity, attribute, value, excerpt, claim_type, confidence.
Only extract claims SUPPORTED by the text. Do not infer.
If a claim has conditions/exceptions, include them in the text.
```

**Validation:** Post-extraction rule-based checks:
- Date parsing normalization (DD/MM/YYYY, MM/DD/YYYY, "last date", "by 31st")
- Numeric normalization (lakhs/crores, percentages)
- Entity linking to ResearchGoal entities

## 10.7 Stage 6: Coverage Mapping

**Input:** `List[ResearchDimension]` + `List[Claim]`  
**Output:** `CoverageMatrix`

```python
class DimensionCoverage(BaseModel):
    dimension_id: str
    status: Literal["covered", "partial", "missing", "conflicting", "outdated", "weak_evidence"]
    claim_count: int
    unique_values: int
    supporting_sources: int
    confidence_avg: float
    latest_source_date: datetime | None
    gaps: List[str]  # Specific missing sub-questions
```

**Algorithm:**
```
For each dimension:
  claims = [c for c in claims if c.dimension_id == dim.id]
  if not claims: status = "missing"
  elif has_conflicts(claims): status = "conflicting"
  elif is_outdated(claims): status = "outdated"
  elif low_evidence(claims): status = "weak_evidence"
  elif len(set(c.value for c in claims)) == 1 and high_confidence(claims): status = "covered"
  else: status = "partial"
```

**Conflict Detection Heuristic (pre-Stage 7):**
- Same entity + same attribute + different values → potential conflict
- Values normalized (dates parsed, numbers standardized) before comparison

## 10.8 Stage 7: Contradiction Detection Engine

**Input:** Claims clustered by (entity, attribute, time_context)  
**Output:** `List[Contradiction]`

```python
class Contradiction(BaseModel):
    id: str
    entity: str
    attribute: str
    conflicting_claims: List[ClaimRef]  # {claim_id, value, source, date, excerpt}
    contradiction_type: Literal["genuine", "contextual", "temporal", "definitional", "jurisdictional"]
    resolution: str  # "Source A newer", "Source B official", "Different cycles", "Unresolvable"
    confidence: float
    evidence_for_resolution: List[EvidenceRef]
```

**Algorithm:**
```
For each claim cluster (same entity + attribute):
  1. Normalize values (dates, numbers, categorical)
  2. If all normalized values equal → no contradiction
  3. Else analyze context:
     - Different time_context (cycle/year) → TEMPORAL
     - Different geography/jurisdiction → JURISDICTIONAL
     - Different definitions (gross vs net income) → DEFINITIONAL
     - Different source authority + date → GENUINE (newer/higher authority wins)
     - Else → CONTEXTUAL (may be both true in different contexts)
  4. Generate resolution recommendation
```

**Key Insight:** Not every difference is a contradiction. The engine classifies and explains.

## 10.9 Stage 8: Freshness Intelligence

**Domain-Aware Freshness Thresholds:**

| Domain | Critical Threshold | Warning Threshold | Validity Signal |
|--------|-------------------|-------------------|-----------------|
| Scholarships/Admissions | > 1 year | > 6 months | Application cycle year |
| Regulations/Policy | > 6 months | > 3 months | Amendment date, gazette notification |
| Technology/API | > 3 months | > 1 month | Version number, changelog |
| Healthcare | > 2 years | > 1 year | Guideline version, systematic review date |
| Market/Prices | > 1 month | > 2 weeks | Publication date, "as of" |

**Algorithm:**
```python
def classify_freshness(source: Source, domain: str) -> FreshnessStatus:
    age = (now - (source.last_modified or source.publication_date or source.retrieval_date)).days
    critical, warning = THRESHOLDS[domain]
    
    if not source.publication_date and not source.last_modified:
        return "undated"
    elif age > critical:
        return "outdated"
    elif age > warning:
        return "aging"
    elif has_validity_period(source):
        return "current" if within_period else "expired"
    else:
        return "current"
```

## 10.10 Stage 9: Evidence Validation

**Goal:** Distinguish extracted facts from AI inferences; flag weak evidence.

```python
class EvidenceValidation(BaseModel):
    claim_id: str
    has_direct_evidence: bool          # Explicit statement in source
    has_indirect_evidence: bool        # Implied, requires inference
    evidence_quality: Literal["strong", "moderate", "weak", "none"]
    source_authority: float            # 0-1
    corroboration_count: int           # Other sources with same claim
    unsupported_ai_inference: bool     # Claim appears only in LLM output, not source
    validation_notes: str
```

**Checks:**
1. **Excerpt verification:** Claim.excerpt must exist in Source.content (fuzzy match)
2. **Corroboration:** Count other sources with same (entity, attribute, value)
3. **Authority weighting:** Gov/edu > established news > forums > commercial
4. **AI hallucination check:** Re-read source with claim as query; verify entailment (NLI or LLM-as-judge)

## 10.11 Stage 10: Gap Prioritization

```python
class GapPriority(BaseModel):
    dimension_id: str
    gap_type: Literal["missing", "partial", "conflicting", "outdated", "weak_evidence"]
    priority_score: float  # 0-100
    priority: Literal["critical", "high", "medium", "low"]
    rationale: str
```

**Scoring Formula:**
```
priority = 
  (importance_weight * dimension.importance) +
  (impact_weight * decision_impact) +
  (evidence_weight * (1 - evidence_quality_score)) +
  (uncertainty_weight * (1 - confidence_avg)) +
  (time_weight * time_sensitivity)
```

**Weights (tunable):** importance=0.3, impact=0.25, evidence=0.2, uncertainty=0.15, time=0.1

## 10.12 Stage 11: Verification Planning

```python
class VerificationAction(BaseModel):
    dimension_id: str
    gap_type: str
    status: Literal["critical", "high", "medium", "low"]
    reason: str
    supporting_evidence: List[EvidenceRef]  # Claims/sources showing the gap
    next_action: str                        # "Check official portal for 2026 notification"
    recommended_authority: str              # "National Scholarship Portal (scholarships.gov.in)"
    estimated_effort: Literal["quick", "moderate", "extensive"]
    verification_method: Literal["official_source", "cross_reference", "contact_authority", "calculate"]
```

**Output:** Prioritized checklist — the user's actionable roadmap.

---

# 11. Research Orchestration Architecture

## 11.1 Orchestration Pattern: Deterministic Pipeline with Selective LLM Reasoning

**Not an agent loop.** Fixed stages, explicit data flow, LLM only where reasoning adds value.

```python
# orchestrator.py
class ResearchOrchestrator:
    def __init__(self):
        self.search = SearchService()
        self.extractor = ExtractionService()
        self.llm_reasoning = ReasoningProvider()      # Gemini Flash
        self.llm_extraction = ExtractionProvider()     # Groq Llama/Qwen
        self.embedder = EmbeddingProvider()            # Jina v3
        self.vector_store = VectorStore()
        self.db = Database()
    
    async def run(self, goal: ResearchGoal, user_dimensions: List[ResearchDimension] = None) -> ResearchReport:
        # Stage 1-2: Understand + Dimensions
        dimensions = await self.generate_dimensions(goal, user_dimensions)
        
        # Stage 3: Initial queries
        queries = self.plan_queries(goal, dimensions)
        
        # Stage 4: Search + Extract (iterative loop, max 2 rounds)
        sources = []
        for round in range(2):
            new_sources = await self.search_and_extract(queries)
            sources.extend(new_sources)
            
            # Stage 5: Extract claims
            claims = await self.extract_claims(new_sources, dimensions)
            
            # Stage 6: Coverage check
            coverage = self.map_coverage(dimensions, claims)
            
            # If all critical dims covered → break
            if self.is_sufficient(coverage):
                break
            
            # Stage 3b: Gap-driven query expansion
            queries = self.generate_gap_queries(coverage, dimensions)
        
        # Stages 7-11: Analysis (can run in parallel)
        contradictions = await self.detect_contradictions(claims)
        freshness = self.analyze_freshness(sources, goal.domain)
        evidence = self.validate_evidence(claims, sources)
        gaps = self.prioritize_gaps(coverage, contradictions, freshness, evidence, dimensions)
        checklist = self.generate_checklist(gaps, claims, sources)
        
        return ResearchReport(
            goal=goal, dimensions=dimensions, sources=sources,
            claims=claims, coverage=coverage, contradictions=contradictions,
            freshness=freshness, evidence=evidence, gaps=gaps, checklist=checklist
        )
```

## 11.2 Iterative Search Control

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max search rounds | 2 | Diminishing returns; 24h constraint |
| Max sources/round | 8 | Token budget, processing time |
| Max total sources | 15 | Coverage vs. noise |
| Stopping criteria | All critical dims "covered" OR no new claims in round | Efficiency |

## 11.3 Parallelization Strategy

```python
# Stages 7-11 independent → run concurrently
async def analyze_parallel(claims, sources, dimensions, coverage):
    async with asyncio.TaskGroup() as tg:
        contradictions_task = tg.create_task(detect_contradictions(claims))
        freshness_task = tg.create_task(analyze_freshness(sources))
        evidence_task = tg.create_task(validate_evidence(claims, sources))
    # Gap prioritization needs all three
    gaps = prioritize_gaps(coverage, contradictions_task.result(), 
                           freshness_task.result(), evidence_task.result())
    checklist = generate_checklist(gaps, claims, sources)
    return gaps, checklist
```

---

# 12. Source Intelligence & Evidence Management

## 12.1 Source Classification

```python
def classify_source_type(url: str, content: str, metadata: dict) -> SourceType:
    domain = urlparse(url).netloc
    
    # Official government
    if any(d in domain for d in [".gov.in", ".nic.in", "gov.", ".gov.", "parliament"]):
        return "official_government"
    
    # Educational
    if any(d in domain for d in [".edu", ".ac.in", "university", "college"]):
        return "academic"
    
    # Known news
    if domain in NEWS_DOMAINS:
        return "news"
    
    # Regulatory bodies
    if any(d in domain for d in ["rbi.org.in", "sebi.gov.in", "irdai.gov.in", "tra.gov.in"]):
        return "regulatory"
    
    # Official portals
    if any(d in domain for d in ["nsp.gov.in", "scholarships.gov.in", "aicte-india.org"]):
        return "official_portal"
    
    # Heuristic from content
    if has_official_indicators(content):
        return "potential_official"
    
    return "general"
```

## 12.2 Authority Scoring

```python
AUTHORITY_WEIGHTS = {
    "official_government": 1.0,
    "official_portal": 0.95,
    "regulatory": 0.9,
    "academic": 0.85,
    "news": 0.7,
    "potential_official": 0.6,
    "general": 0.4,
    "forum": 0.3,
    "commercial": 0.35,
    "unknown": 0.2
}

def calculate_authority(source: Source) -> float:
    base = AUTHORITY_WEIGHTS.get(source.source_type, 0.2)
    # Adjust for HTTPS, domain age, content quality signals
    return min(1.0, base * source.https_bonus * source.content_quality_factor)
```

## 12.3 Evidence Provenance Chain

```
Verification Checklist Item
    │
    ▼
Information Gap (with priority)
    │
    ▼
Coverage Matrix Cell (dimension + status)
    │
    ▼
Claim(s) supporting the gap status
    │
    ▼
Source Excerpt (exact text, char offsets)
    │
    ▼
Source (URL, title, date, authority)
```

**Critical:** Every user-facing finding must trace back to a source excerpt. No "AI says" without evidence.

---

# 13. Contradiction Detection Engine (Deep Dive)

## 13.1 Contradiction Taxonomy

| Type | Example | Resolution Strategy |
|------|---------|---------------------|
| **Genuine** | Source A: "Deadline 15 Nov", Source B: "Deadline 30 Nov" (same cycle) | Newer/higher authority wins; flag for verification |
| **Temporal** | Source A (2023): "Income limit 8L", Source B (2024): "Income limit 6L" | Latest wins; show both with dates |
| **Jurisdictional** | Central: "Income 8L", State: "Income 6L" | Both valid; clarify scope |
| **Definitional** | "Income" = gross vs net; "Family" = parents only vs parents+siblings | Extract definitions; show both |
| **Contextual** | "Required: Aadhaar" vs "Required: Aadhaar OR Voter ID" | Not contradictory; merge as alternatives |
| **Cycle-Based** | "2025 cycle: 15 Nov", "2026 cycle: 30 Nov" | Not contradictory; label by cycle |

## 13.2 Detection Algorithm

```python
def detect_contradictions(claims: List[Claim]) -> List[Contradiction]:
    # 1. Cluster by (entity, attribute, normalized_time_context)
    clusters = cluster_claims(claims)
    
    contradictions = []
    for cluster in clusters:
        if len(cluster) < 2:
            continue
        
        # 2. Normalize values for comparison
        normalized = [(c, normalize_value(c.value, c.attribute)) for c in cluster]
        unique_values = set(v for _, v in normalized)
        
        if len(unique_values) == 1:
            continue  # No contradiction
        
        # 3. Classify contradiction type
        c_type = classify_contradiction_type(cluster)
        
        # 4. Generate resolution
        resolution = generate_resolution(cluster, c_type)
        
        contradictions.append(Contradiction(
            entity=cluster[0].entity,
            attribute=cluster[0].attribute,
            conflicting_claims=[ClaimRef.from_claim(c) for c in cluster],
            contradiction_type=c_type,
            resolution=resolution,
            confidence=calculate_confidence(cluster)
        ))
    
    return contradictions
```

## 13.3 Value Normalization

| Attribute | Normalization |
|-----------|---------------|
| **Dates** | Parse to ISO; handle "last date", "by 31st", "Nov 15" |
| **Currency** | Convert to INR; handle lakhs/crores/k |
| **Percentages** | Decimal (0-1) |
| **Lists** | Sort + deduplicate (Aadhaar, PAN) vs (PAN, Aadhaar) = same |
| **Booleans** | Yes/True/Required/1 = same |
| **Text** | Lowercase, remove stopwords, stemming for fuzzy match |

---

# 14. Freshness Intelligence Engine

## 14.1 Multi-Signal Freshness

| Signal | Extraction Method | Weight |
|--------|-------------------|--------|
| **Publication date** | Meta tags, JSON-LD, heuristics, URL patterns | 0.4 |
| **Last modified** | HTTP headers, sitemap, page signals | 0.2 |
| **Content date references** | Regex for "2024-25", "FY 2026", "w.e.f." | 0.2 |
| **Validity period** | Explicit "valid until", "cycle 2026-27" | 0.2 |

## 14.2 Domain-Specific Logic

```python
SCHOLARSHIP_FRESHNESS_RULES = {
    "cycle_pattern": r"(20\d{2}[-/]20\d{2}|AY\s*20\d{2})",
    "official_portals": ["scholarships.gov.in", "nsp.gov.in", "aicte-india.org"],
    "key_dates": ["application_start", "application_end", "renewal_deadline", "disbursement"],
    "supersession": "Later notification on same scheme supersedes earlier"
}

REGULATION_FRESHNESS_RULES = {
    "gazette_date": "Gazette notification date is authoritative",
    "amendment_chain": "Track amendment notifications; latest consolidates",
    "effective_date": "May differ from publication date",
    "repeal_check": "Check if repealed by subsequent act"
}
```

## 14.3 Freshness Output

```python
class FreshnessAssessment(BaseModel):
    source_id: str
    classification: Literal["current", "aging", "outdated", "expired", "undated", "future"]
    effective_date: datetime | None
    expiry_date: datetime | None
    cycle: str | None          # "2026-27"
    confidence: float
    signals_used: List[str]
    warning: str | None        # "References 2024 cycle; 2026 cycle may differ"
```

---

# 15. Evidence Validation Engine

## 15.1 Evidence Hierarchy

```
Level 1: Direct quote from official primary source
    "The income ceiling is ₹8 lakh per annum." — scholarships.gov.in notification
    
Level 2: Direct quote from secondary authoritative source
    "Income limit ₹8L for Central Sector Scholarship" — PIB press release
    
Level 3: Direct quote from credible news/analysis
    "Scholarship income limit raised to ₹8L" — The Hindu, dated
    
Level 4: Indirect / inferred from source
    "Table shows income brackets up to 8L" — implies ceiling
    
Level 5: AI inference only (NO source excerpt)
    "Likely the limit is ₹8L based on pattern" — FLAGGED
```

## 15.2 Validation Pipeline

```python
async def validate_claim_evidence(claim: Claim, source: Source) -> EvidenceValidation:
    # 1. Excerpt verification
    excerpt_found = fuzzy_match(claim.excerpt, source.content, threshold=0.8)
    
    # 2. Entailment check (claim.text supported by excerpt?)
    entailment = await nli_check(premise=claim.excerpt, hypothesis=claim.text)
    
    # 3. Corroboration
    corroborating = find_corroborating_claims(claim, all_claims)
    
    # 4. Authority
    authority = source.authority_score
    
    # 5. Classify
    if not excerpt_found:
        return EvidenceValidation(..., evidence_quality="none", unsupported_ai_inference=True)
    elif not entailment:
        return EvidenceValidation(..., evidence_quality="weak", validation_notes="Excerpt doesn't fully support claim")
    elif corroborating >= 2 and authority > 0.8:
        return EvidenceValidation(..., evidence_quality="strong")
    elif corroborating >= 1 or authority > 0.7:
        return EvidenceValidation(..., evidence_quality="moderate")
    else:
        return EvidenceValidation(..., evidence_quality="weak")
```

## 15.3 Uncertainty Communication

Every user-facing output includes:
- **Confidence badge:** High/Medium/Low (from evidence quality + corroboration)
- **Evidence toggle:** Click to see exact excerpt + source
- **Uncertainty note:** "Based on 2 sources; 1 from 2023" or "Single source; verify on official portal"

---

# 16. Verification Checklist Engine

## 16.1 Checklist Item Schema

```python
class ChecklistItem(BaseModel):
    id: str
    dimension_id: str
    dimension_name: str
    status: Literal["covered", "partial", "missing", "conflicting", "outdated", "weak_evidence"]
    priority: Literal["critical", "high", "medium", "low"]
    reason: str
    evidence_summary: str           # "2 sources agree on 31 Oct; 1 source says 15 Nov (2023)"
    supporting_evidence: List[EvidenceRef]
    next_action: str                # "Verify deadline on scholarships.gov.in"
    recommended_authority: str      # "National Scholarship Portal"
    verification_method: Literal["official_source", "cross_reference", "contact_authority", "calculate"]
    estimated_effort: Literal["quick", "moderate", "extensive"]
    time_sensitive: bool
    deadline: datetime | None       # If known (e.g., application deadline)
```

## 16.2 Prioritization Logic

| Priority | Criteria |
|----------|----------|
| **Critical** | Missing deadline, conflicting deadline, expired info, legal requirement |
| **High** | Missing required document, conflicting eligibility, outdated regulation |
| **Medium** | Partial coverage, weak evidence, missing contact info |
| **Low** | Nice-to-know, supplementary info, formatting details |

## 16.3 Action Templates (Domain-Aware)

```python
ACTION_TEMPLATES = {
    "scholarship": {
        "deadline": "Check {portal} for {cycle} application timeline",
        "documents": "Download document checklist from {portal}; verify with college nodal officer",
        "eligibility": "Confirm criteria on {portal} FAQ; check income certificate validity",
        "renewal": "Read renewal guidelines on {portal}; note CGPA/attendance requirements",
        "contact": "Email {scheme_email} or call {helpline} for clarification"
    },
    "regulation": {
        "requirement": "Read latest Master Direction/Circular on {regulator}.org.in",
        "definition": "Check definitions section; compare with previous version",
        "date": "Verify effective date vs publication date in Gazette"
    }
}
```

---

# 17. Multilingual Architecture

## 17.1 Requirements

- Input queries in English + Indian languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, etc.)
- Source language detection (most Indian gov sources bilingual English/Hindi)
- Cross-language search (query in Hindi → find English sources + Hindi sources)
- Extraction in source language + translation for UI
- Preserve original excerpts for evidence

## 17.2 Implementation Strategy

| Component | Approach |
|-----------|----------|
| **Query Translation** | User query → detect lang → translate to English for search (Gemini Flash) |
| **Search** | Run English queries + native-language queries (if APIs support) |
| **Extraction** | Jina Reader preserves source language; extract claims in source language |
| **Claim Normalization** | Translate claims to English for comparison; keep original |
| **Contradiction Detection** | Compare normalized English values |
| **UI Display** | User's language for explanations; original excerpt on "View Source" |
| **Output Language** | User-selected (default: English + detected input language) |

## 17.3 Indian Language Support

```python
INDIAN_LANGUAGES = {
    "hi": "Hindi", "bn": "Bengali", "te": "Telugu", "mr": "Marathi",
    "ta": "Tamil", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
    "pa": "Punjabi", "or": "Odia", "as": "Assamese", "ur": "Urdu"
}

# Use Gemini Flash for translation (excellent Indic support)
# For extraction: Jina Reader handles multilingual content well
# Embeddings: Jina v3 is multilingual (100+ languages)
```

**MVP Scope:** English + Hindi fully. Other languages: query translation + UI labels only.

---

# 18. Advanced Differentiating Features

## 18.1 Three Strongest Differentiators (MVP)

### 1. Dynamic Research Coverage Matrix
**What:** Visual matrix showing every research dimension × status (Covered/Partial/Missing/Conflicting/Outdated/Weak) with claim counts and confidence.  
**Why unique:** Competitors show lists; GapLens shows *structured completeness*.  
**Tech:** Deterministic from claims + dimensions.  
**Demo:** "See instantly: Renewal=MISSING, Deadline=CONFLICTING, Documents=COVERED"

### 2. Evidence-Linked Contradiction Cards
**What:** Each contradiction shows both claims side-by-side with excerpts, dates, sources, classification (Genuine/Temporal/Contextual), and resolution recommendation.  
**Why unique:** Others hide or oversimplify conflicts. GapLens makes them inspectable and resolvable.  
**Tech:** Stage 7 algorithm + deterministic UI.  
**Demo:** "Two deadline claims → shows 2023 vs 2024 circular → recommends 2024 official"

### 3. Prioritized Verification Checklist with Authority Routing
**What:** Actionable checklist: "Verify deadline on NSP portal (Critical) → Link opens NSP" not just "Check deadline."  
**Why unique:** Transforms analysis into action with specific next steps and authorities.  
**Tech:** Stage 11 + domain templates.  
**Demo:** "Click 'Verify' → opens official portal in new tab; checklist tracks completion"

## 18.2 Additional Differentiators (P1/P2)

| Feature | Problem Solved | Tech | MVP? |
|---------|----------------|------|------|
| Research Completeness Score | "How done am I?" | Weighted coverage % | P1 |
| Evidence Provenance Graph | "Where did this come from?" | Graph viz (D3/React Flow) | P2 |
| Claim-Level Source Attribution | Granular traceability | Already in schema | P0 |
| Cross-Source Contradiction Graph | Visual conflict map | Graph edges = contradictions | P2 |
| Source Authority Independence | Detect copied content | Text similarity + domain clustering | P2 |
| Adaptive Search Expansion | Auto-find more for gaps | Stage 3b iterative | P0 |
| Search Stopping Criteria | Don't overspend | Coverage threshold + diminishing returns | P0 |
| Temporal Claim Tracking | "How has this changed?" | Versioned claims per session | P2 |
| Source Update Monitoring | "Notify if source changes" | Firecrawl Monitor / cron | P2 |
| Evidence Sufficiency Analysis | "Is this enough to decide?" | Thresholds per dimension | P1 |
| Confidence Calibration | Reliable probabilities | Conformal prediction / Platt scaling | P2 |
| Human-in-the-Loop Verification | User confirms/resolves | Checklist completion tracking | P1 |
| Cross-Language Evidence | Find Hindi source for English claim | Multilingual search + alignment | P1 |
| Research Blind-Spot Detection | "What didn't I think to ask?" | LLM suggests missing dimensions | P1 |
| Primary Source Discovery | Find original gov notification | Authority-biased queries + redirect follow | P1 |
| Missing Stakeholder Perspective | "Who else has a view?" | LLM suggests missing viewpoints | P2 |
| Research Session Comparison | "What changed since last week?" | Diff two reports | P2 |
| Evidence-Backed Verification Roadmap | Checklist is the roadmap | Already in Stage 11 | P0 |

---

# 19. Complete System Architecture

## 19.1 High-Level Architecture

```mermaid
flowchart TB
    subgraph Frontend["Frontend (Next.js 14 + React 18 + Tailwind)"]
        UI["Research Dashboard"]
        Config["Goal Config + Dimension Builder"]
        Sources["Source Manager"]
        Matrix["Coverage Matrix"]
        Contradictions["Contradiction Cards"]
        Checklist["Verification Checklist"]
        History["Session History"]
    end

    subgraph Backend["Backend (FastAPI + Pydantic)"]
        API["REST API /analyze, /sessions, /sources"]
        Orchestrator["Research Orchestrator"]
        Stages["Stage Modules (1-11)"]
    end

    subgraph AI["AI Layer"]
        LLM_R["Gemini Flash (Reasoning)"]
        LLM_E["Groq Llama/Qwen (Extraction)"]
        EMB["Jina Embeddings v3"]
        RERANK["Jina Reranker v2"]
    end

    subgraph Search["Search & Extraction"]
        TAVILY["Tavily Search + Extract"]
        JINA_S["Jina Search (s.jina.ai)"]
        JINA_R["Jina Reader (r.jina.ai)"]
        FIRE["Firecrawl (backup)"]
    end

    subgraph Data["Data Layer"]
        DB[(PostgreSQL + pgvector)]
        CACHE[(Redis)]
        FILES["File Storage (S3/R2)"]
    end

    UI --> API
    Config --> API
    Sources --> API
    Matrix --> API
    Contradictions --> API
    Checklist --> API
    History --> API

    API --> Orchestrator
    Orchestrator --> Stages
    Stages --> LLM_R
    Stages --> LLM_E
    Stages --> EMB
    Stages --> RERANK
    Stages --> TAVILY
    Stages --> JINA_S
    Stages --> JINA_R
    Stages --> FIRE
    Orchestrator --> DB
    Orchestrator --> CACHE
    API --> DB

---

## 19.2 Detailed Component Architecture

### Request Lifecycle
```
POST /api/v1/analyze
    │
    ▼
Validate Request → Create ResearchSession (DB) → Return session_id
    │
    ▼
Background Task: orchestrator.run(goal, dimensions)
    │
    ├── Stage 1-2: Goal Understanding + Dimensions (LLM_R)
    ├── Stage 3: Query Planning (deterministic + LLM_R)
    ├── Stage 4: Search + Extract (TAVILY/JINA) → Store Sources
    ├── Stage 5: Claim Extraction (LLM_E parallel per source)
    ├── Stage 6: Coverage Mapping (deterministic)
    ├── Stage 7-11 Parallel: Contradictions, Freshness, Evidence, Gaps, Checklist
    │
    ▼
Update ResearchSession with Report (DB) → WebSocket/notify frontend
```

### Search Pipeline
```
User Query + Dimensions
    │
    ▼
Query Planner → [Broad, Targeted, Authority, Recency] queries
    │
    ▼
Parallel Search (Tavily primary, Exa backup)
    │
    ▼
Deduplicate URLs (exact + embedding similarity)
    │
    ▼
Parallel Extract (Jina Reader primary, Firecrawl backup)
    │
    ▼
Filter & Score (relevance > 0.3, content > 500 chars)
    │
    ▼
Chunk + Embed (Jina v3) → pgvector
    │
    ▼
Source Objects → DB
```

### AI Analysis Pipeline
```
Sources + Chunks + Dimensions
    │
    ▼
┌─────────────────────────────────────┐
│ Claim Extraction (LLM_E)            │
│ - Parallel per source               │
│ - Structured output (Pydantic)      │
│ - Excerpt verification              │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Coverage Matrix (deterministic)     │
│ - Dimension × Claim status          │
│ - Gap identification                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────┬─────────────┬─────────┐
│Contradictions│ Freshness  │ Evidence│  (Parallel, LLM_R + deterministic)
│ Detection    │ Analysis   │Validation│
└─────────────┴─────────────┴─────────┘
    │
    ▼
Gap Prioritization (weighted scoring)
    │
    ▼
Verification Checklist (templates + LLM_R)
```

## 19.3 Database Schema (PostgreSQL + pgvector)

```sql
-- Core Tables
CREATE TABLE research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,  -- nullable for anonymous
    goal_text TEXT NOT NULL,
    goal_json JSONB NOT NULL,  -- ResearchGoal
    dimensions_json JSONB NOT NULL,  -- ResearchDimension[]
    status VARCHAR(20) DEFAULT 'pending',  -- pending, running, completed, failed
    report_json JSONB,  -- Full ResearchReport
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES research_sessions(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title TEXT,
    domain VARCHAR(255),
    source_type VARCHAR(50),
    publication_date TIMESTAMP,
    last_modified TIMESTAMP,
    retrieval_date TIMESTAMP DEFAULT NOW(),
    authority_score FLOAT,
    relevance_score FLOAT,
    content TEXT,  -- Full markdown
    metadata_json JSONB,  -- Raw extraction metadata
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE source_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    chunk_index INT,
    content TEXT NOT NULL,
    token_count INT,
    embedding VECTOR(1024),  -- Jina v3
    char_start INT,
    char_end INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON source_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES research_sessions(id) ON DELETE CASCADE,
    source_id UUID REFERENCES sources(id),
    chunk_ids UUID[],
    dimension_id VARCHAR(100),
    claim_text TEXT NOT NULL,
    entity VARCHAR(255),
    attribute VARCHAR(255),
    value TEXT,
    claim_type VARCHAR(50),
    excerpt TEXT,
    date_context JSONB,
    confidence FLOAT,
    evidence_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE contradictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES research_sessions(id) ON DELETE CASCADE,
    entity VARCHAR(255),
    attribute VARCHAR(255),
    type VARCHAR(30),  -- genuine, temporal, contextual, etc.
    claim_ids UUID[],
    resolution TEXT,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE freshness_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    classification VARCHAR(30),  -- current, aging, outdated, expired, undated
    effective_date TIMESTAMP,
    expiry_date TIMESTAMP,
    cycle VARCHAR(50),
    confidence FLOAT,
    signals JSONB,
    warning TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE evidence_validations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    quality VARCHAR(20),  -- strong, moderate, weak, none
    has_direct BOOLEAN,
    has_indirect BOOLEAN,
    corroboration_count INT,
    source_authority FLOAT,
    unsupported_ai BOOLEAN,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE checklist_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES research_sessions(id) ON DELETE CASCADE,
    dimension_id VARCHAR(100),
    status VARCHAR(30),
    priority VARCHAR(20),
    reason TEXT,
    evidence_summary TEXT,
    next_action TEXT,
    recommended_authority TEXT,
    verification_method VARCHAR(30),
    effort VARCHAR(20),
    time_sensitive BOOLEAN,
    deadline TIMESTAMP,
    claim_ids UUID[],
    source_ids UUID[],
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 19.4 Pydantic Schemas (Core)

```python
# schemas.py
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime
from uuid import UUID

class ResearchGoal(BaseModel):
    main_objective: str
    scope: List[str]
    entities: List[Dict[str, str]]
    time_period: Dict[str, Optional[str]]
    geography: List[str]
    constraints: List[str]
    expected_answer_types: List[str]
    domain: Literal["scholarship", "admission", "regulation", "healthcare", "general"]

class ResearchDimension(BaseModel):
    id: str
    name: str
    description: str
    importance: int = Field(ge=1, le=5)
    expected_evidence_types: List[str]
    verification_authorities: List[str]
    user_defined: bool = False

class Source(BaseModel):
    id: UUID
    url: HttpUrl
    title: str
    domain: str
    source_type: Literal["official_government", "official_portal", "regulatory", "academic", "news", "potential_official", "general", "forum", "commercial", "unknown"]
    publication_date: Optional[datetime]
    last_modified: Optional[datetime]
    retrieval_date: datetime
    authority_score: float = Field(ge=0, le=1)
    relevance_score: float = Field(ge=0, le=1)
    content: str
    chunks: List['Chunk']

class Chunk(BaseModel):
    id: UUID
    source_id: UUID
    content: str
    token_count: int
    char_start: int
    char_end: int

class Claim(BaseModel):
    id: UUID
    text: str
    dimension_id: str
    source_id: UUID
    excerpt: str
    chunk_ids: List[UUID]
    claim_type: Literal["fact", "requirement", "deadline", "condition", "procedure", "contact", "other"]
    entity: str
    attribute: str
    value: str
    date_context: Dict[str, Any]
    confidence: float = Field(ge=0, le=1)
    evidence_status: Literal["direct", "indirect", "inferred", "unsupported"]

class DimensionCoverage(BaseModel):
    dimension_id: str
    status: Literal["covered", "partial", "missing", "conflicting", "outdated", "weak_evidence"]
    claim_count: int
    unique_values: int
    supporting_sources: int
    confidence_avg: float
    latest_source_date: Optional[datetime]
    gaps: List[str]

class Contradiction(BaseModel):
    id: UUID
    entity: str
    attribute: str
    conflicting_claims: List[Dict[str, Any]]  # ClaimRef
    contradiction_type: Literal["genuine", "contextual", "temporal", "definitional", "jurisdictional"]
    resolution: str
    confidence: float

class FreshnessAssessment(BaseModel):
    source_id: UUID
    classification: Literal["current", "aging", "outdated", "expired", "undated", "future"]
    effective_date: Optional[datetime]
    expiry_date: Optional[datetime]
    cycle: Optional[str]
    confidence: float
    signals_used: List[str]
    warning: Optional[str]

class ChecklistItem(BaseModel):
    id: UUID
    dimension_id: str
    dimension_name: str
    status: str
    priority: Literal["critical", "high", "medium", "low"]
    reason: str
    evidence_summary: str
    supporting_evidence: List[Dict[str, Any]]
    next_action: str
    recommended_authority: str
    verification_method: Literal["official_source", "cross_reference", "contact_authority", "calculate"]
    estimated_effort: Literal["quick", "moderate", "extensive"]
    time_sensitive: bool
    deadline: Optional[datetime]

class ResearchReport(BaseModel):
    session_id: UUID
    goal: ResearchGoal
    dimensions: List[ResearchDimension]
    sources: List[Source]
    claims: List[Claim]
    coverage: List[DimensionCoverage]
    contradictions: List[Contradiction]
    freshness: List[FreshnessAssessment]
    checklist: List[ChecklistItem]
    generated_at: datetime
```

## 19.5 API Endpoint Design

```python
# API Routes
POST   /api/v1/analyze              # Start research session
GET    /api/v1/sessions/{id}        # Get session + report
GET    /api/v1/sessions             # List user sessions
POST   /api/v1/sessions/{id}/sources # Add custom source URLs
DELETE /api/v1/sessions/{id}/sources/{source_id}  # Remove source
POST   /api/v1/sessions/{id}/rerun  # Re-run analysis (with new dims/sources)
GET    /api/v1/sessions/{id}/export # Export report (JSON/Markdown/PDF)
POST   /api/v1/sessions/{id}/checklist/{item_id}/complete  # Mark checklist item done

# Request/Response Examples
# POST /analyze
{
  "goal": "What should I verify before applying for Central Sector Scholarship 2026?",
  "dimensions": null,  // Optional user-defined
  "custom_sources": ["https://scholarships.gov.in/..."],  // Optional
  "language": "en"  // or "hi"
}

# Response: { "session_id": "uuid", "status": "running" }

# GET /sessions/{id} (when completed)
{
  "session_id": "uuid",
  "status": "completed",
  "report": { ... ResearchReport ... }
}
```

## 19.6 Background Task Strategy

```python
# tasks.py
from fastapi import BackgroundTasks
import asyncio

async def run_research(session_id: UUID):
    async with get_db() as db:
        session = await db.get(ResearchSession, session_id)
        session.status = "running"
        await db.commit()
        
        try:
            report = await orchestrator.run(session.goal, session.dimensions)
            session.report = report.model_dump()
            session.status = "completed"
            session.completed_at = datetime.utcnow()
        except Exception as e:
            session.status = "failed"
            session.error = str(e)
        finally:
            await db.commit()
            # Notify via WebSocket / SSE
            await notify_frontend(session_id, session.status)

# In route:
@app.post("/api/v1/analyze")
async def start_analysis(request: AnalyzeRequest, background: BackgroundTasks):
    session = await create_session(request)
    background.add_task(run_research, session.id)
    return {"session_id": session.id, "status": "running"}
```

## 19.7 Error Handling & Resilience

| Failure Point | Fallback |
|---------------|----------|
| Tavily API down | Exa lite → Jina Search → SerpAPI (if configured) |
| Jina Reader fails | Firecrawl Scrape → Tavily Extract → Raw HTML fallback |
| Gemini Flash quota exceeded | GPT-4o-mini → Claude Haiku → Local Llama (Groq) |
| Groq extraction fails | Gemini Flash extraction (slower) |
| pgvector unavailable | In-memory FAISS (session-only) |
| Database down | SQLite local (dev) / Supabase (prod) |
| Rate limit hit | Exponential backoff + queue; degrade to cached demo data |

## 19.8 Caching Strategy

| Cache Key | TTL | Invalidation |
|-----------|-----|--------------|
| Search results (query hash) | 1 hour | Manual refresh button |
| Jina Reader extraction (URL hash) | 24 hours | On re-analyze |
| Embeddings (chunk hash) | Permanent | Content hash change |
| LLM responses (prompt hash) | 1 hour | Model version change |
| Session report | Until update | Session rerun |

## 19.9 Rate Limiting & Security

```python
# Rate limits (per IP + per user)
RATE_LIMITS = {
    "analyze": "10/hour",      # Heavy operation
    "sources": "30/minute",    # Add/remove sources
    "rerun": "5/hour",         # Re-analysis
    "export": "20/hour"
}

# Prompt Injection Protection
def sanitize_input(text: str) -> str:
    # Remove potential injection patterns
    patterns = [
        r"ignore previous instructions",
        r"system prompt",
        r"you are now",
        r"forget everything",
        r"<\|.*?\|>",  # Special tokens
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text[:10000]  # Hard limit

# SSRF Protection
ALLOWED_DOMAINS = None  # Allow all for research; block private IPs
BLOCKED_IPS = ["127.0.0.1", "169.254.169.254", "10.", "192.168.", "172.16.-172.31."]
```

---

# 20. Frontend & UX Specification

## 20.1 Screen Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. LANDING                                                    │
│    Hero: "Find what's missing. Verify what matters."         │
│    Demo video → "Start Research" → /research/new             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. NEW RESEARCH SESSION                                      │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ Research Goal                                       │  │
│    │ "What should I verify before applying for          │  │
│    │  Central Sector Scholarship 2026?"                 │  │
│    ├─────────────────────────────────────────────────────┤  │
│    │ [+] Add Custom Sources (optional)                  │  │
│    │ [+] Add Custom Dimensions (optional)               │  │
│    │ Language: [English ▼] [Hindi ▼]                    │  │
│    │                    [Start Analysis]                │  │
│    └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PROCESSING (Real-time updates via WebSocket)             │
│    ┌─────────────────────────────────────────────────────┐  │
│    │ 🔍 Searching sources... (8/15)                      │  │
│    │ 📄 Extracting content... (5/8)                      │  │
│    │ 🧠 Analyzing claims... (23 claims found)            │  │
│    │ ⚖️  Checking contradictions...                      │  │
│    │ 📋 Building checklist...                            │  │
│    └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. VERIFICATION DASHBOARD (Main View)                       │
│    ┌──────────────┬──────────────────┬────────────────────┐  │
│    │ RESEARCH     │ COVERAGE MATRIX  │ SOURCES (8)        │  │
│    │ OVERVIEW     │                  │                    │  │
│    │              │ ████ Covered     │ 1. scholarships.gov│  │
│    │ Goal: ...    │ ████ Partial     │ 2. nsp.gov.in      │  │
│    │ Domain: Schol│ ████ Missing     │ 3. pib.gov.in      │  │
│    │ Sources: 8   │ ████ Conflicting │ ...                │  │
│    │ Claims: 23   │ ████ Outdated    │ [+] Add Source     │  │
│    │ Gaps: 4      │ ████ Weak Evid.  │                    │  │
│    │              │                  │                    │  │
│    │ Completeness:│ Eligibility ████ │ CLAIMS (23)        │  │
│    │ 67%          │ Deadline   ███░░ │ Filter: [All ▼]    │  │
│    │              │ Documents  ████  │ • Income ≤ 8L      │  │
│    │              │ Renewal    ░░░░  │ • Deadline 31 Oct  │  │
│    │              │ Contact    ███░  │ • Docs: Aadhaar... │  │
│    └──────────────┴──────────────────┴────────────────────┘  │
│    ┌──────────────────────────────────────────────────────┐  │
│    │ ⚠️ CONTRADICTIONS (1)                                 │  │
│    │ Deadline: Source A (2024) = 31 Oct  │ Source B (2023)=15 Nov │
│    │ Type: TEMPORAL  → Resolution: Use 2024 official       │  │
│    │ [View Sources]                                        │  │
│    ├──────────────────────────────────────────────────────┤  │
│    │ ⏰ FRESHNESS WARNINGS (2)                             │  │
│    │ Source 3: 2023 circular (aging for 2026 cycle)       │  │
│    │ Source 7: Undated forum post                          │  │
│    ├──────────────────────────────────────────────────────┤  │
│    │ ✅ VERIFICATION CHECKLIST                             │  │
│    │ 🔴 CRITICAL: Confirm deadline on NSP portal          │  │
│    │ 🟠 HIGH: Find renewal conditions (missing)           │  │
│    │ 🟡 MEDIUM: Verify document list with college         │  │
│    │ 🟢 LOW: Save helpline number                          │  │
│    │ [Mark Complete] [Export] [Share]                     │  │
│    └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 20.2 Component Hierarchy

```
App
├── Layout (Header, Sidebar/Navigation)
├── LandingPage
├── ResearchWizard
│   ├── GoalInput
│   ├── SourceManager (add/remove/paste URLs)
│   ├── DimensionBuilder (add/remove/edit)
│   └── LanguageSelector
├── ProcessingView (WebSocket progress)
├── Dashboard
│   ├── ResearchHeader (goal, stats, actions)
│   ├── CoverageMatrix (interactive grid)
│   ├── SourcePanel (list + add + credibility badges)
│   ├── ClaimExplorer (filterable, sortable table)
│   ├── ContradictionCards (expandable)
│   ├── FreshnessAlerts (timeline view)
│   └── Checklist (priority-sorted, actionable)
├── SourceDetailModal (full content + highlights)
├── ClaimDetailModal (excerpt + evidence + validation)
├── ContradictionDetailModal (side-by-side comparison)
├── SessionHistory (list + compare)
└── Settings (API keys, preferences)
```

## 20.3 Visual Language

| Element | Specification |
|---------|---------------|
| **Colors** | Primary: #2563EB (Blue 600), Success: #059669, Warning: #D97706, Error: #DC2626, Info: #0891B2 |
| **Status Badges** | Covered: Green, Partial: Blue, Missing: Red, Conflicting: Orange, Outdated: Amber, Weak: Gray |
| **Priority** | Critical: Red + 🔴, High: Orange + 🟠, Medium: Yellow + 🟡, Low: Green + 🟢 |
| **Typography** | Inter (UI), JetBrains Mono (code/excerpts), Noto Sans (Indic) |
| **Spacing** | 4px base, 8/12/16/24/32 scale |
| **Icons** | Lucide React (consistent, accessible) |
| **Evidence Links** | Dotted underline → click opens SourceDetailModal at exact position |

## 20.4 Key Interactions

| Interaction | Behavior |
|-------------|----------|
| Click dimension in Matrix | Filters Claims + opens Contradictions for that dimension |
| Click claim in ClaimExplorer | Opens ClaimDetailModal with excerpt highlighted in source |
| Click "View Sources" on Contradiction | Opens ContradictionDetailModal (side-by-side) |
| Click checklist "Verify" | Opens official URL in new tab; marks item in-progress |
| Hover source badge | Tooltip: authority score, type, date |
| Toggle "Show AI-only" | Filters claims with evidence_status=unsupported |
| Export | Generates Markdown with full traceability |

---

# 21. Evaluation & Reliability Framework

## 21.1 Benchmark Design

**Test Set:** 12 research questions across 4 domains

| Domain | Questions | Known Gaps/Contradictions |
|--------|-----------|---------------------------|
| Scholarships | 3 | Renewal missing, deadline conflict, doc list conflict |
| Admissions | 3 | Cutoff outdated, reservation conflict, hostel missing |
| Regulations | 3 | Amendment supersession, definition conflict, date conflict |
| Healthcare | 3 | Dosage conflict, guideline version, population missing |

**Ground Truth:** Manually labeled by domain expert (me) with:
- Expected dimensions per question
- Known contradictions with resolutions
- Expected checklist priorities

## 21.2 Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Dimension Coverage Recall** | ≥ 85% | % of ground-truth dimensions detected |
| **Claim Extraction Precision** | ≥ 80% | % of extracted claims validated by human |
| **Claim Extraction Recall** | ≥ 70% | % of ground-truth claims found |
| **Contradiction Detection Precision** | ≥ 85% | % of flagged contradictions genuine |
| **Contradiction Classification Accuracy** | ≥ 80% | Correct type (genuine/temporal/etc.) |
| **Freshness Classification Accuracy** | ≥ 90% | Correct label vs. manual |
| **Checklist Actionability** | ≥ 4.0/5 | Human rating (1-5) |
| **Evidence Traceability** | 100% | Every checklist item → source excerpt |
| **End-to-End Latency** | < 60s | P95 for 10 sources |
| **Cost per Session** | < $0.05 | API costs |

## 21.3 Evaluation Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **Custom Python Scripts** | Primary: run benchmark, compute metrics | `python eval/run_benchmark.py` |
| **RAGAS** | Faithfulness, Answer Relevancy, Context Precision/Recall | `ragas.evaluate()` on claim extraction |
| **DeepEval** | G-Eval for checklist quality, Hallucination check | `deepeval.test.run()` |
| **Langfuse** (optional) | Trace logging, prompt versioning | `@observe` decorators |

## 21.4 Baseline Comparisons

| Baseline | Description |
|----------|-------------|
| **Keyword Search + Manual** | User searches Google, reads top 10, makes own checklist |
| **Perplexity + Manual** | Perplexity answer → user extracts gaps manually |
| **Naive RAG** | Single retrieval + summary → no gap analysis |
| **GapLens (Ours)** | Full pipeline |

**Demo Metric:** Show side-by-side: "Naive RAG found 3 gaps. GapLens found 7 (including 2 critical deadline conflicts)."

---

# 22. Security & Responsible AI

## 22.1 Threat Model

| Threat | Mitigation |
|--------|------------|
| **Prompt Injection in Retrieved Content** | Sanitize all extracted text before LLM input; use structured output schemas; delimiter-based prompts |
| **Malicious URLs (SSRF)** | Block private IPs, localhost, metadata endpoints; validate URLs |
| **Unsafe HTML/JS in Extraction** | Jina Reader returns clean Markdown; never render raw HTML |
| **API Key Exposure** | Server-side only; never in frontend; env vars + secret manager |
| **Hallucinated Citations** | Excerpt verification (fuzzy match + entailment); flag unsupported |
| **Overconfidence** | Calibrated confidence; show evidence quality; never "guaranteed" |
| **Copyright/Scraping** | Respect robots.txt; use APIs with ToS; cache only for session |
| **PII in Sources** | No PII expected in public sources; redact if detected |
| **High-Stakes Misinformation** | Disclaimer: "Not official advice. Verify with authority." |

## 22.2 Responsible AI Practices

1. **Every AI finding labeled:** "Potential gap detected" not "Gap exists"
2. **Uncertainty visible:** Confidence badges, evidence quality, corroboration count
3. **Source authority transparent:** Badge on each source (Official/News/Forum)
4. **No decision automation:** Checklist guides verification; user decides
5. **Audit trail:** Full session logs for debugging
6. **Privacy:** No user data stored beyond session; anonymous mode default

---

# 23. MVP Scope & Feature Prioritization

## 23.1 Priority Classification

| Feature | Priority | Complexity | Dependencies | Est. Time | Risk | Judging Impact |
|---------|----------|------------|--------------|-----------|------|----------------|
| **Core Pipeline (Stages 1-11)** | **P0** | High | All APIs | 10h | Medium | Critical |
| **Tavily + Jina Integration** | **P0** | Medium | API keys | 2h | Low | Critical |
| **Claim Extraction + Coverage Matrix** | **P0** | High | LLM_E, pgvector | 4h | Medium | Critical |
| **Contradiction Detection** | **P0** | High | Claims clustered | 3h | Medium | High |
| **Freshness Analysis** | **P0** | Medium | Source dates | 2h | Low | High |
| **Verification Checklist** | **P0** | Medium | Gaps + templates | 2h | Low | Critical |
| **Dashboard UI (Matrix, Cards, Checklist)** | **P0** | High | React components | 6h | Medium | Critical |
| **Session Persistence (DB)** | **P0** | Low | PostgreSQL | 1h | Low | Required |
| **Source Manager (Add/Remove URLs)** | **P0** | Low | Frontend + API | 1h | Low | Required |
| **Export (Markdown/JSON)** | **P0** | Low | Report schema | 0.5h | Low | Demo polish |
| **Multilingual (Hindi UI + Query)** | **P1** | Medium | Gemini translation | 2h | Medium | Differentiator |
| **Adaptive Search (Round 2)** | **P1** | Medium | Coverage gaps | 1.5h | Low | Differentiator |
| **Evidence Quality Badges** | **P1** | Low | Validation pipeline | 1h | Low | Trust signal |
| **Confidence Calibration** | **P2** | High | Conformal prediction | 4h | High | Future |
| **Provenance Graph Viz** | **P2** | High | D3/React Flow | 3h | Medium | Demo wow |
| **Session Comparison** | **P2** | Medium | Diff algorithm | 2h | Low | Future |
| **Source Monitoring** | **P2** | High | Firecrawl Monitor | 3h | Medium | Future |

## 23.2 P0 Scope (Must Work in 24h)

1. **Research Session Creation** → Goal input + optional sources/dimensions
2. **Search & Extraction** → Tavily + Jina Reader (10 sources max)
3. **Claim Extraction** → Structured claims with excerpts
4. **Coverage Matrix** → 6-status grid per dimension
5. **Contradiction Cards** → Side-by-side with resolution
6. **Freshness Warnings** → Domain-aware classification
7. **Verification Checklist** → Prioritized, actionable, authority-linked
8. **Dashboard** → All above in single responsive view
9. **Session Save/Load** → PostgreSQL persistence
10. **Export** → Markdown report with evidence

## 23.3 Explicitly Deferred (P2)

- User authentication/accounts
- Multi-language UI beyond Hindi
- Provenance graph visualization
- Session comparison/diff
- Source change monitoring
- Confidence calibration
- Advanced blind-spot detection
- Team collaboration

---

# 24. 24-Hour Execution Roadmap

## Phase 0: Pre-Hackathon Prep (Before Start)

| Task | Done? |
|------|-------|
| Create GitHub repo with structure | ☐ |
| Get API keys: Tavily, Jina, Gemini, Groq | ☐ |
| Prepare 12-question benchmark set + ground truth | ☐ |
| Design DB schema + run migrations locally | ☐ |
| Create `.env.example` with all keys | ☐ |
| Scaffold FastAPI + Next.js with Tailwind | ☐ |
| Write dimension templates for 4 domains | ☐ |

## Phase 1: Backbone (Hours 0-4)

| Time | Task | Output |
|------|------|--------|
| 0:00-0:30 | Repo init, FastAPI skeleton, Pydantic schemas | `backend/app/` runs |
| 0:30-1:30 | Tavily search + Jina extract integration | `search_service.py` working |
| 1:30-2:30 | Claim extraction (Groq Llama/Qwen) | `extraction_service.py` working |
| 2:30-3:30 | Coverage matrix algorithm | `coverage.py` unit tested |
| 3:30-4:00 | DB models + session CRUD | `db.py` + migrations |

**Acceptance:** `POST /analyze` → returns session_id; background task runs Stages 1-6 → saves report.

## Phase 2: Intelligence (Hours 4-10)

| Time | Task | Output |
|------|------|--------|
| 4:00-5:00 | Contradiction detection engine | `contradiction.py` |
| 5:00-5:30 | Freshness analysis | `freshness.py` |
| 5:30-6:30 | Evidence validation | `evidence.py` |
| 6:30-7:30 | Gap prioritization + Checklist | `checklist.py` |
| 7:30-8:30 | Orchestrator wiring (parallel stages) | `orchestrator.py` |
| 8:30-9:30 | Integration test on 3 benchmark Qs | Pass/fail |
| 9:30-10:00 | Fix bugs, add fallbacks | Stable pipeline |

**Acceptance:** Full pipeline runs on benchmark Q1; produces report with all sections.

## Phase 3: Frontend (Hours 10-18)

| Time | Task | Output |
|------|------|--------|
| 10:00-11:00 | Next.js + Tailwind setup, layout | Dev server runs |
| 11:00-12:30 | Research Wizard (Goal + Sources + Dimensions) | `/research/new` works |
| 12:30-14:00 | Processing View (WebSocket progress) | Real-time updates |
| 14:00-16:00 | Dashboard: Overview, Matrix, Sources, Claims | Core views render |
| 16:00-17:00 | Contradiction Cards + Freshness Alerts | Interactive |
| 17:00-18:00 | Checklist + Export + Polish | Complete UX |

**Acceptance:** End-to-end flow works: Wizard → Processing → Dashboard → Export.

## Phase 4: Polish & Demo Prep (Hours 18-22)

| Time | Task | Output |
|------|------|--------|
| 18:00-19:00 | Run full benchmark, record metrics | Metrics JSON |
| 19:00-20:00 | Fix top 3 bugs, add error boundaries | Stable |
| 20:00-21:00 | Deploy: Vercel (FE) + Render (BE) | Live URLs |
| 21:00-22:00 | Record 3-min demo video | MP4 |
| 22:00-22:30 | Write README + submission form | GitHub ready |

## Phase 5: Submission (Hours 22-24)

| Time | Task |
|------|------|
| 22:30-23:30 | Final testing on live deployment |
| 23:30-24:00 | Submit via Unstop/Google Form |
| 24:00 | **Buffer for emergencies** |

## Cut-off Decisions

| If... | Then... |
|-------|---------|
| Tavily fails | Switch to Jina Search + Jina Reader only |
| Gemini quota exceeded | Switch to Groq (Llama/Qwen) for all LLM calls |
| pgvector fails | In-memory list + cosine similarity (no persistence) |
| Frontend build fails | Streamlit fallback (ugly but functional) |
| Deployment fails | ngrok tunnel from local; record demo locally |
| Time < 2h left | Cut adaptive search round 2; skip Hindi UI; ship P0 only |

---

# 25. Repository Structure

```
gaplens/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app, routes, middleware
│   │   ├── config.py               # Settings, API keys, constants
│   │   ├── schemas.py              # All Pydantic models
│   │   ├── database.py             # SQLAlchemy + pgvector setup
│   │   ├── models.py               # ORM models
│   │   ├── api/
│   │   │   ├── routes_analyze.py   # POST /analyze, GET /sessions
│   │   │   ├── routes_sources.py   # Source CRUD
│   │   │   └── routes_export.py    # Export endpoints
│   │   ├── services/
│   │   │   ├── search_service.py   # Tavily, Exa, Jina Search
│   │   │   ├── extraction_service.py # Jina Reader, Firecrawl
│   │   │   ├── llm_reasoning.py    # Gemini Flash provider
│   │   │   ├── llm_extraction.py   # Groq Llama/Qwen provider
│   │   │   ├── embedding_service.py # Jina Embeddings v3
│   │   │   ├── reranker_service.py  # Jina Reranker v2
│   │   │   └── orchestrator.py     # Main pipeline
│   │   ├── stages/
│   │   │   ├── stage1_goal.py
│   │   │   ├── stage2_dimensions.py
│   │   │   ├── stage3_queries.py
│   │   │   ├── stage4_sources.py
│   │   │   ├── stage5_claims.py
│   │   │   ├── stage6_coverage.py
│   │   │   ├── stage7_contradictions.py
│   │   │   ├── stage8_freshness.py
│   │   │   ├── stage9_evidence.py
│   │   │   ├── stage10_gaps.py
│   │   │   └── stage11_checklist.py
│   │   └── utils/
│   │       ├── text.py             # Normalization, cleaning
│   │       ├── dates.py            # Date parsing
│   │       └── clustering.py       # Claim clustering
│   ├── tests/
│   │   ├── test_stages.py
│   │   └── test_integration.py
│   ├── alembic/                    # Migrations
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js 14 App Router
│   │   │   ├── page.tsx            # Landing
│   │   │   ├── research/
│   │   │   │   ├── new/page.tsx    # Wizard
│   │   │   │   ├── [id]/page.tsx   # Dashboard
│   │   │   │   └── history/page.tsx
│   │   │   └── api/                # Proxy to backend
│   │   ├── components/
│   │   │   ├── ui/                 # Button, Card, Badge, Table, Modal
│   │   │   ├── wizard/             # GoalInput, SourceManager, DimensionBuilder
│   │   │   ├── dashboard/
│   │   │   │   ├── CoverageMatrix.tsx
│   │   │   │   ├── SourcePanel.tsx
│   │   │   │   ├── ClaimExplorer.tsx
│   │   │   │   ├── ContradictionCards.tsx
│   │   │   │   ├── FreshnessAlerts.tsx
│   │   │   │   └── Checklist.tsx
│   │   │   └── modals/
│   │   ├── hooks/
│   │   │   ├── useSession.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useDebounce.ts
│   │   ├── lib/
│   │   │   ├── api.ts              # Typed API client
│   │   │   └── utils.ts
│   │   └── styles/
│   │       └── globals.css
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
├── eval/
│   ├── benchmark.json              # 12 questions + ground truth
│   ├── run_benchmark.py
│   └── metrics.py
├── docker-compose.yml              # Local dev (PostgreSQL, Redis)
├── README.md
├── LICENSE
└── .gitignore
```

## 25.1 Key Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `orchestrator.py` | Sequence stages, manage state, handle retries/fallbacks |
| `search_service.py` | Unified interface for Tavily/Exa/Jina search |
| `extraction_service.py` | Unified interface for Jina Reader/Firecrawl |
| `llm_reasoning.py` | Gemini Flash: goal, dimensions, contradictions, gaps, checklist |
| `llm_extraction.py` | Groq: claim extraction (fast, structured) |
| `stage5_claims.py` | Parallel extraction + excerpt verification |
| `stage7_contradictions.py` | Clustering + normalization + classification |
| `stage11_checklist.py` | Priority scoring + action templates |

---

# 26. Deployment Strategy

## 26.1 Target Platforms

| Component | Platform | Plan | Config |
|-----------|----------|------|--------|
| **Frontend** | Vercel | Hobby (free) | `vercel.json` + env vars |
| **Backend** | Render | Free Web Service | `render.yaml` + Docker |
| **Database** | Supabase (PostgreSQL) | Free (500MB) | Connection pooling |
| **Vector** | pgvector on Supabase | Included | `CREATE EXTENSION vector` |
| **Cache** | Upstash Redis | Free (10k req/day) | `REDIS_URL` |
| **Monitoring** | Langfuse Cloud | Free tier | Optional |

## 26.2 Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/gaplens
REDIS_URL=redis://user:pass@host:6379
TAVILY_API_KEY=tvly-...
JINA_API_KEY=jina_...
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...
EXA_API_KEY=exa-...          # Optional backup
FIRECRAWL_API_KEY=fc-...     # Optional backup
SECRET_KEY=...               # For session signing
CORS_ORIGINS=https://gaplens.vercel.app

# Frontend
NEXT_PUBLIC_API_URL=https://gaplens-api.onrender.com
NEXT_PUBLIC_WS_URL=wss://gaplens-api.onrender.com
```

## 26.3 Deploy Commands

```bash
# Backend (Render auto-deploys from GitHub)
# render.yaml specifies: docker build + start command
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Frontend (Vercel auto-deploys)
# vercel --prod

# Database (Supabase)
# Run migrations: alembic upgrade head
```

---

# 27. Final Technology Stack

| Layer | Technology | Version | Why |
|-------|------------|---------|-----|
| **Frontend Framework** | Next.js | 14 (App Router) | React 18, Server Components, Vercel native |
| **UI Library** | Tailwind CSS + shadcn/ui | Latest | Rapid, accessible, customizable |
| **State/Forms** | React Hook Form + Zod | Latest | Type-safe forms |
| **Real-time** | WebSockets (Socket.io) | 4.x | Progress updates |
| **Backend Framework** | FastAPI | 0.110+ | Async, Pydantic, OpenAPI |
| **Validation** | Pydantic | 2.7+ | Schema-driven |
| **Database** | PostgreSQL + pgvector | 16 + 0.7 | ACID + vector search |
| **ORM** | SQLAlchemy | 2.0 | Async support |
| **Migrations** | Alembic | 1.13 | Version control |
| **Cache** | Redis (Upstash) | 7 | Rate limits, caching |
| **Primary Search** | Tavily | API | Agent-optimized, fast |
| **Backup Search** | Exa (lite) | API | Different index, structured |
| **Primary Extraction** | Jina Reader | API | Best Markdown, OCR, free tier |
| **Backup Extraction** | Firecrawl | API | JS-heavy sites |
| **Primary Reasoning LLM** | Gemini 1.5 Flash | API | 1M context, free tier, JSON schema |
| **Backup Reasoning LLM** | GPT-4o-mini / Claude Haiku | API | Fallback |
| **Fast Extraction LLM** | Llama 3.1 8B / Qwen2.5-7B | Groq API | Sub-second, structured |
| **Embeddings** | Jina Embeddings v3 | API | 1024-dim, multilingual, free tier |
| **Reranker** | Jina Reranker v2 | API | Cross-encoder, free tier |
| **Deployment** | Vercel + Render | Free tiers | Zero config, auto-deploy |
| **Local Dev** | Docker Compose | - | PostgreSQL, Redis, hot reload |

---

# 28. Decision Log

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| **Web App (not Extension)** | Browser extension, Hybrid | Judges access via link; full dashboard UX; search APIs > scraping |
| **Tavily Primary Search** | Exa, SerpAPI, Brave, Jina Search | Speed (180ms), built-in extraction, agent-optimized, free tier |
| **Jina Reader Primary Extract** | Firecrawl, Tavily Extract, Custom | Best Markdown quality, OCR, image captions, generous free tier |
| **Gemini Flash Primary LLM** | GPT-4o, Claude Sonnet, Groq Llama | 1M context, free tier, strong reasoning, JSON schema, Indic support |
| **Groq for Extraction** | Gemini Flash, Local Ollama | Sub-second latency, free tier, structured output reliable |
| **Jina v3 Embeddings** | OpenAI text-embedding-3-small, BGE | Multilingual, 1024-dim, 500 RPM free, SOTA MTEB |
| **Deterministic Pipeline** | LangChain/LlamaIndex Agents, AutoGPT | Predictable, debuggable, 24h-feasible, no agent loops |
| **PostgreSQL + pgvector** | SQLite+FAISS, Chroma, Pinecone, Weaviate | Single DB, ACID, vector native, Supabase free tier |
| **No Auth (MVP)** | NextAuth, Clerk, Custom | 24h constraint; anonymous sessions via cookie |
| **Coverage Matrix (not Chat)** | Chat interface, Summary view | Directly matches problem statement deliverables |
| **Structured Output Everywhere** | Free-text + parsing | Reliability, type safety, no regex extraction |

---

# 29. Risks & Failure Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Search API quota exceeded** | Medium | High | Multiple providers; cached demo data; graceful degradation |
| **LLM hallucinates citations** | Medium | High | Excerpt verification (fuzzy + entailment); unsupported flag |
| **Contradiction false positives** | Medium | Medium | Conservative classification; show context; human review |
| **Date parsing errors** | High | Medium | Multiple format handlers; fallback to "undated" |
| **Frontend build fails** | Low | High | Streamlit backup; pre-built static export |
| **Deployment fails** | Low | High | ngrok tunnel; local recording |
| **Time overrun** | High | Critical | Strict P0 scope; cut adaptive round; ship working core |
| **Benchmark fails** | Low | Medium | Pre-recorded metrics; demo with cached results |

---

# 30. Final Strategic Recommendations

## 30.1 Definitive Answers

| Question | Answer |
|----------|--------|
| **Product Name** | **GapLens** |
| **Positioning** | AI Research Intelligence & Information Gap Analysis Engine |
| **Format** | **Standalone Web Application** (Option A) |
| **Primary Search API** | **Tavily** (with Exa lite + Jina Search backup) |
| **Primary Extraction** | **Jina Reader** (with Firecrawl backup) |
| **Primary Reasoning LLM** | **Gemini 1.5 Flash** (with GPT-4o-mini / Claude Haiku backup) |
| **Fast Extraction LLM** | **Llama 3.1 8B / Qwen2.5-7B on Groq** |
| **Embedding Model** | **Jina Embeddings v3** |
| **Vector Database Needed?** | **Yes, pgvector** (single DB, ACID, free on Supabase) |
| **Orchestration Framework** | **Custom Python (FastAPI)** — NOT LangChain/LlamaIndex |
| **Agentic vs Pipeline** | **Deterministic Pipeline with Selective LLM Reasoning** |
| **Top 3 Differentiators** | 1. Dynamic Coverage Matrix 2. Evidence-Linked Contradiction Cards 3. Prioritized Verification Checklist with Authority Routing |
| **Smallest Complete MVP** | Goal → Search → Extract → Claims → Matrix → Contradictions → Freshness → Checklist → Dashboard |
| **Features to Avoid** | Auth, Multi-lang beyond Hindi, Graph viz, Session compare, Monitoring, Calibration, Blind-spot detection |
| **Main Demo Scenario** | **Scholarship Verification** — "What should I verify before applying for Central Sector Scholarship 2026?" |
| **Measurable Technical Value** | Benchmark: 12 Qs, show Coverage Recall 85%+, Contradiction Precision 85%+, Checklist Actionability 4+/5 |
| **Most Likely Failure** | **Time overrun on frontend dashboard** → Mitigation: Build backend API first; frontend can be minimal viable |
| **Build First** | **`POST /analyze` endpoint + Tavily+Jina integration + Claim Extraction + Coverage Matrix** |

## 30.2 Winning-Oriented Strategy

1. **Demo the Checklist, Not the Chat** — Judges expect gaps + checklist per problem statement. Make the checklist the hero.
2. **Show Evidence, Not Magic** — Every card opens to source excerpt. "Don't trust me, verify here."
3. **Benchmark in README** — Table: "GapLens vs Naive RAG vs Manual" with metrics. Proves engineering rigor.
4. **Handle Failures Gracefully** — If API fails, show cached demo data with banner "Using cached data — live APIs temporarily unavailable."
5. **Submit Early** — Working deployed app > perfect local code. Submit at Hour 22, use last 2h for polish.

---

# 31. Official & Technical References

## Official Hackathon Sources
- [Shinchan Online Hackathon 2026 Problem Statement (PDF)](provided) — Official requirements, judging criteria, submission format
- [Devengers LinkedIn](https://in.linkedin.com/company/officialdevengers) — Organizer verification

## Search & Extraction APIs
- [Tavily Documentation](https://docs.tavily.com) — Search, Extract, Research endpoints
- [Exa Documentation](https://docs.exa.ai) — Neural search, highlights, structured output
- [Jina Reader](https://jina.ai/reader/) — URL→Markdown, SERP search, OCR, multilingual
- [Firecrawl](https://docs.firecrawl.dev) — Search, Scrape, Crawl, Map, Interact
- [SerpAPI](https://serpapi.com) — Google/Bing SERP scraping

## LLM Providers
- [Google AI Studio (Gemini)](https://aistudio.google.com) — Gemini 1.5 Flash/Pro free tier
- [OpenAI Platform](https://platform.openai.com/docs/models) — GPT-4o, GPT-4o-mini
- [Anthropic Console](https://console.anthropic.com) — Claude 3.5 Sonnet/Haiku
- [Groq Console](https://console.groq.com) — Llama 3.1, Qwen2.5, ultra-fast inference

## Evaluation Frameworks
- [RAGAS](https://docs.ragas.io) — Faithfulness, Relevancy, Precision, Recall
- [DeepEval](https://deepeval.com) — G-Eval, Task Completion, Hallucination, 30+ metrics
- [Langfuse](https://langfuse.com) — Tracing, prompt management, evals

## Research Papers & Benchmarks
- Tavily Company Search Benchmark — [Blog](https://www.tavily.com/blog/your-agent-has-the-company-name-how-much-can-it-actually-tell-you-about-it)
- Jina Embeddings v3 MTEB Results — [HuggingFace](https://huggingface.co/jinaai/jina-embeddings-v3)
- Exa Deep Search Methodology — [Docs](https://exa.ai/docs/search/deep-search.md)

---

*End of the original blueprint. The product flow remains a reference for pipeline behavior; its Next.js frontend recommendation is superseded by the current implementation decision in `docs/product/App_flow.md`, which serves the six supplied HTML pages from FastAPI.*
