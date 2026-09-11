---
name: create-original-animal-storyboard
description: Create original one-minute anthropomorphic-animal TikTok stories and complete TKDRAMA-compatible Chinese .txt storyboards. Use for 原创剧本、原创故事 or 原创分镜 when the user wants a new story rather than a source-preserving conversion. Design independent 6-second image-to-video clips that can be trimmed to 3–4 seconds and hard-cut without action matching. Do not use for scene-only variants or visual-style conversion.
---

# Original Animal Storyboard Creation

## Objective

Create one genuinely new, low-comprehension-cost animal-person story and a production-ready TKDRAMA `.txt` storyboard. Use **naive visual causality**: events must be instantly understandable, but the story does not need realistic planning, responsible spending, procedural completeness or a socially meaningful resolution. Narrative comprehension comes before shot count, visual spectacle and production convenience. Under the user's production model, one generated clip is normally trimmed to about 3 seconds, so a one-minute story defaults to 20 independent shots. Use another count only when the user supplies a different runtime or verified editing cadence.

Each shot is generated as a separate 6-second image-to-video clip, trimmed to its best 3–4 seconds, then hard-cut to the next clip. Preserve semantic continuity, character identity and recurring-prop identity; never require cinematic action, position or camera matching between clips.

## Required references

Read all three before creating the story:

- [viral-story-contract.md](references/viral-story-contract.md): story selection, originality, emotion, escalation and payoff rules.
- [independent-shot-contract.md](references/independent-shot-contract.md): content-block design and the independent-clip production gate.
- [tkdrama-output-contract.md](references/tkdrama-output-contract.md): output structure, prompt fields, naming and validation.

## Workflow

1. Lock any user-specified characters, duration, style, audience, setting and forbidden content. Do not invent asset traits the user did not provide.
2. Build and approve a story card before deciding how to fill the shot count:
   - one-frame-readable opening hook;
   - one central audience promise or question;
   - one simple goal or rule;
   - the narrative role of any user-required high-salience element such as gold, wealth, a creature or a vehicle;
   - a short `because -> therefore` causal chain whose events each create a new decision, consequence, relationship, conflict or resolved fact;
   - primary emotional engine;
   - 5–9 content blocks;
   - one-frame-readable payoff that resolves the opening promise.
3. Distinguish the **story engine** from a **tested visual carrier**. A user statement such as “gold scenes perform well” requires meaningful gold presence; it does not imply repeated gold production, mandatory quantity growth, cash exchange, luxury consumption or a largest-possible gold climax. Give the element only the role earned by the story.
4. Separate **minimum causal comprehension** from **realistic closure**. Preserve the first so the viewer knows why the next event happens; reject the second when it adds errands after the payoff. Familiar cartoon associations such as `gold -> valuable -> cash/wealth/celebration` may be accepted without showing how every purchase restores the household, job or business.
5. Apply the originality gate in `viral-story-contract.md`. Reuse proven audience mechanisms, not an existing plot with nouns replaced.
6. Reject or redesign premises whose main appeal depends on real-time spatial action, precise choreography, dialogue, hidden rules or extended setup.
7. Build a content-block ledger using viewer-level promises and narrative conclusions, not production steps. Changing tools, poses, locations, quantities or spectacle does not create a new block when the cause, goal and consequence remain unchanged.
8. Count only shots that pass both production independence and editorial independence. Before the payoff, editorial value normally requires new story information. A limited **payoff runway** may show distinct anticipation-building facets such as reveal, disbelief and exchange before the first unmistakable fulfillment image. If the premise otherwise cannot support the requested runtime, reject or enrich it before the payoff; never pad it with making, travel, connector steps, arbitrary scale increases or a post-fulfillment epilogue.
9. Allocate 20 shots across the validated blocks for the default one-minute deliverable. A same-result making, training, care or repair process normally receives 1–2 consecutive shots total, including its progress montage; use more only when the audience receives a genuinely different narrative conclusion rather than another operation or a larger-looking version of the same result. If fewer than 20 valid shots exist, enrich unresolved story stages before the terminal payoff; do not rely on unusually long edits or add post-payoff shots.
10. Apply the independent-shot gate to every shot. Each 6-second clip must support a stable simple action, permit arbitrary trimming to 3–4 seconds without constraining the next clip, and justify its own 3–4 seconds through new story information, rising payoff anticipation or the terminal fulfillment image.
11. Use an **expectation-delivery stop rule**. A compact payoff runway may contain 2–4 beats such as treasure reveal, disbelief, appraisal and cash handoff, but the first frame that fully delivers the audience's expected result is terminal. Wealth celebration, completed reunion, decisive punishment or the promised luxury/status image must be the final shot. Never add another pleasure, luxury image, explanation or practical subgoal after full delivery merely because it is attractive.
12. Write the complete TKDRAMA file with one consistent visual style, simple scenes, dominant subjects and full image prompts. Keep story prose diegetic: the story overview states only what happens inside the story and never contains production or audience instructions such as “故事立即结束”, “观众预期”, “本镜”, “硬切” or “为了完播”. Keep video-prompt blocks empty unless the user supplies or requests video prompts.
13. Save as `<title>-原创版-1-剧本.txt` unless the user specifies a name or destination.
14. Validate structure:

   ```bash
   python3 scripts/validate_tkdrama_story.py OUTPUT.txt --min-shots 20 --max-shots 20
   ```

15. Manually audit naive visual causality, promise consistency, production independence, editorial independence, thumbnail-strip variety, role/prop continuity, visual beauty, payoff strength and whether the ending stops at peak audience satisfaction. Correct and revalidate before delivery.

## Decision priority

