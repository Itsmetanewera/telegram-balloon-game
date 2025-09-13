import logging
from flask import Flask, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from threading import Thread

# ------------------- CONFIG -------------------
BOT_TOKEN = "8324595920:AAG52dCic01MFnolDrlVn_s-_nmEHvhBO3w"  # Вставь токен бота
OWNER_WALLET = "UQCYyfyGwxNT9QjICDeBvxxQ3uTv3hvehuK4UcyDbU-c38at"  # Вставь TON кошелек
WEBAPP_URL = "https://telegram-balloon-game.onrender.com"  # URL Render после деплоя

# ------------------- FLASK APP -------------------
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Balloon Game</title>
<style>
body { margin: 0; overflow: hidden; background: #222; font-family: sans-serif; }
canvas { display: block; margin: auto; }
#depositButton {
    position: absolute; top: 10px; right: 10px;
    background: #0a74da; color: #fff;
    border: none; border-radius: 50%;
    width: 50px; height: 50px; font-size: 30px; cursor: pointer;
}
#depositBox {
    position: absolute; top: 70px; right: 10px;
    background: #fff; color: #000;
    padding: 10px; border-radius: 8px;
    display: none; z-index: 100; width: 200px;
}
</style>
</head>
<body>
<button id="depositButton">+</button>
<div id="depositBox">
    <h3>Buy Balloons</h3>
    <p>Send TON to wallet:</p>
    <p><b>{{ wallet }}</b></p>
    <p>1 TON = 1 Balloon</p>
    <button onclick="simulateDeposit()">I've Paid</button>
</div>
<canvas id="gameCanvas"></canvas>

<script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
<script>
const { Engine, Render, Runner, Bodies, Composite } = Matter;
const canvas = document.getElementById('gameCanvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const engine = Engine.create();
const world = engine.world;

const render = Render.create({
    canvas: canvas,
    engine: engine,
    options: { width: canvas.width, height: canvas.height, wireframes: false, background: '#222' }
});

// Стены
const ground = Bodies.rectangle(canvas.width/2, canvas.height, canvas.width, 40, { isStatic: true });
const leftWall = Bodies.rectangle(0, canvas.height/2, 40, canvas.height, { isStatic: true });
const rightWall = Bodies.rectangle(canvas.width, canvas.height/2, 40, canvas.height, { isStatic: true });
Composite.add(world, [ground, leftWall, rightWall]);

// Падение шариков блокируется до депозита
let canDrop = false;

function addBalloon() {
    const balloon = Bodies.circle(Math.random()*canvas.width, 50, 30, {
        restitution: 0.9,
        render: { fillStyle: 'hsl(' + Math.random()*360 + ',70%,50%)' }
    });
    Composite.add(world, balloon);
}

// Кнопка депозит
document.getElementById('depositButton').onclick = () => {
    const box = document.getElementById('depositBox');
    box.style.display = box.style.display === 'none' ? 'block' : 'none';
}

// Симуляция депозита
function simulateDeposit() {
    canDrop = true;
    alert("Deposit confirmed! Balloons will start falling.");
}

// Таймер добавления шариков
setInterval(() => {
    if(canDrop) addBalloon();
}, 2000);

Render.run(render);
Runner.run(Runner.create(), engine);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, wallet=OWNER_WALLET)

# ------------------- TELEGRAM BOT -------------------
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎈 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    await update.message.reply_text(
        "Добро пожаловать! Покупай шарики за TON и играй 🎮",
        reply_markup=InlineKeyboardMarku_

