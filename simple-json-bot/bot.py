from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# Load data from db.json file
with open("db.json") as f:
    bot_data = json.load(f)

# Telegram bot token (replace with your own token)
BOT_TOKEN = "6529582468:AAHyKmp8yvfen4sbDWTlEvfpxgtHYWhV9xQ"

def start(update: Update, context: CallbackContext):
    for bot_command_data in bot_data:
        if "BotName" in bot_command_data:
            bot_name = bot_command_data["BotName"]
            update.message.reply_text(f"Hi! I'm {bot_name}, Use /list command to explore.")
            break
    else:
        update.message.reply_text("Hi! I'm your bot.")  # If "BotName" is not found in the db.json file

def format_buttons(buttons_data):
    buttons_layout = []
    for button_data in buttons_data:
        button_row = [InlineKeyboardButton(button_name, url=button_url) for button_name, button_url in button_data.items()]
        buttons_layout.append(button_row)
    return buttons_layout

def handle_command(update: Update, context: CallbackContext):
    command = update.message.text.strip()
    for bot_command_data in bot_data:
        if "commands" in bot_command_data and command in bot_command_data["commands"]:
            message = bot_command_data.get("message", "")
            image_url = bot_command_data.get("image", None)
            buttons_data = bot_command_data.get("buttons", [])

            # Create an InlineKeyboardMarkup object with the buttons
            reply_markup = InlineKeyboardMarkup(format_buttons(buttons_data))

            # Send the message and buttons
            if message:
                if image_url and image_url != "none":
                    # Send the image with the message and buttons
                    update.message.reply_photo(photo=image_url, caption=message, reply_markup=reply_markup)
                else:
                    # Send the message and buttons without the image
                    update.message.reply_text(message, reply_markup=reply_markup)

            # Break the loop once the command is found
            break
    else:
        update.message.reply_text("I'm sorry, I don't understand that command. Type /about, /help, or /dev to get started.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Add command handlers dynamically for each command in db.json
    for bot_command_data in bot_data:
        commands = bot_command_data.get("commands", [])
        for command in commands:
            dp.add_handler(CommandHandler(command[1:], handle_command))

    # Add the start command handler
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
