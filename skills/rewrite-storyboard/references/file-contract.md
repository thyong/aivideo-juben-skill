# File and validation contract

## Output

For `/path/title.txt`, default to:

```text
/path/title-二创版-1.txt
```

Increment the version or use another name only when requested or when avoiding an existing-file collision. Never overwrite the source. Do not overwrite an existing output without explicit authorization.

Preserve UTF-8 BOM state when practical and keep the source's TKDRAMA markers, field labels, and filename identifiers. Shot count, order, and image filenames remain unchanged unless the confirmed plan explicitly changes them.

## Approved plan record

Before generation, create a temporary or adjacent JSON plan:

```json
{
  "approval": {
    "direction_confirmed": true,
    "shot_plan_confirmed": true
  },
  "source_shot_count": 20,
  "output_shot_count": 20,
  "direction": "short approved direction",
  "retained_core": ["emotional engine", "payoff"],
  "changed_shots": {
    "1": "short approved change",
    "2": "short approved change"
  },
  "required_terms": ["new recurring role or prop"],
  "forbidden_residue": ["obsolete role or prop"]
}
```

`required_terms` and `forbidden_residue` must be narrow, literal checks supported by the approved plan. Do not include ambiguous words that can appear legitimately in another context.

If the confirmed plan changes count or order, record the approved counts explicitly. Otherwise they must match the source.

## Commands

```bash
python3 scripts/story_rewrite_guard.py inspect SOURCE.txt
python3 scripts/story_rewrite_guard.py validate SOURCE.txt OUTPUT.txt PLAN.json
```

The validator checks approval flags, encoding, structure, shot sequence, declared counts, role references, required new terms, and obsolete literal residue. It cannot judge narrative quality; manually audit the adaptation contract after it passes.

## Formal file requirements

- Rewrite `故事概述` and `故事角色` to match the approved story.
- Every affected `图片提示词` must contain the detail needed to generate the approved event.
- When a source has `视频提示词`, update every affected nonempty block. Fill empty blocks only when the user requested complete video prompts or the established deliverable requires them.
- Preserve unmodified identifiers and unrelated metadata.
- Do not include internal labels such as `source_fact`, approval gates, audience expectation, or validation notes in story prose.
- Do not generate a separate modification summary unless requested.
