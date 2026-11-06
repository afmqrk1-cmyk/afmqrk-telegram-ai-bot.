import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я AFM AI 🤖\nЗадавай любые вопросы!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": update.message.text}
            ]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception:
        await update.message.reply_text("Произошла ошибка. Попробуй позже.")

def main():
    app = Application.builder().token(
        os.getenv("BOT_TOKEN")
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
