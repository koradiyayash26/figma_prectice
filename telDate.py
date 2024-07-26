import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

BOT_TOKEN = '7026601318:AAFLb8ySkLt2_tkgNWBrZ0p1LAVp-ZGlWcM'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /date to get the current date.')

async def date_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_date = datetime.now().strftime('%Y-%m-%d')
    await update.message.reply_text(f"Today's date is: {current_date}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('date', date_command))

    application.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()
