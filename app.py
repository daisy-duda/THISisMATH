import random
import streamlit as st

st.set_page_config(
    page_title="Shape Tetris",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Compact, cleaner styling ----------
st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding: 1rem 1.5rem 0.8rem;
}
.game-title {
    text-align:center;
    font-size:2.1rem;
    font-weight:800;
    margin-bottom:0;
}
.subtitle {
    text-align:center;
    color:#9ca3af;
    margin:0 0 .7rem;
}
.stat {
    background:#171b24;
    border:1px solid #303746;
    border-radius:10px;
    text-align:center;
    padding:7px;
}
.stat b { font-size:1.25rem; }
.stat small { color:#9ca3af; }
.board-wrap {
    display:flex;
    justify-content:center;
    margin:.2rem 0 .5rem;
}
.game-board {
    display:grid;
    grid-template-columns:repeat(8, 38px);
    grid-template-rows:repeat(10, 38px);
    gap:3px;
    padding:6px;
    background:#0d1117;
    border:2px solid #303746;
    border-radius:12px;
}
.game-cell {
    width:38px;
    height:38px;
    border-radius:6px;
    box-sizing:border-box;
}
.empty-cell {
    background:#171b24;
    border:1px solid #252c38;
}
.filled-cell {
    border:1px solid rgba(255,255,255,.3);
    box-shadow:inset 0 1px rgba(255,255,255,.2);
}
.panel {
    background:#151922;
    border:1px solid #303746;
    border-radius:12px;
    padding:12px;
}
.preview {
    display:grid;
    grid-template-columns:repeat(4,24px);
    grid-auto-rows:24px;
    gap:3px;
    justify-content:center;
    margin:8px 0;
}
.preview-cell {
    width:24px;
    height:24px;
    border-radius:4px;
}
</style>
""", unsafe_allow_html=True)

WIDTH, HEIGHT = 8, 10

SHAPES = {
    "L-Shape": [(0,0),(1,0),(2,0),(2,1)],
    "Z-Shape": [(0,0),(1,0),(1,1),(2,1)],
    "Square": [(0,0),(1,0),(0,1),(1,1)],
    "T-Shape": [(0,0),(1,0),(2,0),(1,1)],
    "Line": [(0,0),(1,0),(2,0),(3,0)],
}
COLORS = {
    "L-Shape":"#ff9f43", "Z-Shape":"#ff6b81", "Square":"#ffd93d",
    "T-Shape":"#a66cff", "Line":"#45aaf2"
}

def normalize(shape):
    min_x = min(x for x,y in shape)
    min_y = min(y for x,y in shape)
    return sorted((x-min_x, y-min_y) for x,y in shape)

def rotate(shape):
    return normalize([(-y,x) for x,y in shape])

def reflect(shape):
    return normalize([(-x,y) for x,y in shape])

def piece():
    name = random.choice(list(SHAPES))
    return {"name":name, "shape":normalize(SHAPES[name]), "color":COLORS[name]}

def blank_board():
    return [[None]*WIDTH for _ in range(HEIGHT)]

def can_place(board, shape, px, py):
    for dx,dy in shape:
        x,y = px+dx, py+dy
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False
        if board[y][x] is not None:
            return False
    return True

def put_piece(board, p, px, py):
    b = [row[:] for row in board]
    for dx,dy in p["shape"]:
        b[py+dy][px+dx] = p["color"]
    return b

def clear_rows(board):
    kept = [r for r in board if not all(c is not None for c in r)]
    cleared = HEIGHT - len(kept)
    while len(kept) < HEIGHT:
        kept.insert(0, [None]*WIDTH)
    return kept, cleared

def has_move(board, p):
    max_x = WIDTH - 1 - max(x for x,y in p["shape"])
    max_y = HEIGHT - 1 - max(y for x,y in p["shape"])
    return any(can_place(board,p["shape"],x,y)
               for y in range(max_y+1) for x in range(max_x+1))

def reset():
    st.session_state.board = blank_board()
    st.session_state.piece = piece()
    st.session_state.score = 0
    st.session_state.rows = 0
    st.session_state.moves = 0
    st.session_state.x = 2
    st.session_state.y = 0
    st.session_state.message = "Place your first shape!"
    st.session_state.game_over = False

if "board" not in st.session_state:
    reset()

# ---------- Header ----------
st.markdown('<div class="game-title">🧩 Shape Tetris</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fit shapes • transform them • clear rows • earn points</div>',
            unsafe_allow_html=True)

a,b,c,d = st.columns(4)
for col, value, label in [
    (a, st.session_state.score, "Score"),
    (b, st.session_state.rows, "Rows"),
    (c, st.session_state.moves, "Moves"),
    (d, len(st.session_state.piece["shape"]), "Cells"),
]:
    with col:
        st.markdown(f'<div class="stat"><b>{value}</b><br><small>{label}</small></div>',
                    unsafe_allow_html=True)

st.write("")

# ---------- Main area ----------
left, right = st.columns([1.35, 1], gap="large")

with left:
    display = [row[:] for row in st.session_state.board]
    p = st.session_state.piece

    if not st.session_state.game_over and can_place(
        display, p["shape"], st.session_state.x, st.session_state.y
    ):
        for dx,dy in p["shape"]:
            display[st.session_state.y+dy][st.session_state.x+dx] = p["color"]

    cells = []
    for row in display:
        for cell in row:
            if cell:
                cells.append(
                    f'<div class="game-cell filled-cell" style="background:{cell}"></div>'
                )
            else:
                cells.append('<div class="game-cell empty-cell"></div>')

    # This is the important fix: render HTML instead of showing HTML source.
    st.markdown(
        '<div class="board-wrap"><div class="game-board">' +
        ''.join(cells) + '</div></div>',
        unsafe_allow_html=True
    )
    st.info(st.session_state.message)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f"**Current shape:** {p['name']}")

    max_x_shape = max(x for x,y in p["shape"])
    max_y_shape = max(y for x,y in p["shape"])
    preview = []
    for y in range(max(2,max_y_shape+1)):
        for x in range(max(4,max_x_shape+1)):
            if (x,y) in p["shape"]:
                preview.append(
                    f'<div class="preview-cell" style="background:{p["color"]}"></div>'
                )
            else:
                preview.append(
                    '<div class="preview-cell" style="background:#202633"></div>'
                )
    st.markdown('<div class="preview">'+''.join(preview)+'</div>',
                unsafe_allow_html=True)

    r1,r2 = st.columns(2)
    with r1:
        if st.button("↻ Rotate", use_container_width=True,
                     disabled=st.session_state.game_over):
            st.session_state.piece["shape"] = rotate(p["shape"])
            st.rerun()
    with r2:
        if st.button("↔ Reflect", use_container_width=True,
                     disabled=st.session_state.game_over):
            st.session_state.piece["shape"] = reflect(p["shape"])
            st.rerun()

    max_x = max(0, WIDTH-1-max(x for x,y in p["shape"]))
    max_y = max(0, HEIGHT-1-max(y for x,y in p["shape"]))

    st.session_state.x = st.slider(
        "Horizontal position", 0, max_x,
        min(st.session_state.x,max_x),
        disabled=st.session_state.game_over
    )
    st.session_state.y = st.slider(
        "Vertical position", 0, max_y,
        min(st.session_state.y,max_y),
        disabled=st.session_state.game_over
    )

    if st.button("📌 Place Shape", type="primary", use_container_width=True,
                 disabled=st.session_state.game_over):
        if can_place(st.session_state.board,p["shape"],
                     st.session_state.x,st.session_state.y):
            st.session_state.board = put_piece(
                st.session_state.board,p,st.session_state.x,st.session_state.y
            )
            st.session_state.moves += 1
            st.session_state.board, cleared = clear_rows(st.session_state.board)
            st.session_state.rows += cleared
            st.session_state.score += len(p["shape"])*10 + cleared*100
            st.session_state.piece = piece()
            st.session_state.x = 2
            st.session_state.y = 0

            if not has_move(st.session_state.board,st.session_state.piece):
                st.session_state.game_over = True
                st.session_state.message = "🎉 Game over! No more valid moves."
            elif cleared:
                st.session_state.message = (
                    f"Great! You cleared {cleared} row(s)! "
                    f"+{cleared*100} points"
                )
            else:
                st.session_state.message = "Nice placement!"
            st.rerun()
        else:
            st.session_state.message = "⚠️ That position overlaps another block."
            st.rerun()

    if st.button("🔄 New Game", use_container_width=True):
        reset()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📐 How to play + geometry skills"):
    st.markdown("""
    **How to play:** Move the shape, rotate or reflect it, then place it.
    Complete a full row to clear it and earn bonus points.

    **Geometry:** rotation, reflection, area, symmetry, and spatial reasoning.
    """)

st.caption("Tip: Leave open spaces for larger shapes instead of filling one side too quickly.")
