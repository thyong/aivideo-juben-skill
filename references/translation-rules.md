# Narrative-first translation rules

## 1. Build scene groups first

Group shots that share a location and time before rewriting any prompt. Define for each group:

- narrative function and socioeconomic condition;
- indoor/outdoor, time, weather, and continuity;
- fixed architecture, materials, layout, props, view direction, and light direction;
- allowed palette and coastal cues.

Apply one scene-group definition consistently across its shots.

## 2. Lighting risk

Add points from the original `光线` text:

- warm-yellow/orange light dominates: +2
- backlight without explicit facial/front fill: +3
- dark, low-key, dim, oppressive, or underexposed: +3
- hard shadow or high contrast: +2
- severe indoor/outdoor exposure gap: +2
- no plausible blue environmental fill: +2
- no explicit face/upper-body key light: +3
- neon/cyberpunk tendency: +2

Score below 3: retain unless it conflicts with group continuity. Score 3 or more: rewrite `光线` with the correct adapter. Preserve time, weather, direction when narratively important, and emotional purpose.

## 3. Scene risk

Add points from the original `场景环境` text:

- brown/orange/green surfaces dominate: +2
- dark materials dominate: +2
- closed/flat space lacks plausible depth: +2
- generic source location conflicts with the established ocean-world group: +2
- severe background blur removes scene identity: +2
- irrelevant clutter: +1
- no plausible source of white, pale blue, sky blue, or ocean blue: +2
- no foreground/middle/background where composition permits: +2

Score below 3: retain. Score 3–5: level-1 surface translation. Score above 5: consider level-2 narrative-equivalent coastal subtype.

## 4. Scene conversion constraints

### Level 1: surface translation

Retain location function, structure, and layout. Change only palette, finish, lighting response, irrelevant clutter, and depth readability. Examples:

- dark raw wood -> weathered cream-white/pale-blue paint with limited exposed pale wood;
- green utility fixture -> navy/silver only if color is not narratively important;
- dark concrete -> light gray/white concrete with blue safety elements.

### Level 2: equivalent subtype

Retain why the characters are there and what the place enables. Examples:

- generic construction site -> coastal construction site;
- generic old house -> poor weathered coastal house;
- generic city street -> coastal city street;
- generic service alley -> coastal-building service lane.

Do not use level 2 if it would change travel logic, social status, occupation, danger, access, privacy, or cause-and-effect.

## 5. Conflict lint

Resolve before generation:

- night + sunlight;
- photoreal + cartoon/plastic/toy output language;
- deep depth of field + severe background blur;
- blue-led palette + dominant brown/orange surfaces;
- low contrast + hard shadows/high-contrast silhouette;
- bright/transparent + dark/oppressive exposure;
- medium shot + full-body framing instruction;
- static pose + walking pose;
- simple scene + long list of decorative objects;
- “keep reference image” when no generation reference was supplied;
- “keep original position/size” when position/size is not textually defined.

## 6. Narrative checks

For every changed scene, answer internally:

1. What story function does the original place serve?
2. What facts would become false if the place changed?
3. Does the converted place still permit the exact action and prop relationship?
4. Does it preserve wealth/poverty, safety/danger, public/private, and travel continuity?
5. Is visible ocean plausible, or should ocean identity come from materials and light instead?

If any answer fails, reduce the conversion level.

