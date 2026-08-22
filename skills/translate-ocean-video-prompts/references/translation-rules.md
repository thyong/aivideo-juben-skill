# Narrative-first translation rules

## 1. Build scene groups first

Group shots that share a location and time before rewriting any prompt. Define for each group:

- narrative function and socioeconomic condition;
- indoor/outdoor, time, weather, and continuity;
- fixed architecture, materials, layout, props, view direction, and light direction;
- recurring asset identity, color, material, shape, damage state, and movement between shots;
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

## 5. Scene simplification

Simple visual storytelling benefits from a clean scene, but simplification is subordinate to narrative truth.

- Remove an object when it is neither used nor needed to explain the world, action, continuity, socioeconomic state, danger, or cause-and-effect.
- Preserve environmental evidence that explains a functional prop or action, such as a sparse coastal grove for gathered firewood or a worksite for construction tools.
- Remove background elements that contradict the premise, such as an easily reachable boat in a story about being stranded and awaiting rescue.
- Do not beautify poverty into wealth, danger into safety, a work area into leisure, or an isolated location into a populated one.
- Prefer one or two meaningful environmental cues over a decorative list. Do not add coastal decoration merely to fill space.

## 6. Camera, focus, and depth of field

Depth of field belongs in `镜头`, not in the fixed `画面风格`. Preserve the source shot size, angle, composition, character placement, and movement direction, then make a separate focal decision for every shot.

### Define the focus set first

List every element that must remain clear for the frame to communicate its event. This may include multiple faces, an interaction, a functional prop, a clue, a threat, an injury, a destination, a vehicle, or environmental evidence. Every member of this focus set must remain clear even when split across foreground, middle ground, and background.

### Choose depth from narrative geometry

- **Shallow**: one dominant subject or a compact face/action/prop cluster on nearly the same plane. Use for intimate emotion, feeding, wiping, holding, or close manual actions. Keep the relevant hands and prop sharp with the face.
- **Medium-shallow**: two interacting characters or a compact group whose faces, eye-lines, and contact action must all remain clear while the setting is secondary.
- **Medium**: walking, running, falling, pushing, driving, rescue interactions, pursuit, or a subject plus critical prop across adjacent planes. Preserve movement space and keep the action chain clear.
- **Medium-deep**: cause-and-effect depends on separated planes or recognizable environment, such as subject + SOS + aircraft, pursuer + victim, character + damaged parachute + landing area, or multiple moving vehicles. Keep the background readable with lower contrast and saturation rather than severe blur.

Use deep focus only when the story truly requires the whole space equally sharp. Never choose shallow depth solely to “make the subject stand out” if it hides a required threat, prop, clue, destination, helper, or consequence.

### Subject prominence in vertical 9:16

Treat these as starting ranges, not rigid geometry:

- ordinary character-led medium or medium-close shots: subject or interacting group normally occupies about 60–70% of frame height;
- shots that must connect a character with a separated environmental element: normally about 50–60%;
- vehicle or object spectacle shots: main object normally about 60–70% while preserving functional clearance.

Reduce these ranges only when the locked composition or a critical full object cannot otherwise fit. Do not make characters small merely to display a prettier or more detailed background. In multi-character shots, measure the visual group rather than each individual.

### Motion space and optical wording

- Reserve space along the established direction for walking, running, falling, sailing, driving, flying, pushing, or approaching.
- Keep static interaction shots static; do not add travel direction where none exists.
- Describe which elements are clear and which background layers are only softened. “Background recognizable at lower contrast” is often better than generic “background blur.”
- Allow physical motion blur only on actually fast-moving parts, such as rotor blades, wheels, rain, or splashes; keep the identity-bearing body of the subject sharp.

## 7. Cross-shot continuity lint

Audit the complete story after drafting all replacements:

- adjacent shots in one uninterrupted event must not jump between day, dusk, and night;
- weather and wet/dry ground must follow plausible progression;
- recurring homes, rooms, streets, vehicles, costumes, tools, containers, beds, parachutes, aircraft, and other assets must retain defined color, material, shape, architecture, and damage state;
- the same location must not gain or lose a story-significant access route, population, safety condition, or rescue opportunity without explanation;
- when the source contradicts itself, choose the least invasive value supported by the surrounding sequence and record any required `描述` or `主体角色` correction in the summary.

## 8. Conflict lint

Resolve before generation:

- night + sunlight;
- photoreal + cartoon/plastic/toy output language;
- deep depth of field + severe background blur;
- shallow depth of field + narrative-critical subjects on separated planes;
- blurred foreground/background + critical prop, clue, threat, injury, helper, destination, or consequence placed there;
- blue-led palette + dominant brown/orange surfaces;
- low contrast + hard shadows/high-contrast silhouette;
- bright/transparent + dark/oppressive exposure;
- medium shot + full-body framing instruction;
- static pose + walking pose;
- moving subject + no usable space in the established movement direction;
- simple scene + long list of decorative objects;
- “keep reference image” when no generation reference was supplied;
- “keep original position/size” when position/size is not textually defined.

## 9. Narrative checks

For every changed scene, answer internally:

1. What story function does the original place serve?
2. What facts would become false if the place changed?
3. Does the converted place still permit the exact action and prop relationship?
4. Does it preserve wealth/poverty, safety/danger, public/private, and travel continuity?
5. Is visible ocean plausible, or should ocean identity come from materials and light instead?

If any answer fails, reduce the conversion level.
