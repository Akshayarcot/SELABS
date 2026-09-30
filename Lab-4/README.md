# Lab 4: VibeCoding — Real-Time Fruit Slice Game (Repo #41)

**Course:** Software Engineering (SELABS)  
**Student:** A R Akshay Kumar  
**USN:** PES1UG24CS705  
**Assigned Number:** 41  
**Assigned Repository:** [`SETAPESU26/41_fruit-ninja`](https://github.com/SETAPESU26/41_fruit-ninja)  
**Target Repository:** Personal Lab Repo (`SELABS/Lab-4`)  

---

## 1. Executive Summary

This repository directory contains the complete submission deliverables for **Lab 4: VibeCoding**. The objective of this lab is to use an AI pair-programming assistant (Antigravity / Gemini) to diagnose and repair broken code, iteratively prompt to implement all missing features described in the repository's `README.md` in under 3 to 4 prompt attempts, and document the process with before/after demonstrations and exported chat transcripts.

### Deliverables Checklist (Under `Lab-4/`):
- [x] **Deliverable a (Videos):** Guide and placeholders for 10-second before and after screen capture videos located in [`videos/`](./videos/README.md).
- [x] **Deliverable b (Updated Code):** Fully functioning, enhanced Fruit Ninja game codebase in [`41_fruit-ninja/`](./41_fruit-ninja/).
- [x] **Deliverable c (Chat History):** Exported prompt conversation in Markdown ([`chat_history/chat_history.md`](./chat_history/chat_history.md)), Microsoft Word ([`chat_history/chat_history.docx`](./chat_history/chat_history.docx)), and PDF ([`chat_history/chat_history.pdf`](./chat_history/chat_history.pdf)).

---

## 2. Repository #41 Analysis & Broken Code Diagnosis

Upon cloning and inspecting the assigned repository `SETAPESU26/41_fruit-ninja`, three critical structural defects were identified that prevented the application from launching:

| File | Line | Defect Identified | Consequence |
| :--- | :--- | :--- | :--- |
| `main.py` | 32 | Abrupt truncation at `while ru` | `SyntaxError: unexpected EOF while parsing` |
| `game/fruit.py` | 28 | Incomplete method: `contains_point` ends with `# NOTE: only checks a single poi` | `IndentationError: expected an indented block` |
| `game/game_engine.py` | 50 | Incomplete method: `handle_event` ends with `if event.type == pygame.MOUSEMOTION:` | `IndentationError: expected an indented block` |

### Runnable Buggy Demonstration
To demonstrate the buggy behavior for the required 10-second "before" video, a runnable demonstration is provided in [`original_broken_code/runnable_buggy_game.py`](./original_broken_code/runnable_buggy_game.py). It illustrates:
1. **Discrete Point Tunneling:** Fast mouse swipes cross completely through fruit without registering a slice.
2. **Missing Game Over Screen:** Slicing a bomb or running out of lives causes an immediate silent terminal print and sudden exit.
3. **No Replay or Audio:** No difficulty settings, replay loop, or audio feedback.

---

## 3. Iterative Prompt Engineering Process (Under 4 Attempts)

Following the lab objective (*"Learn how to prompt to get the job done in under three to four attempts"*), the entire implementation was achieved in **4 structured prompts**:

```
[Prompt 1: Baseline Architecture & Broken Syntax Fixes]
                       │
                       ▼
[Prompt 2: Task 1 - Continuous Segment-to-Circle Collision Detection]
                       │
                       ▼
[Prompt 3: Task 2 & 3 - Interactive Game Over Screen & Difficulty Replay]
                       │
                       ▼
[Prompt 4: Task 4 - Self-Contained Procedural Sound Synthesis]
```

### Prompt Log Summary:
1. **Prompt 1 (Codebase Repair):** Repaired broken syntax in `main.py`, `fruit.py`, and `game_engine.py`. Established the core 60 FPS Pygame event loop, gravity physics, and basic mouse tracking.
2. **Prompt 2 (Task 1 - Collision Detection):** Replaced discrete point collision with continuous line-segment-to-circle Euclidean projection. Fast swipes now register with 100% reliability regardless of cursor velocity.
3. **Prompt 3 (Tasks 2 & 3 - Game Over & Replay):** Designed a sleek modal Game Over UI displaying final score, high score, and failure reason. Built difficulty options (Easy, Medium, Hard) selectable via interactive buttons or hotkeys.
4. **Prompt 4 (Task 4 - Sound Synthesis):** Built `game/audio.py` using Python's standard `wave` and `struct` modules to procedurally synthesize 16-bit 44.1 kHz PCM audio (`slice.wav`, `bomb.wav`, `game_over.wav`), eliminating external network download dependencies.

---

## 4. Technical Implementation Details

### Task 1: Refined Continuous Collision Detection
- **Mathematical Principle:** Let $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$ be consecutive mouse positions. Let $C = (x_c, y_c)$ be the fruit center with radius $r$.
- We parameterize the blade segment as $P(t) = P_1 + t \cdot \vec{D}$, where $\vec{D} = P_2 - P_1$ and $t \in [0, 1]$.
- The orthogonal projection factor $t$ is calculated and clamped:
  $$t = \text{clamp}\left(\frac{(C - P_1) \cdot \vec{D}}{\|\vec{D}\|^2}, 0, 1\right)$$
- The closest distance $d$ from the circle center to the segment is:
  $$d^2 = \|C - (P_1 + t \vec{D})\|^2$$
- A collision is registered if $d^2 \le r^2$. This guarantees zero tunneling even during ultra-fast swipes.

### Task 2 & Task 3: Game Over Screen & Difficulty Replay
- When `lives <= 0` or a bomb is sliced, `game_over` is triggered.
- An interactive semi-transparent overlay displays:
  - Game Over Title & Specific Defeat Reason (`"Sliced a Bomb!"` or `"Out of Lives!"`)
  - Score comparison (`Final Score` vs `Personal Best`)
  - Difficulty selection buttons:
    - **Easy Mode:** Spawn interval = 70 frames, Bomb chance = 8%, Velocity scale = 0.85x
    - **Medium Mode:** Spawn interval = 52 frames, Bomb chance = 16%, Velocity scale = 1.0x
    - **Hard Mode:** Spawn interval = 36 frames, Bomb chance = 28%, Velocity scale = 1.25x
- Supported Inputs: Mouse clicks on buttons or hotkeys (`1`/`E`, `2`/`M`, `3`/`H`, `R` for restart, `Q`/`ESC` to quit).

### Task 4: Procedural Audio Synthesis
- To ensure portability without network dependencies, `game/audio.py` generates native `.wav` files:
  - **`slice.wav`:** Dynamic frequency slide (1400 Hz down to 400 Hz) mixed with high-passed noise and fast decay ($e^{-18t}$).
  - **`bomb.wav`:** Low-frequency sub-bass drop (120 Hz to 35 Hz) modulated with white noise and explosive rumble ($e^{-6.5t}$).
  - **`game_over.wav`:** Four-note descending harmonic arpeggio (G4 $\rightarrow$ E4 $\rightarrow$ C4 $\rightarrow$ G3).

---

## 5. Directory Structure

```
Lab-4/
├── README.md                              <- Master lab submission report
├── 41_fruit-ninja/                        <- Completed, enhanced game (Deliverable b)
│   ├── main.py                            <- 60 FPS Pygame game loop
│   ├── requirements.txt                   <- Dependencies (pygame>=2.5.0)
│   ├── README.md                          <- Game documentation
│   ├── sounds/                            <- Procedurally generated WAV audio files
│   │   ├── bomb.wav
│   │   ├── game_over.wav
│   │   └── slice.wav
│   └── game/
│       ├── __init__.py
│       ├── audio.py                       <- 16-bit PCM WAV audio synthesizer
│       ├── fruit.py                       <- Fruit & bomb physics, CCD, and visuals
│       └── game_engine.py                 <- Engine logic, HUD, Game Over & difficulty
├── original_broken_code/                  <- Original broken baseline code
│   ├── main.py
│   ├── requirements.txt
│   ├── runnable_buggy_game.py             <- Runnable script for "before" video
│   └── game/
│       ├── fruit.py
│       └── game_engine.py
├── chat_history/                          <- Prompt engineering history (Deliverable c)
│   ├── chat_history.md                    <- Markdown prompt record
│   ├── chat_history.docx                  <- Word export
│   ├── chat_history.pdf                   <- PDF export
│   └── generate_chat_docs.py              <- Document generation script
└── videos/                                <- Video capture folder (Deliverable a)
    └── README.md                          <- Step-by-step recording instructions
```

---

## 6. How to Run & Verify

### 1. Run the Buggy Version (For 10-Second "Before" Video):
```bash
cd /Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab-4/original_broken_code
python3 runnable_buggy_game.py
```

### 2. Run the Completed Version (For 10-Second "After" Video):
```bash
cd /Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab-4/41_fruit-ninja
pip3 install -r requirements.txt
python3 main.py
```

### 3. Git Push Instructions:
```bash
cd /Users/akshaykumar/.gemini/antigravity/scratch/SELABS
git add Lab-4/
git commit -m "Complete Lab 4: VibeCoding for repo 41_fruit-ninja"
git push origin main
```
> **Note:** As specified in Instruction 10, **do not** raise a pull request to `SETAPESU26`. Push exclusively to your personal repository `Akshayarcot/SELABS`.
