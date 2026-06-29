import os
import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)
    await update.message.reply_text("приветик! ✅ теперь подписана на напоминание в 15:00 про то что тебе БЛЯДЬ НАДО ВЫПИТЬ пробиотики.")

async def remind_all(context: ContextTypes.DEFAULT_TYPE):
    if not users:
        return
    message = "🕒 15:00!\n\nОлеся!\nВыпей пробиотики, пожалуйста ❤️"
    for chat_id in list(users):
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except:
            pass

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await remind_all(context)
    await update.message.reply_text("Тест отправлен!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Подписано: {len(users)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("status", status))
    
    app.job_queue.run_daily(remind_all, time(hour=12, minute=0), days=range(7))
    
    logger.info("✅ Бот запущен полностью!")
    app.run_polling()

if __name__ == "__main__":
    main()
