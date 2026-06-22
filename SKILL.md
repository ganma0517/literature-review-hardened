---
name: literature-review-hardened
description: Helps users write high-quality literature reviews (standalone review papers or the literature-review section of a research paper) under a strict "verify-first, never fabricate" regime. Covers a specific part of academic writing — the literature review: depending on discipline/venue it appears in the Introduction or as a separate "Literature Review / Related Work / Theoretical Framework" section before Methods; as a standalone genre it is the entire narrative review/survey article (it does not replace a formal PRISMA systematic review or meta-analysis protocol). Provides end-to-end guidance from topic selection, literature search, evaluation, structure planning, to writing, with built-in anti-hallucination defenses: search before writing, per-claim verification of DOI/retraction, claim-to-citation alignment, and an auditable "Citation Verification Table." Use when the writing must cite only real, checkable sources and must not fabricate citations.
---

# Literature Review Writing Skill (Anti-Hallucination Hardened v2)

Helps you write high-quality academic literature reviews, providing a systematic methodology and writing framework.

> 📍 **Where this fits in a paper / 屬於文章寫作的哪一部分：** this skill targets **one specific component of academic writing — the literature review**, not the whole paper. It applies to two cases:
> - **Section within a research paper / 研究論文中的一節:** the "Literature Review / Related Work / Theoretical Framework" section. **Depending on discipline and venue**, this is either part of the **Introduction** or a **separate section before Methods**; in social sciences and dissertations it is often a full standalone chapter. It frames your study and motivates the research gap.（依學科與期刊而定，可能在前言內或獨立成節／成章，位於方法之前，用來建立理論框架與凸顯研究缺口。）
> - **Standalone genre / 獨立文類:** a full **narrative review / survey article**, where the literature review *is* the entire paper.（整篇即為敘事綜述／survey 論文。）
> **Scope limits / 範圍界定:** for original research papers it does **not** cover Methods, Results, Data analysis, or the empirical Discussion of original findings. For standalone reviews it provides the **literature-search and narrative-synthesis** framework only — it does **not** replace a formal **PRISMA systematic review, scoping review, or meta-analysis** protocol (those have their own method/results requirements).（不涵蓋原創研究的方法／結果／資料分析；獨立綜述部分僅提供敘事綜述框架，不取代 PRISMA／systematic review／meta-analysis 的正式流程。）

**Core stance / 核心定位:** upgrade the original "writing-guidance only" skill into a **"verify-first, then write"** workflow — keep the proven methodology backbone while structurally suppressing fabricated citations.

> ⚠️ **Honest disclaimer (do not delete) / 誠實聲明：** as long as the final text is model-generated, **no mechanism can 100% guarantee zero hallucination**. This skill blocks "inventing fake bibliography" outright, and uses **claim-to-citation alignment** to also catch the subtler "real paper, wrong claim" failure — but **the author remains finally responsible for verifying every citation**.
>
> 🔑 **Fundamental ceiling / 根本極限（the most important limitation）:** this skill's strongest layer is the audit trail (⑥), yet **that trail is self-reported by the same model that writes the prose**. A model that can hallucinate a citation can equally hallucinate a plausible-looking ⑥ record (a fake URL, fake Crossref JSON, fake excerpt). **No wording in this document can prevent that** — it is a structural limit, not a fixable bug. The only real defenses are external: (1) every ⑥ entry must be a **real, replayable artifact** (a URL/DOI/accession a human can actually open), and (2) a human (or an independent tool) must **spot-check that the ⑥ links truly open and contain the cited excerpt**. Treat this skill as raising the cost of fabrication and making it auditable — **not** as a guarantee of truth.

> 📌 **Provenance / 來源與衍生說明：** derived from the open-source project `brycewang-stanford/Auto-Empirical-Research-Skills`, skill 36 (`literature-review` / taoyunudt, MIT License). It **keeps** the general methodology backbone (five-step method, four organizational structures); **removes** the original author's domain-specific fingerprints (geospatial-database examples) and problematic content (the pirate source SCI-Hub, "lower the plagiarism-check rate" wording); and **adds** all anti-hallucination machinery below.

---

