---
name: taskforce-review-report
description: "Run the taskforce review workflow: perform AI code reviews with mcp__acm__run (codex-ultra, add gemini-ultra if multiple reviews are needed) and then produce a review report with STATUS and DESCRIPTION. Use when asked to follow taskforce_review_report.md or to orchestrate review + report."
user-invocable: true
---

# Taskforce Review Report

Act as the operator and drive the workflow steps below.

## Workflow

1. AI review
   - Use `mcp__acm__run` to have the agent perform a code review.
   - Default model: `codex-ultra`
   - Add `gemini-ultra` when two or more reviews are required.

2. Write report
   - Summarize review results and report as the operator.
   - Format:
     - `STATUS: APPROVE | CHANGE_REQUEST`
     - `DESCRIPTION: <description>`
