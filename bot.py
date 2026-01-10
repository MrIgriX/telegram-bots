import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 15 līmeņi (secībā)
LEVELS = [
    {"code": "Sofija", "reply": "✅ Saņēmējs identificēts! Lai turpinātu paciņas meklēšanu, noskaties šo video #1: https://www.youtube.com/shorts/rihy0PjmtfM\n\nIevadi nākamo kodu 🙂"},
    {"code": "CSDD",  "reply": "✅ Super! Video #2: https://www.youtube.com/watch?v=9bZkp7q19f0\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS3",  "reply": "✅ Lieliski! Video #3: https://www.youtube.com/watch?v=3JZ_D3ELwOQ\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS4",  "reply": "✅ Pareizi! Video #4: https://www.youtube.com/watch?v=kJQP7kiw5Fk\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS5",  "reply": "✅ Pareizi! Video #5: https://www.youtube.com/watch?v=L_jWHffIx5E\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS6",  "reply": "✅ Pareizi! Video #6: https://www.youtube.com/watch?v=fJ9rUzIMcZQ\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS7",  "reply": "✅ Pareizi! Video #7: https://www.youtube.com/watch?v=CevxZvSJLk8\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS8",  "reply": "✅ Pareizi! Video #8: https://www.youtube.com/watch?v=60ItHLz5WEA\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS9",  "reply": "✅ Pareizi! Video #9: https://www.youtube.com/watch?v=2Vv-BfVoq4g\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS10", "reply": "✅ Pareizi! Video #10: https://www.youtube.com/watch?v=YQHsXMglC9A\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS11", "reply": "✅ Pareizi! Video #11: https://www.youtube.com/watch?v=OPf0YbXqDm0\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS12", "reply": "✅ Pareizi! Video #12: https://www.youtube.com/watch?v=hT_nvWreIhg\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS13", "reply": "✅ Pareizi! Video #13: https://www.youtube.com/watch?v=JGwWNGJdvx8\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS14", "reply": "✅ Pareizi! Video #14: https://www.youtube.com/watch?v=KxJ8n4B7G3g\n\nIevadi nākamo kodu 🙂"},
    {"code": "KODS15", "reply": "🏁 Apsveicu! Finišs! 🎉 Video #15: https://www.youtube.com/watch?v=uelHwf8o7_U\n\nBalva tevi gaida 🙂"},
]

def normalize(text: str) -> str:
    return text.strip().upper()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["level"] = 0
    await update.message.reply_text(
        "DPD atbalsta bots 📦\n\n"
        "Sveicināti!\n"
        "Sistēmas traucējumu dēļ sūtījums nav automātiski piesaistīts saņēmējam.\n\n"
        "Lūdzu, noskatieties šo video ar papildu informāciju:\n"
        "https://youtube.com/shorts/_lCWHaQCIfI\n\n"
        "Pēc video noskatīšanās ievadiet sūtījuma saņēmēja vārdu, "
        "lai aktivizētu paciņas meklēšanu."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["level"] = 0
    await update.message.reply_text("Sākam no jauna. Ievadi sūtījuma saņēmēja vārdu 🙂")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = normalize(update.message.text)
    level = context.user_data.get("level", 0)

    if level >= len(LEVELS):
        await update.message.reply_text(
            "Spēle jau ir pabeigta 🎉\n"
            "Ja gribi sākt no jauna, raksti /reset"
        )
        return

    expected_code = normalize(LEVELS[level]["code"])

    if user_text == expected_code:
        await update.message.reply_text(LEVELS[level]["reply"])
        context.user_data["level"] = level + 1
    else:
        await update.message.reply_text("❌ Nepareizs kods. Pamēģini vēlreiz!")

def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN nav atrasts Railway mainīgajos (Variables).")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bots darbojas (Railway).")
    app.run_polling()

if __name__ == "__main__":
    main()
