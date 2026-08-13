---
name: generate-storyboard-variants
description: Generate a user-specified number of format-preserving variants from any TKDRAMA-exported Chinese .txt storyboard or similarly structured script. Use when the user asks for 剧本多版本、微二创、矩阵号版本、批量差异化分镜, or requests outputs such as aaa_1.txt through aaa_N.txt while preserving the input script's own visual style, narrative, roles, actions, props, camera intent, and image-to-video compatibility. Enforce strong differences between versions and strict scene/entity continuity within each version. Do not perform style conversion or image-similarity analysis.
---

# Storyboard Variant Generation

## Objective

Given one structured script and a positive integer `N`, create exactly `N` sibling files:

```text
aaa.txt -> aaa_1.txt ... aaa_N.txt
```

Preserve the source. Do not generate summaries unless the user requests one.

## Required references

Read both before planning variants:

- [continuity-contract.md](references/continuity-contract.md): story locks, entity identity, continuity and safe variation rules.
- [file-contract.md](references/file-contract.md): plan schema, naming, application and validation.

## Workflow

1. Read the entire source file before changing any shot. Detect encoding and retain any UTF-8 BOM.
2. Run `scripts/storyboard_variants.py inspect SOURCE.txt` to inventory shots and prompt fields.
3. Build a whole-script continuity ledger:
   - group shots by physical location and distinguish genuinely different locations;
   - track recurring furniture, architecture, vehicles, containers, clothing and props;
   - record material, color, shape, placement and temporal state;
   - mark every story-dependent attribute as locked.
4. Separate source inconsistencies from intentional story changes. Normalize obvious prompt drift only when the full story establishes that shots share one unchanged location or entity.
5. Design one coherent visual DNA for each requested version. Inherit the source's visual style; never introduce a named style that the source does not contain.
6. Make versions materially distinct through high-impact safe variables such as environment structure, background silhouettes, nonfunctional material families, secondary color distribution, window/door/furniture design and non-story decoration.
7. Apply each version DNA to every occurrence of the same scene or entity. Never improvise shot by shot.
8. Change the least number of fields necessary. Prefer `场景环境`. Change `光线` only when required by the chosen environment and without changing time of day. Do not change `画面风格` merely to create variety.
9. Create one plan JSON per version and apply it:

   ```bash
   python3 scripts/storyboard_variants.py apply SOURCE.txt PLAN.json OUTPUT.txt
   ```

10. Validate every output:

   ```bash
   python3 scripts/storyboard_variants.py validate SOURCE.txt OUTPUT.txt PLAN.json
   ```

11. Read all outputs across recurring scene groups. Correct any within-version contradiction, then rerun validation.

## Decision priority

Use this strict order:

1. Narrative truth and cause-and-effect.
2. Character, action, emotion and functional prop relationships.
3. Image-to-video motion compatibility and camera intent.
4. Within-version continuity.
5. Inherited source style and image quality.
6. Difference between versions.

Never sacrifice items 1–5 to increase variety.

## Hard boundaries

- Treat this skill as style-neutral. It accepts ocean, urban realism, rural, fantasy or any other source style and inherits that style.
- Never call a style-conversion skill unless the user separately requests it.
- Preserve story overview, roles, shot count/order, filenames, corresponding roles, descriptions, subject actions, emotion, camera fields, functional props, generation requirements and video-prompt blocks.
- Do not change food, money, medicine, tools, vehicles or other plot objects into substitutes with different functions.
- A mutable attribute may differ between output versions, but after selection it must remain consistent throughout that version.
- If an attribute is used by the story, lock it across all versions. Example: a metal bed involved in a metal-impact action must remain metal.
- Do not add image similarity scoring, regeneration loops or claims about platform detection thresholds.
- Do not invent reference images, seeds, weights, asset properties or production requirements.

## Quality gate

Deliver only when:

- exactly `N` files exist with names `<source-stem>_1.txt` through `<source-stem>_N.txt`;
- every file passes structural validation;
- outputs preserve the source encoding/BOM and all unplanned text;
- each version has a documented internal visual DNA in its working plan;
- all recurring scenes and entities remain internally consistent;
- versions differ in high-impact environmental features rather than token decoration;
- the original visual style and image-to-video conditions remain intact.