## ⛔ Hard Rules — Non-Negotiable (highest priority / 最高優先級)

> These rules override everything else in this file. If any template or example conflicts with this section, this section wins.

1. **Never fabricate a citation from memory.** Every `(Author, Year)`, every DOI, every cited statistic **must** map to a source you **actually retrieved with a tool this session and verified to exist**. No "fill-in-the-blank" plausible-looking citations.
   （嚴禁憑記憶捏造引用；每一筆都必須對應本次實際檢索且查證存在的真實來源。）

2. **No source → mark it, never invent.** Any claim lacking a source is written as `[needs-retrieval/unverified]` and flagged to the user. **Prefer a blank over a fake citation, fake DOI, or fake number.**
   （無來源就標 `[needs-retrieval/unverified]`，寧缺勿造。）

3. **Separate two kinds of statements:**
   - **Stated-by-source / 文獻明示:** a claim attributed to a source — whether quoted or **paraphrased** — is allowed **only if the verification table records an exact supporting locator** for it: a page, section, paragraph, figure/table number, article-locator, timestamp, or a verbatim/near-verbatim passage. Prose may paraphrase; you do **not** have to quote in the body, but the backing locator must exist. If you cannot locate the specific passage, it is not "stated by source."
   - **Analyst interpretation / 分析者詮釋:** your own inference, synthesis, or evaluation — must be explicitly marked ("This review argues…", "Taken together…") and **must not be disguised as the source's words**.

4. **Existence ≠ support (claim-to-citation alignment).** A real source existing does **not** mean it supports your sentence. Each `(Author, Year)` must be confirmed to **actually support the attached claim** (the most common hallucination is "real paper, fabricated claim"). If you checked and it does **not** support the claim → `[source-does-not-support/recheck]`; if you simply **could not confirm** support yet → `[support-unconfirmed/recheck]`. Either way, do not cite it for that claim.
   （存在 ≠ 支持命題：最隱蔽的幻覺是「真文獻撐假命題」。「確認不支持」與「尚無法確認」用不同標記。）

5. **Prevent citation drift.** Drift includes same-author/same-year confusions, **preprint vs. published version, conference vs. journal extension, revised editions, translations, corrigenda, and same-name authors**. Pin each citation to a **unique identifier (DOI / PMID / arXiv ID / ISBN / publisher URL / database accession)** and confirm it is **the specific item that supports the claim** — never paste paper A's author-year onto paper B's claim.
   （防引用漂移：不只同作者同年，還含 preprint↔正式版、會議↔期刊、修訂版、譯本、勘誤、作者重名；每筆釘一個唯一識別碼。）

6. **Two delivery modes — placeholders are mode-dependent.**
   - **Working draft / 工作稿:** markers like `[needs-retrieval/unverified]`, `[source-does-not-support/recheck]`, `[scope-unclear/recheck]` may remain in-text, clearly flagged for follow-up.
   - **Final submission / 正式稿:** must contain **no** unresolved markers and no `[support 1]` / bare `(Author, Year)` placeholders. Any still-unverified item is moved to an **"Open verification issues"** appendix — never left in the body.

7. **Citations must pass the Citation Verification Layer (below) before entering the body.** Sources that are unverified, or whose status is not ✅ `SUPPORTED`, must not be used as evidence in the body text.

---

## 🛡️ Anti-Hallucination Strategy — Layered Defense / 防範幻覺策略總覽

> Hallucination is not removed by a single rule but by **multiple independent lines of defense**. To enter the final draft, a citation must clear **all** the gates below.

