import os
import heroku3


class Config(object):
    # Get This From @TeleORG_Bot
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    # Get This From @StringSessionGen_Bot
    STRING_SESSION = os.environ.get("STRING_SESSION")
    # Forward From Chat ID
    SOURCE_CHAT_ID = list(
        set(int(x) for x in os.environ.get("FORWARD_FROM_CHAT_ID", "-100").split()))
    # Forward To Chat ID
    DESTINATION_CHAT_ID = list(
        set(int(x) for x in os.environ.get("FORWARD_TO_CHAT_ID", "-100").split()))
    # A regex to extract new message text. Replace with you own
    NEW_MESSAGE_PATTERN = '(?s).*\.\.\.\s([A-Za-z0-9]+)\s\.\.\.(?s).*𝓓𝓲𝓻𝓮𝓬𝓽𝓲𝓸𝓷\s:\s(SHORT|LONG)' \
        '(?s).*(Leverage\s:\s\w+\s\d+x)' \
        '(?s).*(Entry\s:\s\d+\.?\d*\s-\s\d+\.?\d*)' \
        '(?s).*(.Stoploss\s:\s\d+\.?\d*.)'\
        '(?s).*'

    # Regex to extract reply message. Replace with you own
    REPLY_MESSAGE_PATTERN = '([\w\s,]+\\n#[A-Za-z0-9]+/USDT(?s).*)'
    # Forward as Copy. Value Should be True or False
    FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
    # Sleep Time while Kang
    SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 10))
    DATABASE_URL = os.environ.get(
        'DATABASE_URL', "sqlite:///content_generator.db")
    # Heroku Management
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    HEROKU_APP = heroku3.from_key(HEROKU_API_KEY).apps(
    )[HEROKU_APP_NAME] if HEROKU_API_KEY and HEROKU_APP_NAME else None
