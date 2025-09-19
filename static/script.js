const toggleBtn = document.getElementById("toggle");
const simDiv = document.querySelector(".sim");
const showBtn = document.querySelector(".show");
const canvas = document.getElementById("simCanvas");
const ctx = canvas.getContext("2d");

let currScale = 600;
let isPlaying = false;
let interval = null;
const FPS = 10;

showBtn.addEventListener("click", () => {
  showBtn.style.display = "none";
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
  }
}

function stopSim() {
  if (interval) {
    clearInterval(interval);
    interval = null;
    isPlaying = false;
  }
}


function drawBodies(bodies) {
  ctx.fillStyle = "rgba(0, 0, 0, 0.2)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  bodies.forEach((body) => {
    const cx = canvas.width / 2 + body.x;
    const cy = canvas.height / 2 + body.y;
    ctx.beginPath();
    ctx.arc(cx, cy, 0, Math.PI * 2);
    ctx.fillStyle = body.color;
    ctx.fill();
  });
}
