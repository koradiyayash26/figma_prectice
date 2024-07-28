import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
import httpx

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define conversation states
ID, VS_TOKEN = range(2)

# Replace with your bot's token
BOT_TOKEN = '7026601318:AAFLb8ySkLt2_tkgNWBrZ0p1LAVp-ZGlWcM'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""
    await update.message.reply_text('Hello! Use /price to get the price of a token. Please provide the token ID when prompted.')

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /price command."""
    await update.message.reply_text('Please enter the token ID:')
    return ID

async def handle_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle token ID input."""
    token_id = update.message.text.strip()
    await update.message.reply_text(f'Please enter the vsToken for {token_id}:')
    context.user_data['token_id'] = token_id  
    return VS_TOKEN

async def handle_vs_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle vsToken input and fetch price."""
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

                # Create buttons
                keyboard = [
                    [InlineKeyboardButton("Buy", callback_data='buy')],
                    [InlineKeyboardButton("Sell", callback_data='sell')],
                    [InlineKeyboardButton("Position", callback_data='position')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    f"Token ID: {token_id}\n"
                    f"Based on:\n"
                    f"{vs_token_symbol}\n"
                    f"Price: {formatted_price}",
                    reply_markup=reply_markup
                )
                context.user_data['vs_token_symbol'] = vs_token_symbol
                context.user_data['formatted_price'] = formatted_price
                # Set default swap value
                context.user_data['swap_value'] = '0.5'
            else:
                await update.message.reply_text("Invalid token ID or vsToken, or price not available. Please try again.")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            await update.message.reply_text("Failed to retrieve the price. Please try again later.")
    
    return ConversationHandler.END

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()

    choice = query.data
    token_id = context.user_data.get('token_id', '')
    vs_token_symbol = context.user_data.get('vs_token_symbol', '')
    formatted_price = context.user_data.get('formatted_price', '')
    swap_value = context.user_data.get('swap_value', '0.5')  # Default to 0.5 if not set

    if choice == 'buy':
        # Show swap options with default (0.5) pre-selected
        keyboard = [
            [InlineKeyboardButton("✅ Swap 0.5", callback_data='swap_0.5') if swap_value == '0.5' else InlineKeyboardButton("Swap 0.5", callback_data='swap_0.5')],
            [InlineKeyboardButton("✅ Swap 1", callback_data='swap_1') if swap_value == '1' else InlineKeyboardButton("Swap 1", callback_data='swap_1')],
            [InlineKeyboardButton("Confirm Buy", callback_data='confirm_buy')],
            [InlineKeyboardButton("Back", callback_data='back_to_options')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Token ID: {token_id}\n"
                 f"Based on: {vs_token_symbol}\n"
                 f"Price: {formatted_price}\n"
                 f"Select swap option:",
            reply_markup=reply_markup
        )
    elif choice == 'sell':
        await query.edit_message_text(text="You chose to sell the token.")
    elif choice == 'position':
        await query.edit_message_text(text="You chose to check the position.")
    elif choice == 'back_to_options':
        keyboard = [
            [InlineKeyboardButton("Buy", callback_data='buy')],
            [InlineKeyboardButton("Sell", callback_data='sell')],
            [InlineKeyboardButton("Position", callback_data='position')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Token ID: {token_id}\n"
                 f"Based on: {vs_token_symbol}\n"
                 f"Price: {formatted_price}",
            reply_markup=reply_markup
        )
    elif choice.startswith('swap_'):
        swap_value = choice.split('_')[1]
        context.user_data['swap_value'] = swap_value

        # Create the buttons with the tick mark on the selected swap option
        keyboard = [
            [InlineKeyboardButton("✅ Swap 0.5", callback_data='swap_0.5') if swap_value == '0.5' else InlineKeyboardButton("Swap 0.5", callback_data='swap_0.5')],
            [InlineKeyboardButton("✅ Swap 1", callback_data='swap_1') if swap_value == '1' else InlineKeyboardButton("Swap 1", callback_data='swap_1')],
            [InlineKeyboardButton("Confirm Buy", callback_data='confirm_buy')],
            [InlineKeyboardButton("Back", callback_data='back_to_options')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Token ID: {token_id}\n"
                 f"Based on: {vs_token_symbol}\n"
                 f"Price: {formatted_price}\n"
                 f"Swap option: {swap_value} {vs_token_symbol}\n"
                 f"Confirm your buy:",
            reply_markup=reply_markup
        )
    elif choice == 'confirm_buy':
        swap_value = context.user_data.get('swap_value', '0.5')  # Default to 0.5 if not set
        
        # Notify user about the purchase
        await query.edit_message_text(
            text=f"You have bought {swap_value} {vs_token_symbol} of token {token_id}.",
            reply_markup=None  # Hide the buttons
        )

        # Log to confirm the action
        logger.info(f"User confirmed buy: {swap_value} {vs_token_symbol} of token {token_id}")

        # Optionally clear user data if necessary
        context.user_data.clear()  # Clear all user data or selectively clear if needed

        # Optional: Log state of context user data for debugging
        logger.info(f"User data after buy confirmation: {context.user_data}")

def main():
    """Run the bot."""
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
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()


