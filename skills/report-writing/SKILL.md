---
name: report-writing
description: Use when the user needs to plan, draft, rewrite, polish, or quality-check a written report, including lab reports, course reports, project reports, research summaries, investigation reports, internship reports, thesis-style sections, or final deliverables. Focus on structure, argument flow, evidence, citation hygiene, figures/tables narration, and revision. Pair with documents:documents for Word files, pdf:pdf for PDFs, and presentations:Presentations for presentation files. Do not use for ordinary chat, short answers, code-only tasks, or simple file conversion without writing or revision.
---

# Report Writing

## Scope

Use this skill to turn source materials into report-ready writing, improve existing drafts, or audit report quality. This skill is format-agnostic: it handles writing decisions, while file-format skills handle documents.

## Workflow

1. Identify the deliverable: report type, audience, length, language, required sections, formatting rules, source materials, citation style, and deadline-sensitive constraints.
2. Build a structure before drafting medium or long reports: title, purpose, section order, key claims, evidence needed, figures/tables, and expected conclusion. For short tasks, keep the outline implicit and proceed.
3. Extract evidence from provided materials. Separate source facts from inference. Do not invent measurements, citations, experiment results, or institutional requirements.
4. Draft each section for a clear role: introduction sets the problem and scope; methods explain a reproducible process; results state observations; discussion explains meaning and limitations; conclusion answers the task.
5. Treat figures, tables, formulas, and screenshots as evidence. Refer to them in the body, explain what the reader should notice, and keep numbering/captions consistent.
6. Revise for flow: each paragraph should advance the argument, transitions should make the logic visible, and repeated or decorative wording should be cut.
7. Run a final report check: requirements covered, claims supported, units and terminology consistent, references present when needed, no placeholders, no contradiction between text and figures/tables, and final format matches the requested deliverable.

## Coordination

Use the named companion skills when they are available. If a companion skill is missing, use an available tool for the requested format and explain any material limitation.

- Use `documents:documents` after this skill when the report needs to be created, edited, formatted, or delivered as a `.docx` Word document.
- Use `pdf:pdf` when source PDFs need extraction, rendering checks, or final PDF layout review.
- Use `presentations:Presentations` when converting report content into a slide deck, following the user's requested format and editability.
- For university math or physics derivations, use `scientific-reasoning`; use `sympy` when symbolic or numerical formula checks are useful. Do not require a separate course-organizer skill.

## Style Defaults

- For Chinese reports, write in concise formal Chinese and avoid slogan-like filler.
- For English reports, use clear academic or professional prose without overclaiming.
- When polishing an existing draft, preserve the user's intent and technical meaning; report the major edits made.
- When source evidence is weak or missing, state the gap and offer a safe placeholder or evidence request instead of fabricating content.
