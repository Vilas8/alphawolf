from db import update_user_points

# Coin tap task
def complete_task(user_id):
    points = 10  # Points for tapping the coin
    update_user_points(user_id, points)

# Daily reward logic
def claim_daily_reward(update, context):
    user_id = update.message.from_user.id
    points = 20  # Points for claiming daily reward
    update_user_points(user_id, points)
    context.bot.send_message(chat_id=update.effective_chat.id, text="You claimed 20 points!")
