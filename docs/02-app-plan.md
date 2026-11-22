# App plan

## 1. Goal

A tablet app that teaches maths to a 6-year-old in England who understands things by **seeing them happen**. It starts at the foundations he is missing and grows with him to GCSE. It covers everything the English curriculum tests, plus the best methods from Japan and Singapore.

The child should never need someone to read a rule out to him. **Every objective is taught through an animated, touchable model.** The rule appears afterwards, as a label on something he has already seen work.

## 2. Visual-first rules (non-negotiable)

These rules apply to every screen and every lesson. Code review and content review check against them.

1. **The animation is the explanation.** If the concept cannot be seen happening in the motion, the lesson is not finished. "8 + 5 = 13 because you add" is not an explanation. Watching 2 of the 5 slide across to complete the ten is.
2. **Numbers ride on objects.** Symbols appear attached to the thing they describe: the 8 tag sits on the ten-frame and changes as it fills. Symbols never appear alone first.
3. **No reading required up to Stage 2.** Prompts are spoken and shown with icons or demonstration. Text is optional support.
4. **Show, don't tell, when stuck.** After a pause, the hint is a short ghost animation of the next move, not a paragraph.
5. **Wrong answers animate their consequence.** If he says 8 + 5 = 12, the counters are placed and one is visibly left over, or the frame shows a gap. No red cross and no buzzer.
6. **The same model every time.** One ten-frame, one number line, one bar model, with consistent colours (ones, tens and hundreds always use the same colours in every scene). Reuse builds intuition.
7. **The child controls time.** Every demo can be replayed, slowed or stepped through. Steps run at 500-900 ms with a pause between them. Nothing auto-advances while he is thinking.
8. **Fade the picture, don't remove it.** Real model, then simplified sketch, then symbols with the model on tap, then symbols only. The model is always one tap away.
9. **He does it with his hands.** Every *watch* is followed by a *do* on the same model: drag, split, fill, turn, pour.
10. **Calm by default.** No countdown timers until Stage 3 and only as an opt-in game (needed for the Year 4 tables check). No streak guilt and no losing lives.

## 3. The animation grammar

Every storyboard in `curriculum/animations.py` is built from a small set of motions. Children learn to read these motions as maths ideas, so they must look and behave the same in every scene.

| Motion | Maths idea | Example |
|---|---|---|
| **Pulse-count** | counting, one-to-one | each bear pulses as its number tag appears |
| **Lasso** | cardinality, a group as a unit | a ring wraps the set and shows its total |
| **Split** | partitioning, part-whole | 5 counters slide into 2 and 3 on a cherry |
| **Join** | addition, combining | parts slide together into the whole |
| **Fill** | bonds, complements | empty frame spaces glow and fill |
| **Exchange** | place value | 10 ones snap into a rod; a flat breaks into 10 rods |
| **Align** | comparison | two bars line up from the same start |
| **Hop** | counting on and back, number line | arcs hop along the line |
| **Copy / Scale** | multiplication, ratio | a row copies itself 4 times; a bar stretches |
| **Share / Deal** | division | items deal round to plates one by one |
| **Balance** | equality, equations | the beam tips, then levels |
| **Fold / Cut** | fractions | paper folds into equal parts |
| **Turn / Flip / Slide** | geometry, transformations | a shape rotates, leaving a sweep |
| **Level** | mean, redistribution | towers even out |
| **Fade** | abstraction | the model becomes a sketch, then a symbol |

## 4. Scene library

The app is built from **30 reusable scenes**: animated, touchable models defined in `curriculum/animations.py` and exported in `objectives.json` under `scenes`. Each objective names which scenes it uses. Build the scenes once and configure them per lesson.

Build order is set by what the earliest stages need:

| Priority | Scenes | Unlocks |
|---|---|---|
| **P0: prototype** | Ten-frame, Part-whole / cherry, Counters | Make-ten lesson (AS1.5) |
| **P1: foundations** | Dot flash, Number track, Number line, Bead frame, Balance, Story stage | Stages 0-1 |
| **P2** | Base-10 blocks, Hundred square, Bar model, Arrays, Fraction strips, Clock, Money, Measuring lab, Shape lab, Calendar | Stages 1-2 |
| **P3** | Place-value chart, Area model, Chart builder, Angle turner, 3D solids, Coordinate grid, Soroban | Stages 3-6 |
| **P4** | Function machine, Algebra tiles, Graph plotter, Chance lab | Stages 6-11 |

