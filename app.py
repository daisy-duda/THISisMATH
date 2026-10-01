import streamlit as st
import random

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Shape Tetris",
    page_icon="🧩",
    layout="centered"
)

# --------------------------------------------------
# GAME SETTINGS
# --------------------------------------------------

BOARD_WIDTH = 8
BOARD_HEIGHT = 10

SHAPES = {
    "Triangle": [
        (0, 0),
        (1, 0),
        (2, 0),
        (1, 1)
    ],

    "L-Shape": [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2)
    ],

    "Z-Shape": [
        (0, 0),
        (1, 0),
        (1, 1),
        (2, 1)
    ],

    "Square": [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1)
    ],

    "T-Shape": [
        (0, 0),
        (1, 0),
        (2, 0),
        (1, 1)
    ]
}

COLORS = {
    "Triangle": "#8B5CF6",
    "L-Shape": "#F59E0B",
    "Z-Shape": "#EF4444",
    "Square": "#22C55E",
    "T-Shape": "#3B82F6"
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def normalize_shape(cells):
    """
    Moves a shape so its smallest x and y coordinates
    are both 0.
    """

    min_x = min(x for x, y in cells)
    min_y = min(y for x, y in cells)

    normalized = [
        (x - min_x, y - min_y)
        for x, y in cells
    ]

    return sorted(normalized)


def rotate_shape(cells):
    """
    Rotates a shape 90 degrees clockwise.
    """

    rotated = [
        (-y, x)
        for x, y in cells
    ]

    return normalize_shape(rotated)


def reflect_shape(cells):
    """
    Reflects a shape across a vertical axis.
    """

    reflected = [
        (-x, y)
        for x, y in cells
    ]

    return normalize_shape(reflected)


def create_piece():
    """
    Creates a random geometric piece.
    """

    name = random.choice(list(SHAPES.keys()))

    return {
        "name": name,
        "cells": normalize_shape(SHAPES[name]),
        "x": 0,
        "y": 0
    }


def can_place(board, cells, position_x, position_y):
    """
    Checks whether a piece can be placed
    at a specific location.
    """

    for x, y in cells:

        board_x = position_x + x
        board_y = position_y + y

        # Outside board
        if board_x < 0:
            return False

        if board_x >= BOARD_WIDTH:
            return False

        if board_y < 0:
            return False

        if board_y >= BOARD_HEIGHT:
            return False

        # Occupied square
        if board[board_y][board_x] is not None:
            return False

    return True


def place_piece(board, cells, position_x, position_y, name):
    """
    Places a piece onto the board.
    """

    for x, y in cells:

        board_x = position_x + x
        board_y = position_y + y

        board[board_y][board_x] = name


def clear_completed_rows(board):
    """
    Removes rows that are completely filled.
    """

    completed = []

    for row_index, row in enumerate(board):

        if all(cell is not None for cell in row):
            completed.append(row_index)

    # Remove completed rows
    for row_index in reversed(completed):
        del board[row_index]

    # Add empty rows at the top
    for _ in completed:
        board.insert(
            0,
            [None] * BOARD_WIDTH
        )

    return len(completed)


def possible_position(board, piece):
    """
    Checks whether a piece can be placed anywhere.
    """

    cells = piece["cells"]

    max_x = max(x for x, y in cells)
    max_y = max(y for x, y in cells)

    for y in range(BOARD_HEIGHT - max_y):

        for x in range(BOARD_WIDTH - max_x):

            if can_place(
                board,
                cells,
                x,
                y
            ):
                return True

    return False


# --------------------------------------------------
# INITIALIZE GAME
# --------------------------------------------------

def start_game():

    st.session_state.board = [
        [None] * BOARD_WIDTH
        for _ in range(BOARD_HEIGHT)
    ]

    st.session_state.piece = create_piece()

    st.session_state.score = 0

    st.session_state.rows_cleared = 0

    st.session_state.moves = 0

    st.session_state.message = (
        "Place your first shape!"
    )

    st.session_state.game_over = False


if "board" not in st.session_state:
    start_game()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🧩 Shape Tetris")

st.write(
    "Combine Tetris with geometry! "
    "Rotate, reflect, and position shapes to "
    "complete rows."
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📖 How to Play")

    st.write(
        """
        **Goal:** Complete as many rows as possible.

        1. Choose a transformation.
        2. Move your shape.
        3. Place it on the board.
        4. Complete rows.
        5. Earn points!
        """
    )

    st.divider()

    st.subheader("📐 Geometry Skills")

    st.write("🔄 Rotation")
    st.write("↔️ Reflection")
    st.write("📏 Area")
    st.write("⭐ Symmetry")
    st.write("🧠 Spatial reasoning")

    st.divider()

    if st.button(
        "🔄 Restart Game",
        use_container_width=True
    ):

        start_game()

        st.rerun()


# --------------------------------------------------
# CURRENT PIECE
# --------------------------------------------------

piece = st.session_state.piece

st.subheader(
    f"Current Shape: {piece['name']}"
)


# --------------------------------------------------
# TRANSFORMATION BUTTONS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "↻ Rotate",
        use_container_width=True
    ):

        piece["cells"] = rotate_shape(
            piece["cells"]
        )

        st.session_state.moves += 1

        st.rerun()


with col2:

    if st.button(
        "↔ Reflect",
        use_container_width=True
    ):

        piece["cells"] = reflect_shape(
            piece["cells"]
        )

        st.session_state.moves += 1

        st.rerun()


with col3:

    if st.button(
        "🎲 New Shape",
        use_container_width=True
    ):

        st.session_state.piece = create_piece()

        st.rerun()


# --------------------------------------------------
# POSITION CONTROLS
# --------------------------------------------------

max_x = max(
    x for x, y in piece["cells"]
)

max_y = max(
    y for x, y in piece["cells"]
)


max_horizontal_position = (
    BOARD_WIDTH - 1 - max_x
)

max_vertical_position = (
    BOARD_HEIGHT - 1 - max_y
)


piece["x"] = st.slider(
    "Horizontal Position",
    min_value=0,
    max_value=max_horizontal_position,
    value=min(
        piece["x"],
        max_horizontal_position
    )
)


piece["y"] = st.slider(
    "Vertical Position",
    min_value=0,
    max_value=max_vertical_position,
    value=min(
        piece["y"],
        max_vertical_position
    )
)


# --------------------------------------------------
# DRAW BOARD
# --------------------------------------------------

board_html = """
<style>

.game-board {

    display: grid;

    grid-template-columns:
        repeat(8, 1fr);

    gap: 4px;

    max-width: 440px;

    margin: auto;

}

.game-cell {

    aspect-ratio: 1 / 1;

    border-radius: 6px;

    border: 1px solid
        rgba(128,128,128,0.4);

}

.empty-cell {

    background:
        rgba(128,128,128,0.08);

}

</style>

<div class="game-board">
"""


for y in range(BOARD_HEIGHT):

    for x in range(BOARD_WIDTH):

        # Is the current piece occupying this square?
        current_piece = False

        for cell_x, cell_y in piece["cells"]:

            if (
                x == piece["x"] + cell_x
                and
                y == piece["y"] + cell_y
            ):

                current_piece = True

                break


        # Current moving piece
        if current_piece:

            color = COLORS[
                piece["name"]
            ]

            board_html += f"""
            <div
                class="game-cell"
                style="background:{color};"
            ></div>
            """

        # Existing piece
        elif st.session_state.board[y][x]:

            existing_name = (
                st.session_state.board[y][x]
            )

            color = COLORS[
                existing_name
            ]

            board_html += f"""
            <div
                class="game-cell"
                style="background:{color};"
            ></div>
            """

        # Empty square
        else:

            board_html += """
            <div
                class="game-cell empty-cell"
            ></div>
            """


board_html += "</div>"


st.markdown(
    board_html,
    unsafe_allow_html=True
)


# --------------------------------------------------
# GAME STATISTICS
# --------------------------------------------------

st.write("")


stat1, stat2, stat3 = st.columns(3)


with stat1:

    st.metric(
        "⭐ Score",
        st.session_state.score
    )


with stat2:

    st.metric(
        "🧱 Rows",
        st.session_state.rows_cleared
    )


with stat3:

    st.metric(
        "🔄 Moves",
        st.session_state.moves
    )


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

valid_position = can_place(
    st.session_state.board,
    piece["cells"],
    piece["x"],
    piece["y"]
)


if not valid_position:

    st.warning(
        "⚠️ This shape cannot be placed here. "
        "Move or transform it!"
    )


# --------------------------------------------------
# PLACE BUTTON
# --------------------------------------------------

if st.button(
    "📍 PLACE SHAPE",
    use_container_width=True,
    disabled=not valid_position
):

    # Put shape onto board
    place_piece(
        st.session_state.board,
        piece["cells"],
        piece["x"],
        piece["y"],
        piece["name"]
    )

    # Check completed rows
    rows = clear_completed_rows(
        st.session_state.board
    )

    # Calculate score
    shape_area = len(
        piece["cells"]
    )

    points = (
        shape_area * 10
        +
        rows * 100
    )

    st.session_state.score += points

    st.session_state.rows_cleared += rows

    st.session_state.moves += 1


    # Message
    if rows > 0:

        st.session_state.message = (
            f"🎉 AMAZING! You cleared "
            f"{rows} row(s) and earned "
            f"{points} points!"
        )

    else:

        st.session_state.message = (
            f"Nice placement! "
            f"+{points} points."
        )


    # Generate next piece
    st.session_state.piece = create_piece()


    # Check game over
    if not possible_position(
        st.session_state.board,
        st.session_state.piece
    ):

        st.session_state.game_over = True


    st.rerun()


# --------------------------------------------------
# MESSAGE
# --------------------------------------------------

st.info(
    st.session_state.message
)


# --------------------------------------------------
# GAME OVER
# --------------------------------------------------

if st.session_state.game_over:

    st.error(
        "🏁 GAME OVER!"
    )

    st.subheader(
        f"Final Score: "
        f"{st.session_state.score}"
    )

    st.write(
        f"You cleared "
        f"{st.session_state.rows_cleared} rows!"
    )

    if st.button(
        "🎮 Play Again",
        use_container_width=True
    ):

        start_game()

        st.rerun()


# --------------------------------------------------
# GEOMETRY INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("📐 Geometry Challenge")

st.write(
    f"""
    Every piece currently contains **4 unit squares**,
    so each piece has an area of **4 square units**.

    Try rotating and reflecting the pieces to discover
    which transformations help you fit them together!
    """
)

st.caption(
    "Shape Tetris — Math + Geometry Game"
)