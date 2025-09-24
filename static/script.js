// DOM references
const toggleBtn = document.getElementById("toggle");
const toggleTrail = document.getElementById("toggleTrail");
const simDiv = document.querySelector(".sim");
const startSimBtn = document.querySelector(".startSim");
const canvas = document.getElementById("simCanvas");
const ctx = canvas.getContext("2d");
const zoomInBtn = document.getElementById("zoomIn");
const zoomOutBtn = document.getElementById("zoomOut");

// Simulation constants
const FPS = 30;
const BUFFER_SIZE = 10;
const MAX_TRAIL_LENGTH = 1000;
const interval = 1000 / FPS;
const renderTime = 24 * 60 * 60;

// Simulation state
let evtSource = null;
let isPlaying = false;
let scaleFactor = 1;
let showTrails = false;
let lastTime = 0;
let frameBuffer = [];
let simTime = 0;
const trails = {};
let selectedBodies = [];

// Simulation functions
function animate(now) {
  const elapsed = now - lastTime;
  if (elapsed >= interval) {
    lastTime = now - (elapsed % interval);
    if (isPlaying) drawInterpolated();
  }
  requestAnimationFrame(animate);
}

function drawInterpolated() {
  if (frameBuffer.length < 2) return;
  simTime = Math.min(
    Math.max(simTime, frameBuffer[0].timestamp),
    frameBuffer[frameBuffer.length - 1].timestamp
  );

  let frame1 = null,
    frame2 = null;
  for (let i = 0; i < frameBuffer.length - 1; i++) {
    if (
      frameBuffer[i].timestamp <= simTime &&
      frameBuffer[i + 1].timestamp >= simTime
    ) {
      frame1 = frameBuffer[i];
      frame2 = frameBuffer[i + 1];
      break;
    }
  }
  if (!frame1 || !frame2) return;

  const alpha =
    (simTime - frame1.timestamp) / (frame2.timestamp - frame1.timestamp);
  const interpolated = frame1.bodies.map((body, idx) => {
    const next = frame2.bodies[idx];
    return {
      ...body,
      x: body.x + (next.x - body.x) * alpha,
      y: body.y + (next.y - body.y) * alpha,
    };
  });

  drawBodies(interpolated);
  simTime += renderTime;

  while (
    frameBuffer.length > 2 &&
    (frameBuffer[1].timestamp < simTime ||
      frameBuffer.length > 1.5 * BUFFER_SIZE)
  ) {
    frameBuffer.shift();
  }
}

async function prefillBuffer() {
  const res = await fetch(`/data?count=${BUFFER_SIZE - frameBuffer.length}`);
  const frames = await res.json();
  frameBuffer.push(...frames);
}

function drawBodies(bodies) {
  ctx.fillStyle = "rgba(24, 24, 24, 1)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  bodies.forEach((body) => {
    const cx = canvas.width / 2 + body.x * scaleFactor;
    const cy = canvas.height / 2 + body.y * scaleFactor;

    if (showTrails) {
      if (!trails[body.label]) trails[body.label] = [];
      trails[body.label].push([cx, cy]);
      if (trails[body.label].length > MAX_TRAIL_LENGTH)
        trails[body.label].shift();

      ctx.beginPath();
      trails[body.label].forEach(([tx, ty], idx) =>
        idx === 0 ? ctx.moveTo(tx, ty) : ctx.lineTo(tx, ty)
      );
      ctx.strokeStyle = body.color;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    ctx.beginPath();
    ctx.arc(cx, cy, body.size * Math.sqrt(scaleFactor), 0, Math.PI * 2);
    ctx.fillStyle = body.color;
    ctx.fill();

    ctx.font = "14px Consolas";
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.fillText(body.label, cx, cy - 10);
  });
}

function startSim() {
  if (!isPlaying) {
    isPlaying = true;
    toggleBtn.innerText = "Pause";
    lastTime = performance.now();
    if (!evtSource) {
      evtSource = new EventSource("/stream");
      evtSource.onmessage = (e) => frameBuffer.push(JSON.parse(e.data));
      evtSource.onerror = (err) => {
        if (!isPlaying) return;
        console.warn("SSE disconnected, reconnecting...", err);
        evtSource.close();
        evtSource = null;
        setTimeout(startSim, 1000);
      };
    }

    requestAnimationFrame(animate);
  }
}

function stopSim() {
  isPlaying = false;
  toggleBtn.innerText = "Play";
  if (evtSource) {
    evtSource.close();
    evtSource = null;
  }
}

// Loading celestial bodies

function createRow() {
  const row = document.createElement("div");
  row.className = "cards-row";
  return row;
}

async function loadBodies() {
  const res = await fetch("static/bodies.json");
  const bodies = await res.json();
  const optionsDiv = document.getElementById("bodyOptions");

  const sun = bodies.filter((b) => b.label === "Sun");
  const inner = bodies.filter((b) =>
    ["Mercury", "Venus", "Earth", "Mars"].includes(b.label)
  );
  const outer = bodies.filter(
    (b) => !["Sun", "Mercury", "Venus", "Earth", "Mars"].includes(b.label)
  );
  const groups = [sun, inner, outer];

  groups.forEach((group) => {
    const row = createRow();
    group.forEach((body) => {
      const card = document.createElement("div");
      card.className = "body-card";
      card.dataset.label = body.label;
      card.innerHTML = `
        <img src="static/images/${body.label}.png" alt="${body.label}" />
        <h3>${body.label}</h3>
        <p>Mass: ${body.mass}</p>
        <p>Radius: ${body.radius} km</p>
        <p>Year Length: ${body.yearLen} days</p>
      `;
      if (["Sun", "Earth", "Mars"].includes(body.label))
        card.classList.add("selected");
      card.addEventListener("click", () => {
        card.classList.toggle("selected");
        updateSelectedBodies();
      });
      row.appendChild(card);
    });
    optionsDiv.appendChild(row);
  });

  updateSelectedBodies();

  function updateSelectedBodies() {
    selectedBodies = Array.from(
      optionsDiv.querySelectorAll(".body-card.selected")
    ).map((c) => bodies.find((b) => b.label === c.dataset.label));
  }
}

loadBodies();

// UI event handlers

startSimBtn.addEventListener("click", async () => {
  await fetch("/init", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(selectedBodies),
  });
  document.getElementById("bodySelection").style.display = "none";
  simDiv.style.display = "block";
  setTimeout(() => simDiv.classList.add("show"), 50);
  frameBuffer = [];
  simTime = 0;
  await prefillBuffer();
  startSim();
});

toggleBtn.addEventListener("click", () => (isPlaying ? stopSim() : startSim()));

toggleTrail.addEventListener("click", (e) => {
  showTrails = !showTrails;
  e.target.classList.toggle("active", showTrails);
  if (!showTrails) Object.keys(trails).forEach((key) => (trails[key] = []));
});

zoomInBtn.addEventListener("click", () => {
  if (scaleFactor <= 10) scaleFactor *= 1.2;
});
zoomOutBtn.addEventListener("click", () => {
  if (scaleFactor >= 0.01) scaleFactor /= 1.2;
});

document.addEventListener("visibilitychange", async () => {
  if (document.hidden) stopSim();
  else {
    await prefillBuffer();
    startSim();
  }
});
