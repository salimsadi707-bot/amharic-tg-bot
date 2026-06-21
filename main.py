import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = f"""
    አንተ በአማርኛ የምትነጋገር AI ረዳት ነህ።

    - ሁልጊዜ በአማርኛ መልስ
    - ግልጽ እና ጠቃሚ መልስ ስጥ

    ተጠቃሚ:
    {user_text}
    """

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    r = requests.post(url, json=payload)

    try:
        answer = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        answer = "ይቅርታ፣ ስህተት ተፈጥሯል።"

    await update.message.reply_text(answer)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

app.run_polling()