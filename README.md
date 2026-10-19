# 🟩 Wordle Clone

A clean, minimalist word-guessing game built with Python, `ttkbootstrap`, and SQLite.

---

## About

The goal is to guess a hidden 5-letter word in 6 attempts or fewer. Each guess provides color-coded feedback:

- 🟩 **Green**: Letter is correct and in the right position.
- 🟨 **Yellow**: Letter is in the word, but in the wrong position.
- ⬛ **Gray**: Letter is not in the word.

---

## Quick Start

1. **Prerequisites:**
   - Python 3.10+
   - `ttkbootstrap` package

2. **Install Dependencies:**
   ```bash
   pip install ttkbootstrap

3. **Run the game:**
   ```bash
   python gui.py

## 🛠️ Built With
- Python 3 – Core application and game logic (GameLogic.py)
- Tkinter / ttkbootstrap – Graphical user interface (gui.py)
- SQLite – Score tracking & history database (DB.py)
