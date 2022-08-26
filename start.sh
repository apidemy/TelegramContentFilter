#!/bin/bash

export API_ID=""
export API_HASH=""
export STRING_SESSION=""
export SOURCE_CHAT_ID=""
export DESTINATION_CHAT_ID=""
export FORWARD_FROM_CHAT_ID=""
export FORWARD_TO_CHAT_ID=""

set -e
source $HOME/TelegramContentFilter/venv/bin/activate
nohup python3 $HOME/TelegramContentFilter/main.py &