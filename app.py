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
<div id="score">Score: 0</div>
<div id="gameover">Game Over!</div>
<canvas id="game" width="400" height="400"></canvas>
<br>
<button onclick="restartGame()">Restart</button>

<script>
canvas.setAttribute("tabindex", "0");
canvas.focus();

const grid = 20;
let snake, direction, food, score, gameOver;
let gameInterval;
let directionQueue = [];

// Initialize game
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

// Spawn food safely
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

// Controls (Arrow + WASD)
canvas.addEventListener("keydown", function(e) {
    e.preventDefault();

    if (e.key === "ArrowUp" || e.key === "w") newDir = "UP";
    if (e.key === "ArrowDown" || e.key === "s") newDir = "DOWN";
    if (e.key === "ArrowLeft" || e.key === "a") newDir = "LEFT";
    if (e.key === "ArrowRight" || e.key === "d") newDir = "RIGHT";

    if (!newDir) return;

    const lastDir = directionQueue.length > 0 
        ? directionQueue[directionQueue.length - 1] 
        : direction;

    // Prevent reverse moves
    if (
        (newDir === "UP" && lastDir === "DOWN") ||
        (newDir === "DOWN" && lastDir === "UP") ||
        (newDir === "LEFT" && lastDir === "RIGHT") ||
        (newDir === "RIGHT" && lastDir === "LEFT")
    ) return;

    directionQueue.push(newDir);
});

// Dynamic speed
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

// Update logic
function update() {
    if (directionQueue.length > 0) {
        direction = directionQueue.shift();
    }

    let head = {...snake[0]};

    if (direction === "UP") head.y--;
    if (direction === "DOWN") head.y++;
    if (direction === "LEFT") head.x--;
    if (direction === "RIGHT") head.x++;

    // Collision: wall
    if (head.x < 0 || head.y < 0 || head.x >= 20 || head.y >= 20) {
        endGame();
        return;
    }

    // Collision: self
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

// Draw game
function draw() {
    ctx.fillStyle = "#222";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "lime";
    snake.forEach(part => {
        ctx.fillRect(part.x * grid, part.y * grid, grid - 2, grid - 2);
    });

    ctx.fillStyle = "red";
    ctx.fillRect(food.x * grid, food.y * grid, grid - 2, grid - 2);
}

// End game
function endGame() {
    gameOver = true;
    document.getElementById("gameover").style.display = "block";
}

// Restart
function restartGame() {
    initGame();
    startGameLoop();
}

// Start
initGame();
startGameLoop();

</script>

</body>
</html>
""", height=500)
