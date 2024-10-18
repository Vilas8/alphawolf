import os
from dotenv import load_dotenv
from telegram.ext import Updater
from handlers import register_handlers
from db import init_db

# Load environment variables
load_dotenv()

TOKEN = os.getenv('BOT_API_TOKEN')

def main():
    init_db()  # Initialize the database
    
    # Set up the updater and dispatcher
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    register_handlers(dispatcher)

    # Start polling to receive messages
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
