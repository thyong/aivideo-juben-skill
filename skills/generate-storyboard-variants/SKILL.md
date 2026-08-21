---
name: generate-storyboard-variants
description: Generate a user-specified number of format-preserving variants from any TKDRAMA-exported Chinese .txt storyboard or similarly structured script. Use for 剧本多版本、微二创、矩阵号版本 or 批量差异化分镜. Preserve narrative, roles, actions, props, source style and image-to-video compatibility while improving scene relevance, visual appeal, subject prominence, focus and depth of field. Enforce strong differences between versions and strict continuity within each version. Do not perform style conversion or image-similarity analysis.
---

# Storyboard Variant Generation

## Objective

Given one structured script and a positive integer `N`, create exactly `N` sibling files:

```text
aaa.txt -> aaa_1.txt ... aaa_N.txt
```

Preserve the source. Do not generate summaries unless the user requests one.

## Required references

Read all three before planning variants:

- [continuity-contract.md](references/continuity-contract.md): story locks, entity identity, continuity and safe variation rules.
- [scene-composition-contract.md](references/scene-composition-contract.md): source-residue removal, scene simplicity, aesthetic value, subject scale, focus and depth-of-field rules.
- [file-contract.md](references/file-contract.md): plan schema, naming, application and validation.

## Workflow

1. Read the entire source file before changing any shot. Detect encoding and retain any UTF-8 BOM.
2. Run `scripts/storyboard_variants.py inspect SOURCE.txt` to inventory shots and prompt fields.
3. Build a whole-script continuity ledger:
   - group shots by physical location and distinguish genuinely different locations;
   - track recurring furniture, architecture, vehicles, containers, clothing and props;
   - record material, color, shape, placement and temporal state;
   - mark every story-dependent attribute as locked.
4. Audit every scene element. Keep narrative-functional elements, keep at most one high-value aesthetic anchor, and remove or replace source-video residue that has no story, location-recognition or composition value.
5. Classify every shot as interaction/emotion, movement/action, spectacle/reveal or result/environment-upgrade. Use that classification to choose subject scale, focal target, motion clearance and depth of field.
6. Separate source inconsistencies from intentional story changes. Normalize obvious prompt drift only when the full story establishes that shots share one unchanged location or entity.
7. Design one coherent visual DNA for each requested version. Inherit the source's visual style; never introduce a named style that the source does not contain. Keep pre-reward socioeconomic conditions truthful and reserve upgrades for story-established results.
8. Make versions materially distinct through high-impact safe variables such as environment structure, background silhouette, nonfunctional material family, secondary palette, window/door/furniture design and one controlled aesthetic anchor. Do not manufacture difference through clutter.
9. Apply each version DNA to every occurrence of the same scene or entity. Never improvise shot by shot.
10. Change the least number of fields necessary:
    - use `场景环境` for scene relevance, simplicity, continuity and visual value;
    - use `镜头` only to refine subject prominence, focal target, motion clearance and depth of field while preserving the original shot size, angle and framing purpose;
    - add `"authorized_fields": ["镜头"]` to the plan when `镜头` is refined;
    - change `光线` only to resolve a direct environmental contradiction, never to invent a new time of day or style;
    - do not change `画面风格` merely to create variety.
11. Create one plan JSON per version and apply it:

   ```bash
   python3 scripts/storyboard_variants.py apply SOURCE.txt PLAN.json OUTPUT.txt
   ```

12. Validate every output:

   ```bash
   python3 scripts/storyboard_variants.py validate SOURCE.txt OUTPUT.txt PLAN.json
   ```

13. Read all outputs across recurring scene groups. Audit narrative truth, continuity, scene residue, visual appeal, subject scale and depth of field, then rerun validation after corrections.

## Decision priority

Use this strict order:

1. Narrative truth and cause-and-effect.
2. Character, action, emotion and functional prop relationships.
3. Image-to-video motion compatibility and camera intent.
4. Within-version continuity.
5. Subject readability and scene simplicity.
6. Inherited source style and visual quality.
7. Difference between versions.

Never sacrifice items 1–6 to increase variety.

## Hard boundaries

- Treat this skill as style-neutral. It accepts ocean, urban realism, rural, fantasy or any other source style and inherits that style.
- Never call a style-conversion skill unless the user separately requests it.
- Preserve story overview, roles, shot count/order, filenames, corresponding roles, descriptions, subject actions, emotion, functional props, generation requirements and video-prompt blocks.
- Preserve every shot's original size, angle, camera direction and narrative framing purpose. Camera refinement may clarify scale, focus, motion space and depth of field; it must not redesign the shot.
- Do not change food, money, medicine, tools, vehicles or other plot objects into substitutes with different functions.
- A mutable attribute may differ between output versions, but after selection it must remain consistent throughout that version.
- If an attribute is used by the story, lock it across all versions. Example: a metal bed involved in a metal-impact action must remain metal.
- Do not add image similarity scoring, regeneration loops or claims about platform detection thresholds.
- Do not invent reference images, seeds, weights, asset properties or production requirements.
- Do not treat simple scenery as permission to make it dull, dirty, empty or aesthetically cheap. Do not upgrade a poor or ordinary household into luxury before the story earns that change.

## Quality gate

Deliver only when:

- exactly `N` files exist with names `<source-stem>_1.txt` through `<source-stem>_N.txt`;
- every file passes structural validation;
- outputs preserve the source encoding/BOM and all unplanned text;
- each version has a documented internal visual DNA in its working plan;
- all recurring scenes and entities remain internally consistent;
- versions differ in high-impact environmental features rather than token decoration;
- irrelevant source-scene residue has been removed;
- each scene is minimally sufficient for the action and uses no more than one nonfunctional aesthetic anchor;
- subjects and functional props remain visually dominant without losing required movement space;
- depth of field matches shot function instead of being uniformly shallow or uniformly sharp;
- reward, wealth or environment-upgrade shots retain enough background readability to communicate the payoff;
- the original visual style and image-to-video conditions remain intact.
