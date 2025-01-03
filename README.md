# Telenotif

A simple Python library for sending notifications via Telegram bot when your long-running tasks complete.

## Installation

```bash
pip install telenotif
```

## Usage

```python
from telenotif import notif

# Initialize with your bot token and user ID
# Both are strings
notifier = notif(BOT_TOKEN, USER_ID)

# Send a simple notification
for item in range(10000):
    print(item)
notifier.alert("Loop finished")

# Or use it as a decorator
@notifier.decorator("Long process completed!")
def long_process():
    for i in range(10000):
        print(i)

# Run the function
long_process()  # Will send notification when done
```

## Getting Started

1. Create a Telegram bot using [@BotFather](https://t.me/botfather)
2. Get your bot token from BotFather
3. Get your user ID by messaging [@userinfobot](https://t.me/userinfobot)
4. Note that before the bot be able to message you must at least send the bot a message "Simply send a hello to your bot after creation."
## Features

- Simple interface with `alert()` method
- Decorator support for automatic notifications
- Async support under the hood
- Error handling and logging
- Silent notifications option
- Credential validation on initialization

## License

MIT License

# LICENSE
MIT License

Copyright (c) 2024 Sina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
