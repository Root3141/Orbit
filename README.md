# Orbit2.0 🌌

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)

A modular, minimalistic, and physically accurate orbital simulator.  
Experience as a modern interactive web app or classic desktop Python/matplotlib animation. Powered by symplectic Velocity-Verlet integration, Flask, and vanilla JS.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quickstart](#quickstart)
- [Editing or Adding Bodies](#editing-or-adding-bodies)
- [What's New in 2.0](#whats-new-in-20)
- [Design Philosophy](#design-philosophy)
- [Educational Value](#educational-value)
- [Future Work](#future-work)
- [Screenshots / GIFs](#screenshots--gifs)
- [Why Two Interfaces?](#why-two-interfaces)
- [License](#license)
- [Credits](#credits)

---

## Overview

Orbit2.0 simulates planetary and celestial motion using **energy-conserving Velocity-Verlet integration** for long-term orbital stability.

**Experience it as:**

- 🖥️ **Desktop:** Python + Matplotlib animation – for research, teaching, or offline demos.
- 🌐 **Web:** Flask backend + HTML/JS/CSS frontend – modern interactive simulation.

Both interfaces use the **same NumPy-based simulation core** for scientific consistency.

---

## Features

### Physics Engine

- Symplectic **Velocity-Verlet integration** (replaces semi-implicit Euler), numerically stable for long-term orbits.
- Planetary/body data stored in **editable `bodies.json`**.

### Web / UI

- Dynamic body selection via interactive cards.
- Real-time Canvas animation with **buffering and interpolation**.
- **Server-Sent Events (SSE)** for low-latency updates.
- Play/Pause toggle, zoom in/out, configurable trails, starry background, and auto pause on tab change.

### Backend & Architecture

- Modular OOP physics core (**simulation.py**).
- Flask backend serves snapshots to web; Matplotlib mode remains fully supported.

### Other

- Fully responsive design for desktop & mobile.
- Clean separation of **code, data, and UI** for maintainability.
- Open-source.

---

## Quickstart

### Clone & Install

```
git clone https://github.com/Root3141/Orbit.git
cd Orbit
pip install -r requirements.txt
```

### Run Web App

```
python app.py
```

Open http://localhost:5000
or view the live demo [here](https://weborbitsim.onrender.com/)↗.

### Desktop (Matplotlib) Mode

```
python sim.py
```

## Architecture

```
   [bodies.json]
        |
+---------------------+
|   simulation.py     |  <-- Shared OOP simulation engine (NumPy + Verlet)
+---------------------+
      |            |
[Matplotlib]  [Flask backend/API]
                   |
             [HTML/JS frontend]
```

## Editing or Adding Bodies

All celestial object data lives in **`bodies.json`**.  
Add, remove, or edit entries - changes are reflected instantly in both interfaces.

---

## What's New in 2.0

| Feature       | v1.0                | v2.0 (Current)                              |
| ------------- | ------------------- | ------------------------------------------- |
| Integration   | Semi-implicit Euler | Velocity-Verlet (energy-conserving, stable) |
| Data          | Hardcoded           | Fully editable JSON file                    |
| Visualization | Matplotlib only     | Web (Canvas/SSE) + Matplotlib               |
| Architecture  | Flat script         | Modular, shared core, clean separation      |
| UI/UX         | Static plots        | Modern, animated, interactive web UI        |

---

## Design Philosophy

**Simplicity without compromise:**  
Minimal dependencies, clean architecture, clarity in purpose. Every feature is purposeful, and every UI element is functional and visually appealing.

---

## Educational Value

Orbit2.0 is ideal for learning:

- Numerical integration and stability
- Real-time web data streaming & buffering
- Software modularity and shared-core design
- Python + JS full-stack development

---

## Future Work

- Modularize frontend JS/CSS for maintainability
- Expose user-configurable options (timestep, colors, trail memory)
- Expand `bodies.json` to include moons, comets, dwarf planets
- Optional: Web Workers / WebGL support for performance
- Add multi-user support

---

## Screenshots / GIFs

<p align="center">
  <img src="static/media/demo.gif" alt="Demo" width="720"/>
  <br>
  <em>Web demo</em>
</p>

<p align="center">
  <img src="static/media/screenshot.png" alt="Web Selection Screen" width="720"/>
  <br>
  <em>Body Selection Screen</em>
</p>

<p align="center">
  <img src="static/media/plot.png" alt="Desktop Matplotlib view" width="560"/>
  <br>
  <em>Matplotlib simulation</em>
</p>

---

## Why Two Interfaces?

- **Scientific repeatability:** Same core logic in web & desktop
- **Broader audience:** Serves both research users and general learners
- **Skill showcase:** Demonstrates backend + modern frontend engineering

---

## License

MIT

---

## Credits

Developed by **[Aaryan Aaloke](https://github.com/Root3141)**
