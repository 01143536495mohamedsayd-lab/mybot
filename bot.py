import os, time
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
    models = ["gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemini-1.5-flash"]
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"رد كصاحب جدع وودود بالعامية المصرية: {text}"
            )
            if response.text:
                await update.message.reply_text(response.text)
                return
        except Exception as e:
            print(f"فشل {model_name}: {e}")
            time.sleep(2)
            continue
    await update.message.reply_text("جوجل عليها ضغط دلوقتي، جرب تاني بعد دقيقة 🙏")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("البوت قيد التشغيل...")
    app.run_polling()

if __name__ == "__main__":
    main()
