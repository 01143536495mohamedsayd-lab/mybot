import os
import telebot
import google.generativeai as genai

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا بيك، انا بوت ذكاء اصطناعي، اسألني اي حاجة")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "حصل مشكلة، جرب تاني")

bot.polling()
