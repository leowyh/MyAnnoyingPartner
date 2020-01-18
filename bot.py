from telegram.ext import CommandHandler, Updater
from telegram import ChatAction, ParseMode
from datetime import datetime
import json
import os
import requests
import logging

# Initialise logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load bot token
with open('token.ini', 'r') as file: # Specific bot token created by Bot Father saved in the token.ini file
    BOT_TOKEN = file.read()

# Create the bot
updater = Updater(token=BOT_TOKEN, use_context=True) # Construct bot

# Load persistent state
if os.path.isfile('data.txt'):
    with open('data.txt', 'r') as file:
        counter_dict = json.load(file) # Load pre-existing stats if exist, otherwise create new counter dictionary to keep track of counter variable per unique user
else:
    counter_dict = {}

# Add /start handler
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello {update.effective_message.chat.first_name}! Type /quote to receive the quote of the day.'
    )

# Add /quote handler
def quote(update, context):
    # Update /quote count
    user_key = str(update.effective_chat.id)
    count = counter_dict.get(user_key, 0) + 1
    counter_dict[user_key] = count

    # Send thinking message
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hmm...let me think...'
    )

    # Send typing status (telegram xxx is typing...)
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    # Generate image url
    img_url = f'https://picsum.photos/seed/{datetime.now()}/500'

    # Fetch quote
    response = requests.get('https://quotable.dev/random')
    if response.status_code != 200:
        # Document not found
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Hmm, got nothing on me at the moment. Try again later.'
        )
        return

    random_quote = response.json() # Get random quote from request
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img_url,
        caption=f'_{random_quote["content"]}_\n- _{random_quote["author"]}_\n\nYou have called /quote {count} time(s)!',
        parse_mode=ParseMode.MARKDOWN # Changes ability to format printed text
    )

updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler(
    CommandHandler('quote', quote)
)

# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()

# Dump persistent state
with open('data.txt', 'w') as file:
    json.dump(counter_dict, file)

print('Bot stopped!')