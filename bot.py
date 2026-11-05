import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا بيك يا صاحبي ❤️ انا بوت ذكي، اسألني اي حاجة!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"رد بالعامية المصرية وبطريقة صاحب جدع وودود: {text}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("حصل مشكلة صغيرة، جرب تاني")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
