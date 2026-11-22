# Rethink: making it something a 5-6 year old wants to play

The first pilot (`pilot/make-ten.html`) failed. This document records why, what changes, and the redesigned first lesson. It replaces the lesson design in `02-app-plan.md` wherever the two disagree.

## What went wrong

| Problem | Why it matters for a child who already dislikes maths |
|---|---|
| **Robotic browser voice** | The voice *is* the teacher. A cold voice makes the whole thing feel cold. |
| **Nobody showed him what to do** | Instructions were spoken once and then the screen waited. A 5-year-old needs to *see* the action demonstrated, then copy it. |
| **It looked like a worksheet with animation** | Ten-frames, equations and a "check" with 10 questions is school, which is the thing he already dislikes. |
| **Too long, too much** | 12 minutes and five phases in the first session. |
| **Started too high** | Make-ten assumes he already understands what a number *is*. We should not assume that. |
| **"Check", "questions", right/wrong** | Test language triggers the anxiety we want to remove. |

## New rules (added to the visual-first rules)

1. **Natural, warm voice only.** Every line is pre-recorded with a neural voice (Kokoro, free and open source) or a real human, never browser speech. Lines are short, friendly and specific ("You counted every single one!").
2. **Show, then copy, then do.** Each new action is first done by Dot with a big pointing hand. The child copies it straight away, and the first attempt always succeeds.
3. **A world, not a worksheet.** Maths happens inside small stories: a ladybird needs spots, a picnic needs plates. The child is **helping someone**, not answering questions.
4. **Every tap is delightful.** Things bounce, giggle, sparkle and make a sound when touched. Tapping something is never "wrong", it just responds.
5. **Episodes of 3-5 minutes.** One idea per episode. He should finish wanting more.
6. **No school words.** We never say "maths", "test", "check", "question" or "wrong". Mistakes are funny ("Hee hee, you counted me twice!").
7. **Something grows.** Each episode adds a creature or flower to *his* garden, so progress is something he can see and show.
8. **Sound design matters.** Soft music under scenes, a pop for each count, a short jingle for success. A parent can mute it.
9. **Illustration quality matters.** Characters are properly drawn, with idle animations (blinking, wiggling). Hand-made SVG is fine for testing but final art should use a professional set (e.g. CC0 game art from Kenney.nl) or a commissioned illustrator.

## New starting point: before Stage 0

We now assume he doesn't know what a number is. The first world, **Ladybird Garden**, has five short episodes before any of the existing Stage 0 objectives:

| Episode | Big idea | Inventory link |
|---|---|---|
| **1. How many?** | A number tells us *how many* things there are | new **NS0.0** |
| **2. One, two, three** | Counting words always go in the same order, one word for each thing | NS0.2 (part) |
| **3. Touch and count** | One tap per thing; don't skip, don't double up; the last word is the answer | NS0.2 |
| **4. Spot the spots** | Small amounts (1-3, then up to 5) can be *seen* without counting | NS0.1 |
| **5. Number shapes** | The written number 3 means three things | NS0.4 |

The existing objectives then continue as planned, with every lesson rebuilt to these rules.

## Episode 1 storyboard: "How many?" (about 4 minutes)

**Setting:** a sunny garden with swaying grass, a flower and Dot, a round yellow friend with big eyes, waving.

**1. Hello (30 s): teaches tapping, guaranteed success**
- Dot: *"Hi! I'm Dot. This is my garden. Can you tap me to say hello?"*
- A big pulsing hand taps Dot once to show how.
- He taps → Dot giggles, spins and does a happy bounce. *"Hee hee! That tickles!"*

**2. Visitors arrive (60 s): a number tells you how many**
- A ladybird flies in and lands on a leaf. Dot: *"Ooh, a visitor! One ladybird."* A soft **1** floats above it.
- A second lands. *"Another one! Now there are two ladybirds."* The 1 turns into **2**.
- A third: *"Three ladybirds!"*
- Each time, all the ladybirds wiggle together so the *group* is what the number describes, not the newest ladybird.

**3. Your turn to count (90 s): one tap per ladybird**
- Dot: *"Let's count them together. Watch me first."* The hand taps the first ladybird: it lights up gold and Dot says *"one"*.
- *"Now you!"* He taps the others. Each one hops, turns gold and Dot says the next number.
- Tap a gold one again → it giggles: *"You already counted me!"*
- After the last one, the ladybirds hold hands in a circle and a big **3** appears in the middle: *"Three! There are three ladybirds."*

**4. Help a ladybird (60 s): making an amount**
- A sad ladybird with no spots: *"Can you give me two spots?"*
- He drags spots onto its back. Each spot lands with a pop and a count. When it has two, it smiles and flies a loop.
- If he adds too many, the ladybird laughs: *"Too tickly! Just two please"* and one spot drifts off.

**5. Goodbye (20 s): progress he can see**
- The ladybirds fly to his garden. A new flower blooms there.
- Dot: *"You helped me so much today. See you tomorrow!"*

**What the app learns quietly:** whether he taps each ladybird once in order, whether he skips or double-counts, and how sure he is when making two. That decides whether Episode 2 needs extra practice.

## Next steps

1. Parent chooses Dot's voice (samples: Emma, Isabella, Alice, Lily, George, Fable, Heart).
2. Parent approves this Episode 1 storyboard.
3. Build Episode 1 with recorded voice, sound effects and proper character art, then try it with him.
