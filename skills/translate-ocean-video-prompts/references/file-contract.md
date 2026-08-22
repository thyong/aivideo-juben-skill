# TKDRAMA file contract

## Input preservation

Preserve:

- UTF-8 BOM when present;
- header and format version;
- story overview and role blocks;
- shot order, `序号`, `文件名`, and `对应角色`;
- all `<<<...>>>` markers;
- empty video-prompt sections;
- field order inside every image prompt;
- all text not listed in the replacement plan.
- unlabeled generation-requirement tails appended directly after `画面风格`, including forms beginning with `反推后生成的图片将用于` or `[反推后生成的图片将用于`.

## Replacement plan

Create UTF-8 JSON with this structure:

```json
{
  "global_fields": {
    "画面风格": "exact fixed style text without the 画面风格： prefix"
  },
  "shots": {
    "8": {
      "fields": {
        "镜头": "replacement preserving source size/angle/composition while adding focus set, depth, prominence, and motion space",
        "光线": "replacement without the 光线： prefix",
        "场景环境": "replacement without the 场景环境： prefix"
      },
      "summary": {
        "scene_before": "露天建筑工地",
        "scene_after": "滨海建筑工地",
        "reason": "统一视觉世界，同时保留工地功能、劳动动作和红砖道具",
        "narrative_check": "通过：职业、贫困状态、动作、手推车和红砖均未改变"
      }
    }
  }
}
```

Only use recognized image-prompt fields: `描述`, `主体角色`, `镜头`, `光线`, `场景环境`, `画面风格`, `生成要求`.

Include a shot-specific `镜头` replacement for every shot. It must preserve the source shot size, angle, composition, placement, and movement direction while adding the focal plan, depth of field, subject prominence, background readability, and motion space. Do not copy one fixed camera suffix across all shots.

Normally include `镜头`, any necessary `光线` or `场景环境`, and the global `画面风格`. If `描述` or `主体角色` must change to resolve a recurring-asset, temporal, or cause-and-effect contradiction, include the field explicitly and explain the exact reason in `summary.reason`.

Use `global_fields` for a field that must be identical in every shot, especially the fixed `画面风格`. Shot-level fields override global fields only when explicitly present; do not override the fixed style per shot.

## Commands

```bash
python3 scripts/tkdrama_transform.py inspect SOURCE.txt
python3 scripts/tkdrama_transform.py apply SOURCE.txt PLAN.json OUTPUT.txt --summary SUMMARY.md
python3 scripts/tkdrama_transform.py validate SOURCE.txt OUTPUT.txt PLAN.json
```

`apply` must fail rather than silently skip an unknown shot or missing field. `validate` must fail when structural markers, shot identities, unplanned fields, or locked sections differ.
