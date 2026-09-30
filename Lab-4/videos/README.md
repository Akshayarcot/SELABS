# Lab 4 Video Submission Guidelines

According to the Lab 4 instructions:
- **Deliverable a:** Videos (before and after)
- **Duration:** 10 seconds each

---

## 1. Video 1: "Before" Video (`before_changes.mp4` / `.mov`)
- **Purpose:** Demonstrate the broken behavior of the assigned repository before applying fixes.
- **How to run the buggy demonstration:**
  ```bash
  cd /Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab-4/original_broken_code
  python3 runnable_buggy_game.py
  ```
- **What to show in the 10 seconds:**
  1. Make quick, fast swipes across fruits — demonstrate that rapid swipes pass right through fruits without slicing them (tunneling bug).
  2. Let lives run out or hit a bomb — show that the game abruptly exits to terminal without an interactive Game Over screen or sound.

---

## 2. Video 2: "After" Video (`after_changes.mp4` / `.mov`)
- **Purpose:** Demonstrate the fully completed and enhanced game with all README tasks working.
- **How to run the updated game:**
  ```bash
  cd /Users/akshaykumar/.gemini/antigravity/scratch/SELABS/Lab-4/41_fruit-ninja
  python3 main.py
  ```
- **What to show in the 10 seconds:**
  1. Slice fruits with fast, energetic swipes — demonstrate that fast continuous swipes reliably slice every fruit into two halves with juice particles (Task 1).
  2. Notice the sound effects playing for slicing and bomb detonation (Task 4).
  3. Show the Game Over screen with final score and reason (Task 2).
  4. Select a difficulty (e.g. Easy / Medium / Hard) from the replay menu to show the replay functionality (Task 3).

---

## 3. How to Record on macOS
1. Press `Cmd + Shift + 5` to open the built-in macOS Screen Recorder.
2. Select "Record Selected Portion" and draw a box around the Pygame game window (700x600).
3. Under "Options", ensure your microphone/audio is enabled if you want to capture the synthesized sound effects.
4. Click **Record**, interact with the game for 10 seconds, then press the Stop button in the top menu bar.
5. Save the recordings in this `videos/` folder as:
   - `before_changes.mp4` (or `.mov`)
   - `after_changes.mp4` (or `.mov`)
