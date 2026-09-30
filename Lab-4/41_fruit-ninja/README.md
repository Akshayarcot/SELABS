# Real-Time Fruit Slice Game (41_fruit-ninja)

This project is a Fruit Ninja–style slicing game using **Pygame**. It introduces interactive game design using object-oriented principles, real-time physics simulation, continuous swipe collision detection, and procedural audio synthesis.

---

## What’s Provided
A fully completed and enhanced version of the Fruit Slice game:
- **Fruit & Bomb Dynamics:** Fruits and bombs are launched upward from the bottom in arcing trajectories under gravity.
- **Continuous Blade Collision Detection (Task 1):** Fast swipes reliably intersect fruit hitboxes using line segment-to-point Euclidean projection, eliminating tunneling.
- **Game Over Screen (Task 2):** Stylized modal card displaying final score, high score, defeat reason, and graceful waiting for player input.
- **Replay & Difficulty Selection (Task 3):** Easy, Medium, and Hard difficulty modes with adjustable spawn intervals, bomb chances, and flight speeds.
- **Procedural Sound Feedback (Task 4):** Integrated WAV sound effects for fruit slicing, bomb detonations, and game over, generated procedurally without external asset dependencies.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Pygame

### Setup & Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the game
python main.py
```

---

## Tasks Completed

### Task 1: Refine Collision Detection
- **Issue:** Fast mouse swipes caused discrete point checks to miss fruits between consecutive animation frames.
- **Solution:** Implemented `Fruit.intersects_segment(p1, p2)` which calculates the shortest perpendicular distance from the fruit center to the continuous blade segment traversed during the frame. Quick swipes register 100% reliably.

### Task 2: Implement Game Over Condition
- **Solution:** When lives drop to 0 or a bomb is sliced, the engine pauses gameplay and renders a sleek Game Over overlay showing final score, high score, and game termination reason.

### Task 3: Add Replay Option
- **Solution:** Players can immediately replay by clicking on-screen difficulty buttons or pressing keys:
  - `[1]` or `[E]`: **Easy Mode** (longer spawn intervals, 8% bomb chance, slower speeds)
  - `[2]` or `[M]`: **Medium Mode** (standard arcade balance, 16% bomb chance)
  - `[3]` or `[H]`: **Hard Mode** (rapid spawns, 28% bomb chance, accelerated speeds)
  - `[R]`: Quick Restart current difficulty
  - `[Q]` or `[ESC]`: Quit Game

### Task 4: Add Sound Feedback
- **Solution:** Created `game/audio.py` which procedurally synthesizes 16-bit PCM WAV audio for:
  - Slicing sound (`sounds/slice.wav` - frequency sweep whoosh)
  - Bomb detonation (`sounds/bomb.wav` - low frequency blast with noise)
  - Game Over chime (`sounds/game_over.wav` - descending four-note harmonic arpeggio)
  - Handled with graceful fallback for headless/silent environments.

---

## Folder Structure
```
41_fruit-ninja/
├── main.py
├── requirements.txt
├── README.md
├── sounds/
│   ├── bomb.wav
│   ├── game_over.wav
│   └── slice.wav
└── game/
    ├── __init__.py
    ├── audio.py
    ├── fruit.py
    └── game_engine.py
```
