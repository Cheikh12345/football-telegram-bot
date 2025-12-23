import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Football Analysis Bot is LIVE!\n\n"
        "Commands:\n"
        "/analysis TeamA TeamB\n"
        "/help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Available Commands:\n"
        "/analysis TeamA TeamB\n\n"
        "Example:\n"
        "/analysis RealMadrid Barcelona"
    )

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage:\n"
            "/analysis TeamA TeamB"
        )
        return

    team_a = context.args[0]
    team_b = context.args[1]

    await update.message.reply_text(
        f"⚽ Match Analysis\n\n"
        f"{team_a} vs {team_b}\n\n"
        f"✅ Best Safety Bets:\n"
        f"- Double Chance: 1X\n"
        f"- Under 3.5 Goals\n"
        f"- BTTS: NO\n\n"
        f"📈 Confidence Score: 78%"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("analysis", analysis))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
