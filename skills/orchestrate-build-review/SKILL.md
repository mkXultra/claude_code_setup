---
name: orchestrate-build-review
description: Orchestrate a multi-model build-and-review workflow with progress-aware waits and two-reviewer degradation. Use when Codex receives YAML input with an optional builder model defaulting to codex-ultra, optional builder session_id, fixed reviewer slots, a shared review prompt, a reviewer verification prompt, done criteria, and a max loop count, and must run a builder, collect review findings via files, merge and deduplicate findings, resolve contradictions by resuming reviewer sessions, loop the builder until done, and return each agent's final model, session_id, and status.
---

# Orchestrate Build Review

Run this skill as an operator. Accept the YAML input below. Use `mcp__acm__run` for agent launches, `mcp__acm__wait` for normal waiting, `mcp__acm__get_result` plus `mcp__acm__peek` for timeout diagnosis, and `mcp__acm__kill_process` only for a confirmed stalled process. Use the current working directory as `workFolder` for every agent launch. Use local file reads and writes only for the review artifact flow described here.

## Input

Use this YAML shape:

```yaml
builder:
  model: codex-ultra
  session_id: sess_build_optional
  task_prompt: |
    Implement the requested task.

reviewers:
  codex:
    model: codex-ultra
    session_id: sess_codex
  glm5.3:
    primary_model: oc-ollama-cloud/glm-5.3
    fallback_model: oc-ollama-cloud/glm-5.2
    session_id: sess_glm53_or_glm52
  claude:
    model: claude-ultra
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

- Treat reviewer slots as fixed: `codex`, `glm5.3`, and `claude`.
- Require at least two successful reviewer slots in every review and contradiction-resolution stage.
- If one reviewer slot fails after any configured model fallback is exhausted, mark it inactive for the rest of the workflow, emit a brief degradation progress note, and continue with the other two slots.
- If fewer than two reviewer slots remain active or produce valid artifacts, stop immediately and return `status: failed`.
- Treat `codex.model` as fixed to `codex-ultra`.
- Treat `glm5.3.primary_model` as fixed to `oc-ollama-cloud/glm-5.3` and `glm5.3.fallback_model` as fixed to `oc-ollama-cloud/glm-5.2`.
- Treat `claude.model` as optional. If it is absent or empty, default to `claude-ultra`.
- Allow only `claude-ultra` or `fable` for `claude.model`.
- Use `fable` only when the input explicitly sets `claude.model: fable`. Never select `fable` implicitly or use it as a fallback.
- Resolve the Claude reviewer model once before round 1 and use that same model for every review and contradiction-resolution round.
- Treat every reviewer `session_id` as optional. If a session is present, pass it into the initial `mcp__acm__run` call for that reviewer slot. If it is absent, start a new session.
- For `glm5.3`, prefer `oc-ollama-cloud/glm-5.3` for the reviewer slot. If any `glm5.3` primary launch fails, stalls, has an unrecoverable diagnostic failure, finishes with status `failed`, or still produces invalid review YAML after its one resumed artifact-repair attempt, emit a brief progress note to the user that the primary `glm5.3` reviewer failed and the workflow is continuing with `oc-ollama-cloud/glm-5.2`; then launch `oc-ollama-cloud/glm-5.2` for the same reviewer slot.
- After `glm5.3` falls back to `oc-ollama-cloud/glm-5.2` within a workflow, use `oc-ollama-cloud/glm-5.2` for later reruns of that reviewer slot, including contradiction resolution.
- If `oc-ollama-cloud/glm-5.2` also fails for the `glm5.3` slot, mark that reviewer slot inactive and apply the minimum-two-reviewers rule.
- Track each reviewer by slot id, not by model name. Preserve `model_used`, whether fallback or artifact repair was used, and the latest known `session_id` for every reviewer slot.
- Treat `builder.model` as optional. If it is absent or empty, default to `codex-ultra`.
- Resolve the builder model once before round 1 and use that same model for every builder round.
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
      codex.yaml
      glm5.3.yaml
      claude.yaml
      reconsider/
        codex.yaml
        glm5.3.yaml
        claude.yaml
    merged-findings.yaml
```

Apply these artifact rules:

