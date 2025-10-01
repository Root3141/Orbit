# Orbit2.0 🌌

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)

A modular, minimalistic, and physically accurate orbital simulator.  
Experience as a modern interactive web app or classic desktop Python/matplotlib animation. Powered by symplectic Velocity-Verlet integration, Flask, and vanilla JS.

---

## Table of Contents

- [Overview](#overview)
- [Screenshots / GIFs](#screenshots--gifs)
- [Features](#features)
- [Architecture](#architecture)
- [Quickstart](#quickstart)
- [Editing or Adding Bodies](#editing-or-adding-bodies)
- [What's New in 2.0](#whats-new-in-20)
- [Educational Value](#educational-value)
- [Future Work](#future-work)
- [Known Issues](#known-issues)
- [License](#license)
- [Credits](#credits)

---

## Overview

Orbit2.0 simulates planetary and celestial motion using **energy-conserving Velocity-Verlet integration** for long-term orbital stability. It has been designed to maximize functionality through an elegant yet minimal design without compromising on performance or user experience.

**Experience it as:**

- 🖥️ **Desktop:** Python + Matplotlib animation – for research, teaching, or offline demos.
- 🌐 **Web:** Flask backend + HTML/JS/CSS frontend – modern interactive simulation.

Both interfaces use the **same NumPy-based simulation core** for scientific consistency.

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
| Integration   | Semi-implicit Euler | Velocity-Verlet |
| Data          | Hardcoded           | Editable JSON file                    |
| Visualization | Matplotlib only     | Web + Matplotlib               |
| Architecture  | Flat script         | Modular, shared core, clean separation      |
| UI/UX         | Static plots        | Modern, animated, interactive web UI        |


---

## Educational Value

Orbit2.0 is ideal for learning:

- Visualizes Newtonian mechanics and orbital dynamics.
- Helps students experiment with orbital parameters and see real-time effects.
- Encourages hands-on learning with minimal setup.

---

## Future Work

- Modularize frontend JS/CSS for maintainability
- Expose user-configurable options (timestep, colors, trail memory)
- Expand `bodies.json` to include moons, comets, dwarf planets
- Optional: Web Workers/WebGL support for performance
- Add multi-user support

---

## Known Issues

- On the deployed web version (Render), resuming a paused simulation may occasionally jump ahead instead of continuing from the pause point before proceeding smoothly. This does **not** occur when running locally, where it resumes as expected.

## License

[MIT License](LICENSE)

---

## Credits

Developed by **[Aaryan Aaloke](https://github.com/Root3141)**
