# literature-review-hardened

A Claude Code skill for writing academic **literature reviews** under a strict **"verify-first, never fabricate"** regime. It keeps a proven five-step methodology backbone but adds layered **anti-hallucination** machinery so the AI cites only real, checkable sources.

一個用於撰寫學術**文獻綜述**的 Claude Code skill，核心是「**先查證、再寫作，嚴禁捏造引用**」。保留標準五步法骨架，並加上分層**防幻覺**機制，讓 AI 只引用真實、可稽核的來源。

> ⚠️ **It targets one part of academic writing — the literature review** (the Literature Review / Related Work / Theoretical Framework section, or a standalone narrative review/survey). It does **not** cover Methods/Results/empirical Discussion, and does **not** replace a formal PRISMA systematic review or meta-analysis.

## What it adds (anti-hallucination, layered defense)

- **Mandatory grounding** — search real sources with tools before writing; never from memory.
- **Per-claim verification** — the unit is the *claim–citation pair*, not just the source.
- **"Evidence-or-it-didn't-happen"** — every check (existence, DOI resolve, support) needs an actual captured tool return logged in an audit trail; no record ⇒ stays `CANDIDATE`.
- **Existence ≠ support** — catches the subtle "real paper, fabricated claim" failure via locator + greppable excerpt.
- **Status state machine** — `CANDIDATE → EXISTS_ONLY → SUPPORTED`, with off-ramps `SUPPORT_UNCONFIRMED / UNSUPPORTED / REJECTED`, each mapped to an in-text marker. Only `SUPPORTED` may enter the body / References.
- **Auditable "Claim–Citation Verification Table"** attached to every output.

### Honest ceiling / 根本極限

The audit trail is **self-reported by the same model that writes the prose** — a model that can hallucinate a citation can hallucinate its evidence too. **No wording closes this.** The skill raises the cost of fabrication and makes it auditable; it is **not** a guarantee of truth. Always keep every audit-trail entry a **real, replayable artifact** and **human-spot-check** that the links truly open and contain the cited excerpt.

## Install

```bash
mkdir -p ~/.claude/skills/literature-review-hardened
cp SKILL.md ~/.claude/skills/literature-review-hardened/
```
Restart Claude Code or start a new conversation.

## Usage

> Help me write a literature review on **[your topic]**.

The skill will search first, verify each claim–citation pair, and deliver the review plus a Citation Verification Table (with any unresolved items moved to an "Open verification issues" appendix).

## Provenance & attribution

Derived from `brycewang-stanford/Auto-Empirical-Research-Skills`, skill 36 (`literature-review` / taoyunudt, MIT License). This version removes the original's domain-specific examples, the pirate source SCI-Hub, and "lower the plagiarism-check rate" wording, and adds all anti-hallucination machinery. Verification mechanisms borrow from the companion skills `academic-paper-digest` and `literature-single-paper-decompose`.

## License

MIT — see [LICENSE](LICENSE).
