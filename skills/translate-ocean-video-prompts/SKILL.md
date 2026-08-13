---
name: translate-ocean-video-prompts
description: Convert TKDRAMA-exported Chinese .txt storyboards and image prompts from mixed source-video aesthetics into a consistent bright, premium ocean-healing visual system while preserving narrative truth, shot intent, roles, actions, props, camera structure, file markers, field order, and import compatibility. Use when Codex receives a TKDRAMA 剧本导出文件 or similarly structured 分镜提示词 file and must output a converted file plus a scene-focused modification summary.
---

# Ocean Video Prompt Translation

## Objective

Produce two files beside the source unless the user specifies another destination:

1. `<source-stem>-海洋风转换.txt`: import-ready conversion with the source format preserved.
2. `<source-stem>-修改总结.md`: concise shot-level change report emphasizing scene-environment changes and narrative justification.

Never produce API system prompts. This skill only performs file conversion and reporting.

## Required references

Read all three before converting:

- [visual-style.md](references/visual-style.md): fixed visual-style block and lighting adapters.
- [translation-rules.md](references/translation-rules.md): narrative-first decision rules and quality checks.
- [file-contract.md](references/file-contract.md): parsing, replacement-plan schema, and output guarantees.

## Workflow

1. Read the entire source file. Detect encoding and retain any UTF-8 BOM.
2. Run `scripts/tkdrama_transform.py inspect <source>` to inventory shots, fields, and scene groups.
3. Build story continuity before editing individual prompts:
   - identify location groups, time, weather, recurring props, and narrative function;
   - resolve pronouns and repeated locations from the full story, not isolated frames;
   - preserve poverty, danger, occupation, social status, and cause-and-effect.
4. Classify every prompt element:
   - **LOCK**: story event, role identity, emotion, action, interaction, prop and its function, shot size, angle, composition, time continuity;
   - **TRANSLATE WHEN NEEDED**: lighting, palette, material finish, location subtype, background depth, irrelevant clutter;
   - **FIXED**: the exact `画面风格` block from `visual-style.md`.
5. Score lighting and scene risk using `translation-rules.md`. Do not rewrite a field merely because it exists.
6. Choose the least invasive scene treatment:
   - level 0: retain;
   - level 1: recolor/rematerialize while retaining place and structure;
   - level 2: use a narrative-equivalent coastal subtype while retaining function and plausibility.
7. Create a replacement-plan JSON matching `file-contract.md`. Only include fields that truly change. Never cite or require a reference image unless the user explicitly supplied that image to the generation workflow.
8. Apply the plan:

   ```bash
   python3 scripts/tkdrama_transform.py apply SOURCE.txt PLAN.json OUTPUT.txt --summary SUMMARY.md
   ```

9. Validate structure and locked content:

   ```bash
   python3 scripts/tkdrama_transform.py validate SOURCE.txt OUTPUT.txt PLAN.json
   ```

10. Read the output and summary. Correct any semantic or continuity issue, then rerun validation.

## Decision priority

Use this strict order whenever requirements compete:

1. Narrative correctness and cause-and-effect.
2. Scene function and continuity.
3. Character action, prop relationship, and camera intent.
4. Fixed visual identity.
5. Decorative beauty.

Never sacrifice items 1–3 to make a scene more oceanic or luxurious. “Premium” describes execution quality, not the characters' wealth. A poor home remains poor; convert it into a coherent, carefully art-directed coastal poor home, not a villa.

## Editing discipline

- Preserve the source file's markers, shot count, shot order, filenames, roles, video-prompt blocks, field order, and unrelated text byte-for-byte where practical.
- Do not rewrite `故事概述`, `故事角色`, `描述`, `主体角色`, `镜头`, or `生成要求` unless a requested visual conversion creates a direct contradiction that cannot be solved inside `光线` or `场景环境`.
- If an exceptional locked-field edit is unavoidable, record the exact reason in the summary.
- Replace every existing `画面风格` value with the fixed block verbatim. Do not customize it per shot.
- Adapt time-specific illumination only in `光线`; never insert daylight into a night scene.
- Keep functional props in their natural colors when recoloring would harm recognition or narrative (for example red bricks and a red sports car).
- Avoid forcing visible ocean into every frame. Use coastal materials, reflected light, palette, air, and architecture when a literal sea view is implausible.
- Do not invent “原始参考图”, “保持参考图”, seeds, weights, coordinates, or asset properties that the user did not provide.

## Quality gate

Do not deliver until all checks pass:

- The converted file has the same shot count and structural markers as the source.
- Every shot retains its narrative event, roles, action, functional props, camera intent, and temporal continuity.
- Recurring locations use consistent architecture, materials, time, and light direction.
- Lighting is bright and readable without contradicting night, dusk, interior, or dramatic context.
- Blue/ice-blue/cream-white lead the palette without monochrome electric blue.
- Warm colors remain controlled accents; shadows retain detail.
- Scenes retain foreground, middle ground, and background where the camera description permits.
- The summary lists all changed fields and gives narrative-aware reasons, with no invented evidence.

