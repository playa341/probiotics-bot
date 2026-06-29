import os
import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users.add(chat_id)
    logger.info(f"Новый пользователь: {chat_id}")
    await update.message.reply_text("Привет! ✅\nТы подписан на ежедневное напоминание в 15:00 ❤️")

async def remind_all(context: ContextTypes.DEFAULT_TYPE, is_test=False):
    if not users:
        logger.warning("Нет подписанных пользователей")
        return
    message = "🕒 ТЕСТОВОЕ НАПОМИНАНИЕ!\n\nОлеся и все подписанные!\nНе забудьте выпить пробиотики ❤️" if is_test else \
              "🕒 15:00!\n\nОлеся и все подписанные!\nНе забудьте выпить пробиотики ❤️"
    
    logger.info(f"Отправка {'тестового' if is_test else 'ежедневного'} напоминания {len(users)} пользователям")
    for chat_id in list(users):
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logger.error(f"Ошибка отправки {chat_id}: {e}")
            if "Forbidden" in str(e):
                users.discard(chat_id)

async def test_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await remind_all(context, is_test=True)
    await update.message.reply_text("Тестовое напоминание отправлено всем!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Сейчас подписано: {len(users)} человек")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("test", test_reminder))   # ← новая команда
    
    app.job_queue.run_daily(remind_all, time(hour=12, minute=0), days=range(7))
    
    logger.info("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