1. Immediate comprehension, naive visual causality and one stable audience promise.
2. Each shot's new narrative conclusion or rising reason to keep waiting for the promised result.
3. Independent clip production and hard-cut editability.
4. Strong payoff that follows the established cartoon rule or conflict without requiring realistic closure.
5. Character, prop and socioeconomic continuity.
6. Visual novelty, beauty and generation reliability.
7. Decorative complexity.

## Hard boundaries

- Do not begin with lore, explanations, ceremonies, delayed triggers or “第二天才发生”的 setup when the core premise can appear immediately.
- Do not pad duration by splitting one physical action into approach, reach, throw, catch, pull and climb shots.
- Do not pad duration by splitting one result into design, cut, hammer, weld, assemble and inspect shots. Different tools are not different content blocks when they build the same object for the same purpose.
- Do not make adjacent clips depend on matching trajectories, exact left/right positions, damage progression, hand placement, entrances, exits or the previous clip's final frame.
- Do not use shot/reverse-shot coverage, reaction close-ups or environmental establishing shots merely because films use them. Every shot must carry independent story or viewing value.
- Do not demand realism beyond instant viewer comprehension. Repair obvious rule contradictions and continuity errors, but do not add explanatory errands, transactions or dialogue that slow the story.
- Do not turn the ending into a responsible-life plan. After gold, cash, rescue, transformation, victory or punishment has delivered the promised satisfaction, do not add `purchase -> practical use -> proof that life improved` merely to make the story feel complete.
- Do not force rewards to solve every opening hardship item by item. A poor character receiving visible wealth may end by celebrating or enjoying it; the audience does not need to see debts paid, tools replaced, work resumed or income stabilized unless one of those was the explicit opening promise.
- Do not append an epilogue after the first full-delivery image. If cash-and-gold celebration already makes “they are rich” unmistakable, a later mansion, sports car, yacht, feast or vacation is weaker post-payoff content and must be removed. If a yacht or another luxury object is the opening promise, make that object the terminal fulfillment instead of showing an earlier full wealth celebration.
- Do not leak analysis or production control language into story prose. “故事立即结束”, “预期已经交付”, “为了提升完播率” and similar statements belong in internal review or notes, never in `故事概述` or diegetic descriptions.
- Do not turn a successful visual element into a mechanical plot template. Gold, cash, luxury, size, destruction or another tested image may remain constant, appear only at turning points or serve as a character/prop; it does not need to grow repeatedly.
- Do not count a larger pile, wider scene, more expensive object or more numerous crowd as narrative progress unless it changes a character's decision, goal, conflict, relationship, consequence or final resolution.
- A compact payoff runway is not post-payoff permission. Gold reveal, shocked appraisal and cash handoff may lead toward a terminal celebration because the viewer is still waiting for full fulfillment. Once celebration, reunion, victory or punishment unmistakably resolves the promise, stop immediately.
- Do not switch the audience promise late. Friendship, sacrifice, morality, romance, revenge, transformation or punishment must be established as a central thread before the midpoint; never attach one near the ending merely to create emotion or a climax.
- Do not expand a simple magical discovery into sourcing, scaling, manufacturing, sales, branding or business-growth steps unless running that business is the story's central promise.
- Do not create originality by replacing only fruit, color, species, metal, clothing or another carrier in an existing plot.
- Do not weaken the payoff with lower-value substitutions or enlarge it by changing to an unrelated stimulation type such as disaster, violence or city destruction.
- Do not overfill scenes. Keep one dominant action, one dominant emotion and usually one functional prop group per shot.
- Do not relabel one repeated process as several blocks to bypass the shot budget. Define blocks by the audience's current question or expected result.
- Keep most character-led shots as flat, readable medium shots with the subject visually dominant. Use wider views only when scale, travel, transformation or environment is itself the story information.

## Quality gate

Deliver only when:

- the hook is visible within shots 1–2 and the core goal or rule is understood without dialogue;
- the story can be retold as a short `because -> therefore` chain rather than an “and then” list;
- any required high-salience visual element has one explicit narrative role and is not mistaken for the story engine;
- the story contains 5–9 meaningful content blocks rather than one continuous action stretched across the runtime;
- every shot passes independent understanding, arbitrary trimming, hard-cut, simple-motion and editorial-value tests;
- before the payoff, every shot produces a new decision, consequence, relationship change, conflict, resolved fact or rising payoff expectation; reveal, reaction and exchange may form a short runway, but the first full-delivery image is the final shot;
- no consecutive run can be summarized as “the character keeps making/training/repairing the same thing” with only the tool or pose changing;
- no more than two consecutive shots share the same main subject, location, goal and core object unless each shot delivers a visibly different result, beneficiary or reward;
- every adjacent 1–3 shots refresh at least one meaningful dimension: action, prop, task, relationship, emotion, setting stage, progress, reveal or reward;
- repeated settings are justified by a rule test, effort/care/build montage, chase/comedy escalation, survival task, reaction contrast or reward loop;
- character and recurring-prop identities remain stable without requiring exact spatial matching;
- the climax is stronger than the setup, readable in one frame and stays within the story's established stimulation type;
- the ending resolves the opening promise and does not introduce a new moral, relationship or transformation theme;
- the ending uses only the minimum intuitive link needed to understand the payoff and stops before realistic aftercare, financial planning or lifestyle proof begins;
- no shot appears after the first image that unmistakably fulfills the central audience expectation;
- the file passes structural validation and retains complete TKDRAMA markers and prompt fields.
- the default one-minute deliverable has exactly 20 valid shots, with no runtime padding after the terminal payoff;
- the story overview contains only in-world events and no author, editing, audience or completion instructions.