| # | Defense line | Hallucination it intercepts | Mechanism |
|---|--------------|-----------------------------|-----------|
| 1 | **Mandatory grounding** | Inventing bibliography from thin air | Retrieve real sources with tools before writing — never skip (Step 1.3) |
| 2 | **Existence check** | Fake bibliography / wrong DOI / mismatch | Verification Layer ①② (title·author·year·journal·resolvable DOI) |
| 3 | **Retraction / red-flag screen** | Citing retracted work, AI-chat links, predatory journals | Verification Layer ③④ |
| 4 | **Claim-to-citation alignment** | Real paper, fabricated claim (most subtle) | Hard Rule #4 + Layer ⑤: attach an exact supporting locator, else `[source-does-not-support/recheck]` |
| 5 | **Citation-drift guard** | Wrong paper among same author/year, preprint↔published, versions | Hard Rule #5: pin a unique ID (DOI/PMID/arXiv/ISBN/URL) to the paper that supports the claim |
| 6 | **Stated vs. interpreted split** | Passing model inference off as the source's words | Hard Rule #3: "stated" needs a backing locator; interpretation marked explicitly |
| 7 | **Over-claim gate** | Over-linear causal chains, absolute assertions | Body principle "Avoid over-generalization": add conditions/scope/mediators |
| 8 | **Uncertain → leave blank** | Filling gaps with plausible fabrication | Hard Rule #2: no source ⇒ `[needs-retrieval/unverified]`, never invent |
| 9 | **Auditable evidence trail** | Claiming "verified" with no proof | Layer ⑥: log source URL / method / excerpt |
| 10 | **Pre-submission full scan** | Stray placeholders, unaligned citations | "Final self-check": reconcile every in-text citation against the table |

**Strategy in one line:** *Search first, then write; it's "stated" only with a backing locator, "supported" only with alignment; when unsure, leave it blank — never fill it in.*
（一句話：先檢索再寫作；後台有定位才算明示，能對齊才算支持；不確定就留白，絕不填空。）

---

## Core Principles / 核心理念

