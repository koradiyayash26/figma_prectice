import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import httpx

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

ID, VS_TOKEN = range(2)

BOT_TOKEN = '7026601318:AAFLb8ySkLt2_tkgNWBrZ0p1LAVp-ZGlWcM'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /price to get the price of a token. Please provide the token ID when prompted.')

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Please enter the token ID:')
    return ID

async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    token_id = update.message.text.strip()
    
    
    await update.message.reply_text(f'Please enter the vsToken for {token_id}:')
    context.user_data['token_id'] = token_id  
    return VS_TOKEN

async def handle_vs_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    vs_token = update.message.text.strip()
    token_id = context.user_data.get('token_id', '')

    url = f'https://price.jup.ag/v6/price?ids={token_id}&vsToken={vs_token}'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            
            logger.info(f"API Response: {data}")
            
            if 'data' in data and token_id in data['data']:
                price = data['data'][token_id]['price']
                vs_token_symbol = data['data'][token_id]['vsTokenSymbol']
                formatted_price = f"${price:,.2f}"
                await update.message.reply_text(   f"Token ID: {token_id} \n"
                    f" \n Based on: \n "
                    f"{vs_token_symbol}\n"
                    f"Price: {formatted_price}"
                )
            else:
                await update.message.reply_text("Invalid token ID or vsToken, or price not available. Please try again.")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            await update.message.reply_text("Failed to retrieve the price. Please try again later.")
    
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('price', price_command)],
        states={
            ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id)],
            VS_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vs_token)],
        },
        fallbacks=[],
    )
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(conversation_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
