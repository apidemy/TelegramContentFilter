import logging
from configs import Config
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

User = Client(session_name=Config.STRING_SESSION,
              api_hash=Config.API_HASH, api_id=Config.API_ID, plugins=dict(root="handlers"))

# Run User Bot
if __name__ == "__main__":
    try:
        User.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        User.send_message(
            chat_id="me", text="Your API_ID/API_HASH is not valid.")
        raise Exception("Your API_ID/API_HASH is not valid.")
    except:
        print("Exeption: Cannot run app")
        raise
    uname = User.get_me().username
    print(f"@{uname} Started Successfully!")
    idle()
    User.stop()
    print("Bot stopped!")
    User.send_message(
        chat_id="me", text="Bot stopped!")
