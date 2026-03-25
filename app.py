import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Snake Game", layout="centered")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background-color: #111;
    color: white;
    text-align: center;
    font-family: Arial;
}
canvas {
    background-color: #222;
    border: 2px solid #555;
}
#score {
    font-size: 24px;
    margin: 10px;
}
#gameover {
    color: red;
    font-size: 20px;
    display: none;
}
button {
    padding: 10px 20px;
    font-size: 16px;
    margin-top: 10px;
}
#overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    background: rgba(0, 0, 0, 0.7);

    display: none;
    justify-content: center;
    align-items: center;
}

#popup {
    background: #1a1a1a;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 20px #00ff88;
}

#popup h2 {
    color: red;
    margin-bottom: 10px;
}

#popup button {
    padding: 10px 20px;
    font-size: 16px;
    margin-top: 10px;
    cursor: pointer;
}
</style>
</head>

<body>

<h2>🐍 Snake Game</h2>
<p>👉 Click the game area first, then use arrow keys or WASD</p>
<div id="score">Score: 0</div>
<div id="gameover">Game Over!</div>

<canvas id="game" width="400" height="400"></canvas>
<br>
<div id="overlay">
    <div id="popup">
        <h2>Game Over</h2>
        <p id="finalScore"></p>
        <button onclick="restartGame()">Play Again</button>
    </div>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// 🔥 FIX: Enable keyboard focus
canvas.setAttribute("tabindex", "0");
canvas.focus();

const grid = 20;
let snake, direction, food, score, gameOver;
let gameInterval;
let directionQueue = [];

// Init
function initGame() {
    snake = [{x: 10, y: 10}];
    direction = "RIGHT";
    directionQueue = [];
    score = 0;
    gameOver = false;

    document.getElementById("score").innerText = "Score: 0";
    document.getElementById("gameover").style.display = "none";

    spawnFood();
}

// Food spawn
function spawnFood() {
    while (true) {
        let newFood = {
            x: Math.floor(Math.random() * 20),
            y: Math.floor(Math.random() * 20)
        };

        if (!snake.some(s => s.x === newFood.x && s.y === newFood.y)) {
            food = newFood;
            return;
        }
    }
}

// 🎮 FIXED CONTROLS
canvas.addEventListener("keydown", function(e) {
    e.preventDefault();

    let newDir = null;

    if (e.key === "ArrowUp" || e.key === "w") newDir = "UP";
    if (e.key === "ArrowDown" || e.key === "s") newDir = "DOWN";
    if (e.key === "ArrowLeft" || e.key === "a") newDir = "LEFT";
    if (e.key === "ArrowRight" || e.key === "d") newDir = "RIGHT";

    if (!newDir) return;

    const lastDir = directionQueue.length > 0 
        ? directionQueue[directionQueue.length - 1] 
        : direction;

    // Prevent reverse
    if (
        (newDir === "UP" && lastDir === "DOWN") ||
        (newDir === "DOWN" && lastDir === "UP") ||
        (newDir === "LEFT" && lastDir === "RIGHT") ||
        (newDir === "RIGHT" && lastDir === "LEFT")
    ) return;

    directionQueue.push(newDir);
});

// Speed control
function getSpeed() {
    return Math.max(70, 120 - score * 2);
}

// Game loop
function startGameLoop() {
    clearInterval(gameInterval);

    gameInterval = setInterval(() => {
        if (!gameOver) {
            update();
            draw();
        }
    }, getSpeed());
}

// Update
function update() {
    if (directionQueue.length > 0) {
        direction = directionQueue.shift();
    }

    let head = {...snake[0]};

    if (direction === "UP") head.y--;
    if (direction === "DOWN") head.y++;
    if (direction === "LEFT") head.x--;
    if (direction === "RIGHT") head.x++;

    // Wall collision
    if (head.x < 0 || head.y < 0 || head.x >= 20 || head.y >= 20) {
        endGame();
        return;
    }

    // Self collision
    if (snake.some(part => part.x === head.x && part.y === head.y)) {
        endGame();
        return;
    }

    snake.unshift(head);

    // Eat food
    if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById("score").innerText = "Score: " + score;
        spawnFood();
        startGameLoop(); // update speed
    } else {
        snake.pop();
    }
}

