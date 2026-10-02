
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Shape Tetris",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1180px;
            padding: 0.8rem 1rem 0.5rem;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

:root {
  --bg: #0a0d14;
  --panel: #111722;
  --panel2: #171e2b;
  --border: #2a3445;
  --text: #f4f7fb;
  --muted: #8f9caf;
  --accent: #7c5cff;
  --accent2: #45d6c5;
  --danger: #ff5c7a;
}

html, body {
  margin: 0;
  padding: 0;
  background: transparent;
  color: var(--text);
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  overflow: hidden;
}

#app {
  width: 100%;
  max-width: 1140px;
  margin: 0 auto;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 10px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 38px;
  height: 38px;
  border-radius: 11px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #7c5cff, #45d6c5);
  font-size: 21px;
  box-shadow: 0 7px 22px rgba(124,92,255,.22);
}

.title {
  font-size: 25px;
  font-weight: 850;
  letter-spacing: -.5px;
}

.subtitle {
  font-size: 12px;
  color: var(--muted);
  margin-top: 1px;
}

.status {
  border: 1px solid var(--border);
  background: rgba(17,23,34,.9);
  border-radius: 999px;
  padding: 7px 12px;
  color: #b8c2d1;
  font-size: 12px;
  white-space: nowrap;
}

.layout {
  display: grid;
  grid-template-columns: minmax(430px, 1fr) minmax(310px, .75fr);
  gap: 18px;
  align-items: start;
}

.card {
  background: linear-gradient(180deg, rgba(23,30,43,.96), rgba(14,19,28,.96));
  border: 1px solid var(--border);
  border-radius: 16px;
}

.game-card {
  padding: 13px;
}

.board-area {
  display: flex;
  justify-content: center;
  align-items: center;
}

.board {
  display: grid;
  grid-template-columns: repeat(10, minmax(30px, 43px));
  grid-template-rows: repeat(14, minmax(30px, 43px));
  gap: 4px;
  padding: 7px;
  background: #080b11;
  border: 1px solid #344055;
  border-radius: 14px;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.02),
              0 12px 30px rgba(0,0,0,.25);
}

.cell {
  min-width: 0;
  min-height: 0;
  border-radius: 7px;
  background: #151c28;
  border: 1px solid #202a3a;
  transition: background .06s linear, transform .06s linear;
}

.cell.filled {
  border: 1px solid rgba(255,255,255,.26);
  box-shadow: inset 0 1px rgba(255,255,255,.2), 0 2px 7px rgba(0,0,0,.25);
}

.cell.ghost {
  background: transparent !important;
  border: 1px dashed rgba(255,255,255,.22);
  opacity: .55;
}

.bottom-help {
  text-align: center;
  color: var(--muted);
  font-size: 11px;
  margin-top: 8px;
}

