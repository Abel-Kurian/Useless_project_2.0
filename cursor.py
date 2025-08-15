# cursor.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Runaway Cursor", layout="centered")
st.title("🖱️ Runaway Cursor — client-side (works in Streamlit Cloud)")
st.markdown(
    "Move your real mouse over the canvas — the fake red cursor will run away. "
    "Adjust **Speed**, **Repel distance**, and **Autoplay** using the controls below."
)

# Controls
canvas_w = 700
canvas_h = 420
cursor_radius = 12

speed = st.slider("🏃 Cursor Speed (pixels per frame)", 1, 40, 8)
repel_distance = st.slider("📏 Repel distance (px)", 10, 400, 120)
autoplay = st.checkbox("▶️ Autoplay (continuous)", value=True)
show_mouse_dot = st.checkbox("Show mouse dot (debug)", value=False)

# Build an HTML+JS canvas that runs entirely in the browser.
# We pass the Python-controlled values into the JS environment via f-string interpolation.
html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin:0; display:flex; align-items:center; justify-content:center; }}
    canvas {{ border:1px solid #ddd; background: #fff; display:block; }}
  </style>
</head>
<body>
  <canvas id="c" width="{canvas_w}" height="{canvas_h}"></canvas>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

let cx = {canvas_w // 2};
let cy = {canvas_h // 2};
const radius = {cursor_radius};
let mouse = {{x: -9999, y: -9999}};
let speed = {speed};
let threshold = {repel_distance};
let autoplay = { 'true' if autoplay else 'false' };
const showMouseDot = { 'true' if show_mouse_dot else 'false' };

canvas.addEventListener('mousemove', (e) => {{
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
}});

canvas.addEventListener('touchmove', (e) => {{
  const rect = canvas.getBoundingClientRect();
  const t = e.touches[0];
  mouse.x = t.clientX - rect.left;
  mouse.y = t.clientY - rect.top;
  e.preventDefault();
}}, {{ passive: false }});

canvas.addEventListener('mouseleave', () => {{
  mouse.x = -9999; mouse.y = -9999;
}});

function step() {{
  const dx = cx - mouse.x;
  const dy = cy - mouse.y;
  const dist = Math.hypot(dx, dy);
  if (dist < threshold) {{
    const angle = Math.atan2(dy, dx);
    // move more strongly when closer
    const closeness = Math.min(1, (threshold - dist) / threshold);
    const moveAmount = speed * (0.4 + 1.6 * closeness);
    cx += Math.cos(angle) * moveAmount;
    cy += Math.sin(angle) * moveAmount;
    // clamp to canvas bounds
    cx = Math.max(radius, Math.min({canvas_w} - radius, cx));
    cy = Math.max(radius, Math.min({canvas_h} - radius, cy));
  }}
}}

function draw() {{
  ctx.clearRect(0,0,canvas.width, canvas.height);
  // background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0,0,canvas.width,canvas.height);
  // fake cursor
  ctx.beginPath();
  ctx.fillStyle = 'red';
  ctx.arc(cx, cy, radius, 0, Math.PI*2);
  ctx.fill();
  // optional mouse dot to show where your real mouse is
  if (showMouseDot && mouse.x > -500) {{
    ctx.beginPath();
    ctx.fillStyle = 'rgba(0,0,0,0.18)';
    ctx.arc(mouse.x, mouse.y, 6, 0, Math.PI*2);
    ctx.fill();
  }}
}}

function loop() {{
  if (autoplay) step();
  draw();
  requestAnimationFrame(loop);
}}

// start animation
loop();
</script>
</body>
</html>
"""

components.html(html, height=canvas_h + 20)