Each scene component takes a **script** (a list of steps built from the motions above) and an **interaction mode** (watch, guided, free, check). It also reports every touch to the engine, so the app can tell *how* he solved something, not just whether he got it right.

## 5. The lesson loop

Each objective becomes one lesson with five phases. Lessons are short and the same shape every time, so he always knows what is coming.

```
 1. WATCH      animated demo on the scene (from the storyboard)
 2. DO         he repeats it on the same model, with ghost-hints if stuck
 3. VARY       3-5 new examples; the model starts to fade
 4. CHECK      mastery task from the inventory; model available on tap
 5. SAY        "show me how you know": he records a drag-demo or voice note
```

A daily **session lasts about 12 minutes**:

1. **Warm-up (2 min).** 2-3 spaced-review items from objectives already mastered.
2. **New learning (6 min).** One lesson (watch, do, vary).
3. **Play (3 min).** A game on the same scene (e.g. Ten-Frame Flash).
4. **Finish (1 min).** A sticker on his map, and one off-screen activity for a parent (e.g. "make 10 with socks").

## 6. Learning engine

### Knowledge graph
`objectives.json` is the graph: 285 nodes, with prerequisite edges (validated by the build script).

### Placement
1. Start with the **12 starting objectives** (NS0.1, NS0.2, NS0.5, AS0.1, AS0.2, NS1.7, AS1.1, NS1.4, AS1.5, AS1.8, NS2.2, NS2.4).
2. Each probe is 2-3 short visual tasks.
3. A failed probe tests its prerequisites; a passed probe tests what depends on it.
4. The result is his **frontier**: the objectives whose prerequisites are all mastered but which he has not mastered yet.

### Mastery states
```
locked -> ready -> learning -> practising -> mastered -> (review due) -> mastered
```
- **Mastered** means the check is passed in 3 sessions on different days, at least 90% correct, with the final pass done without opening the model.
- **Speed** counts only for fact-fluency objectives (bonds, times tables), and only after accuracy is secure.

### Spaced review
Mastered objectives come back after 1, 3, 7, 21 and 60 days. A miss resets that objective to *practising* and adds a short re-watch.

### How he solved it
Scenes log touches, so the engine can spot strategies:
- tapping every counter on a frame means **counting all**;
- answering instantly means **subitising or recall**;
- moving counters one at a time across the ten means he **hasn't seen make-ten yet**.

The engine uses these signals to pick the next demo, and the parent view shows them in plain words.

## 7. Parent view

- **Map.** The knowledge graph lights up as he progresses, with his current frontier highlighted.
- **School alignment.** Where he is against his UK year, and what his class is probably doing this term.
- **Insights.** For example: "Still counts all on ten-frames; working on subitising."
- **Upcoming tests.** The Year 4 tables check and Year 6 SATs, with readiness shown.
- **Off-screen ideas.** One activity per day.

## 8. Technical architecture

| Concern | Choice | Why |
|---|---|---|
| App shell | **React + TypeScript + Vite**, installable **PWA**, responsive from phone to TV | Runs on tablets, phones, laptops and TV browsers from one codebase; can be wrapped with Capacitor for the app stores later |
| Scenes | **SVG** components | Crisp at any size, easy hit-testing, scenes contain tens of objects rather than thousands |
| Animation and gestures | **Motion** (motion.dev, formerly Framer Motion) | Springs, layout animations, drag with snapping and timelines in one library; supports reduced motion |
| 3D solids (Stage 3+) | three.js via react-three-fiber | Rotate, unfold nets |
| State | Zustand | Small and simple |
| Storage | IndexedDB via Dexie, **local-first** | Works offline; the child's data stays on the device |
| Audio | Short recorded voice clips and sound effects (Howler.js) | Spoken prompts so he doesn't have to read; TTS only as fallback |
| Scene development | Storybook | Build and tune each scene and animation script in isolation |
| Tests | Vitest (engine) and Playwright (scene screenshots, lesson flows) | |

### Proposed layout
```
curriculum/          objectives, storyboards, scenes (source of truth)
docs/                research and this plan
app/
  src/scenes/        one folder per scene: component, motions, stories
  src/motion/        shared animation grammar (pulse-count, split, exchange ...)
  src/lessons/       lesson specs, one JSON per objective
  src/engine/        graph, placement, mastery, spacing, strategy detection
  src/screens/       child home map, lesson player, parent view
  public/audio/      voice prompts
```

