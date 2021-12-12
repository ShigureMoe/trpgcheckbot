#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
import logging
import random
import re

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('{骰子数}d{面数}\n{骰子数}d{面数}+{附加数}')


def roll(update: Update, context: CallbackContext) -> None:
    """Roll dice."""
    try:
        command = update.message.text.split("/r ")[1]
    except:
        update.message.reply_text('指令格式错误')
        return None
    try:
        num = int(command.split("d")[0])
        rrange = command.split("d")[1]
        if re.search("\+", rrange):
            range_num = int(rrange.split("+")[0])
            ext_num = int(rrange.split("+")[1])
        else:
            range_num = int(rrange)
            ext_num = 0
        if num >= 1000 or range_num >= 1000:
            update.message.reply_text('数字过大')
        else:
            result = ext_num
            for i in range(num):
                result += random.randint(1, range_num)
            update.message.reply_text(command + ": " + str(result))
    except ValueError:
        update.message.reply_text('表达式错误')
    except:
        update.message.reply_text('内部错误')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rhelp", help_command))
    dispatcher.add_handler(CommandHandler("r", roll))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
