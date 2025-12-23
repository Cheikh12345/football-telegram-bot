import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# -------- Commands --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Football Prediction Bot is LIVE!\n\n"
        "Commands:\n"
        "/analysis TeamA TeamB\n"
        "/help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Available commands:\n"
        "/analysis TeamA TeamB"
    )

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage:\n/analysis TeamA TeamB"
        )
        return

    team_a = context.args[0]
    team_b = context.args[1]

    await update.message.reply_text(
        f"⚽ Match Analysis\n\n"
        f"{team_a} vs {team_b}\n\n"
        f"✅ Best Safety Bets:\n"
        f"- Double Chance (1X)\n"
        f"- Under 3.5 Goals\n"
        f"- BTTS: NO\n\n"
        f"📊 Confidence: 78%"
    )

# -------- Main --------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("analysis", analysis))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
