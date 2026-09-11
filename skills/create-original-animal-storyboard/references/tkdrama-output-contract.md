# TKDRAMA Output Contract

## Naming and location

- Default filename: `<title>-原创版-1-剧本.txt`.
- Use the user-specified directory when provided; otherwise save in the active task's normal deliverable directory.
- Do not overwrite an unrelated existing file.

## Required file structure

Use UTF-8 text and retain this order:

1. `TKDRAMA 剧本导出文件`
2. `格式版本：1`
3. `视频文件：`
4. `剧本标题：`
5. `备注：`
6. `<<<故事概述>>>` block
7. `<<<故事角色>>>` block
8. sequential `<<<分镜开始>>>` blocks

`<<<故事概述>>>` must contain only in-world story events. Do not write authorial or production-control phrases such as “故事立即结束”, “到此结束”, “观众预期已交付”, “本镜”, “硬切”, “为了完播率” or instructions about what should not follow. Put such constraints in `备注` or keep them internal.

Each shot must contain:

- `序号：N`
- `文件名：N.jpg`
- `对应角色：[...]`
- `<<<图片提示词>>>` and closing marker
- one prompt containing `描述：`, `主体角色：`, `镜头：`, `光线：`, `场景环境：`, `画面风格：`, `生成要求：`
- `<<<视频提示词>>>` and closing marker
- `<<<分镜结束>>>`

Keep video-prompt contents empty unless the user provides or requests them.

## Image-prompt requirements

- **描述:** state the complete independent narrative beat and emotion.
- **主体角色:** name visible roles, stable appearance/wardrobe from assets when known, simple action and interaction.
- **镜头:** normally use readable flat medium framing and a dominant subject; specify wider framing only when scale or travel matters.
- **光线:** keep faces and core actions bright and readable without contradicting time or mood.
- **场景环境:** use a simple, plausible scene with only narrative, socioeconomic and one optional aesthetic anchor.
- **画面风格:** use one consistent style block across the story unless the user supplies another style system.
- **生成要求:** include TikTok 9:16, clarity, role-asset consistency and American setting/language defaults when relevant. Do not invent reference-image instructions.

## Continuity

Lock across all occurrences unless the story changes them:

- character identity, body type, fur color and wardrobe;
- recurring prop color, material and recognizable shape;
- socioeconomic state before and after a demonstrated change;
- injuries, transformations, constructed objects and acquired wealth;
- causal facts established by previous shots.

Do not lock exact screen position, hand placement, walking direction, camera location or background geometry unless required to understand the story.

## Validation

Run:

```bash
python3 scripts/validate_tkdrama_story.py FILE --min-shots 20 --max-shots 20
```

The default one-minute workflow uses 20 shots because finished clips are normally about 3 seconds. Change the shot bounds only when the user specifies a different runtime or verified cadence. Structural success does not replace the independent-shot manual audit.