.panel {
  padding: 15px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.panel-title {
  font-size: 15px;
  font-weight: 800;
}

.shape-name {
  color: var(--accent2);
  font-size: 12px;
  font-weight: 700;
}

.preview-wrap {
  min-height: 78px;
  display: grid;
  place-items: center;
  background: #0c111a;
  border: 1px solid #263143;
  border-radius: 12px;
  margin-bottom: 12px;
}

.preview {
  display: grid;
  grid-template-columns: repeat(4, 22px);
  grid-auto-rows: 22px;
  gap: 3px;
}

.preview-cell {
  border-radius: 5px;
  background: #202a3a;
}

.preview-cell.on {
  border: 1px solid rgba(255,255,255,.25);
  box-shadow: inset 0 1px rgba(255,255,255,.2);
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 7px;
  margin-bottom: 12px;
}

.stat {
  background: #0d131d;
  border: 1px solid #263143;
  border-radius: 10px;
  padding: 7px 5px;
  text-align: center;
}

.stat-value {
  font-size: 17px;
  font-weight: 850;
}

.stat-label {
  font-size: 9px;
  color: var(--muted);
  margin-top: 2px;
}

.controls {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 7px;
  margin-bottom: 11px;
}

button {
  appearance: none;
  border: 1px solid #303b4e;
  background: #171f2d;
  color: var(--text);
  border-radius: 10px;
  min-height: 40px;
  padding: 8px 10px;
  font-size: 12px;
  font-weight: 750;
  cursor: pointer;
  transition: transform .08s, background .12s, border-color .12s;
}

button:hover {
  background: #202a3b;
  border-color: #45536a;
}

button:active {
  transform: scale(.97);
}

button.primary {
  grid-column: span 2;
  background: linear-gradient(135deg, #7c5cff, #6550df);
  border-color: #8871ff;
}

button.primary:hover {
  background: linear-gradient(135deg, #896eff, #7059ec);
}

.key-guide {
  background: #0d131d;
  border: 1px solid #263143;
  border-radius: 11px;
  padding: 10px;
  margin-bottom: 10px;
}

.guide-title {
  font-size: 11px;
  font-weight: 800;
  margin-bottom: 7px;
}

.keys {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 5px;
}

.key {
  text-align: center;
  padding: 5px 2px;
  border-radius: 7px;
  background: #171f2d;
  border: 1px solid #303b4e;
  color: #cbd4e1;
  font-size: 9px;
}

.message {
  min-height: 32px;
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 9px;
  background: rgba(69,214,197,.08);
  border: 1px solid rgba(69,214,197,.2);
  color: #a9efe6;
  font-size: 11px;
  line-height: 1.3;
}

.geometry {
  margin-top: 9px;
  padding: 9px 10px;
  border-radius: 9px;
  background: #0d131d;
  border: 1px solid #263143;
  color: #aeb8c7;
  font-size: 10px;
  line-height: 1.4;
}

.geometry b { color: #e8edf5; }

.gameover {
  position: absolute;
  inset: 0;
  display: none;
  place-items: center;
  background: rgba(7,10,15,.72);
  backdrop-filter: blur(3px);
  border-radius: 14px;
}

.gameover.show { display: grid; }

.gameover-box {
  text-align: center;
  background: #151c28;
  border: 1px solid #3b4659;
  border-radius: 15px;
  padding: 20px 25px;
  box-shadow: 0 18px 45px rgba(0,0,0,.4);
}

.gameover-box h2 {
  margin: 0 0 5px;
  font-size: 23px;
}

.gameover-box p {
  margin: 0 0 13px;
  color: var(--muted);
  font-size: 12px;
}

.board-holder {
  position: relative;
}

@media (max-width: 800px) {
  html, body { overflow: auto; }
  .layout { grid-template-columns: 1fr; }
  .board {
    grid-template-columns: repeat(10, 34px);
    grid-template-rows: repeat(14, 34px);
  }
  .topbar { align-items: flex-start; }
  .status { display: none; }
}
</style>
</head>

<body>
<div id="app">
  <div class="topbar">
    <div class="brand">
      <div class="logo">🧩</div>
      <div>
        <div class="title">Shape Tetris</div>
        <div class="subtitle">Geometry + strategy + transformations</div>
      </div>
    </div>
    <div class="status" id="status">● Keyboard ready</div>
  </div>

  <div class="layout">
    <section class="card game-card">
      <div class="board-holder">
        <div class="board-area">
          <div id="board" class="board" aria-label="Shape Tetris board"></div>
        </div>
        <div class="gameover" id="gameover">
          <div class="gameover-box">
            <h2>Game Over</h2>
            <p id="finalScore">No more valid moves.</p>
            <button class="primary" id="restartOverlay">Play Again</button>
          </div>
        </div>
      </div>
      <div class="bottom-help">Click the game once, then use the arrow keys.</div>
    </section>

    <section class="card panel">
      <div class="panel-head">
        <div class="panel-title">Current Shape</div>
        <div class="shape-name" id="shapeName">Square</div>
      </div>

      <div class="preview-wrap">
        <div class="preview" id="preview"></div>
      </div>

      <div class="stats">
        <div class="stat"><div class="stat-value" id="score">0</div><div class="stat-label">SCORE</div></div>
        <div class="stat"><div class="stat-value" id="rows">0</div><div class="stat-label">ROWS</div></div>
        <div class="stat"><div class="stat-value" id="moves">0</div><div class="stat-label">MOVES</div></div>
      </div>

      <div class="controls">
        <button id="rotate">↻ Rotate</button>
        <button id="reflect">↔ Reflect</button>
        <button class="primary" id="newGame">🔄 New Game</button>
      </div>

      <div class="key-guide">
        <div class="guide-title">Keyboard Controls</div>
        <div class="keys">
          <div class="key">← Move</div>
          <div class="key">→ Move</div>
          <div class="key">↓ Faster</div>
          <div class="key">↑ Rotate</div>
          <div class="key">Space Drop</div>
          <div class="key">Z Reflect</div>
          <div class="key">R Restart</div>
          <div class="key">P Pause</div>
        </div>
      </div>

      <div class="message" id="message">Place your first shape!</div>

      <div class="geometry">
        <b>📐 Geometry skills:</b> rotation, reflection, area, symmetry, and spatial reasoning.
        Each block represents 1 square unit.
      </div>
    </section>
  </div>
</div>

<script>
(() => {
  const W = 10, H = 14;

  const SHAPES = {
    "L-Shape": [[0,0],[1,0],[2,0],[2,1]],
    "Z-Shape": [[0,0],[1,0],[1,1],[2,1]],
    "Square": [[0,0],[1,0],[0,1],[1,1]],
    "T-Shape": [[0,0],[1,0],[2,0],[1,1]],
    "Line": [[0,0],[1,0],[2,0],[3,0]]
  };

  const COLORS = {
    "L-Shape": "#ff9f43",
    "Z-Shape": "#ff6b81",
    "Square": "#ffd447",
    "T-Shape": "#a879ff",
    "Line": "#4db8ff"
  };

  let board, current, next, score, rows, moves, gameOver, paused;
  let lastKeyTime = 0;

  const $ = id => document.getElementById(id);

  function normalize(shape) {
    const minX = Math.min(...shape.map(p => p[0]));
    const minY = Math.min(...shape.map(p => p[1]));
    return shape
      .map(([x,y]) => [x-minX, y-minY])
      .sort((a,b) => a[1]-b[1] || a[0]-b[0]);
  }

  function rotate(shape) {
    return normalize(shape.map(([x,y]) => [-y,x]));
  }

  function reflect(shape) {
    return normalize(shape.map(([x,y]) => [-x,y]));
  }

  function makePiece(name=null) {
    const names = Object.keys(SHAPES);
    const n = name || names[Math.floor(Math.random()*names.length)];
    return { name:n, shape:normalize(SHAPES[n]), color:COLORS[n], x:2, y:0 };
  }

  function emptyBoard() {
    return Array.from({length:H}, () => Array(W).fill(null));
  }

  function canPlace(p, x=p.x, y=p.y) {
    return p.shape.every(([dx,dy]) => {
      const bx = x+dx, by = y+dy;
      return bx>=0 && bx<W && by>=0 && by<H && board[by][bx] === null;
    });
  }

  function move(dx,dy) {
    if (gameOver || paused) return false;
    if (canPlace(current, current.x+dx, current.y+dy)) {
      current.x += dx;
      current.y += dy;
      render();
      return true;
    }
    return false;
  }

  function transform(fn) {
    if (gameOver || paused) return;
    const old = current.shape;
    const transformed = fn(old);
    const test = {...current, shape:transformed};
    if (canPlace(test, current.x, current.y)) {
      current.shape = transformed;
    } else {
      // Try small horizontal corrections so rotation near an edge still feels natural.
      const corrections = [-1, 1, -2, 2];
      for (const dx of corrections) {
        if (canPlace(test, current.x+dx, current.y)) {
          current.x += dx;
          current.shape = transformed;
          break;
        }
      }
    }
    render();
  }

  function ghostY() {
    let y = current.y;
    while (canPlace(current, current.x, y+1)) y++;
    return y;
  }

  function hardDrop() {
    if (gameOver || paused) return;
    const start = current.y;
    current.y = ghostY();
    score += Math.max(0, current.y-start) * 2;
    lockPiece();
  }

  function lockPiece() {
    if (!canPlace(current)) {
      gameOver = true;
      updateMessage("Game over — press R to restart.");
      render();
      return;
    }

    current.shape.forEach(([dx,dy]) => {
      board[current.y+dy][current.x+dx] = current.color;
    });

    moves++;

    let cleared = 0;
    for (let y=H-1; y>=0; y--) {
      if (board[y].every(Boolean)) {
        board.splice(y,1);
        board.unshift(Array(W).fill(null));
        cleared++;
        y++;
      }
    }

    if (cleared > 0) {
      rows += cleared;
      score += cleared * 100;
      updateMessage(`Nice! ${cleared} row${cleared>1?'s':''} cleared. +${cleared*100}`);
    } else {
      score += 40;
      updateMessage("Nice placement! Keep building.");
    }

    current = next;
    next = makePiece();
    current.x = 2;
    current.y = 0;

    if (!canPlace(current)) {
      gameOver = true;
      updateMessage("No valid moves left — press R to restart.");
    }

    render();
  }

  function softDrop() {
    if (gameOver || paused) return;
    if (!move(0,1)) lockPiece();
  }

  function updateMessage(text) {
    $("message").textContent = text;
  }

  function reset() {
    board = emptyBoard();
    current = makePiece();
    next = makePiece();
    score = 0;
    rows = 0;
    moves = 0;
    gameOver = false;
    paused = false;
    updateMessage("Place your first shape!");
    $("gameover").classList.remove("show");
    $("status").textContent = "● Keyboard ready";
    render();
  }

  function renderBoard() {
    const el = $("board");
    el.innerHTML = "";

    const view = board.map(row => row.slice());
    const gy = ghostY();

    if (!gameOver) {
      current.shape.forEach(([dx,dy]) => {
        const x=current.x+dx, y=gy+dy;
        if (x>=0 && x<W && y>=0 && y<H && view[y][x]===null) {
          view[y][x] = "ghost";
        }
      });

      current.shape.forEach(([dx,dy]) => {
        const x=current.x+dx, y=current.y+dy;
        if (x>=0 && x<W && y>=0 && y<H) view[y][x] = current.color;
      });
    }

    view.forEach(row => row.forEach(value => {
      const cell = document.createElement("div");
      cell.className = "cell";
      if (value === "ghost") {
        cell.classList.add("ghost");
      } else if (value) {
        cell.classList.add("filled");
        cell.style.background = value;
      }
      el.appendChild(cell);
    }));
  }

  function renderPreview() {
    const el = $("preview");
    el.innerHTML = "";
    const shape = next.shape;
    for (let y=0; y<4; y++) {
      for (let x=0; x<4; x++) {
        const c = document.createElement("div");
        c.className = "preview-cell";
        if (shape.some(([sx,sy]) => sx===x && sy===y)) {
          c.classList.add("on");
          c.style.background = next.color;
        }
        el.appendChild(c);
      }
    }
  }

  function render() {
    renderBoard();
    renderPreview();
    $("shapeName").textContent = current.name;
    $("score").textContent = score;
    $("rows").textContent = rows;
    $("moves").textContent = moves;

    if (gameOver) {
      $("finalScore").textContent = `Final score: ${score} • Rows cleared: ${rows}`;
      $("gameover").classList.add("show");
      $("status").textContent = "● Game over";
    } else if (paused) {
      $("status").textContent = "● Paused";
    } else {
      $("status").textContent = "● Keyboard ready";
    }
  }

  function keyHandler(e) {
    const tag = document.activeElement?.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;

    const now = performance.now();
    if (now-lastKeyTime < 28 && ["ArrowLeft","ArrowRight","ArrowDown"].includes(e.key)) return;
    lastKeyTime = now;

    if (["ArrowLeft","ArrowRight","ArrowDown","ArrowUp"," "].includes(e.key)) {
      e.preventDefault();
    }

    if (e.key === "ArrowLeft") move(-1,0);
    else if (e.key === "ArrowRight") move(1,0);
    else if (e.key === "ArrowDown") softDrop();
    else if (e.key === "ArrowUp") transform(rotate);
    else if (e.key === " ") hardDrop();
    else if (e.key.toLowerCase() === "z") transform(reflect);
    else if (e.key.toLowerCase() === "r") reset();
    else if (e.key.toLowerCase() === "p") {
      if (!gameOver) {
        paused = !paused;
        render();
        updateMessage(paused ? "Paused. Press P to continue." : "Back in action!");
      }
    }
  }

  $("rotate").addEventListener("click", () => transform(rotate));
  $("reflect").addEventListener("click", () => transform(reflect));
  $("newGame").addEventListener("click", reset);
  $("restartOverlay").addEventListener("click", reset);

  document.addEventListener("keydown", keyHandler, {passive:false});

  // Automatic downward movement is intentionally slow and lightweight.
  setInterval(() => {
    if (!gameOver && !paused) softDrop();
  }, 850);

  reset();
})();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=705, scrolling=False)
