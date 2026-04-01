---
name: orchestrate-build-review
description: Orchestrate a multi-model build-and-review workflow. Use when Codex receives YAML input with a builder model, optional builder session_id, fixed reviewer sessions, a shared review prompt, a reviewer verification prompt, done criteria, and a max loop count, and must run a builder, collect review findings via files, merge and deduplicate findings, resolve contradictions by resuming reviewer sessions, loop the builder until done, and return each agent's final model, session_id, and status.
---

# Orchestrate Build Review

Run this skill as an operator. Accept the YAML input below. Use `mcp__acm__run` and `mcp__acm__wait` for agent execution. Use the current working directory as `workFolder` for every agent launch. Use local file reads and writes only for the review artifact flow described here.

## Input

Use this YAML shape:

```yaml
builder:
  model: gpt-5
  session_id: sess_build_optional
  task_prompt: |
    Implement the requested task.

reviewers:
  codex-ultra:
    session_id: sess_codex
  gemini-ultra:
    session_id: sess_gemini
  claude-ultra:
    session_id: sess_claude

review_prompt: |
  Review the builder result and report actionable findings.

verification_prompt: |
  Verify the implementation by running the relevant checks and describing what was validated.

done_criteria: |
  Stop when the requested task is satisfied and no accepted needs_fix findings remain.

max_loop_rounds: 3

artifacts_dir: .codex-artifacts/orchestrate-build-review
```

Apply these input rules:

- Treat reviewer models as fixed: `codex-ultra`, `gemini-ultra`, `claude-ultra`.
- Treat every reviewer `session_id` as optional. If a session is present, pass it into the initial `mcp__acm__run` call for that agent. If it is absent, start a new session.
- Treat `builder.model` as required.
- Treat `builder.task_prompt` as required.
- Treat `builder.session_id` as optional. If it is absent, start a new builder session in round 1 and preserve the latest builder `session_id` for later rounds and final output.
- Treat `review_prompt` as the shared review instruction for every reviewer round.
- Treat `verification_prompt` as required. Every reviewer must use it to validate the builder result, including concrete checks or commands when appropriate.
- Treat `done_criteria` as required.
- Treat `max_loop_rounds` as required.
- Treat `artifacts_dir` as optional. If omitted, default to `.codex-artifacts/orchestrate-build-review`.
- Preserve the latest known `session_id` for every agent and use that latest `session_id` for contradiction-resolution reruns, later rounds, and final output.

## Artifact Contract

Use `artifacts_dir` as the shared workspace for each loop round.

For each round `N`, create this structure:

```text
<artifacts_dir>/
  round-N/
    builder/
      handoff.md
    reviews/
      codex-ultra.yaml
      gemini-ultra.yaml
      claude-ultra.yaml
      reconsider/
        codex-ultra.yaml
        gemini-ultra.yaml
        claude-ultra.yaml
    merged-findings.yaml
```

Apply these artifact rules:

- `round-N/builder/handoff.md` is written by the builder. It must summarize what changed, what remains risky, and how reviewers should verify the result.
- `round-N/reviews/<model>.yaml` is written by each reviewer and is the only source of record for that reviewer's findings for that round.
- `round-N/reviews/reconsider/<model>.yaml` is written only during contradiction resolution and preserves the original round review file.
- `round-N/merged-findings.yaml` is written by the operator after merging and contradiction resolution.
- If a required artifact file is missing, malformed, or unreadable after an agent completes, stop immediately and return `status: failed` with a concrete reason.

## Reviewer Output Contract

Wrap the user-provided `review_prompt` and `verification_prompt` with an instruction that every reviewer must write YAML only to its assigned review file in this shape:

```yaml
verification_summary: ran targeted checks for touched files
findings:
  - key: requirement-a-missing
    position: needs_fix
    severity: major
    target: src/example.ts
    reason: Requirement A is missing
    fix: Add the missing requirement A condition
```

Apply these reviewer output rules:

- `verification_summary` is required and must summarize the checks performed.
- `findings` must be a list. Return `findings: []` when nothing needs fixing.
- `key` must identify the issue stably enough for deduplication across reviewers.
- `position` must be `needs_fix` or `no_fix`.
- `severity` should be a reviewer hint such as `major` or `minor`. Do not use severity to discard accepted findings.
- `target` should identify the affected area.
- `reason` should explain why the reviewer took that position.
- `fix` should describe the proposed change. For `no_fix`, allow a short explanation instead of an edit instruction.

## Wait Recovery Policy

