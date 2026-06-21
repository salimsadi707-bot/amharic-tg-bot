import os
import requests

from flask import Flask, request
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

def ask_gemini(user_text):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
አንተ በአማርኛ የምትነጋገር AI ረዳት ነህ።

- ሁልጊዜ በአማርኛ መልስ
- ግልጽ እና ጠቃሚ መልስ ስጥ

ተጠቃሚ:
{user_text}
"""
                    }
                ]
            }
        ]
    }

    try:
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return "ይቅርታ፣ ስህተት ተፈጥሯል።"

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    try:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        answer = ask_gemini(text)

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": answer
            }
        )

    except Exception as e:
        print(e)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
