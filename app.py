import logging
from flask import Flask, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# ------------------- CONFIG -------------------
BOT_TOKEN = "8324595920:AAG52dCic01MFnolDrlVn_s-_nmEHvhBO3w"  # замените на токен вашего бота
OWNER_WALLET = "UQCYyfyGwxNT9QjICDeBvxxQ3uTv3hvehuK4UcyDbU-c38at"  # замените на ваш кошелек TON

# После деплоя на Render замените на URL вашего сервиса, например:
NGROK_URL = "https://telegram-balloon-game.onrender.com"

# ------------------- FLASK APP -------------------
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Balloon Game</title>
    <style>
        body { margin: 0; overflow: hidden; background: #222; }
        canvas { display: block; margin: auto; }
        #depositBox {
            position: absolute;
            top: 10px;
            left: 10px;
            background: #fff;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div id="depositBox">
        <h3>Buy Balloons</h3>
        <p>Send TON to wallet:</p>
        <p><b>{{ wallet }}</b></p>
        <p>Each balloon = 1 TON</p>
    </div>
    <canvas id="gameCanvas"></canvas>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
    <script>
        const { Engine, Render, Runner, Bodies, Composite } = Matter;

        const engine = Engine.create();
        const world = engine.world;

        const canvas = document.getElementById('gameCanvas');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const render = Render.create({
            canvas: canvas,
            engine: engine,
            options: { width: canvas.width, height: canvas.height, wireframes: false, background: '#222' }
        });

        // Walls
        const ground = Bodies.rectangle(canvas.width/2, canvas.height, canvas.width, 40, { isStatic: true });
        const leftWall = Bodies.rectangle(0, canvas.height/2, 40, canvas.height, { isStatic: true });
        const rightWall = Bodies.rectangle(canvas.width, canvas.height/2, 40, canvas.height, { isStatic: true });

        Composite.add(world, [ground, leftWall, rightWall]);

        // Add balloons
        function addBalloon(x, y) {
            let balloon = Bodies.circle(x, y, 30, {
                restitution: 0.9,
                render: { fillStyle: 'hsl(' + Math.random()*360 + ', 70%, 50%)' }
            });
            Composite.add(world, balloon);
        }

        // Spawn balloons every 2 seconds
        setInterval(() => {
            addBalloon(Math.random() * canvas.width, 50);
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
        [
            InlineKeyboardButton(
                "🎈 Играть",
                web_app=WebAppInfo(url=NGROK_URL)  # публичный URL Render
            )
        ]
    ]
    await update.message.reply_text(
        "Добро пожаловать! Покупай шарики за TON и играй 🎮",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Отправь TON на кошелек: {OWNER_WALLET}\n1 TON = 1 шарик")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    from threading import Thread

    def run_flask():
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    Thread(target=run_flask).start()

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("deposit", deposit))

    application.run_polling()