Apply this policy to every builder and reviewer wait:

- Start with `mcp__acm__wait` using `timeout: 900`.
- If the wait times out without a terminal agent failure, call `mcp__acm__wait` again for the same PID or PIDs.
- Continue re-waiting for the same PID or PIDs until the stage completes or a cumulative wait budget of 7200 seconds is exhausted.
- If `mcp__acm__wait` returns a terminal failure for an agent, stop immediately and return `status: failed`.
- If the stage is still not complete after the 7200-second cumulative wait budget is exhausted, stop immediately and return `status: failed`.

## Workflow

1. Initialize loop state
   - Use only `mcp__acm__run` and `mcp__acm__wait` for agent execution.
   - Use the current working directory as `workFolder` for every `mcp__acm__run` call.
   - Use `timeout: 900` for every initial `mcp__acm__wait` call and apply the wait recovery policy above when needed.
   - Validate that all required input fields are present and non-empty: `builder.model`, `builder.task_prompt`, `review_prompt`, `verification_prompt`, `done_criteria`, and `max_loop_rounds`.
   - If any required input field is missing or invalid, stop immediately and return `status: failed` with a reason naming the offending field.
   - Create `artifacts_dir` if needed.
   - Before any round `N`, create `<artifacts_dir>/round-N/builder`, `<artifacts_dir>/round-N/reviews`, and `<artifacts_dir>/round-N/reviews/reconsider`.
   - If any required `mcp__acm__run`, artifact read/write operation, or exhausted wait recovery fails, stop immediately and return YAML with top-level `status: failed` and a concrete `reason`.

2. Run builder for round 1
   - Start one builder agent with `builder.model`.
   - Pass `builder.session_id` when present.
   - Instruct the builder to perform `builder.task_prompt`.
   - Instruct the builder to write `<artifacts_dir>/round-1/builder/handoff.md`.
   - Instruct the builder to include in the handoff:
     - a concise summary of the implementation,
     - the files changed or created,
     - suggested verification focus for reviewers,
     - any known limitations or follow-up risks.

3. Wait for builder
   - Wait until the builder finishes, applying the wait recovery policy if needed.
   - Record the latest builder `session_id` and agent status from the result.
   - If the builder fails, stop immediately and return top-level `status: failed`.
   - Read `<artifacts_dir>/round-N/builder/handoff.md`. If it is missing or malformed, stop immediately and return `status: failed`.

4. Run reviewers for round N
   - Start three review agents in parallel with `codex-ultra`, `gemini-ultra`, and `claude-ultra`.
   - Pass each reviewer's provided or latest `session_id` when present.
   - Give every reviewer:
     - the shared `review_prompt`,
     - the shared `verification_prompt`,
     - the current `done_criteria`,
     - the path to `<artifacts_dir>/round-N/builder/handoff.md`,
     - the path to its assigned output file `<artifacts_dir>/round-N/reviews/<model>.yaml`.
   - Instruct each reviewer to:
     - read the builder handoff,
     - inspect the working tree as needed,
     - perform the requested verification,
     - write YAML only to its assigned review file using the reviewer output contract.

5. Wait for reviewers
   - Wait until all three review agents finish, applying the wait recovery policy if needed.
   - Record each reviewer's latest `session_id` and agent status from the result.
   - If any reviewer finishes with agent status `failed`, stop immediately and return top-level `status: failed`.
   - Read all three review files at `<artifacts_dir>/round-N/reviews/<model>.yaml`. If any review file is missing or malformed, stop immediately and return `status: failed`.

6. Merge findings
   - Extract reviewer findings from the three YAML review files.
   - Deduplicate findings by `key` when keys match directly.
   - When keys differ but the issue is clearly equivalent, treat them as the same logical finding and merge them.
   - Keep all accepted `needs_fix` findings as fix candidates. Do not discard findings because they seem lower priority.

