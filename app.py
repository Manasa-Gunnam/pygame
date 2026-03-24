import streamlit as st
import random
import time

# Grid size
GRID_SIZE = 20

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
    st.session_state.game_over = False

def move_snake():
    head = st.session_state.snake[0]
    x, y = head

    if st.session_state.direction == "UP":
        new_head = (x - 1, y)
    elif st.session_state.direction == "DOWN":
        new_head = (x + 1, y)
    elif st.session_state.direction == "LEFT":
        new_head = (x, y - 1)
    else:
        new_head = (x, y + 1)

    # Check collision
    if (
        new_head in st.session_state.snake or
        new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    if new_head == st.session_state.food:
        st.session_state.food = (
            random.randint(0, 19),
            random.randint(0, 19)
        )
    else:
        st.session_state.snake.pop()

def draw_grid():
    grid = ""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) in st.session_state.snake:
                grid += "🟩"
            elif (i, j) == st.session_state.food:
                grid += "🍎"
            else:
                grid += "⬛"
        grid += "\n"
    st.text(grid)

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆️"):
        st.session_state.direction = "UP"
with col3:
    if st.button("➡️"):
        st.session_state.direction = "RIGHT"

if st.button("⬇️"):
    st.session_state.direction = "DOWN"

# Game loop simulation
if not st.session_state.game_over:
    move_snake()
    draw_grid()
    time.sleep(0.3)
    st.rerun()
else:
    st.error("Game Over!")
    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
