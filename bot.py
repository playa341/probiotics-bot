import os
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("8962415977:AAFTccn6BrU5vqEahg5PJIlf7SGJHE65GJ0")

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)
    await update.message.reply_text("Привет! ✅ Ты подписан на напоминание в 15:00 про пробиотики ❤️")

async def remind_all(context: ContextTypes.DEFAULT_TYPE):
    if not users: return
    msg = "🕒 15:00!\n\nОлеся и все!\nВыпей пробиотики ❤️"
    for cid in list(users):
        try:
            await context.bot.send_message(chat_id=cid, text=msg)
        except:
            pass

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Подписано: {len(users)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.job_queue.run_daily(remind_all, time(hour=12, minute=0), days=range(7))
    print("Бот запущен на Render!")
    app.run_polling()

if __name__ == "__main__":
    main()
