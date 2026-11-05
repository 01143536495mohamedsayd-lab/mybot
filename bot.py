import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا بيك! اسألني اي حاجة ✨")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"رد كصاحب جدع وودود: {text}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"الخطأ هو: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("البوت قيد التشغيل...")
    app.run_polling()

if __name__ == "__main__":
    main()