function draw() {
    // 🌿 Background with subtle grid
    ctx.fillStyle = "#0f1a0f";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#1f2f1f";
    for (let i = 0; i < canvas.width; i += grid) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }

    // 🐍 Draw smooth snake body
    for (let i = snake.length - 1; i >= 0; i--) {
        const part = snake[i];
        const x = part.x * grid + grid / 2;
        const y = part.y * grid + grid / 2;

        let radius = grid / 2 - 2;

        // Tail smaller
        if (i > snake.length - 4) {
            radius *= 0.7;
        }

        // Head slightly bigger
        if (i === 0) {
            radius *= 1.2;
        }

        // Gradient body
        let gradient = ctx.createRadialGradient(x, y, 2, x, y, radius);
        gradient.addColorStop(0, "#9eff6e");
        gradient.addColorStop(1, "#1f7a1f");

        ctx.fillStyle = gradient;

        // Glow
        ctx.shadowColor = "#00ff88";
        ctx.shadowBlur = 8;

        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.shadowBlur = 0;
    }

    // 👀 Eyes (realistic with pupils)
    const head = snake[0];
    const hx = head.x * grid + grid / 2;
    const hy = head.y * grid + grid / 2;

    let eyeOffsetX = 5;
    let eyeOffsetY = 5;

    ctx.fillStyle = "white";

    let eyes = [];

    if (direction === "RIGHT") {
        eyes = [[hx + 6, hy - 5], [hx + 6, hy + 5]];
    } else if (direction === "LEFT") {
        eyes = [[hx - 6, hy - 5], [hx - 6, hy + 5]];
    } else if (direction === "UP") {
        eyes = [[hx - 5, hy - 6], [hx + 5, hy - 6]];
    } else if (direction === "DOWN") {
        eyes = [[hx - 5, hy + 6], [hx + 5, hy + 6]];
    }

    // Draw eyes
    eyes.forEach(([ex, ey]) => {
        ctx.beginPath();
        ctx.arc(ex, ey, 3, 0, Math.PI * 2);
        ctx.fill();

        // pupils
        ctx.fillStyle = "black";
        ctx.beginPath();
        ctx.arc(ex, ey, 1.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "white";
    });

    // 👅 Tongue animation
    if (Math.random() < 0.1) {
        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;

        ctx.beginPath();

        if (direction === "RIGHT") {
            ctx.moveTo(hx + 8, hy);
            ctx.lineTo(hx + 16, hy - 3);
            ctx.moveTo(hx + 8, hy);
            ctx.lineTo(hx + 16, hy + 3);
        } else if (direction === "LEFT") {
            ctx.moveTo(hx - 8, hy);
            ctx.lineTo(hx - 16, hy - 3);
            ctx.moveTo(hx - 8, hy);
            ctx.lineTo(hx - 16, hy + 3);
        } else if (direction === "UP") {
            ctx.moveTo(hx, hy - 8);
            ctx.lineTo(hx - 3, hy - 16);
            ctx.moveTo(hx, hy - 8);
            ctx.lineTo(hx + 3, hy - 16);
        } else if (direction === "DOWN") {
            ctx.moveTo(hx, hy + 8);
            ctx.lineTo(hx - 3, hy + 16);
            ctx.moveTo(hx, hy + 8);
            ctx.lineTo(hx + 3, hy + 16);
        }

        ctx.stroke();
    }

    // 🍎 Apple (realistic)
    const fx = food.x * grid + grid / 2;
    const fy = food.y * grid + grid / 2;

    let appleGrad = ctx.createRadialGradient(fx, fy, 3, fx, fy, grid / 2);
    appleGrad.addColorStop(0, "#ff6b6b");
    appleGrad.addColorStop(1, "#8b0000");

    ctx.fillStyle = appleGrad;
    ctx.beginPath();
    ctx.arc(fx, fy, grid / 2 - 2, 0, Math.PI * 2);
    ctx.fill();

    // Stem
    ctx.strokeStyle = "#5a3d1e";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(fx, fy - 8);
    ctx.lineTo(fx, fy - 14);
    ctx.stroke();
}
// Game over
function endGame() {
    gameOver = true;

    document.getElementById("overlay").style.display = "flex";
    document.getElementById("finalScore").innerText = "Score: " + score;
}

// Restart
function restartGame() {
    document.getElementById("overlay").style.display = "none";
    initGame();
    startGameLoop();
}
// Start game
initGame();
startGameLoop();

</script>

</body>
</html>
""", height=520)