- `round-N/builder/handoff.md` is written by the builder. It must summarize what changed, what remains risky, and how reviewers should verify the result.
- `round-N/reviews/<reviewer-id>.yaml` is written by each launched reviewer slot and is the only source of record for that reviewer's findings for that round.
- `round-N/reviews/reconsider/<reviewer-id>.yaml` is written only during contradiction resolution and preserves the original round review file.
- `round-N/merged-findings.yaml` is written by the operator after merging and contradiction resolution.
- A review or reconsideration artifact is required only for a reviewer slot that is still active after the stage completes.
- If an active reviewer finishes successfully without a valid artifact, apply the review artifact validation and repair policy before fallback or degradation.
- Record active and degraded reviewer slot ids in `round-N/merged-findings.yaml` so later builder and reviewer rounds know which opinions participated.

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
- Every finding must contain all six keys: `key`, `position`, `severity`, `target`, `reason`, and `fix`. Every value must be a non-empty string.
- `key` must identify the issue stably enough for deduplication across reviewers and must not repeat within the same file.
- `position` must be `needs_fix` or `no_fix`.
- `severity` should be a reviewer hint such as `major` or `minor`. Do not use severity to discard accepted findings.
- `target` should identify the affected area.
- `reason` should explain why the reviewer took that position.
- `fix` should describe the proposed change. For `no_fix`, `fix` is still required and must contain a short explanation of why no edit is required.

## Review Artifact Validation and Repair Policy

Apply this policy to every round review file and every contradiction-reconsideration file:

- Resolve `scripts/validate_review_yaml.py` relative to this `SKILL.md`, not relative to `workFolder`.
- Give every reviewer the absolute validator path and instruct it to run `python3 <validator-path> <assigned-review-file>` after writing the file, correcting the file until the command succeeds before the reviewer exits.
- After a reviewer finishes successfully, the operator must independently run the same validator command on that reviewer's assigned file. Do not replace this command with ad hoc YAML inspection.
- Validator exit code `0` means the artifact is valid. Exit code `1` means the artifact is missing or violates the review YAML contract. Exit code `2` means the validator itself could not run; stop the workflow with `status: failed` because review validity cannot be established.
- When validation exits `1`, capture the validator diagnostics and resume the same reviewer slot with its latest successful `model_used` and `session_id`. Give it the exact diagnostics, the same assigned output path, and a direct instruction to repair only the YAML artifact, overwrite it, and run the validator before completing. Do not ask it to re-review or change implementation files.
- Allow exactly one resumed artifact-repair attempt per model run for a given assigned file. Wait for that attempt with the normal wait and stall detection policy, then run the validator again independently.
- If the repaired artifact validates, continue with the same reviewer slot and record that artifact repair was used.
- If the repair agent fails or the repaired artifact is still invalid, treat that model run as failed. For the `glm5.3` primary model, launch `oc-ollama-cloud/glm-5.2`; for a `glm5.3` fallback run, deactivate the slot; for `codex` or `claude`, deactivate the slot. Apply the minimum-two-reviewers rule after deactivation.
- A `glm5.3` fallback reviewer gets its own single resumed artifact-repair attempt if its output is invalid.
- Do not run artifact repair for a reviewer process that itself ended with terminal status `failed`; apply the normal reviewer failure or GLM fallback policy instead.
- Apply the same validation and single-repair sequence to reconsideration YAML before using it to update contradiction positions.

## Wait and Stall Detection Policy

Apply this policy to every builder and reviewer wait:

