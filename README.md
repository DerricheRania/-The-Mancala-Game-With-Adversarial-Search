# 🧠 Mancala (Awalé) with Adversarial Search & GUI

This project is an intelligent implementation of the **Mancala (Awalé)** game using **adversarial search (Minimax with Alpha-Beta pruning)**, combined with a **graphical user interface (GUI) built with Pygame**.
The goal is to demonstrate how classical AI techniques can be applied to strategic board games.

## 🎯 Features

* ✅ Full Mancala (Awalé) rule implementation (including captures)
* 🤖 AI powered by **Minimax + Alpha-Beta Pruning**
* 🧠 Two heuristics:
  * **H1**: Simple store difference
  * **H2**: Advanced multi-criteria evaluation
* 🧍 Human vs Computer mode
* 🤖 Computer vs Computer (AI vs AI) mode
* 🎮 Interactive **Pygame GUI**
* 🎀 Custom visual theme ("Pink Mancala")
* ⚙️ Configurable search depth and delay

## 🧩 Game Architecture

The project is divided into **two main components**:

```
├── mancala.py   # Game logic + AI (Minimax, heuristics)
├── gui.py       # Pygame graphical interface
```

## 🧠 AI & Adversarial Search

### Minimax with Alpha-Beta Pruning

The AI uses **Minimax** to explore the game tree and choose the optimal move assuming an optimal opponent.
To improve efficiency, **Alpha-Beta pruning** is applied to eliminate branches that cannot affect the final decision.

**Key properties:**

* MAX player → Computer
* MIN player → Human (or second computer)
* Configurable depth (recommended: 4–7)

```python
MinimaxAlphaBetaPruning(game, player, depth, alpha, beta)
```

## 📊 Heuristics

### 🔹 H1 – Simple Heuristic

Evaluates the position using:

```
H1 = Computer_Store - Human_Store
```

✔ Fast
✔ Suitable for Human vs Computer

### 🔹 H2 – Advanced Heuristic (Multi-Criteria)

H2 combines multiple strategic factors:

| Component          | Description                  | Weight |
| ------------------ | ---------------------------- | ------ |
| Store Score        | Difference in captured seeds | 1.0    |
| Potential Captures | Possible captures next move  | 0.5    |
| Tempo Control      | Moves that grant replay      | 0.3    |
| Distribution       | Seed balance across pits     | 0.2    |
| Mobility           | Number of legal moves        | 0.1    |

This heuristic produces **stronger and more human-like play**, especially in AI vs AI matches.

## 🎮 Game Modes

### 1️⃣ Human vs Computer

* Human chooses side (Player 1 or Player 2)
* Computer uses **H1**
* Search depth selectable via GUI
* Legal moves are visually highlighted

### 2️⃣ Computer vs Computer

* AI vs AI simulation
* Player 1 uses **H1**
* Player 2 uses **H2**
* Independent depths for each AI
* Optional delay to observe decision-making

This mode is useful for:

* Comparing heuristics
* Observing strategic behavior
* Studying adversarial search performance

## 🖼️ Graphical Interface (Pygame)

* Interactive pits (mouse-based input)
* Visual highlighting of valid moves
* Animated transitions between turns
* End-game result screen (no flickering)
* Custom color palette and UI design

The GUI is fully synchronized with the game logic and AI decision engine.

## ⚙️ Rules Implemented

* Standard Mancala sowing
* Capture rule:
  * If the last seed lands in an empty pit on the player’s side, the opposite pit is captured
* Game ends when one side is empty
* Remaining seeds are collected automatically

⚠️ **Note**: No extra turn is granted when landing in the store (custom rule choice).

## ▶️ How to Run

### Requirements

```bash
pip install pygame
```

### Run GUI version

```bash
python gui.py
```

### Run console version

```bash
python mancala.py
```

## 📌 Educational Value

This project demonstrates:

* Practical use of **adversarial search**
* Heuristic design and evaluation
* Game tree exploration
* AI vs AI experimentation
* Separation of logic and interface
* Clean object-oriented game modeling

**Author:** *Rania Derriche*


