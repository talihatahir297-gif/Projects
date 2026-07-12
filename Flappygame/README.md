###  Flappy Game

```markdown
#  2D Flappy Bird Replica

An interactive 2D GUI game built using Python and the **Pygame** library. It features real-time gravity physics, procedural obstacle spawning, and persistent high-score tracking.

## File Directory & Purpose
* `flappygame.py` - Core game loop running frame updates, rendering pipes, and managing physics.
* `highscore.txt` - File-handling system storing the highest score achieved.
* `test.py` - Testing script used to debug collision masks and mechanics.

## 🛠️ Key Technical Features
* **File I/O Persistence:** Reads and writes to `highscore.txt` dynamically to maintain local scoreboard history.
* **Collision Detection:** Utilizes bounding boxes to monitor pixel/rect intersections between the bird and moving pipes.
* **Physics Simulation:** Mimics arcade mechanics with incremental downward gravity forces counteracted by jump/flap events.

## How to Run
```bash
pip install pygame
python flappygame.py
