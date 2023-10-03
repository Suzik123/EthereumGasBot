import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from telegram.ext import CallbackQueryHandler, JobQueue
from Menu import *
import shutil
from Web3 import *
import threading
import asyncio
import sqlite3
from telegram import Bot


async def background_task(context):
 

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    gas = get_gas_Rprice()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        try:
            x = row[4] + 20

            cursor.execute("UPDATE users SET time_to_alert = ? WHERE username = ?", (x, row[0]))

            if row[1] > gas and row[4] >= row[3]:
                await context.bot.send_message(chat_id=row[2], text="Current gas: " + str(gas))
                cursor.execute("UPDATE users SET time_to_alert = ? WHERE username = ?", (0, row[0]))
            conn.commit()
        except:
            cursor.execute("UPDATE users SET CD = ?, time_to_alert = ? WHERE username = ?",
                           (3600, 3600, row[0]))
            conn.commit()
    conn.close()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def gas1(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_gas_price())

class TgBot():
    def __init__(self):
        TOKEN = '<your-token>'
        self.application = ApplicationBuilder().token(TOKEN).build()
        job_q = self.application.job_queue
        job_q.run_repeating(background_task, interval=20)
    def add_handler(self, handler):
        self.application.add_handler(handler)
    def start_bot(self):
        self.application.run_polling()
    def create_DB(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                  (username TEXT PRIMARY KEY, value INTEGER, value2 INTEGER, CD INTEGER, time_to_alert INTEGER)''')
        conn.commit()
        conn.close()




Bot = TgBot()
Bot.create_DB()
Bot.add_handler(CommandHandler('start', start))
Bot.add_handler(CommandHandler('gas', gas1))
Bot.add_handler(CallbackQueryHandler(button_callback))
Bot.add_handler(MessageHandler(None, message_handler))

Bot.start_bot()
