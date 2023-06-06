from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your API credentials
API_ID = 2727928
API_HASH = '8e959f089c05109d1c5f8ea4aec8af21'
BOT_TOKEN = '5878531007:AAFOrzBsytaPFWBAaxErx0W4Coz4jKLdxio'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Function to handle incoming media messages
@app.on_message(filters.media)
def handle_media(client, message):
    # Check if the message is an edited message
    # if the edit_date property of the message is None.
    # If it's not None, it means the message is an edited message, and
    # the function doesn't proceed with copying and reposting the edited message.
    if message.edit_date is None:
        # Extract the media caption or name
        media_name = message.caption or message.document.file_name

        # Extract the user ID if available
        user_id = message.from_user.id if message.from_user is not None else None

        # Get the post ID of the media message
        media_id = message.message_id

        # Create the approve and disapprove buttons
        approve_button = InlineKeyboardButton("Approve", callback_data=f"approve:{media_id}")
        disapprove_button = InlineKeyboardButton("Disapprove", callback_data=f"disapprove:{media_id}")

        # Create an inline keyboard markup with the buttons
        keyboard = InlineKeyboardMarkup([[approve_button, disapprove_button]])

        # Send the media message to the channel with the buttons
        client.copy_message(
            chat_id="-1001878725736",
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=keyboard,
        )


# Function to handle button clicks
@app.on_callback_query()
def handle_button_click(client, query):
    # Get the callback data
    data = query.data.split(":")

    # Get the action and media ID from the callback data
    action = data[0]
    media_id = int(data[1])

    if action == "approve":
        # Post the information to the target channel (-1001973521419)
        client.send_message(
            chat_id="-1001973521419",
            text="**Media Name:** {}\n\n**Uploaded By:** {}\n\n**Post ID:** {}\n\n**Command:** `/getpost {}`\n\n**Please use @MultiUseRobot to get the file**".format(
                query.message.caption or query.message.document.file_name,
                query.message.from_user.id if query.message.from_user is not None else None,
                query.message.message_id,
                query.message.message_id,
            ),
        )
        # Answer the callback query to remove the "loading" state
        query.answer()
        # Delete the buttons from the media message
        query.message.edit_reply_markup(reply_markup=None)
        # Notify the bot user
        client.send_message(
            chat_id=query.from_user.id,
            text="Message approved: {}".format(query.message.caption or query.message.document.file_name),
        )
    elif action == "disapprove":
        # Delete the media message with buttons
        client.delete_messages(chat_id=query.message.chat.id, message_ids=query.message.message_id)
        # Notify the bot user
        client.send_message(
            chat_id=query.from_user.id,
            text="Message disapproved: {}".format(query.message.caption or query.message.document.file_name),
        )


# Run the bot
app.run()
