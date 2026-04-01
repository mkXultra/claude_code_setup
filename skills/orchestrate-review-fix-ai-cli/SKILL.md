---
name: orchestrate-review-fix-ai-cli
description: Orchestrate a multi-model review-and-fix workflow using only ai-cli run and ai-cli wait. Use when Codex receives YAML input with fixed reviewer sessions, a shared review prompt, and a required fixer model/session, and must run codex-ultra, gemini-ultra, and claude-ultra reviews, enforce structured reviewer output, merge and deduplicate findings, resolve contradictions by resuming reviewer sessions, optionally run a fixer, and return each agent's final model, session, and status.
---

# Orchestrate Review Fix AI CLI

Run this skill as an operator. Accept the YAML input below, use only `ai-cli run` and `ai-cli wait`, do not read files, and do not use any other `ai-cli` subcommands.

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

fixer:
  model: gpt-5
  session: sess_fix
```

Apply these input rules:

- Treat reviewer models as fixed: `codex-ultra`, `gemini-ultra`, `claude-ultra`.
- Treat every reviewer `session` as optional. If a session is present, pass it to `ai-cli run --session-id`. If it is absent, start a new session.
- Preserve the latest known session for every agent and use that latest session for contradiction-resolution reruns and final output.
- Treat `review_prompt` as the shared prompt for the initial three review agents.
- Treat `fixer.model` as required.
- Treat `fixer.session` as required in v1. If it is missing, stop immediately and return `status: failed` with a reason that fixer context is required.
- Use the current working directory as `ai-cli run --cwd` for every agent launch.
- Write the fixer prompt in natural language from the merged reviewer findings. Do not require a separate fixer prompt input.

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

1. Run only required CLI calls
   - Use only `ai-cli run` and `ai-cli wait`.
   - Use `--cwd <current-working-directory>` for every `ai-cli run` call.
   - Use `--timeout 900` for every `ai-cli wait` call.
   - If any required `ai-cli run` or `ai-cli wait` call is unavailable or fails, including a 900-second wait timeout, stop immediately and return YAML with top-level `status: failed` and a concrete `reason`.

2. Launch initial reviews
   - Start three review agents in parallel with `codex-ultra`, `gemini-ultra`, and `claude-ultra`.
   - Pass the same `review_prompt` to all three agents, wrapped with the reviewer output contract above.
   - Pass each reviewer's provided session when present.
   - Use command shape equivalent to:
     - `ai-cli run --cwd <current-working-directory> --model <reviewer-model> --prompt <wrapped-review-prompt> [--session-id <reviewer-session>]`

3. Wait for initial reviews
   - Wait until all three review agents finish with `ai-cli wait <pid...> --timeout 900`.
   - Record each agent's latest `session_id` and agent status from the result.
   - If waiting fails, stop immediately and return `status: failed`.
   - If any initial review agent finishes with agent status `failed`, stop immediately and return top-level `status: failed`.

4. Merge findings
   - Extract reviewer findings from the three structured YAML review results.
   - Deduplicate findings by `key` when keys match directly.
   - When keys differ but the issue is clearly equivalent, treat them as the same logical finding and merge them.
   - Keep all accepted `needs_fix` findings as fix candidates. Do not discard findings because they seem lower priority.

5. Resolve contradictions
   - Treat a contradiction as a case where the same or equivalent finding has conflicting `position` values across reviewers.
   - Do not treat silence as a contradiction. If one reviewer omits a finding and others report it, merge based on the reported findings and continue.
   - If no contradictions remain, continue to the next step.
   - If contradictions remain, start a contradiction-resolution round for only the conflicting items.
   - Resume each reviewer session and provide the conflicting opinions from the other reviewers.
   - Ask each reviewer to reconsider the conflicting items and return YAML only for those items using the same reviewer output contract.
   - Use command shape equivalent to:
     - `ai-cli run --cwd <current-working-directory> --model <reviewer-model> --prompt <contradiction-prompt> --session-id <latest-reviewer-session>`
   - Wait for each contradiction-resolution round with `ai-cli wait <pid...> --timeout 900`.
   - If any contradiction-resolution run or wait fails, stop immediately and return `status: failed`.
   - If any reviewer returns agent status `failed` during contradiction resolution, stop immediately and return top-level `status: failed`.
   - Repeat until all reviewers converge or 3 contradiction-resolution rounds have completed.
   - Treat convergence as all three reviewers agreeing on `position` for a conflicting item.
   - If round 3 ends with a `2:1` split for a conflicting item, adopt the majority view for that item.
   - If round 3 ends with a `1:1:1` split for any conflicting item, stop immediately and return `status: stopped` with a reason that reviewer opinions did not converge after 3 rounds and no majority was available.

6. Decide whether to fix
   - If no accepted `needs_fix` findings remain after merge and contradiction resolution, stop and return `status: completed` with reason `no fixes required`.

7. Launch fixer
   - Start one fix agent with `fixer.model`.
   - Pass `fixer.session`. Do not start a new fixer session in v1.
   - Build one natural-language fixer prompt that includes:
     - the accepted merged findings,
     - any contradiction-resolution outcomes that changed the final decision,
     - a direct instruction to implement all accepted fixes.
   - Use command shape equivalent to:
     - `ai-cli run --cwd <current-working-directory> --model <fixer-model> --prompt <fixer-prompt> --session-id <fixer-session>`

8. Wait for fixer
   - Wait until the fix agent finishes with `ai-cli wait <pid...> --timeout 900`.
   - Record the latest fixer `session_id` and agent status from the result.
   - If fixer launch or wait fails, return `status: failed`.

## Output

Return YAML only. Use this shape:

```yaml
status: completed
reason: all reviews merged and fixer completed
accepted_findings_count: 3
contradiction_rounds: 1
unresolved_items_count: 0

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

fixer:
  model: gpt-5
  session: sess_fix_final
  status: completed
```

Apply these output rules:

- Use top-level `status` values: `completed`, `stopped`, `failed`.
- Use agent-level `status` values: `completed`, `skipped`, `failed`.
- Always include `accepted_findings_count`, `contradiction_rounds`, and `unresolved_items_count`.
- Always return all three reviewer entries.
- Always return the fixer entry.
- When the fixer does not run, set fixer `status: skipped`.
- When processing fails before an agent launches, preserve the provided input session if one exists and mark that agent `status: skipped`.
- When processing fails after an agent launches or waits unsuccessfully, return the latest known session and mark that agent `status: failed`.
- When processing stops without running the fixer because no fixes are needed, set top-level `status: completed`, set fixer `status: skipped`, and explain that no fixes were required.
- When processing stops because reviewer opinions do not converge, set top-level `status: stopped`, set fixer `status: skipped`, and explain the contradiction outcome in `reason`.
