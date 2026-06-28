# Neon Snake 🐍

Neon Snake is a retro-modern, arcade-style Snake Game built using Python and Pygame. It features a custom aesthetic with deep dark backgrounds and fluorescent teal, blue, and pink elements.

## Features
- **Fluid Controls**: Use arrow keys or `W`, `A`, `S`, `D` keys to steer.
- **Particle Feedbacks**: Dynamic explosion particles when eating food to give tactile satisfaction.
- **Persistent High Scores**: High scores are stored locally in a `highscore.txt` file and load on game startup.
- **Pause & Resume Menu**: Pause the speed run anytime with `P`.
- **Fault-Tolerant Audio**: Initializes Pygame audio safely to run smoothly on systems without dedicated sound hardware.

## Tech Stack
- **Language**: Python 3.8+
- **Game Engine**: Pygame

## How to Play & Setup

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run the Game
Execute the python script from this directory:
```bash
python main.py
```

### 3. Controls
- **Arrow Keys** or **WASD** to move.
- **P** to Pause / Unpause the game.
- **SPACE** or **ENTER** to Start / Restart (after Game Over).
- **ESC** to quit.
