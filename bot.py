import os
import math
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway environment variable
DEFAULT_LANG = "en"

user_lang = {}

# ================= LANGUAGE =================
TEXT = {
    "en": {
        "welcome": "⚽ Welcome to Football Analysis Bot\n\nUse:\n/analysis TeamA TeamB\n/lang en|fr|ar",
        "analysis": "🔍 Match Analysis",
        "prob": "📊 Probabilities",
        "goals": "⚽ Goals Markets",
        "confidence": "🎯 Confidence Score",
        "scenario": "🔮 Likeliest Scenario",
        "risk": "⚠️ Risk Ranking",
        "final": "🧠 Final Conclusion",
        "safety": "🛡️ Best 3 Safety Bets"
    },
    "fr": {
        "welcome": "⚽ Bienvenue sur le bot d'analyse football\n\nUtilisez:\n/analysis ÉquipeA ÉquipeB",
        "analysis": "🔍 Analyse du Match",
        "prob": "📊 Probabilités",
        "goals": "⚽ Marchés de Buts",
        "confidence": "🎯 Indice de Confiance",
        "scenario": "🔮 Scénario Probable",
        "risk": "⚠️ Niveau de Risque",
        "final": "🧠 Conclusion Finale",
        "safety": "🛡️ 3 Paris les Plus Sûrs"
    },
    "ar": {
        "welcome": "⚽ مرحباً بك في بوت تحليل كرة القدم\n\nاستخدم:\n/analysis فريقA فريقB",
        "analysis": "🔍 تحليل المباراة",
        "prob": "📊 نسب الاحتمالات",
        "goals": "⚽ أسواق الأهداف",
        "confidence": "🎯 مؤشر الثقة",
        "scenario": "🔮 السيناريو المتوقع",
        "risk": "⚠️ مستوى المخاطرة",
        "final": "🧠 الخلاصة النهائية",
        "safety": "🛡️ أفضل 3 رهانات آمنة"
    }
}

def t(lang, key):
    return TEXT.get(lang, TEXT["en"])[key]

# ================= MODEL =================
def match_probabilities():
    home = 0.56
    draw = 0.24
    away = 0.20
    return home, draw, away

def goal_markets():
    over25 = 0.63
    btts = 0.60
    return over25, btts

def confidence_score(home, over25, btts):
    score = int((home * 40 + over25 * 35 + btts * 25))
    return min(100, score)

# ================= COMMANDS =================
def start(update, context):
    lang = user_lang.get(update.effective_chat.id, DEFAULT_LANG)
    update.message.reply_text(t(lang, "welcome"))

def lang_cmd(update, context):
    if not context.args:
        update.message.reply_text("Use /lang en | fr | ar")
        return
    choice = context.args[0].lower()
    if choice in ["en", "fr", "ar"]:
        user_lang[update.effective_chat.id] = choice
        update.message.reply_text(f"Language set to {choice}")
    else:
        update.message.reply_text("Available: en, fr, ar")

def analysis(update, context):
    lang = user_lang.get(update.effective_chat.id, DEFAULT_LANG)

    if len(context.args) < 2:
        update.message.reply_text("Usage:\n/analysis TeamA TeamB")
        return

    home_team = context.args[0]
    away_team = context.args[1]

    home, draw, away = match_probabilities()
    over25, btts = goal_markets()
    conf = confidence_score(home, over25, btts)

    scenario = "Goals expected" if over25 > home else "Tactical match"
    conclusion = "Goals market safer than result" if over25 > home else "Result market playable"

    message = f"""
{t(lang, "analysis")}
*{home_team} vs {away_team}*

{t(lang, "prob")}
Home: {int(home*100)}%
Draw: {int(draw*100)}%
Away: {int(away*100)}%

{t(lang, "goals")}
Over 2.5: {int(over25*100)}%
BTTS: {int(btts*100)}%

{t(lang, "confidence")}: *{conf}/100*

{t(lang, "scenario")}
{scenario}

{t(lang, "risk")}
LOW: Goals
MEDIUM: BTTS
HIGH: Result

{t(lang, "final")}
{conclusion}

{t(lang, "safety")}
1️⃣ Over 1.5 Goals  
2️⃣ BTTS YES  
3️⃣ Home Double Chance
"""
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

# ================= MAIN =================
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("lang", lang_cmd))
    dp.add_handler(CommandHandler("analysis", analysis))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
