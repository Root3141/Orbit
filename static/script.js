const toggleBtn = document.getElementById("toggle");
const simDiv = document.querySelector(".sim");
const startSimBtn = document.querySelector(".startSim");
const canvas = document.getElementById("simCanvas");
const ctx = canvas.getContext("2d");
const toggleTrail = document.getElementById("toggleTrail");

let isPlaying = false;
let interval = null;
let scaleFactor = 1;
let showTrails = false;
const FPS = 30;
const trails = {};
const MAX_TRAIL_LENGTH = 1000;

let selectedBodies = [];

function createRow(){
  const row = document.createElement("div");
  row.className = "cards-row";
  return row; 
}

async function loadBodies() {
  const res = await fetch("static/bodies.json");
  const bodies = await res.json();
  const optionsDiv = document.getElementById("bodyOptions");
  const sun = bodies.filter(b => b.label === "Sun");
  const inner = bodies.filter(b => ["Mercury", "Venus", "Earth", "Mars"].includes(b.label));
  const outer = bodies.filter(b => !["Sun", "Mercury", "Venus", "Earth", "Mars"].includes(b.label));
  const groups = [sun, inner, outer];

  groups.forEach(group => {
    const row = createRow();
    group.forEach(body => {
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
      if (["Sun", "Earth", "Mars"].includes(body.label)) {
        card.classList.add("selected");
      }
      card.addEventListener("click", () => {
        card.classList.toggle("selected");
        updateSelectedBodies();
      });

      row.appendChild(card);
    });
    optionsDiv.appendChild(row);
  })

  updateSelectedBodies();
  function updateSelectedBodies() {
    selectedBodies = Array.from(
      optionsDiv.querySelectorAll(".body-card.selected")
    ).map((c) => bodies.find((b) => b.label === c.dataset.label));
  }
}
loadBodies();

startSimBtn.addEventListener("click", async() => {
  await fetch('/init', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(selectedBodies)
  });
  document.getElementById("bodySelection").style.display = "none";
  simDiv.style.display = "block";
  setTimeout(() => simDiv.classList.add("show"), 50);
  startSim();
});

toggleBtn.addEventListener("click", () => {
  if (isPlaying) {
    stopSim();
  } else {
    startSim();
  }
});

toggleTrail.addEventListener("click", (e) => {
  showTrails = !showTrails;
  e.target.classList.toggle("active", showTrails);
  if (!showTrails) {
    for (let key in trails) {
      trails[key] = [];
    }
  }
});

async function update() {
  if (!isPlaying) return;
  try {
    const res = await fetch("/data");
    const bodies = await res.json();
    drawBodies(bodies);
  } catch (err) {
    console.error("Error fetching data:", err);
  }
}

function startSim() {
  if (!interval) {
    interval = setInterval(update, 1000 / FPS);
    isPlaying = true;
    toggleBtn.innerText = "Pause";
  }
}

function stopSim() {
  if (interval) {
    clearInterval(interval);
    interval = null;
    isPlaying = false;
    toggleBtn.innerText = "Play";
  }
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

      if (trails[body.label].length > MAX_TRAIL_LENGTH) {
        trails[body.label].shift();
      }
      ctx.beginPath();
      trails[body.label].forEach(([tx, ty], idx) => {
        if (idx === 0) ctx.moveTo(tx, ty);
        else ctx.lineTo(tx, ty);
      });
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

document.getElementById("zoomIn").addEventListener("click", () => {
  if (scaleFactor <= 10) {
    scaleFactor *= 1.2;
  }
});

document.getElementById("zoomOut").addEventListener("click", () => {
  if (scaleFactor >= 0.01) {
    scaleFactor /= 1.2;
  }
});