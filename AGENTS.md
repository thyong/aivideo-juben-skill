# AI video storyboard skill router

This repository contains independent skills. Route by explicit command first; never blend their rules implicitly.

## Commands

- `海洋风转换` -> `translate-ocean-video-prompts`
- `剧本多版本` -> `generate-storyboard-variants`
- `查看技能` -> read `skills-index.yaml` and list available skills
- `帮助：<技能名或命令>` -> read the matching index entry and its `SKILL.md`

## Routing rules

1. An explicit command selects exactly one skill.
2. `剧本多版本` inherits the source style and must not call ocean conversion.
3. `海洋风转换` creates one converted file and must not create numbered variants.
4. If a request uniquely matches one indexed skill, implicit selection is allowed.
5. If multiple skills are requested, execute only in the user's stated order. Ask for order when order materially changes the result.
6. Announce the selected skill before acting.
7. Add every future skill to `skills-index.yaml` and this command list.
