# 🐍 Snake — Mythic Edition v9

A feature-packed Snake game built with Python and Pygame, far beyond the classic.  
40 stages, 3 bosses, 15 power-ups, dynamic weather, and a full skill system.

---

## ✨ Features

- **40 Stages** across 8 Acts — from tutorial meadows to nightmare labyrinths
- **3 Boss Fights** at stages 5, 10, and 15 — each with unique attack patterns
- **15 Power-ups** including Shield, Ghost, Dash, Time Warp, and more
- **8 Hazard types** — Vortex, Portals, Darkness, Gravity, Electric Fences, and Maze walls
- **Dynamic Weather** — Rain (slippery), Snow (slow), Lightning (screen flash)
- **Skill Shop** — earn skill points from stages, buy passive upgrades
- **Smart Prey** — a fleeing creature that spawns every 4 eats, worth bonus points
- **10 visual themes** — color skins that change as you play
- **Combo system** — chain eats for multiplied score
- **Procedural particles** — sparks, rings, floating text, meteors, and aurora

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W A S D` or Arrow Keys | Move snake |
| `SPACE` / `ENTER` | Confirm / Start / Retry |
| `P` or `ESC` | Pause / Back to menu |
| `S` | Open Skill Shop (in pause or main menu) |
| `F` | Free Play mode (no stage limits) |
| `1–8` | Buy skills (when shop is open) |

---

## 🗺️ Game Modes

### Stage Mode
- 40 stages organized into 8 Acts
- Each stage has a score target to unlock the next
- Complete stages to earn Skill Points

### Free Play
- No target, no pressure — play as long as you want
- Great for practicing combos and power-up usage

---

## ⚔️ Boss Guide

| Stage | Boss | Weakness (Power-up) |
|-------|------|---------------------|
| 5 | Stone Warden | 💥 NUKE |
| 10 | Storm Eye | 🐢 SLOW |
| 15 | Frost King | ❄️ FREEZE |

Collect the matching power-up to damage the boss. Each boss gets faster and angrier as its HP drops.

---

## ⚡ Power-ups

| Name | Effect |
|------|--------|
| DERQA (Shield) | Blocks one hit from wall, boss, or electric fence |
| SIR3A (Speed) | +4 moves/sec for 5 seconds |
| MAGNIT (Magnet) | Food moves toward you when within 4 cells |
| x2 NQT | Doubles points for 9 seconds |
| GHOUL | Walk through stage walls for 5 seconds |
| JLID (Freeze) | Freezes all boss attacks for 4.5 seconds |
| NUKE | Instantly clears all boss warning zones |
| DASH | Teleport 3 cells forward instantly |
| WQFA (Time Warp) | Slows everything else by 65% for 6 seconds |
| KHAYEL (Phase) | Boss loses track of you + walk through your body |
| x3 NQT | Triples points for 8 seconds |
| BRAS (Heal) | Remove 5 body segments and gain bonus points |
| SQOL (Shrink) | Cut body in half + speed boost |

---

## 🧠 Skill Shop

Earn Skill Points by completing stages. Harder stages = more points.

| Skill | Effect | Cost |
|-------|--------|------|
| Daker l-Combo | Combo timer lasts 1 second longer | 3 pts |
| Bda Kbir | Start with length 5 instead of 3 | 3 pts |
| Sabr mezyan | +5 seconds to catch prey | 4 pts |
| Khzzen l-Qwa | All power-ups last 30% longer | 5 pts |
| Zid n-Nqat | +2 bonus points per food eaten | 4 pts |
| Dash Sir3 | DASH power-up appears more often | 5 pts |
| Droa l-Jdar | Shield also blocks stage walls | 6 pts |
| 3in l-Ghoul | See food through dark hazard patches | 5 pts |

---

## 🌦️ Weather System

Weather changes every 45 seconds during gameplay.

| Weather | Effect |
|---------|--------|
| 🌧 Rain | Slight directional slip chance |
| ❄ Snow | −18% movement speed |
| ⚡ Storm | Periodic lightning strikes + screen flash |

---

## 🚀 Installation & Run

### Requirements
- Python 3.8+
- Pygame

### Setup

```bash
# Install Pygame
pip install pygame

# Run the game
python snake.py
```

No other dependencies required.

---

## 🏗️ Project Structure

```
snake.py        # Full game — single file, ~1900 lines
README.md       # This file
```

All game logic, rendering, audio synthesis, and UI are contained in a single Python file.

---

## 🔊 Audio

Sound effects are synthesized at runtime using pure Python — no audio files needed.  
Each power-up, boss hit, level-up, and death has a unique procedurally generated sound.

---

## 🛠️ Tech Stack

- **Python 3** — core language
- **Pygame** — rendering, input, and audio
- **colorsys** — HSV color generation
- **math / random** — particle physics and procedural effects

---

## 👤 Author

**Zakariae Lahrache**  
IT Development Student , Meknes  
[github.com/2akariae](https://github.com/2akariae)

---

