# 🌌 N-Body Orbit Simulation

A modular, extensible orbital simulation engine—run it as a **classic Python/matplotlib animation** or as a **modern interactive web app** powered by Flask + HTML/JS.  
**Both interfaces use the same NumPy-based simulation core for scientific consistency and maintainability.**

---

## 🚀 Overview

Simulate the motion of celestial bodies (Sun, planets, etc.) using a semi-implicit Euler method and real astronomical data, loaded from `bodies.json`.  
- **Two interfaces** from the same engine:
  - 🖥️ Desktop: Matplotlib animation
  - 🌐 Web: Flask API backend + HTML/JS/CSS canvas frontend
- **Core logic is shared:** All interfaces call the same simulation code.

---

## ✨ Features

- Accurate N-body simulation (NumPy + OOP, semi-implicit Euler)
- Select/deselect bodies with intuitive UI (checklist or cards)
- Real-time animation with pause/play, zoom, and orbital trails
- Fully responsive web design
- Modular: Easily add or edit bodies in `bodies.json`
- **Consistent scientific results on both desktop and web**

---

## 🏗️ Architecture

[bodies.json]
|
+----------------------+
| simulation.py | <-- Shared simulation engine (NumPy, OOP)
+----------------------+
| |
[matplotlib] [Flask API backend]
|
[JS/HTML5 Canvas frontend]


Same simulation core powers both UI options.

---

## ⚡ Quickstart

### 1. Clone & Install

`git clone <your_repo_url>
cd <repo>
pip install -r requirements.txt`

### 2. Run Desktop Version (matplotlib)
`python sim.py`

### 3. Run Web Version (Flask + Web UI)
`python app.py`
or click [here](https://weborbitsim.onrender.com)

---

## 🛠️ Editing or Adding Bodies

All celestial body info is stored in [`bodies.json`](./bodies.json).  
Add, remove, or edit planets/bodies—changes are reflected immediately in both UI modes.

---


## 🌀 Project Evolution

Started as a [matplotlib desktop animation](https://github.com/Root3141/Orbit),  
now featuring a web app for modern, interactive exploration.  
**Both interfaces use the same simulation code!**

---

## ❓ Why Two Interfaces?

- **Scientific repeatability:** Guarantee consistency by sharing the simulation code
- **User reach:** Serve both notebook/script users (scientists, tinkerers) and general audiences (browser UI)
- **Showcase growth:** Demonstrate full-stack and desktop skills in one project

---

## 👤 Credits

Developed by [Aaryan Aaloke](https://github.com/Root3141).  
Open-source, MIT licensed.

---

## 📜 License

MIT
