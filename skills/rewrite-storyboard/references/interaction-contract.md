# Interaction contract

## Two approvals

### Gate 1: direction selection

When requirements are absent, read the source first and offer 2–3 tailored directions. Keep each to a short name plus one or two sentences. Let the user choose, combine, or state a different requirement.

Direction selection authorizes planning only. It does not authorize file creation.

### Gate 2: shot-plan approval

After a direction is selected, present a compact scheme summary and a numbered plan for the affected shots. State what changes, not the final prompt wording. Group truly unchanged shots only when doing so does not hide a continuity consequence.

Ask the user to confirm or name shots to revise. Formal generation begins only after an explicit approval of the current shot plan.

## Concision rules

- Lead with the decision the user needs to make.
- Do not expose fact ledgers, dependency graphs, JSON, validation rules, or internal reasoning unless asked.
- Candidate directions must be meaningfully different, not three wordings of the same substitution.
- A shot-plan line normally contains one main change and its essential consequence.
- Put production details in the generated file, not in chat.

## Direct requests

If the user says exactly what to change, skip candidate directions. Summarize the requested direction, build the affected shot plan, and wait for Gate 2 approval.

If the user supplies a complete shot-by-shot plan, verify propagation and show only necessary corrections or a concise normalized plan. Still obtain explicit approval before generating.

## Revisions and cancellation

- When the user revises a plan, update all dependent shots and request approval of the new plan.
- `返回` returns from the shot plan to direction selection without generating.
- `取消` stops the rewrite and creates no formal output.
- Never use silence, an unrelated reply, or mere attachment of a file as approval.