### Lesson spec (example: AS1.5 make ten)
```json
{
  "id": "AS1.5",
  "scenes": ["frame", "partwhole"],
  "watch": [
    {"do": "show", "frame": "A", "count": 8, "tag": true},
    {"do": "show", "frame": "B", "count": 5, "tag": true},
    {"do": "split", "from": "B", "parts": [2, 3], "via": "cherry"},
    {"do": "move", "count": 2, "from": "B", "to": "A"},
    {"do": "lasso", "frame": "A", "label": "10"},
    {"do": "join", "label": "10 + 3 = 13"}
  ],
  "do": {"mode": "guided", "task": "split second addend, drag part that completes ten"},
  "vary": {"pairs": [[9,4],[7,6],[8,7],[6,5],[9,8]], "fade": ["full", "sketch", "symbols+tap"]},
  "check": {"items": 6, "pass": 0.9, "sessions": 3, "modelAllowed": "tap"}
}
```

## 9. Roadmap

| Milestone | Scope | Exit test |
|---|---|---|
| **M0: Prototype** (1-2 weeks) | Ten-frame, cherry and counter scenes; the full watch/do/vary/check loop for **AS1.5 make ten**; Storybook | He uses it 3 times. Can he explain 9 + 4 by "moving one to make ten"? This is the key test of the visual-first approach. |
| **M1: Foundations** (4-6 weeks) | P1 scenes; all Stage 0 lessons and the first half of Stage 1; placement test; mastery and spacing engine; local storage; parent map v1 | Placement finds his frontier; he completes 2 weeks of daily sessions |
| **M2: Number up to 100** (2-3 months) | P2 scenes; the rest of Stages 1-2 | Steady progress on Stage 1-2 objectives |
| **M3: Stages 3-4** | P3 scenes; times-tables trainer for the Year 4 check | Ready for the tables check |
| **M4: Stages 5-6** | Fractions, ratio and SATs practice mode | Ready for KS2 SATs |
| **M5: Secondary** | P4 scenes; KS3 and GCSE | |
| **TV mode** (after M2) | Remote-control navigation, big-screen watch mode, answer with arrow keys | Usable on a TV from the sofa |

## 10. Trying it with him

After each milestone, sit with him for a session and note:

- Can he **explain using the model** ("I moved one to make ten") rather than just give an answer?
- Where does he **hesitate**? Those are the places where the animation isn't clear enough.
- Does he **ask to replay** demos? That is good. Does he skip them? Then they may be too slow.
- Is he **calm**? Any sign of anxiety means slowing the pace.

## 11. Decisions (agreed with the parent)

1. **Devices: tablet first, phones supported, TV later.**
   - Lessons are designed for a touch tablet (landscape), because dragging and splitting objects is central to how he learns.
   - Every screen must also work on a phone. Phones suit short practice and review; there is less room for two-model scenes, so those stack vertically.
   - TV: for now, mirror the tablet to the TV (AirPlay or Chromecast), with no extra work. A remote-controlled **TV mode** (watch the demos big, answer with arrow keys) is a later milestone, since a remote can't do hands-on dragging.
   - Layouts are fluid from 360 px phones to 1920 px TVs, and touch targets are at least 48 px.
2. **Voice: English only**, using National Curriculum wording (part-whole, exchange, bar model, partition) so the app and school reinforce each other.
3. **Builder: Claude, step by step.** Code is written here in small working pieces and pushed to this repo. The parent tests each piece with his son before the next one starts.
4. **Standard: the National Curriculum is the minimum, and excellence is the goal.**
   - Every core and tested objective must be mastered. Beyond that, each stage has an **excellence layer**: the Japan and Singapore objectives already marked *beyond*, plus "greater depth" tasks (explain, prove, solve unfamiliar problems, find more than one method).
   - A stage counts as complete only when its core objectives are mastered **and** he passes a greater-depth challenge for each strand.
   - School scheme is unknown, so lessons use standard National Curriculum vocabulary, which all the common schemes share.
5. **Art style: clean flat shapes plus one mascot.**
   - All maths objects (counters, blocks, frames, bars) are clear flat shapes with consistent colours, so nothing distracts from the maths.
   - One friendly mascot demonstrates in the *watch* phase, gives hints, and celebrates.

## 12. Risks

- **Too much content, too early.** Keep strictly to M0-M1 until the visual approach is proven with him.
- **Animation polish takes time.** Getting the timing of each motion right matters more than the number of lessons. Tune it in Storybook.
- **Screen time.** Pair each session with an off-screen activity. Physical counters and a real ten-frame on the table help as much as the app.