1. **Verifiability first** — retrieve and verify real sources before writing (this version's core).
2. **Systematic method** — follow the five-step method from search to final writing.
3. **Critical thinking** — analyze, synthesize, and critically evaluate, not just summarize.
4. **Structured organization** — choose the best structure for your topic.
5. **Advance the field** — often by identifying research gaps and proposing future directions, but a review may instead synthesize theories, clarify concepts, map methods, or appraise the evidence base.

---

## What Is a Literature Review / 什麼是文獻綜述

A literature review collects, reads, distills, and synthesizes the main data, sources, and viewpoints on a topic over a period, then presents an integrated account of the latest progress, scholarly views, and recommendations on that topic.

**Purpose:** demonstrate command of the field's background; build a theoretical/methodological frame for your own study; connect your work to others in the field; and advance the field — often by exposing a research gap, but also by synthesizing theories, clarifying concepts, mapping methods, or appraising evidence.

---

## The Five-Step Method / 五步法

### Step 1 — Search the Literature (mandatory grounding / 強制檢索)

> **This step cannot be skipped.** No real retrieval results → no writing.

#### 1.1 Define the research question
- **Standalone review:** pick a focus; pose one central question answerable **purely by reviewing existing literature** (no new data/experiment).
- **Review section in a research paper:** retrieve literature tied to the paper's existing research question.

#### 1.2 Build a keyword list
- List every key concept / variable; list all synonyms, near-synonyms, related terms; keep adding new keywords found during searching.

**Keyword example** (topic: "social media use and adolescent mental health"; replace with your own):
```
Core concepts: social media use, adolescent mental health,
               problematic internet use, screen time
Related areas: depression, anxiety, self-esteem, social comparison,
               digital well-being, longitudinal study
```

#### 1.3 Real retrieval tools (actually fetch — do not rely on memory)
**Tool-agnostic rule:** use **whatever search / scholar / database / PDF-reading tools are available** in your environment; **fetch a real source list first**, then proceed. If no retrieval tool is available, either ask the user to supply the sources or **stop** — do not produce cited writing from memory. Examples in this environment (substitute equivalents elsewhere):
- **firecrawl:** `firecrawl_search` (web/news), `firecrawl_research_search_papers` (papers), `firecrawl_research_read_paper`, `firecrawl_research_related_papers`
- **WebSearch / WebFetch:** general search and page reading
- **MCP `Scholar Gateway`:** `semanticSearch` (semantic academic search) · **MCP `Scite`:** citation context and reliability
- **Legitimate databases** (for the user to search / cross-check): Web of Science, Google Scholar; IEEE Xplore, ACM DL, ScienceDirect, Springer, IOP Science; PubMed/Medline; JSTOR, Project MUSE, EconLit; CNKI, Wanfang, VIP (Chinese).

**Retrieval levels — what each tier may support / 檢索分級:**
| Level | What you obtained | What it may support |
|-------|-------------------|---------------------|
| **L1 metadata-only** | title/author/year/DOI from an index | Existence of the bibliographic item only — reaches `SUPPORTED` as `existence · L1`. **Never** content claims, and not "cited N times" (needs a citation-index return) |
| **L2 abstract** | the **actual abstract** from a publisher / database / paper record | High-level background claims **explicitly stated in the abstract**; mark `abstract-only`. A search-engine **snippet** is discovery-only (keeps the pair at `CANDIDATE`) — it may **not** support a body claim |
| **L3 full text** | full article or the locatable passage itself | Specific findings, numbers, methods, limitations, author conclusions |

> ⚠️ **Never cite specifics (results, statistics, method details, limitations) from L1/L2 alone.** If only an abstract is available (paywall etc.), restrict claims to what the abstract states and tag `abstract-only`.
> ⚠️ **Do not recommend or use pirate sources (e.g., SCI-Hub):** copyright/ethics concerns, and unreliable metadata.

#### 1.4 Search techniques
- **Boolean operators:** `AND` (all terms) / `OR` (any synonym) / `NOT` (exclude a term).
- Read abstracts to judge relevance; snowball from a good paper's reference list; watch for highly cited and recurring authors/works.

---

### Step 2 — Evaluate and Select / 評估與選取

**Criteria:** **relevance** (does it answer the question?), **credibility** (authoritative venue?), **impact** (citation count), **timeliness** (sciences favor the newest; humanities may trace concept evolution).

**Management:**
- Use a reference manager (Zotero, EndNote, Mendeley).
- While reading, record core points, data, and **traceable sources** (DOI / page).
- Build an annotated bibliography with full citation info and a summary analysis.
- **Organize prose through original analysis and synthesis — avoid collage/copy-paste — to ensure genuine scholarly originality** (originality means truly digesting the literature, not gaming a plagiarism checker).

---

### Step 3 — Identify Themes, Controversies, Gaps / 主題、爭議、空白

Map five elements while reading:

| Element | Meaning | Probing question |
|---------|---------|------------------|
| **Trends & patterns** | How theory/method/results change over time | Are some methods rising or falling out of favor? |
| **Recurring themes** | Questions/concepts that reappear | Which concepts recur across papers? |
| **Controversies** | Disagreements between works | Where do researchers diverge? |
| **Pivotal papers** | Influential work that shifted the field | Which papers are the milestones? |
| **Gaps & weaknesses** | Missing research, unresolved limitations | What are current limitations? |

> When naming "pivotal papers" / "milestones," the **Hard Rules still apply**: every cited work must be retrieved and verified, never listed from impression.

---

### Step 4 — Plan the Structure / 規劃結構

Four structures, usable alone or combined:
- **4.1 Chronological** — track development over time; don't merely list — analyze turning points and key arguments.
- **4.2 Thematic** — organize around recurring themes.
- **4.3 Methodological** — compare quantitative / qualitative / mixed-method findings.
- **4.4 Theoretical** — discuss theories, models, key concepts; integrate into a framework.

---

### Step 5 — Write the Review / 撰寫

> **Precondition (verify-first):** every `(Author, Year)` in the templates below is format-only. **Write a claim only after its claim–citation pair reached `SUPPORTED` (✅) in the Verification Layer**; where no source supports it, mark `[needs-retrieval/unverified]` (or `[source-does-not-support/recheck]`) — never invent.

#### 5.1 Introduction
Include: background; importance; scope/boundaries; research question/objective; structure preview.
```
[Field] has drawn growing attention because [reason of importance].
However, a systematic review of [specific topic] is still lacking.
This review aims to [objective], specifically answering: [Q1]; [Q2].
It first [structure], then [structure], and finally [structure].
```

#### 5.2 Body
| Principle | Meaning | Technique |
|-----------|---------|-----------|
| **Summarize & synthesize** | Synthesize across sources, not paper-by-paper | Find links and contrasts |
| **Analyze & explain** | Add your interpretation (marked as analyst interpretation) | "This review argues that this indicates…" |
| **Critically evaluate** | Note method limits, small samples, etc. | Evaluation must be grounded |
| **Well-structured** | Transitions and topic sentences | "However…", "In contrast…" |
| **Avoid over-generalization** | Don't over-linearize causal chains; qualify universal/absolute claims | Every comparison/trend/causal/universal claim must state its **scope, population, time, and method limits**; otherwise downgrade to tentative wording or mark `[scope-unclear/recheck]`. Use "in many cases…", "under condition X…" not "has shifted from A to B"; name mediators/moderators for multi-variable causation |

**Body paragraph template (every citation must be a verified real source):**
```
[Topic sentence: the subsection's main point]
(Real source A, Year) shows that…           ← must be verified; else mark [needs-retrieval/unverified]
(Real source B, Year) further finds…        ← must be verified
[Synthesis] Taken together, these studies…   ← mark: analyst interpretation
[Critique] However, this review argues these studies have [limitation]…
[Transition to next point]
```

#### 5.3 Conclusion
Include: summary of main findings; gaps identified; future directions; theoretical/practical significance.
```
This review systematically surveyed [topic], yielding: 1)… 2)… 3)…
Current research shows these gaps: - [gap 1] - [gap 2]
Future research could pursue: 1) [direction 1] 2) [direction 2]
```

---

## 🔍 Citation Verification Layer / 引用查證層 (mandatory gate before the body)

> Borrows the forensic-grade checking of `literature-single-paper-decompose`. **The unit of verification is the claim, not just the source:** one source may support several claims, and one claim may need several sources — so each *claim–citation pair* is checked before it enters the body.

> **Evidence-or-it-didn't-happen (overriding rule for this layer):** every "confirmed / resolves / retrieved / checked" below is only valid if backed by an **actual tool return captured this session** (URL / accession / API response), logged in ⑥. A check you *believe* would pass but did **not** actually run keeps the pair at `CANDIDATE`. No tool return ⇒ not verified — never infer verification from memory or plausibility.

| Check | Point |
|-------|-------|
| ① **Source really exists** | **Actually run a retrieval tool** and confirm title + author + year + venue appear in the returned result; paste/log the tool return in ⑥. "Looks retrievable" without a captured return does **not** pass — stays `CANDIDATE` |
| ② **DOI / ID resolves correctly** | **Actually resolve the DOI/ID via a tool this session** (doi.org / Crossref / publisher) and confirm the *returned* metadata matches title/author — not just that the string is well-formed. Store the response in ⑥. **Note:** some social-science/humanities works have no DOI — "no DOI" ≠ "doesn't exist"; use ISBN / stable URL / database accession instead; don't judge fake just for lacking a DOI |
| ③ **Retraction check** | Check Retraction Watch / publisher notices / Crossmark / PubMed tag. **"No retraction found" ≠ "confirmed not retracted"** — record only "no retraction record found in checked sources" |
| ④ **Red-flag source** | Check for misplaced AI-chat links (chatgpt.com / claude.ai / gemini.google.com), preprints mislabeled as published, predatory journals |
| ⑤ **Claim support (this version's focus)** | Does the source **actually support this specific claim**? Attach an **exact locator** (page / section / paragraph / figure-table no. / article-locator / timestamp) **plus a verbatim excerpt** from that locator. For **every L3 content claim** the excerpt must be **greppable in the retrieved text** (paraphrase in prose is fine, but the ⑥ record must hold the real supporting words) — a bare locator like "p.12" with no reproducible excerpt does **not** pass. Specifics (results, numbers, methods) need an **L3** locator; abstract-only support is `abstract-only` and limited to high-level claims. If checked and unsupported → `UNSUPPORTED`; if not yet checkable → `SUPPORT_UNCONFIRMED`; either way do not cite for that claim |
| ⑥ **Auditable evidence trail** | Log retrieval source (database/URL/accession), method, the tool return, and the supporting excerpt, so every "verified" has a traceable record — not a mere verbal claim. **A claim–citation pair with no ⑥ record cannot leave `CANDIDATE`.** |

### Status lifecycle (use these exact labels)
`CANDIDATE` → `EXISTS_ONLY` (passed ①②③④, each with a ⑥ tool-return record) → `SUPPORTED` (also passed ⑤ for that claim) → **body-eligible**.
Off-ramps: `SUPPORT_UNCONFIRMED` (exists, but support **not yet** checked / full text not yet read) · `UNSUPPORTED` (full text **was** checked and contains no passage supporting the claim — includes the strong case where the source explicitly contradicts it) · `REJECTED` (does not exist / red-flagged / retracted).

> **`EXISTS_ONLY` is never body-eligible under that label** — it is an intermediate state. Nothing enters the body until it is relabeled `SUPPORTED`.
> **Only `SUPPORTED` (✅) pairs may serve as evidence in the body, and only `SUPPORTED` sources cited in the body go to References.**
> **Existence-only claims are a valid `SUPPORTED` type — but narrowly.** `existence · L1` covers **only** the pure bibliographic fact that *the item exists / is indexed*. Passing ①②③④ (with ⑥ records) satisfies ⑤ for that claim — relabel `EXISTS_ONLY` → `SUPPORTED (existence · L1)`; it is then body-eligible and goes to References.
> **Claims beyond mere existence are content claims, not existence claims**, and L1 does **not** support them: "has been cited / cited N times" needs a citation-index / cited-by return; "belongs to literature L / addresses topic T" needs the abstract or full text; any restatement of what the work *did, found, or argued* needs an **L3** locator. When in doubt, classify as content.
> For any **content** claim (a finding, number, method, conclusion, topic membership), existence is not enough — the pair must reach `SUPPORTED` via the appropriate L2/L3 evidence first, else it stays off-body.

**Status ↔ in-text marker map (every pipeline status has exactly one marker):**
| Status | In-text marker | Meaning |
|--------|----------------|---------|
| `CANDIDATE` | `[needs-retrieval/unverified]` | not yet verified (no ⑥ record) |
| `EXISTS_ONLY` (content claim) | `[support-unconfirmed/recheck]` | exists, but ⑤ not yet satisfied for this claim |
| `EXISTS_ONLY` (existence claim) | *(relabel to `SUPPORTED`)* | passes ⑤ by existence — must be relabeled before body |
| `SUPPORTED` | *(none — write the real citation)* | exists + supports this claim |
| `SUPPORT_UNCONFIRMED` | `[support-unconfirmed/recheck]` | support not yet checked |
| `UNSUPPORTED` | `[source-does-not-support/recheck]` | checked; no supporting passage (incl. explicit contradiction) |
| `REJECTED` | `[needs-retrieval/unverified]` | could not be verified to exist |

> Separate axis (not a pipeline status): an over-broad claim is marked `[scope-unclear/recheck]` regardless of its citation status.
> `CANDIDATE` / `EXISTS_ONLY` / `SUPPORT_UNCONFIRMED` / `UNSUPPORTED` / `REJECTED` may never serve as evidence in the body.

### Always attach the "Claim–Citation Verification Table"
| Claim ID | Claim (exact sentence) | Citation (Author, Year) | DOI / unique ID | Support type / level | Locator + excerpt | Status |
|----------|------------------------|-------------------------|-----------------|----------------------|-------------------|--------|
| C1 | "X reduces Y by 30%." | (Smith, 2020) | 10.xxxx/xxxx (resolved) | direct finding · L3 | p.12 "…30% reduction…" | ✅ `SUPPORTED` |
| C2 | "X is widely studied." | (Lee, 2019) | 10.yyyy/yyyy (resolved) | background · L2 | abstract "growing literature" | ✅ `SUPPORTED` (abstract-only) |
| C3 | "Z exists in literature." | (Mudde, 2004) | 10.aaaa/bbbb (resolved) | existence · L1 | index hit (Crossref) | ✅ `SUPPORTED` (existence·L1) |
| C4 | "X causes Z." | (Wu, 2021) | 10.zzzz/zzzz (resolved) | — | full text read, no matching passage | ⚠️ `UNSUPPORTED` → `[source-does-not-support/recheck]` |
| C5 | "X moderates Y." | (Ng, 2022) | 10.cccc/dddd (resolved) | — | full text not yet read | ⚠️ `SUPPORT_UNCONFIRMED` → `[support-unconfirmed/recheck]` |
| C6 | "W exists." | (Tan, 2018) | not found via tools | — | — | ❌ `REJECTED` → `[needs-retrieval/unverified]`, off body |

### References vs. audit log
- **References** list **only the `SUPPORTED` sources actually cited in the body.**
- `SUPPORT_UNCONFIRMED` / `REJECTED` / unused candidates stay in the **audit log / "Open verification issues" appendix**, never in References.

### Final self-check before submission / 交稿前自檢
- Scan **every in-text citation form** — parenthetical `(Smith, 2020)`, narrative `Smith (2020) argues…`, numeric `[12]`, footnotes, table/figure captions — and confirm each maps to a `SUPPORTED` row.
- Confirm no leftover markers/placeholders in a **final** draft (unresolved items moved to the appendix; see Hard Rule #6).
- Confirm no "analyst interpretation" is mis-written as "stated by source," and every strong causal/comparative/universal claim is either aligned to a source or marked as analyst interpretation (or `[scope-unclear/recheck]`).

---

## Structure Templates / 結構模板

### Standalone review paper
```
Title / Abstract / Keywords
1. Introduction (background / aim & questions / scope / structure)
2. Method (search strategy / inclusion criteria / analytic framework)
3.–5. [Themes 1–3] and subthemes
6. Discussion & synthesis (main findings / gaps / theoretical contribution)
7. Conclusion & outlook (summary / future directions / limitations)
References (only the SUPPORTED sources actually cited in the body)
Appendix: Open verification issues / audit log (unresolved or rejected candidates)
```

### Review section inside a research paper
```
2. Literature Review & Theoretical Framework
   2.1 Core concept definitions  2.2 Theoretical basis  2.3 Related work
   2.4 Critical appraisal & research gap  2.5 Summary
```

---

## FAQ

- **Q1 Too many sources — how to filter?** Set inclusion/exclusion criteria; prioritize high-impact and highly cited; snowball from review papers. **Recency is field-sensitive:** fast-moving fields favor recent work, but foundational theory, methods, and classic studies must not be excluded just for being old.
- **Q2 How to avoid mere listing?** Organize by theme not by paper; find links/contrasts; add (clearly labeled) analytic commentary.
- **Q3 How to find gaps?** Read "future work" suggestions; find contradictions; note method limitations; consider how new tech/theory challenges existing work.
- **Q4 (this version) Unsure whether a citation is real?** Always mark `[needs-retrieval/unverified]` and flag it — **never** invent to fill the gap.

---

## Workflow / 使用流程

1. **Define question and scope.**
2. **Mandatory retrieval:** fetch a real source list with tools (Step 1.3).
3. **Evaluate & select:** relevance / credibility / impact / field-sensitive recency.
4. **Identify themes, trends, controversies, gaps.**
5. **Outline claims** and, **for each claim, run the Citation Verification Layer first** → build the Claim–Citation Verification Table.
6. **Write the body using only `SUPPORTED` (✅) pairs** (intro/body/conclusion templates); claims still unresolved stay marked, not silently dropped.
7. **Final self-check & deliver:** body + References (SUPPORTED only) + verification table + "Open verification issues" appendix; in a **final** draft no unresolved markers remain in the body.

---

## Attribution / 衍生與致謝

- **Methodology backbone** is derived from `brycewang-stanford/Auto-Empirical-Research-Skills`, skill 36 (`literature-review` / taoyunudt, MIT License); the original methodology itself was compiled from public materials on writing literature reviews.
- **Changes in this version:** removed the original author's domain-specific examples (geospatial database), the pirate source (SCI-Hub), and the "lower the plagiarism-check rate" wording; added all anti-hallucination machinery.
- **Verification mechanisms** borrow from `academic-paper-digest` and `literature-single-paper-decompose` (online verification, DOI/retraction checks, AI-chat-link misplacement detection).
