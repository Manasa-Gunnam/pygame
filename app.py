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
</style>
</head>

<body>

<h2>🐍 Snake Game</h2>
<p>👉 Click the game area first, then use arrow keys or WASD</p>
<div id="score">Score: 0</div>
<div id="gameover">Game Over!</div>

<canvas id="game" width="400" height="400"></canvas>
<br>
<button onclick="restartGame()">Restart</button>

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
    // Background
    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 🐍 Draw Snake
    snake.forEach((part, index) => {
        const x = part.x * grid;
        const y = part.y * grid;

        // Gradient body
        let gradient = ctx.createRadialGradient(
            x + grid/2, y + grid/2, 2,
            x + grid/2, y + grid/2, grid
        );

        gradient.addColorStop(0, "#7CFC00"); // light green center
        gradient.addColorStop(1, "#228B22"); // darker edges

        ctx.fillStyle = gradient;

        // Rounded body
        ctx.beginPath();
        ctx.roundRect(x, y, grid - 2, grid - 2, 6);
        ctx.fill();

        // 👀 Draw eyes on head
        if (index === 0) {
            ctx.fillStyle = "white";

            let eyeOffsetX = 4;
            let eyeOffsetY = 4;

            if (direction === "RIGHT") {
                ctx.beginPath();
                ctx.arc(x + 14, y + 6, 2, 0, Math.PI * 2);
                ctx.arc(x + 14, y + 14, 2, 0, Math.PI * 2);
                ctx.fill();
            }
            if (direction === "LEFT") {
                ctx.beginPath();
                ctx.arc(x + 4, y + 6, 2, 0, Math.PI * 2);
                ctx.arc(x + 4, y + 14, 2, 0, Math.PI * 2);
                ctx.fill();
            }
            if (direction === "UP") {
                ctx.beginPath();
                ctx.arc(x + 6, y + 4, 2, 0, Math.PI * 2);
                ctx.arc(x + 14, y + 4, 2, 0, Math.PI * 2);
                ctx.fill();
            }
            if (direction === "DOWN") {
                ctx.beginPath();
                ctx.arc(x + 6, y + 14, 2, 0, Math.PI * 2);
                ctx.arc(x + 14, y + 14, 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    });

    // 🍎 Food (better look)
    const fx = food.x * grid;
    const fy = food.y * grid;

    let foodGradient = ctx.createRadialGradient(
        fx + grid/2, fy + grid/2, 2,
        fx + grid/2, fy + grid/2, grid
    );

    foodGradient.addColorStop(0, "#ff4d4d");
    foodGradient.addColorStop(1, "#990000");

    ctx.fillStyle = foodGradient;
    ctx.beginPath();
    ctx.arc(fx + grid/2, fy + grid/2, grid/2 - 2, 0, Math.PI * 2);
    ctx.fill();
}

// Game over
function endGame() {
    gameOver = true;
    document.getElementById("gameover").style.display = "block";
}

// Restart
function restartGame() {
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
