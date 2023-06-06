from pyrogram import Client, filters

# Replace with your API credentials
API_ID = 2727928
API_HASH = '8e959f089c05109d1c5f8ea4aec8af21'
BOT_TOKEN = '5878531007:AAFOrzBsytaPFWBAaxErx0W4Coz4jKLdxio'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Function to handle incoming media messages
@bot.on_message(filters.media)
def handle_media(client, message):
    # Check if the message is an edited message
    if message.edit_date is None:
        # Copy the media to the private channel (-100123456789)
        media = client.copy_message(
            chat_id="-1001878725736",
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        
        # Extract the media caption or name
        media_name = message.caption or message.document.file_name
        
        # Extract the user ID if available
        user_id = message.from_user.id if message.from_user is not None else None
        
        # Get the post ID of the copied message
        media_id = media.message_id
        
        # Post the information to the target channel (-100987654321)
        client.send_message(
            chat_id="-1001973521419",
            text=f"**Media Name:** {media_name}\n\n**Uploaded By:** {user_id}\n\n**Post ID:** {media_id}\n\n**Command:** `/getpost {media_id}`\n\n**Please use @MultiUseRobot to get the file**"
        )
        
        # Send a response to the user
        client.send_message(
            chat_id=message.chat.id,
            text=f"**Saved Successfully ✅**\n\n**Media Name:** __{media_name}__\n\n**Post ID:** `{media_id}`\n\n**You can retrieve it using `/getpost {media_id}`**"
        )


# Run the bot
app.run()
