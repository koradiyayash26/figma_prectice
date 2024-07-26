import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import httpx

BOT_TOKEN = '7026601318:AAFLb8ySkLt2_tkgNWBrZ0p1LAVp-ZGlWcM'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /date to get the current date or /btc to get the current Bitcoin price.')

async def date_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_date = datetime.now().strftime('%Y-%m-%d')
    await update.message.reply_text(f"Today's date is: {current_date}")

async def btc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        # Print raw API response for debugging
        logging.info(f"API Response: {data}")
        btc_price = data['bitcoin']['usd']
        # Format the price to include more decimal places
        formatted_price = f"${btc_price:,.2f}"
        await update.message.reply_text(f"The current price of Bitcoin (BTC) is: {formatted_price}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('date', date_command))
    application.add_handler(CommandHandler('btc', btc_command))

    application.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()
