# Continuity and variation contract

## 1. Whole-script reasoning

Never edit isolated shots first. Read the story and every storyboard prompt, then construct:

- a location table;
- an entity/prop table;
- a temporal sequence;
- a list of locked narrative facts;
- one visual DNA per output version.

Words such as “同一间”, repeated activities, shared windows/furniture and story adjacency are evidence that shots belong to one location. Do not merge locations merely because both are bedrooms or living rooms.

## 2. Attribute status

Classify each candidate attribute:

- **LOCK**: affects plot, action, recognition, social condition, time, camera intent or downstream motion.
- **VERSION-LOCK**: may vary between outputs but must remain identical at every recurrence inside one output.
- **SHOT-SAFE**: nonrecurring background detail with no story or continuity consequence.

When uncertain, choose LOCK.

Example: if a bed is merely environmental, V1 may use an iron bed and V2 a wooden bed. Within V1, every recurrence must use the same iron design, finish, bedding and relevant placement. If a later action depends on striking or gripping metal, material becomes LOCK across all versions.

## 3. Preserve

Preserve unless the user explicitly authorizes otherwise:

- plot events, causality and emotional arc;
- role identity, body, face, clothing and relationships;
- action, pose, gaze, expression and interaction;
- functional prop identity, count, ownership, state and contact;
- location function and socioeconomic meaning;
- shot size, angle, framing purpose and motion clearance;
- day/night, season, weather events and light direction when narratively established;
- source visual style and quality requirements.

## 4. Safe difference hierarchy

Prefer high-impact differences:

1. background architecture and spatial silhouette;
2. recurring nonfunctional furniture design;
3. wall/floor/window/door material family;
4. secondary palette and its spatial distribution;
5. landscape, vegetation and distant landmarks;
6. lighting fixture design and nonfunctional decoration.

Use these variables by replacement, not accumulation, and stay within the scene-detail budget in `scene-composition-contract.md`. Tiny decorative swaps or simple hue changes are insufficient as the sole distinction. Do not clutter a scene to manufacture differences.

## 5. Version DNA

Define each version with a compact specification, for example:

```text
Home: white weathered farmhouse
Structure: rectangular white-grid windows
Materials: pale oak + black iron
Secondary palette: sage green + cream
Exterior anchor: one mature oak
```

Use mutually distinguishable combinations. Avoid combining arbitrary features that contradict the inherited style or characters' means.

## 6. Continuity audit

Before delivery, audit every repeated scene/entity for:

- material;
- color;
- shape/design;
- window and door type;
- wall and floor finish;
- furniture and bedding;
- persistent decoration;
- outdoor view;
- prop state and temporal changes.

Allow changes only when the story itself changes the object or location.
