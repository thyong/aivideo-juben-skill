---
name: translate-ocean-video-prompts
description: Convert TKDRAMA-exported Chinese .txt storyboards and image prompts into a consistent bright, premium ocean-healing visual system while preserving narrative truth and import compatibility. Use for 海洋风转换 when Codex must also optimize each shot's subject prominence, focus set, depth of field, motion space, scene simplicity, and cross-shot continuity, then output a converted file plus a modification summary.
---

# Ocean Video Prompt Translation

## Objective

Produce two files beside the source unless the user specifies another destination:

1. `<source-stem>-海洋风转换.txt`: import-ready conversion with the source format preserved.
2. `<source-stem>-修改总结.md`: concise shot-level change report emphasizing scene-environment changes and narrative justification.

Never produce API system prompts. This skill only performs file conversion and reporting.

## Required references

Read all three before converting:

- [visual-style.md](references/visual-style.md): fixed visual-style block, lighting adapters, and the boundary between style and optical depth of field.
- [translation-rules.md](references/translation-rules.md): narrative-first scene, continuity, camera, focus, depth-of-field, and quality rules.
- [file-contract.md](references/file-contract.md): parsing, replacement-plan schema, and output guarantees.

## Workflow

1. Read the entire source file. Detect encoding and retain any UTF-8 BOM.
2. Run `scripts/tkdrama_transform.py inspect <source>` to inventory shots, fields, and scene groups.
3. Build story continuity before editing individual prompts:
   - identify location groups, time, weather, recurring props/assets, and narrative function;
   - record the stable color, material, shape, damage state, and location of recurring assets when the source defines them;
   - resolve pronouns and repeated locations from the full story, not isolated frames;
   - preserve poverty, danger, occupation, social status, and cause-and-effect.
4. Classify every prompt element:
   - **LOCK**: story event, role identity, emotion, action, interaction, prop and its function, shot size, angle, composition, movement direction, and time continuity;
   - **CONTROLLED CAMERA**: focus set, depth of field, subject occupancy, background readability, and motion space; optimize these inside `镜头` without changing the locked camera intent;
   - **TRANSLATE WHEN NEEDED**: lighting, palette, material finish, location subtype, background depth, irrelevant clutter;
   - **FIXED**: the exact `画面风格` block from `visual-style.md`.
5. Score lighting and scene risk, then derive a per-shot focal plan using `translation-rules.md`. Do not use one fixed depth-of-field sentence for all shots.
6. Choose the least invasive scene treatment:
   - level 0: retain;
   - level 1: recolor/rematerialize while retaining place and structure;
   - level 2: use a narrative-equivalent coastal subtype while retaining function and plausibility.
7. Create a replacement-plan JSON matching `file-contract.md`:
   - replace `镜头` in every shot with the original shot size, angle, composition, and direction preserved, plus the shot-specific focus, depth, subject occupancy, and motion-space decision;
   - include `光线` and `场景环境` only where risk or continuity requires change;
   - edit `描述` or `主体角色` only when an otherwise unresolved recurring-asset or cause-and-effect contradiction would remain, and document the exception;
   - never cite or require a reference image unless the user explicitly supplied that image to the generation workflow.
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
- Do not rewrite `故事概述`, `故事角色`, or `生成要求`.
- `镜头` is a controlled optimization field: retain the source shot size, angle, composition, character placement, and movement direction while adding a shot-specific focus set, depth of field, subject occupancy, background readability, and motion space.
- Do not rewrite `描述` or `主体角色` unless a recurring asset, time sequence, or cause-and-effect contradiction cannot be resolved in `镜头`, `光线`, or `场景环境`. Record the exact exception in the summary.
- Replace every existing `画面风格` value with the fixed block verbatim. Do not customize it per shot.
- Adapt time-specific illumination only in `光线`; never insert daylight into a night scene.
- Keep functional props in their natural colors when recoloring would harm recognition or narrative (for example red bricks and a red sports car).
- Avoid forcing visible ocean into every frame. Use coastal materials, reflected light, palette, air, and architecture when a literal sea view is implausible.
- Keep scenes as simple as the story permits. Remove visually distracting objects only when they carry no action, continuity, socioeconomic, danger, occupation, or cause-and-effect information. Preserve plausible sources for functional props, such as a coastal grove when a character gathers firewood.
- Never blur a narrative-critical face, action, interaction, injury, prop, clue, threat, vehicle, destination, or cause-and-effect element merely because it sits in the foreground or background.
- Do not invent “原始参考图”, “保持参考图”, seeds, weights, coordinates, or asset properties that the user did not provide.

## Quality gate

Do not deliver until all checks pass:

- The converted file has the same shot count and structural markers as the source.
- Every shot retains its narrative event, roles, action, functional props, camera intent, and temporal continuity.
- Recurring locations use consistent architecture, materials, time, weather, and light direction; recurring assets keep the same defined appearance and state unless the story changes them.
- Lighting is bright and readable without contradicting night, dusk, interior, or dramatic context.
- Blue/ice-blue/cream-white lead the palette without monochrome electric blue.
- Warm colors remain controlled accents; shadows retain detail.
- Scenes retain foreground, middle ground, and background where the camera description permits.
- Every `镜头` names an appropriate depth-of-field level and keeps all narrative-critical elements in focus.
- Character-led shots keep the subject visually dominant; wider environment-dependent shots do not shrink the subject more than the narrative requires.
- Moving subjects have usable motion space, while static interaction shots do not invent movement.
- The summary lists all changed fields and gives narrative-aware reasons, with no invented evidence.
