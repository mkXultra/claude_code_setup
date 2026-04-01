---
name: orchestrate-review-only
description: Orchestrate a 3-model parallel review workflow using mcp__acm__run and mcp__acm__wait. Runs codex-ultra, gemini-ultra, and claude-ultra reviews in parallel, enforces structured output, merges and deduplicates findings, resolves contradictions, and returns a final merged review report. No fixer agent is involved.
---

# Orchestrate Review Only

Run this skill as an operator. Accept the YAML input below, use only `mcp__acm__run` and `mcp__acm__wait`, do not read files, and do not use any other tools.

## Input

Use this YAML shape:

```yaml
reviewers:
  codex-ultra:
    session: sess_xxx
  gemini-ultra:
    session: sess_yyy
  claude-ultra:
    session: sess_zzz

review_prompt: |
  Review this change and report actionable findings.
```

Apply these input rules:

- Treat reviewer models as fixed: `codex-ultra`, `gemini-ultra`, `claude-ultra`.
- Treat every `session` as optional. If a session is present, pass it into the initial `mcp__acm__run` call for that agent. If it is absent, start a new session.
- Preserve the latest known session for every agent and use that latest session for contradiction-resolution reruns and final output.
- Treat `review_prompt` as the shared prompt for the initial three review agents.

## Reviewer Output Contract

Wrap the user-provided `review_prompt` with an instruction that every reviewer must return YAML only in this shape:

```yaml
findings:
  - key: requirement-a-missing
    position: needs_fix
    severity: major
    target: section 2 paragraph 3
    reason: Requirement A is missing
    fix: Add the missing requirement A condition
```

Apply these reviewer output rules:

- `findings` must be a list. Return `findings: []` when nothing needs fixing.
- `key` must identify the issue stably enough for deduplication across reviewers.
- `position` must be `needs_fix` or `no_fix`.
- `severity` should be a reviewer hint such as `major` or `minor`. Do not use severity to discard accepted findings.
- `target` should identify the affected area.
- `reason` should explain why the reviewer took that position.
- `fix` should describe the proposed change. For `no_fix`, allow a short explanation instead of an edit instruction.

## Workflow

1. Run only required MCP calls
   - Use only `mcp__acm__run` and `mcp__acm__wait`.
   - Use `timeout: 900` for every `mcp__acm__wait` call.
   - If any required `mcp__acm__run` or `mcp__acm__wait` call is unavailable or fails, including a 900-second wait timeout, stop immediately and return YAML with top-level `status: failed` and a concrete `reason`.

2. Launch initial reviews
   - Start three review agents in parallel with `codex-ultra`, `gemini-ultra`, and `claude-ultra`.
   - Pass the same `review_prompt` to all three agents, wrapped with the reviewer output contract above.
   - Pass each reviewer's provided session when present.

3. Wait for initial reviews
   - Wait until all three review agents finish with `mcp__acm__wait` and `timeout: 900`.
   - Record each agent's latest `session_id` and agent status from the result.
   - If waiting fails, stop immediately and return `status: failed`.
   - If any initial review agent finishes with agent status `failed`, stop immediately and return top-level `status: failed`.

4. Merge findings
   - Extract reviewer findings from the three structured YAML review results.
   - Deduplicate findings by `key` when keys match directly.
   - When keys differ but the issue is clearly equivalent, treat them as the same logical finding and merge them.
   - Keep all accepted `needs_fix` findings as review results. Do not discard findings because they seem lower priority.

5. Resolve contradictions
   - Treat a contradiction as a case where the same or equivalent finding has conflicting `position` values across reviewers.
   - Do not treat silence as a contradiction. If one reviewer omits a finding and others report it, merge based on the reported findings and continue.
   - If no contradictions remain, continue to the next step.
   - If contradictions remain, start a contradiction-resolution round for only the conflicting items.
   - Resume each reviewer session and provide the conflicting opinions from the other reviewers.
   - Ask each reviewer to reconsider the conflicting items and return YAML only for those items using the same reviewer output contract.
   - Wait for each contradiction-resolution round with `mcp__acm__wait` and `timeout: 900`.
   - If any contradiction-resolution run or wait fails, stop immediately and return `status: failed`.
   - If any reviewer returns agent status `failed` during contradiction resolution, stop immediately and return top-level `status: failed`.
   - Repeat until all reviewers converge or 3 contradiction-resolution rounds have completed.
   - Treat convergence as all three reviewers agreeing on `position` for a conflicting item.
   - If round 3 ends with a `2:1` split for a conflicting item, adopt the majority view for that item.
   - If round 3 ends with a `1:1:1` split for any conflicting item, stop immediately and return `status: stopped` with a reason that reviewer opinions did not converge after 3 rounds and no majority was available.

6. Produce final report
   - After merge and contradiction resolution, compile the final list of accepted findings.
   - Include each finding's `key`, `position`, `severity`, `target`, `reason`, and `fix`.
   - Group findings by final `position` (`needs_fix` and `no_fix`).

## Output

Return YAML only. Use this shape:

```yaml
status: completed
reason: all reviews merged successfully
accepted_findings_count: 3
contradiction_rounds: 1
unresolved_items_count: 0

findings:
  - key: requirement-a-missing
    position: needs_fix
    severity: major
    target: section 2 paragraph 3
    reason: Requirement A is missing
    fix: Add the missing requirement A condition
    agreed_by: [codex-ultra, gemini-ultra, claude-ultra]
  - key: naming-convention
    position: needs_fix
    severity: minor
    target: src/utils.ts line 42
    reason: Variable name does not follow project convention
    fix: Rename fooBar to foo_bar
    agreed_by: [codex-ultra, gemini-ultra]

reviewers:
  codex-ultra:
    session: sess_xxx_final
    status: completed
  gemini-ultra:
    session: sess_yyy_final
    status: completed
  claude-ultra:
    session: sess_zzz_final
    status: completed
```

Apply these output rules:

- Use top-level `status` values: `completed`, `stopped`, `failed`.
- Use agent-level `status` values: `completed`, `skipped`, `failed`.
- Always include `accepted_findings_count`, `contradiction_rounds`, and `unresolved_items_count`.
- Always return all three reviewer entries.
- Always include the `findings` list with all accepted findings and their details.
- Each finding must include `agreed_by` listing which reviewers agreed on that position.
- When no findings exist, return `findings: []` with `accepted_findings_count: 0`.
- When processing fails before an agent launches, preserve the provided input session if one exists and mark that agent `status: skipped`.
- When processing fails after an agent launches or waits unsuccessfully, return the latest known session and mark that agent `status: failed`.
- When processing stops because reviewer opinions do not converge, set top-level `status: stopped` and explain the contradiction outcome in `reason`.
