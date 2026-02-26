---
title: "Building a Bowling Score Calculator"
date: 2024-02-10
tags: [javascript, node.js, algorithms]
description: "How I built a real-time bowling scorer that handles strikes, spares, and the tricky 10th frame."
status: merged
---

## The Challenge

Bowling scoring looks simple on the surface, but the rules for **strikes**, **spares**, and especially the **10th frame** make it a surprisingly fun algorithmic problem.

A perfect game is 300 points across 10 frames. Each frame allows up to 2 rolls (3 in the 10th frame), and bonus points cascade forward based on strikes and spares.

## Scoring Rules

- **Normal frame**: Sum of two rolls
- **Spare** (knock all 10 down in 2 rolls): 10 + next 1 roll as bonus
- **Strike** (knock all 10 down in 1 roll): 10 + next 2 rolls as bonus
- **10th frame**: If you get a strike or spare, you get bonus rolls (up to 3 total)

## The Core Algorithm

```javascript
function calculateScore(rolls) {
  let score = 0;
  let rollIndex = 0;

  for (let frame = 0; frame < 10; frame++) {
    if (isStrike(rolls, rollIndex)) {
      score += 10 + strikeBonus(rolls, rollIndex);
      rollIndex += 1;
    } else if (isSpare(rolls, rollIndex)) {
      score += 10 + spareBonus(rolls, rollIndex);
      rollIndex += 2;
    } else {
      score += rolls[rollIndex] + rolls[rollIndex + 1];
      rollIndex += 2;
    }
  }

  return score;
}

function isStrike(rolls, i) { return rolls[i] === 10; }
function isSpare(rolls, i) { return rolls[i] + rolls[i + 1] === 10; }
function strikeBonus(rolls, i) { return rolls[i + 1] + rolls[i + 2]; }
function spareBonus(rolls, i) { return rolls[i + 2]; }
```

## What I Learned

The key insight is to track by **roll index** rather than frame number. The frame boundaries shift when strikes occur (only 1 roll per frame instead of 2). This makes the algorithm clean and avoids special-casing.

The project uses Node.js for the backend logic and Bootstrap for a simple UI that updates scores in real-time as you enter each roll.

Check out the [source code on GitHub](https://github.com/OggyMishra/bowling-scorer).
