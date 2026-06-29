import os
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)
    await update.message.reply_text(
        "Привет! ✅\n\nТы подписан на ежедневное напоминание в 15:00 про пробиотики ❤️"
    )

async def remind_all(context: ContextTypes.DEFAULT_TYPE):
    if not users:
        return
    message = "🕒 15:00!\n\nОлеся и все подписанные!\nНе забудьте выпить пробиотики ❤️"
    for chat_id in list(users):
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except:
            pass

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Сейчас подписано: {len(users)} человек")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    
    app.job_queue.run_daily(remind_all, time(hour=12, minute=0), days=range(7))
    
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
