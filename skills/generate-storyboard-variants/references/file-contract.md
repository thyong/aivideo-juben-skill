# Storyboard variant file contract

## Output naming

For source `/path/aaa.txt` and count `N`, write beside the source unless the user specifies another directory:

```text
/path/aaa_1.txt
...
/path/aaa_N.txt
```

Never overwrite the source. Existing output files may be overwritten only when the user clearly asks to regenerate them; otherwise stop and report the collision.

## Preserve exactly

- encoding and UTF-8 BOM state;
- header, version and story blocks;
- all section markers;
- shot count/order, `序号`, `文件名`, `对应角色`;
- field order;
- video prompts, including empty blocks;
- every field/text not included in the plan.

## Plan schema

Create one UTF-8 JSON plan per output:

```json
{
  "variant": {
    "number": 1,
    "dna": "white farmhouse; sage and cream; pale oak and black iron"
  },
  "continuity": {
    "family-bedroom": "black iron bed; sage checked bedding; white-grid window"
  },
  "shots": {
    "1": {
      "fields": {
        "场景环境": "replacement without the field prefix"
      }
    }
  }
}
```

`variant` and `continuity` document reasoning and are ignored by the application engine. `shots` drives exact field replacement.

Recognized fields: `描述`, `主体角色`, `镜头`, `光线`, `场景环境`, `画面风格`, `生成要求`.

Normally change only `场景环境`; exceptionally change `光线` to resolve a direct environmental contradiction. Editing locked fields requires explicit user authorization.

When the user explicitly authorizes a normally locked field for the current task, declare the exact field in the plan so the application and validator can audit it:

```json
{
  "authorized_fields": ["镜头"],
  "shots": {}
}
```

Do not add `authorized_fields` based on inference. Its presence records task-specific permission and does not relax the default lock for other plans.

## Commands

```bash
python3 scripts/storyboard_variants.py inspect SOURCE.txt
python3 scripts/storyboard_variants.py apply SOURCE.txt PLAN.json OUTPUT.txt
python3 scripts/storyboard_variants.py validate SOURCE.txt OUTPUT.txt PLAN.json
```

The application must fail on unknown shots, missing fields, duplicate output paths or output equal to source. Validation must fail on structural differences or unplanned edits.
