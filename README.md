# TelegramContentFilter

Inspired from https://github.com/AbirHasan2005/Forward-Client.git

This is Telegram Messages Filter Userbot(https://github.com/apidemy).

Use this at your own risk. I will not be responsible for any kind of issue while using this! Better use a different Telegram Account instead of using Main Telegram Account.

### Features:
- Kang Whole Chat Messages to other Chats.
    - Can cause Telegram Account Ban!
- Forward From Chat To Chat.
    - Can Forward from Multiple Chats to Multiple Chats :)
    - Automatically forward new messages From Chat To Chat.
- Userbot 😁
- Simple & Userfriendly 😅

### Configs:
- `API_ID` - Get from my.telegram.org or [@TeleORG_Bot](https://t.me/TeleORG_Bot)
- `API_HASH` - Get from my.telegram.org or [@TeleORG_Bot](https://t.me/TeleORG_Bot)
- `STRING_SESSION` - Get this from [@StringSessionGen_Bot](https://t.me/StringSessionGen_Bot)
- `FORWARD_FILTERS` - Filters can be `text`, `video`, `document`, `gif`, `sticker`, `photo`, `audio`, `poll`, `forwarded`. Separate with Space.
- `FORWARD_TO_CHAT_ID` - Forward To Chat IDs. Separate with Space.
- `FORWARD_FROM_CHAT_ID` - Forward From Chat IDs. Separate with Space.
- `FORWARD_AS_COPY` - Forward Messages as Copy or with Forward Tag. Value should be `True`/`False`.
- `BLOCKED_EXTENSIONS` - Don't Forward those Media Messages which contains Blocked Extensions. Example: `mp4 mkv mp3 zip rar`. Separate with Space.
- `MINIMUM_FILE_SIZE` - Minimum File Size for Media Message to be able to Forward. Should be in Bytes.
- `BLOCK_FILES_WITHOUT_EXTENSIONS` - Value can be `True`/`False`. If `True` those files which doesn't have file extension will not be Forwarded.

### **Commands:**
- `!start` - Check UserBot Alive or Not.
- `!help` - Get this Message.
- `!kang` - Start All Messages Kanger.
- `!restart` - Restart Heroku App Dyno Workers.
- `!stop` - Stop Kanger & Restart Service.

### Support Group:
<a href="https://t.me/linux_repo"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>

### Video Tutorial:
[![YouTube](https://img.shields.io/badge/YouTube-Video%20Tutorial-red?logo=youtube)](https://youtu.be/_xuptk2KUbk)

### Deploy Now:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/apidemy/TelegramContentFilter.git)

### Host Locally:
```sh
git clone https://github.com/apidemy/TelegramContentFilter.git
cd TelegramContentFilter
pip3 install -r requirements.txt
# Setup Configurations in configs.py file!
python3 main.py
```

### Follow on:
<p align="left">
<a href="https://github.com/apidemy"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>
