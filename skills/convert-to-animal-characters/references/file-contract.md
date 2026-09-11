# File and validation contract

## Approved plan

After confirmation, create a temporary JSON plan:

```json
{
  "approval": {"mapping_confirmed": true},
  "source_shot_count": 18,
  "role_mappings": [
    {"source": "小橙子男孩", "target": "小猫"},
    {"source": "橙子儿子", "target": "小猫"}
  ],
  "approved_replacements": []
}
```

List every literal source alias in `role_mappings`. `approved_replacements` is only for a non-name correction that the user explicitly approved. Each item contains exact `source` and `target` strings and may contain an exact positive `count`.

## Commands

```bash
python3 scripts/animal_character_guard.py inspect SOURCE.txt
python3 scripts/animal_character_guard.py apply SOURCE.txt OUTPUT.txt PLAN.json
python3 scripts/animal_character_guard.py validate SOURCE.txt OUTPUT.txt PLAN.json
```

The validator constructs the only permitted output by applying all role mappings simultaneously, then applying approved exact replacements. It requires byte-equivalent text and matching UTF-8 BOM after those operations. Therefore formatting cleanup, summary rewriting, prompt optimization, or any undeclared wording change fails validation.

## Output rules

- Never overwrite the source or an existing output.
- Preserve source UTF-8 BOM state, line endings, markers, field order, whitespace, shot count, sequence, and identifiers.
- Default name: `<原文件名>-动物人版-1.txt`.
- Do not produce a modification summary unless requested.
- If exact mechanical replacement cannot produce a coherent file, return to the user with the precise incompatibility; do not bypass the guard.
