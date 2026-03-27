import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(name)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello — I’m Claw. Send me a message.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_text = update.message.text.strip()
        logger.info("Received message: %s", user_text)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.output_text
        if not reply:
            reply = "I got your message, but I couldn't generate a reply."

        logger.info("Sending reply.")
        await update.message.reply_text(reply)

    except Exception as e:
        logger.exception("Message handling failed")
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    logger.info("Claw is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
