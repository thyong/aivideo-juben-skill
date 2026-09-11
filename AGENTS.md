# AI video storyboard skill router

This repository contains independent skills. Route by explicit command first; never blend their rules implicitly.

## Commands

- `开始` -> `aivideo-story-assistant`; show the indexed guided menu
- `技能清单` / `查看技能` -> `aivideo-story-assistant`; group indexed skills by status
- `帮助` / `返回` / `取消` -> `aivideo-story-assistant`; manage guided interaction
- `海洋风转换` -> `translate-ocean-video-prompts`
- `剧本多版本` -> `generate-storyboard-variants`
- `原创剧本` -> `create-original-animal-storyboard`
- `剧本二创` -> `rewrite-storyboard`; require direction confirmation and then shot-plan confirmation before generation
- `动物人转换` / `转换角色` -> `convert-to-animal-characters`; confirm the literal role mapping and preserve all unapproved content exactly
- `帮助：<技能名或命令>` -> read the matching index entry and its `SKILL.md`

## Routing rules

1. An explicit command selects exactly one skill.
2. `剧本多版本` inherits the source style and must not call ocean conversion.
3. `海洋风转换` creates one converted file and must not create numbered variants.
4. `原创剧本` creates a genuinely new story and independent hard-cut storyboard; it must not be used as a source-preserving variant or style conversion.
5. `动物人转换` changes only the current script's role system. Do not classify the source, rewrite the story, or alter any unapproved shot content.
6. If a request uniquely matches one indexed skill, implicit selection is allowed.
7. If multiple skills are requested, execute only in the user's stated order. Ask for order when order materially changes the result.
8. Announce the selected skill before acting.
9. Status, aliases, inputs, outputs, and menu content come from `skills-index.yaml`.
10. Add every future skill to `skills-index.yaml`; update this command list only for a new canonical command or navigation behavior.
