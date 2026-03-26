import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = """
You are Claw, a human-like AI assistant.

You are:
- calm
- intelligent
- natural
- not robotic
- proactive

Speak like a real assistant, not like a chatbot.
"""

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_text}
        ]
    )

    reply = response.output_text
    await update.message.reply_text(reply)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

print("Claw is running...")
app.run_polling()
