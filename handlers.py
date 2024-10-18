from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

from db import add_user, get_user_points, update_user_points
from tasks import complete_task, claim_daily_reward

# Function to handle when a user taps the coin
def coin_tap(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Acknowledge the tap to stop the loading animation

    user_id = query.from_user.id
    # Fetch current points and update the user's points
    current_points = get_user_points(user_id)
    new_points = current_points + 1  # Increment points by 1 (adjust logic as needed)
    update_user_points(user_id, new_points)

    # Send an updated message
    query.edit_message_text(text=f"You tapped the coin and now have {new_points} points!")

# Register handlers here
def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('register', register, pass_args=True))
    dispatcher.add_handler(CommandHandler('points', points))
    dispatcher.add_handler(CommandHandler('daily', claim_daily_reward))
    dispatcher.add_handler(CallbackQueryHandler(coin_tap, pattern='tap_coin'))

# Start command
def start(update, context):
    # Button to tap the coin
    button = [[InlineKeyboardButton("🪙 Tap the Coin!", callback_data='tap_coin')]]
    reply_markup = InlineKeyboardMarkup(button)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Tap the coin to earn points!", reply_markup=reply_markup)

# Register command
def register(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    referrer = context.args[0] if context.args else None
    add_user(user_id, user_name, referrer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome {user_name}, you are registered!")

# Points command
def points(update, context):
    user_id = update.message.from_user.id
    user_points = get_user_points(user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"You have {user_points} points.")