- Start with `mcp__acm__wait` using `timeout: 900`.
- When a wait times out, call `mcp__acm__get_result` for every unfinished PID and store a compact progress fingerprint from its status and current output. Compare it with that PID's fingerprint from the previous timeout checkpoint when one exists.
- For PIDs still reported as running, call `mcp__acm__peek` once with `peek_time_sec: 60` and `include_tool_calls: true`, then call `mcp__acm__get_result` again.
- Treat a PID as making progress when the first `get_result` differs meaningfully from the previous timeout checkpoint, `peek` observes a message or tool call, or the second `get_result` differs meaningfully from the first fingerprint.
- If progress is observed, reset that PID's consecutive stale-check count to zero and call `mcp__acm__wait` again with `timeout: 900` for unfinished PIDs. Do not stop merely because a cumulative wall-clock budget has elapsed while progress continues.
- If no progress is observed, increment that PID's consecutive stale-check count and re-wait once more with `timeout: 900` while the count is below two.
- Treat a PID as stalled when two consecutive timeout checks observe no progress. A stale check is consecutive only when no intervening `peek` event or meaningful `get_result` change was observed.
- If `get_result` or `peek` fails or reports an unknown PID, retry the failed diagnostic call once. If it fails again, treat that PID as a wait-recovery failure.
- If `get_result` reports a terminal result during diagnosis, handle it immediately instead of re-waiting.
- Before handling a still-running PID as stalled or as an unrecoverable wait-recovery failure, terminate it with `mcp__acm__kill_process`. Confirm termination from a successful kill result or a subsequent terminal `get_result`; if termination cannot be confirmed, stop the workflow with `status: failed` so an orphaned agent cannot write stale artifacts later.
- A builder terminal failure, stall, or wait-recovery failure stops the workflow with `status: failed`.
- A reviewer terminal failure, stall, or wait-recovery failure marks that reviewer slot failed and inactive, then applies the minimum-two-reviewers rule.
- Exception: a failure or stall from the `glm5.3` primary reviewer first triggers its `oc-ollama-cloud/glm-5.2` fallback. Deactivate the slot only if that fallback fails, stalls, or exhausts its artifact-repair attempt without valid YAML.

## Workflow

1. Initialize loop state
   - Use only `mcp__acm__run` for agent launches, `mcp__acm__wait` for normal waiting, `mcp__acm__get_result` plus `mcp__acm__peek` for timeout diagnosis, and `mcp__acm__kill_process` for confirmed stalled processes.
   - Use the current working directory as `workFolder` for every `mcp__acm__run` call.
   - Use `timeout: 900` for every initial `mcp__acm__wait` call and apply the wait and stall detection policy above when needed.
   - Validate that all required input fields are present and non-empty: `builder.task_prompt`, `review_prompt`, `verification_prompt`, `done_criteria`, and `max_loop_rounds`.
   - Resolve the builder model from `builder.model`, defaulting to `codex-ultra` when it is absent or empty.
   - Resolve the Claude reviewer model from `claude.model`, defaulting to `claude-ultra` when it is absent or empty; reject any value other than `claude-ultra` or `fable`.
   - If any required input field is missing or invalid, stop immediately and return `status: failed` with a reason naming the offending field.
   - Create `artifacts_dir` if needed.
   - Before any round `N`, create `<artifacts_dir>/round-N/builder`, `<artifacts_dir>/round-N/reviews`, and `<artifacts_dir>/round-N/reviews/reconsider`.
   - If a builder launch, required builder artifact operation, or builder wait recovery fails, stop immediately and return YAML with top-level `status: failed` and a concrete `reason`.
   - Route reviewer launch, artifact, and wait failures through the reviewer degradation policy instead of failing immediately while at least two reviewer slots remain active.

2. Run builder for round 1
   - Start one builder agent with the resolved builder model.
   - Pass `builder.session_id` when present.
   - Instruct the builder to perform `builder.task_prompt`.
   - Instruct the builder to write `<artifacts_dir>/round-1/builder/handoff.md`.
   - Instruct the builder to include in the handoff:
     - a concise summary of the implementation,
     - the files changed or created,
     - suggested verification focus for reviewers,
     - any known limitations or follow-up risks.

3. Wait for builder
   - Wait until the builder finishes, applying the wait and stall detection policy if needed.
   - Record the latest builder `session_id` and agent status from the result.
   - If the builder fails, stop immediately and return top-level `status: failed`.
   - Read `<artifacts_dir>/round-N/builder/handoff.md`. If it is missing or malformed, stop immediately and return `status: failed`.

