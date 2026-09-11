---
name: convert-to-animal-characters
description: Convert the existing characters in a Chinese TKDRAMA storyboard into the user's animal-character system while preserving the source story and every shot's event state. Use for 动物人转换、转换角色、改成动物人 or equivalent requests. Confirm the role mapping before generating, and never make unapproved plot, action, prop, weapon, outcome, or visual changes.
---

# Animal Character Conversion

Convert only the source's character system. Do not classify or name the source character category, and do not infer a broader adaptation request from examples in the source.

## Workflow

1. Read the complete source, including the story overview, role block, corresponding-role lists, image prompts, video prompts, and adjacent shots.
2. Check whether those fields agree about who acts, what happens, and the state at the end of each shot. If a discrepancy affects safe conversion, identify the exact shot and conflicting statements, then stop. Ask the user to provide a corrected file or the correct fact. Never resolve it silently.
3. Build a literal source-name-to-target-name mapping. Treat aliases for the same role as separate source strings that map to one target role.
4. Show the mapping concisely. List any truly necessary non-name adjustment in a separate section. If none is needed, state `除角色名称与必要的角色指代外，其他内容不变。`
5. Wait for explicit confirmation of the current mapping and any listed adjustment. Confirmation authorizes exactly those changes and nothing else.
6. Record the approved literals in a plan, apply them mechanically, validate the output, and then manually recheck every shot against the source.

Read [references/conversion-contract.md](references/conversion-contract.md) before proposing a mapping. Read [references/file-contract.md](references/file-contract.md) before creating or validating an output file.

## Role mapping rules

- Derive role identity from story function and relationships, not from a guessed source category.
- Prefer the user's existing animal IP names or mapping when supplied.
- Main role names normally contain only stable identity and relationship, such as `小猫`、`猫爸爸`、`小猫玩伴`. Do not add colors, body shape, clothing, personality, or other appearance traits unless the user requires them.
- Keep family and peer relationships coherent. Do not assign a different species merely to create variety, and do not use animal stereotypes to infer morality, strength, or personality.
- Keep a role unchanged when it is already compatible and the user has not asked to replace it.
- When the user's IP assets do not determine a safe target, ask one focused question or mark that single mapping for confirmation; do not invent a detailed character design.

## Absolute boundaries

Unless explicitly listed and confirmed, preserve exactly:

- story facts, causality, conflict, escalation, climax, and ending;
- shot count, order, and each shot's current event state;
- actions, weapons, tools, key props, injury, damage, success, failure, and outcomes;
- scene, lighting, composition, camera, camera movement, visual intensity, style, dialogue, and timing;
- TKDRAMA markers, field order, identifiers, image filenames, and encoding.

Do not rewrite the story overview for polish. Apply only the approved literal role substitutions and approved corrections. Never move a later result into an earlier shot: if one shot ends with a threat still advancing and the next shot resolves it, preserve that boundary.

If an action truly cannot work with the target body or IP asset, do not fix it automatically. Explain the single incompatibility and propose the minimum necessary adjustment for approval.

## Output

Default to `<原文件名>-动物人版-1.txt` beside the source without overwriting any file. Deliver only after the exact-change guard passes and the manual source comparison finds no unapproved change.
