import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 15 līmeņi (secībā)
LEVELS = [
    {
        "code": "SOFIJA",
        "reply": (
            "✅ Saņēmējs identificēts!\n\n"
            "Sūtījuma meklēšana ir aktivizēta.\n\n"
            "Skaties šo video ar nākamo pavedienu:\n"
            "https://www.youtube.com/shorts/rihy0PjmtfM\n\n"
            "Kurjera maršrutā reģistrēta izkraušanās pietura:\n"
            "📍 Balvi, Robežiela X\n\n"
            "Nosaki, kāda iestāde atrodas šajā adresē, "
            "un ievadi tās nosaukumu atbalsta botā kā KODU."
        )
    },
    {
        "code": "CSDD",
        "reply": (
            "🚗 Labi, braucam tālāk…\n\n"
            "Jā, pareizi — tas bija CSDD.\n"
            "Pēc tam DPD kurjers devās ceļā uz Balvu pilsētas estrādes parku.\n\n"
            "🧠 Atceros tikai vienu detaļu:\n"
            "pie parka bija ēka ar ļoti košu, 🎨 RAIBU 🎨 uzrakstu.\n"
            "🟥 🟨 🟦 🟥 🟨\n\n"
            "🎥 Noskaties video un atrodi kodu:\n"
            "https://youtube.com/shorts/e_KY9mUWtMw?si=jp_Jmd70M3HvM1tj\n\n"
            "Kad zini atbildi — ieraksti to šeit.\n\n"
            "Veiksmi! 🙂"
        )
    },
    {
        "code": "JOKER",
        "reply": (
            "☕ Pareizi — JOKER!\n\n"
            "Tālāk atceros, ka tā bija degvielas uzpildes stacija, kur ar LIDL aplikāciju\n"
            "var dabūt atlaidi degvielai,\n"
            "un katra 8. kafija ir BEZMAKSAS.\n\n"
            "🚗 Braucam tālāk uz nākamo pieturu…\n"
            "🎥 https://youtube.com/shorts/Kzg0QCfPpME?si=V4ZnIvrwYmVqxyFI\n\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "code": "VIADA",
        "reply": (
            "☕ Pareizi — VIADA!\n\n"
            "Noskaties video 👇\n"
            "https://youtube.com/shorts/yjPMw0WxBrs?si=X6fV-eWSC4PKDjQV\n\n"
            "Tālāk aizvedu nākamo paciņu uz Brīvības ielu 60.\n"
            "Atceros, ka tur bija smukas meitenes\n"
            "un ļoti garšīgi smaržoja pēc ēdiena…\n\n"
            "🎱 Kur es biju?\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "code": "ZEBRA",
        "reply": (
            "🍕 Pareizi — ZEBRA!\n\n"
            "Čikitas pica tiešām ir visgaršīgākā.\n\n"
            "🎥 Noskaties video 👇\n"
            "https://www.youtube.com/shorts/zsI9D3bbVdU\n\n"
            "Tālāk bija jāved daudz un dažādi saldumi\n"
            "uz jauno veikalu Balvos.\n\n"
            "🤔 Neatceros nosaukumu,\n"
            "bet logo bija ar Bigfoot.\n\n"
            "🏪 Kā sauc šo veikalu?\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "code": "BIGIJS",
        "reply": (
            "🍬 Pareizi — BIGIJS!\n\n"
            "🎥 Noskaties video 👇\n"
            "https://youtube.com/shorts/41QOZD5Ys3Q?si=wx2jY3J3v6WYLaGy\n\n"
            "Tālāk DPD kurjers devās uz Redakciju\n"
            "Teātra ielā 8.\n\n"
            "🤔 Neatceros, kā tā saucas tagad,\n"
            "bet agrāk to sauca par \"Balvu Taisnība\".\n\n"
            "📰 Kāds ir pareizais nosaukums?\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "code": "VADUGUNS",
        "reply": (
            "📰 Pareizi!\n\n"
            "Redakcija palūdza DPD kurjeram\n"
            "aizvest laikrakstu *Vaduguns*\n"
            "uz pasta nodaļu Brīvības ielā 57.\n\n"
            "🤔 Bet kā saucās tā ēka?\n\n"
            "🎥 Noskaties video un atrodi atbildi 👇\n"
            "https://youtube.com/shorts/pbbLwqjo67Y?si=CLJecX2Utd7hHXXQ\n\n"
            "🏬 Ieraksti ēkas nosaukumu (bez garumzīmēm) 🙂"
        )
    },
    {
        "codes": ["PLANETA", "PLANĒTA"],
        "reply": (
            "📬 Pareizi — PLANĒTA!\n\n"
            "🎥 Noskaties video 👇\n"
            "https://youtube.com/shorts/IUFZCLGnB8k?si=JCvUdRaYUSAKPK8t\n\n"
            "No pasta nodaļas DPD kurjers saņēma vēstuli,\n"
            "kas bija jānogādā Balvu maizniekam.\n\n"
            "🤔 Adresi neatceros,\n"
            "bet ielas nosaukums bija tāds pats\n"
            "kā aizslēgtajam veikalam.\n\n"
            "📍 Kā sauc šo ielu?\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "codes": ["LIEPA", "LIEPU", "LIEPAS"],
        "reply": (
            "✅ Pareizi!\n\n"
            "🚒 Nākamais uzdevums:\n"
            "DPD kurjeram jāaizved ugunsdzēšamais aparāts uz Ezera ielu.\n\n"
            "Pagalmā stāv veca sarkanbalta padomju laika kravas automašīna ZIL-157.\n"
            "Parasti uz šāda auto ir liels numurs, ko redz gandrīz visur.\n\n"
            "🎥 Noskaties video 👇\n"
            "https://youtube.com/shorts/edYvbWNLils?si=k4ShfkhvTfTfv2Of\n\n"
            "🔎 Atrodi šo numuru uz auto vai citur un ievadi to kā kodu.\n\n"
            "Veiksmi! 🙂"
        )
    },
    {
        "code": "112",
        "reply": (
            "🚒 Pareizi — 112!\n\n"
            "Ugunsdzēsēju priekšnieks palūdza DPD kurjeram\n"
            "aizvest mapīti uz Dārza ielu 2.\n\n"
            "🧠 Atceros tikai vienu detaļu:\n"
            "tur bija kautkāda sāls istaba.\n\n"
            "🎥 Noskaties video 👇\n"
            "https://youtube.com/shorts/YHfm3E7dVN4?si=9FtnDAfPJ-z3uNSm\n\n"
            "🔎 Kā sauc šo vietu? 🏊‍♂️\n"
            "Ievadi nākamo kodu 🙂"
        )
    },
    {
        "code": "BASEINS",
        "reply": (
            "🏊‍♂️ Pareizi — BASEINS!\n\n"
            "DPD kurjers ieradās baseinā,\n"
            "kur meitenes atpūtās SPA hidromasāžas baseinā.\n\n"
            "Kurjers jautāja:\n"
            "— Kur ir treneris?\n\n"
            "Atbilde bija vienkārša:\n"
            "— Viņš ir aizbraucis pusdienās.\n\n"
            "🧠 Vēl viena detaļa palika prātā:\n"
            "netālu stāv T veida ūdenstornis,\n"
            "un pašā augšā — gailis 🐓\n\n"
            "Tur esot arī labs pusdienu piedāvājums no 12-15 darba dienās!\n\n"
            "🎥 Noskaties video un atrodi nākamo kodu 👇\n"
            "https://www.youtube.com/shorts/AeppiTnW1rc\n\n"
            "Ievadi atbildi 🙂"
        )
    },
    {
    "code": "KURETI",
    "reply": (
        "✅ Pareizi — KURETI!\n\n"
        "Kureti darbinieki iedeva DPD kurjeram projektoru 📽️\n"
        "un palūdza to nogādāt uz veco kinoteātri **Aurora**.\n\n"
        "🤔 Viņi tikai vairs neatcerējās, kā tagad saucas tā vieta\n"
        "(turpat blakus ir elektro uzlādes stacija ⚡).\n\n"
        "👀 Skatoties apkārt (un pat **zem kājām**!),\n"
        "🍍uz bruģa ir uzraksts ar vienu vārdu…\n\n"
        "🎥 Noskaties video un atrodi jauno nosaukumu 🍍👇\n"
        "🍍https://youtube.com/shorts/OODnC_vMKto?si=smvrCcQOeiaf6VIK \n\n"
        "🔑 Kad zini atbildi — ievadi kodu.\n"
        "Padoms: kods ir 1 vārds (bez garumzīmēm)."
    )
},
    {
        "code": "Ananass",
        "reply": "✅ Pareizi! Video #14: https://www.youtube.com/watch?v=KxJ8n4B7G3g\n\nIevadi nākamo kodu 🙂"
    },
    {
        "code": "KODS15",
        "reply": "🏁 Apsveicu! Finišs! 🎉 Video #15: https://www.youtube.com/watch?v=uelHwf8o7_U\n\nBalva tevi gaida 🙂"
    },
]

def normalize(text: str) -> str:
    return text.strip().upper()

def expected_codes_for_level(level_obj: dict) -> list[str]:
    """Atgriež sarakstu ar derīgiem kodiem konkrētajam līmenim."""
    if "codes" in level_obj:
        return [normalize(c) for c in level_obj["codes"]]
    return [normalize(level_obj["code"])]

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

    level_obj = LEVELS[level]
    valid_codes = expected_codes_for_level(level_obj)

    if user_text in valid_codes:
        await update.message.reply_text(level_obj["reply"])
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