4. Run reviewers for round N
   - In round 1, start the three review slots in parallel: `codex` with `codex-ultra`, `glm5.3` first with `oc-ollama-cloud/glm-5.3`, and `claude` with the resolved Claude reviewer model.
   - Treat reviewer launches independently: a launch failure for one slot must not prevent attempts to launch the other slots.
   - In later rounds, start only reviewer slots that remain active. Never relaunch a reviewer slot after it has been degraded out of the workflow.
   - Pass each reviewer's provided or latest `session_id` when present.
   - Give every reviewer:
     - the shared `review_prompt`,
     - the shared `verification_prompt`,
     - the current `done_criteria`,
     - the path to `<artifacts_dir>/round-N/builder/handoff.md`,
     - the path to its assigned output file `<artifacts_dir>/round-N/reviews/<reviewer-id>.yaml`.
   - Instruct each reviewer to:
     - read the builder handoff,
     - inspect the working tree as needed,
     - perform the requested verification,
     - write YAML only to its assigned review file using the reviewer output contract,
     - run the provided review YAML validator against its assigned file and correct any reported errors before completing.
   - If the `glm5.3` primary launch fails, stalls, has an unrecoverable diagnostic failure, finishes with status `failed`, or exhausts its one resumed artifact-repair attempt without valid YAML, emit the fallback progress note and rerun only that reviewer slot with `oc-ollama-cloud/glm-5.2` using the same assigned output file.

5. Wait for reviewers
   - Wait until all launched review agents finish, applying the wait and stall detection policy if needed.
   - Record each reviewer slot's latest `session_id`, `model_used`, fallback state, and agent status from the result.
   - Independently validate every successfully completed review artifact with `scripts/validate_review_yaml.py` and apply the single resumed artifact-repair attempt when validation fails.
   - Resolve each reviewer failure independently. For a `glm5.3` primary terminal failure, stall, wait-recovery failure, or exhausted artifact repair, attempt its fallback, including one fallback artifact-repair attempt when needed, before marking the slot inactive. Mark failed `codex`, failed `claude`, or an exhausted GLM fallback inactive immediately.
   - Continue when at least two reviewer slots remain active and have valid review files. If fewer than two do, stop immediately and return top-level `status: failed`.
   - Read and merge only the valid review files from active reviewer slots at `<artifacts_dir>/round-N/reviews/<reviewer-id>.yaml`.

6. Merge findings
   - Extract reviewer findings from the valid YAML review files for active reviewer slots.
   - Deduplicate findings by `key` when keys match directly.
   - When keys differ but the issue is clearly equivalent, treat them as the same logical finding and merge them.
   - Keep all accepted `needs_fix` findings as fix candidates. Do not discard findings because they seem lower priority.

7. Resolve contradictions
   - Treat a contradiction as a case where the same or equivalent finding has conflicting `position` values across reviewers.
   - Do not treat silence as a contradiction. If one reviewer omits a finding and others report it, merge based on the reported findings and continue.
   - If no contradictions remain, continue to the next step.
   - If contradictions remain, start a contradiction-resolution round for only the conflicting items.
   - Resume each active reviewer session and provide:
     - the conflicting opinions from the other reviewers,
     - the current builder handoff path,
     - the reconsideration output file path at `<artifacts_dir>/round-N/reviews/reconsider/<reviewer-id>.yaml`,
     - the same `review_prompt`, `verification_prompt`, and `done_criteria`.
   - For each reviewer slot, resume the latest successful `model_used` and `session_id`; if `glm5.3` previously fell back, continue contradiction resolution with `oc-ollama-cloud/glm-5.2`.
   - If a `glm5.3` primary contradiction-resolution run fails before fallback has been used, emit the fallback progress note and rerun only that reviewer slot with `oc-ollama-cloud/glm-5.2`.
   - Ask each reviewer to reconsider only the conflicting items and write YAML only for those items to its reconsideration file using the same reviewer output contract.
   - Require each reviewer to run the provided validator on its reconsideration file before completing.
   - Wait for each contradiction-resolution round, applying the wait and stall detection policy if needed.
   - Independently validate each reconsideration file and apply the single resumed artifact-repair attempt before treating it as failed.
   - Route contradiction-resolution launch, wait, terminal, and exhausted artifact-repair failures through the reviewer degradation policy. Stop with `status: failed` if fewer than two reviewer slots remain active.
   - After each contradiction-resolution round, read the valid reconsideration files for active reviewer slots at `<artifacts_dir>/round-N/reviews/reconsider/<reviewer-id>.yaml`.
   - If a reviewer was degraded during contradiction resolution, remove its opinion from the current contradiction set before recomputing positions.
   - Update the conflicting findings with the latest reviewer positions from those reconsideration files.
   - Recompute the remaining contradiction set before deciding whether another contradiction round is needed.
   - Repeat until all active reviewers converge or 3 contradiction-resolution rounds have completed.
   - Treat convergence as all active reviewers agreeing on `position` for a conflicting item.
   - If round 3 ends with three active reviewers and a `2:1` split, adopt the majority view for that item.
   - If round 3 ends with two active reviewers in a `1:1` split, stop immediately and return `status: stopped` with a reason that the two remaining reviewer opinions did not converge after 3 rounds.
   - If any other unresolved contradiction has no majority after round 3, stop immediately and return `status: stopped` with a concrete reason.

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
   - Start the next builder round with `mcp__acm__run` using the resolved builder model, the current working directory as `workFolder`, and the latest builder `session_id`.
   - Wait for the builder, applying the wait and stall detection policy if needed.
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
active_reviewers_count: 3
degraded_reviewer_ids: []

