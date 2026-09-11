# Conversion contract

## Source truth check

Build the mapping only after comparing these sources of evidence:

1. story overview and declared roles;
2. each shot's `对应角色`;
3. that shot's image prompt and video prompt;
4. the preceding and following shots.

A conflict is material when choosing one reading would change an actor, target, action, prop, result, relationship, or role mapping. Report the concrete conflict rather than diagnosing or repairing the source. A user-supplied correction becomes the task fact, but it must be recorded as an approved exact replacement if the source file itself remains unchanged.

## Minimal conversion

The normal transformation is literal name and pronoun replacement only. The target role must keep the source role's function, relationships, actions, possessions, and fate.

Do not:

- add or remove roles;
- merge roles because they look similar;
- split a role into multiple animals;
- redesign costumes or appearance;
- replace weapons, tools, jobs, props, locations, or actions;
- soften or intensify violence, emotion, spectacle, or consequences;
- repair perceived plot weaknesses;
- turn a role conversion into story adaptation, visual optimization, or de-duplication.

These changes are allowed only when individually proposed and explicitly confirmed.

## Proposal shown to the user

Keep the proposal short:

```text
角色映射：
- <源角色/别名> → <动物人角色>

必要调整：
- 无。除角色名称与必要的角色指代外，其他内容不变。

请确认这份映射。
```

When a non-name change is necessary, name the exact shot, original content, proposed content, and reason. Do not hide it inside the role list.

## Final audit

After deterministic validation, compare each source and output shot. Check especially:

- action owner and action target;
- weapon/tool/prop nouns;
- action and outcome verbs;
- whether the threat succeeds, fails, continues, or is resolved in that shot;
- prompt intensity, camera, lighting, and scene;
- role lists versus prompt text.

Any difference not present in the confirmed plan is a failure, even if it appears more logical or visually suitable.
