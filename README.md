# Maths Mastery Map

A visual, animated maths app for a young learner in England. It starts from early number sense and grows to GCSE. It covers the English National Curriculum and borrows the best methods from Japan, Singapore and Finland.

**Main rule:** every objective is taught through an animated model the child watches and then works with his own hands. Nobody has to read the rule out to him.

## Contents

| Path | What it is |
|---|---|
| `docs/01-curriculum-research.md` | Comparison of England, Japan, Singapore, Finland, abacus training and interactive platforms; teaching principles; UK test calendar |
| `docs/02-app-plan.md` | App plan: visual-first rules, animation grammar, scene library, lesson loop, learning engine, architecture, roadmap |
| `curriculum/build_inventory.py` | Source of truth for the **285 learning objectives** (Reception to GCSE Higher) |
| `curriculum/animations.py` | The **30 animated scenes** and a **storyboard (watch + do) for every objective** |
| `curriculum/objectives.json` | Generated data for the app: stages, strands, scenes, objectives |
| `curriculum/objectives.csv` | The same data as a spreadsheet |
| `curriculum/explorer.html` | A browsable view of the inventory |

## Each objective contains

- stage, UK year, age and strand
- the objective in plain words
- **animation**: what the child watches happen
- **interaction**: what the child does on the same model
- scenes used, a visual model, a mastery check and prerequisites
- type: core curriculum, tested in a statutory exam (MTC, SATs, GCSE), or beyond the UK curriculum (from Japan, Singapore or research)

## Rebuild the data

After editing objectives or storyboards:

```bash
cd curriculum && python3 build_inventory.py
```

The script stops with an error if an objective has no storyboard, uses an unknown scene, or lists a prerequisite that doesn't exist.

## View the explorer locally

```bash
cd curriculum && python3 -m http.server 8000
```

Then open http://localhost:8000/explorer.html
