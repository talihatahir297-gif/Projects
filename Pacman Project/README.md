#  Console-Based Pacman Game

A terminal-based implementation of the classic Pacman arcade game written in Java. This project focuses on object separation, game loops, and matrix-based grid navigation.

##  File Directory & Purpose
* `PacmanGame.java` - Core game engine containing the rendering loop and state management.
* `Pacman.java` - Character logic handling user input and Pacman's coordinates.
* `App.java` - Entry point (`main` method) to boot up the console application.
* `Objects/` - Directory holding supplementary behavioral structures.

## 🛠️ Key Technical Features
* **Matrix Grid Layout:** Uses a 2D array matrix to build custom maze walls, paths, and score points.
* **Movement Logic:** Validates boundaries before updating characters to prevent wall clipping.
* **Compiled Separation:** Pre-compiled bytecode (`.class`) ensures quick immediate execution.

##  How to Run
```bash
javac App.java
java App