7. Resolve contradictions
   - Treat a contradiction as a case where the same or equivalent finding has conflicting `position` values across reviewers.
   - Do not treat silence as a contradiction. If one reviewer omits a finding and others report it, merge based on the reported findings and continue.
   - If no contradictions remain, continue to the next step.
   - If contradictions remain, start a contradiction-resolution round for only the conflicting items.
   - Resume each reviewer session and provide:
     - the conflicting opinions from the other reviewers,
     - the current builder handoff path,
     - the reconsideration output file path at `<artifacts_dir>/round-N/reviews/reconsider/<model>.yaml`,
     - the same `review_prompt`, `verification_prompt`, and `done_criteria`.
   - Ask each reviewer to reconsider only the conflicting items and write YAML only for those items to its reconsideration file using the same reviewer output contract.
   - Wait for each contradiction-resolution round, applying the wait recovery policy if needed.
   - If any contradiction-resolution run or exhausted wait recovery fails, stop immediately and return `status: failed`.
   - If any reviewer returns agent status `failed` during contradiction resolution, stop immediately and return top-level `status: failed`.
   - After each contradiction-resolution round, read all reconsideration files at `<artifacts_dir>/round-N/reviews/reconsider/<model>.yaml`.
   - Update the conflicting findings with the latest reviewer positions from those reconsideration files.
   - Recompute the remaining contradiction set before deciding whether another contradiction round is needed.
   - Repeat until all reviewers converge or 3 contradiction-resolution rounds have completed.
   - Treat convergence as all three reviewers agreeing on `position` for a conflicting item.
   - If round 3 ends with a `2:1` split for a conflicting item, adopt the majority view for that item.
   - If round 3 ends with any remaining unresolved contradiction that does not produce a final majority decision under these rules, stop immediately and return `status: stopped` with a reason that reviewer opinions did not converge after 3 rounds.

8. Decide whether the round is done
   - Write `<artifacts_dir>/round-N/merged-findings.yaml` with the accepted merged findings and contradiction-resolution outcomes.
   - If no accepted `needs_fix` findings remain after merge and contradiction resolution, stop and return `status: completed` with reason `done criteria satisfied and no fixes required`.

9. Decide whether to continue looping
   - If round `N` equals `max_loop_rounds` and accepted `needs_fix` findings remain, stop and return `status: stopped` with a reason that the loop limit was reached before satisfying `done_criteria`.

10. Run builder for round N+1
   - Create `<artifacts_dir>/round-(N+1)/builder`, `<artifacts_dir>/round-(N+1)/reviews`, and `<artifacts_dir>/round-(N+1)/reviews/reconsider`.
   - Resume the latest builder `session_id`.
   - Build one natural-language continuation prompt that includes:
     - the original `builder.task_prompt`,
     - the current `done_criteria`,
     - the path to `<artifacts_dir>/round-N/merged-findings.yaml`,
     - a direct instruction to implement all accepted fixes,
     - a direct instruction to write the next handoff file at `<artifacts_dir>/round-(N+1)/builder/handoff.md`.
   - Start the next builder round with `mcp__acm__run` using `builder.model`, the current working directory as `workFolder`, and the latest builder `session_id`.
   - Wait for the builder, applying the wait recovery policy if needed.
   - Record the latest builder `session_id` and agent status from the result.
   - If the builder fails, stop immediately and return top-level `status: failed`.
   - Read `<artifacts_dir>/round-(N+1)/builder/handoff.md`. If it is missing or malformed, stop immediately and return `status: failed`.
   - Continue with the next review round.

## Output

Return YAML only. Use this shape:

```yaml
status: completed
reason: all reviews merged and builder completed
accepted_findings_count: 0
contradiction_rounds: 1
unresolved_items_count: 0
loop_rounds: 2

reviewers:
  codex-ultra:
    session_id: sess_codex_final
    status: completed
  gemini-ultra:
    session_id: sess_gemini_final
    status: completed
  claude-ultra:
    session_id: sess_claude_final
    status: completed

builder:
  model: gpt-5
  session_id: sess_build_final
  status: completed
```

Apply these output rules:

- Use top-level `status` values: `completed`, `stopped`, `failed`.
- Use agent-level `status` values: `completed`, `skipped`, `failed`.
- Always include `accepted_findings_count`, `contradiction_rounds`, `unresolved_items_count`, and `loop_rounds`.
- Always return all three reviewer entries.
- Always return the builder entry.
- Use `session_id` consistently in both input and output.
- When processing fails before an agent launches, preserve the provided input `session_id` if one exists and mark that agent `status: skipped`.
- When processing fails after an agent launches or after exhausted wait recovery, return the latest known `session_id` and mark that agent `status: failed`.
- When no `session_id` was ever observed for a failed newly started agent, set `session_id: null`.
- When processing stops because no accepted `needs_fix` findings remain and `done_criteria` is satisfied, set top-level `status: completed`.
- When processing stops because reviewer opinions do not converge, set top-level `status: stopped` and explain the contradiction outcome in `reason`.
- When processing stops because the loop limit is reached, set top-level `status: stopped` and explain that `max_loop_rounds` was exhausted before satisfying `done_criteria`.