reviewers:
  codex:
    model_used: codex-ultra
    fallback_used: false
    artifact_repair_used: false
    session_id: sess_codex_final
    status: completed
  glm5.3:
    primary_model: oc-ollama-cloud/glm-5.3
    fallback_model: oc-ollama-cloud/glm-5.2
    model_used: oc-ollama-cloud/glm-5.3
    fallback_used: false
    artifact_repair_used: false
    fallback_reason: null
    session_id: sess_glm53_or_glm52_final
    status: completed
  claude:
    model_used: claude-ultra
    fallback_used: false
    artifact_repair_used: false
    session_id: sess_claude_final
    status: completed

builder:
  model: codex-ultra
  session_id: sess_build_final
  status: completed
```

Apply these output rules:

- Use top-level `status` values: `completed`, `stopped`, `failed`.
- Use agent-level `status` values: `completed`, `skipped`, `failed`.
- Always include `accepted_findings_count`, `contradiction_rounds`, `unresolved_items_count`, and `loop_rounds`.
- Always include `active_reviewers_count` and `degraded_reviewer_ids` based on the final reviewer set.
- Always return all three reviewer entries.
- Always return the builder entry.
- Set `builder.model` to the resolved builder model used for all builder rounds.
- Use `session_id` consistently in both input and output.
- For every reviewer slot, include `model_used`, `fallback_used`, and `artifact_repair_used`. Set `artifact_repair_used: true` if any review or reconsideration artifact repair was attempted for that slot, whether or not it succeeded.
- For `claude`, set `model_used` to the resolved Claude reviewer model and always set `fallback_used: false`; selecting `fable` explicitly is not fallback behavior.
- For `glm5.3`, also include `primary_model`, `fallback_model`, and `fallback_reason`; set `fallback_reason: null` when no fallback was used. When invalid YAML caused fallback, include the post-repair validator diagnostics in `fallback_reason`.
- When processing fails before an agent launches, preserve the provided input `session_id` if one exists and mark that agent `status: skipped`.
- When an attempted reviewer launch fails or a reviewer is degraded after launch, preserve its provided or latest known `session_id` when available and mark that reviewer `status: failed`.
- A top-level `status: completed` or `status: stopped` may include one reviewer with `status: failed` when two reviewer slots remained active and the workflow otherwise reached that outcome.
- When processing fails after an agent launches or after stall detection, return the latest known `session_id` and mark that agent `status: failed`.
- When no `session_id` was ever observed for a failed newly started agent, set `session_id: null`.
- When processing stops because no accepted `needs_fix` findings remain and `done_criteria` is satisfied, set top-level `status: completed`; if degraded, mention the two-reviewer completion in `reason`.
- When processing stops because reviewer opinions do not converge, set top-level `status: stopped` and explain the contradiction outcome in `reason`.
- When processing stops because the loop limit is reached, set top-level `status: stopped` and explain that `max_loop_rounds` was exhausted before satisfying `done_criteria`.
