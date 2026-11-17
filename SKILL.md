---
name: learning-map
description: Use when the user wants a 역량지도, skill map, competency map, or clickable mindmap of what they have learned on a topic, or when a socratic-tutor session should record which concepts the learner now knows. Triggers - "역량지도", "배운 거 마인드맵으로", "skill map 시각화", "learning map", "update my map".
---

# Learning Map

One `.map.md` file is the source of truth for a learner's map of a topic. `scripts/render.py` turns it into one offline `.html` mindmap: click a node and its sub-concepts pop out, click a concept to see its description. Learned = green, not yet known = gray.

In the HTML: wheel or trackpad pinch zooms toward the cursor, drag the background to pan, bottom-right buttons zoom in/out, fit to screen (keys `+` `-` `0`), and ⤓ downloads the whole map, every node expanded, as a 2x PNG.

## File format (`<TOPIC>.map.md`)

```markdown
---
title: "Physical AI"
learner: Peter
updated: 2026-11-18
---
# Physical AI

## 감지→판단→행동 루프 [2/5]
- [x] 오픈 루프의 한계 — 딱 한 번 보고 움직이면, 컵이 옮겨져도 모른 채 허공을 잡는다.
- [ ] 지연과 연산의 트레이드오프
  - [ ] 큰 모델은 느리다
```

| Syntax | Meaning |
|---|---|
| `# X` | root (map title) |
| `## X [n/5]` | branch = one subskill; `[n/5]` is the socratic-tutor level (optional) |
| `- [x] label — desc` | learned concept, green; `desc` shows on click |
| `- [ ] label` | not yet known, gray |
| 2-space indent | child concept (any depth) |

Separator between label and description: ` — ` (also accepts ` -- ` or ` :: `).

## Rules for `[x]`

Mark `[x]` only when the learner showed it themselves: they answered it, predicted it, or explained it without being handed the answer (same bar as socratic-tutor levels). A concept you only named or explained stays `[ ]`.

The description is one sentence, in the learner's own reasoning, plain words. Unknown concepts need no description.

## Workflow

1. Map file lives at `~/.buzz/RESEARCH/learning-maps/<TOPIC>.map.md` unless the user names another place. Create it with every subskill as a `##` branch and the concepts under each, all `[ ]` at first.
2. After each tutoring check the learner passes: flip that concept to `[x]`, write the description, update `[n/5]` and `updated:`.
3. Render:
   ```bash
   python3 ~/.claude/skills/learning-map/scripts/render.py ~/.buzz/RESEARCH/learning-maps/<TOPIC>.map.md
   ```
   Writes `<TOPIC>.map.html` next to the md (or `-o OUT.html`). Prints `learned/total`.
4. Open it: `open -a "ego lite" <file>.html`. Also works as a plain file in VS Code (Live Preview / Open in browser) and in Orca's browser. No server, no CDN, no install.

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing the `.html` by hand | Edit the `.md`, re-render. HTML is a build output. |
| Concept line missing `[ ]` / `[x]` | Every concept needs a checkbox, or the parser skips it. |
| `- [x]` before any `##` | Concepts must sit under a branch. |
| Marking `[x]` right after you explained it | Wait for an unprompted check the learner passes. |
| Tabs and spaces mixed in indents | Use 2 spaces per level. |
| PNG button does nothing in VS Code's built-in preview | Webviews can block downloads. Open the file in a real browser for export. |
