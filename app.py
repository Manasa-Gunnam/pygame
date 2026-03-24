import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

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
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const grid = 20;
let snake, direction, food, score, gameOver;
let gameInterval;

// Start game
function initGame() {
    snake = [{x: 10, y: 10}];
    direction = "RIGHT";
    score = 0;
    gameOver = false;
    document.getElementById("score").innerText = "Score: 0";
    document.getElementById("gameover").style.display = "none";
    spawnFood();
}

// Food spawn (fixed)
function spawnFood() {
    while (true) {
        let newFood = {
            x: Math.floor(Math.random() * 20),
            y: Math.floor(Math.random() * 20)
        };

        let onSnake = snake.some(s => s.x === newFood.x && s.y === newFood.y);
        if (!onSnake) {
            food = newFood;
            return;
        }
    }
}

// Controls
document.addEventListener("keydown", function(e) {
    if (e.key === "ArrowUp" && direction !== "DOWN") direction = "UP";
    if (e.key === "ArrowDown" && direction !== "UP") direction = "DOWN";
    if (e.key === "ArrowLeft" && direction !== "RIGHT") direction = "LEFT";
    if (e.key === "ArrowRight" && direction !== "LEFT") direction = "RIGHT";
});

// Game loop using setInterval (fixed)
function startGameLoop() {
    clearInterval(gameInterval); // FIX: prevent multiple loops

    gameInterval = setInterval(() => {
        if (!gameOver) {
            update();
            draw();
        }
    }, 120);
}

// Update logic
function update() {
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
    } else {
        snake.pop();
    }
}

// Draw everything
function draw() {
    ctx.fillStyle = "#222";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Snake
    ctx.fillStyle = "lime";
    snake.forEach(part => {
        ctx.fillRect(part.x * grid, part.y * grid, grid-2, grid-2);
    });

    // Food
    ctx.fillStyle = "red";
    ctx.fillRect(food.x * grid, food.y * grid, grid-2, grid-2);
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

// Initialize
initGame();
startGameLoop();

</script>

</body>
</html>
""", height=500)
