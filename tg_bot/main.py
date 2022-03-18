import threading
from os import environ
import telebot
import logging.config

from schedule_task import start_scheduler

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Bot:

    def __init__(self, bot_token, chat_id=None):
        self.bot = telebot.TeleBot(bot_token)
        try:
            self.chat_id = int(chat_id)
        except:
            self.chat_id = None
            logger.warning("Chat id is not set.")

        @self.bot.message_handler(commands=["get_id"])
        def get_id(m):
            self.bot.send_message(m.chat.id, f"Chat id: {m.chat.id}")

        @self.bot.message_handler(content_types=['new_chat_members'])
        def delete_join_message(m):
            # If bot is not admin, then it will not be able to delete message.
            try:
                self.bot.delete_message(m.chat.id, m.message_id)
            except:
                if m.new_chat_members[0].id != self.bot.get_me().id:
                    self.bot.send_message(m.chat.id,
                                     "Please make me an admin in order for me to remove the join and leave messages on this group!")
                else:
                    self.bot.send_message(m.chat.id,
                                     "Hi! Don't forget to make me an admin!")
                    if self.chat_id is None:
                        self.bot.send_message(m.chat.id,
                                              "Also get chat id from /get_id, set it in .env and restart the bot.")

        @self.bot.message_handler(content_types=['left_chat_member'])
        def delete_leave_message(m):
            # If bot is the one that is being removed, it will not be able to delete the leave message.
            if m.left_chat_member.id != self.bot.get_me().id:
                try:
                    self.bot.delete_message(m.chat.id, m.message_id)
                except:
                    self.bot.send_message(m.chat.id,
                                     "Please make me an admin in order for me to remove the join and leave messages on this group!")

    def get_members_count(self):
        if self.chat_id is None:
            logger.warning("Attempt to get members count with no chat id set. Get chat id from /get_id, set it in .env and restart the bot.")
            return None
        try:
            amount = self.bot.get_chat_member_count(self.chat_id)
        except Exception as e:
            logger.error(e)
            return None
        return amount

    def start_bot(self):
        self.bot.infinity_polling()

if __name__ == "__main__":


    bot_token = environ.get("BOT_TOKEN")
    chat_id = environ.get("CHAT_ID")

    bot = Bot(bot_token, chat_id)
    t1 = threading.Thread(target=bot.start_bot)
    t2 = threading.Thread(target=start_scheduler, args=(bot,))
    t1.start()
    t2.start()
