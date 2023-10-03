def show_data():
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()
class Status:
    def __init__(self):
        self.status = 0

    def change_status(self, to):
        self.status = to

    def get_status(self):
        return self.status


St = Status()


async def execute_once(update, context):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton('Current ethereum gas'), KeyboardButton('Set gas alert')],
                  [KeyboardButton('Show gas chart')]],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='''If you don't want to keep writing /start to get the menu back. You can also use the keyboard which was created. If this keyboard disappears, type /start again to make it appear''',
        reply_markup=keyboard
    )
    context.user_data['executed'] = True       

async def start(update, context):
    message_text = "Hello. This bot is designed to help users find the right time to work with good gas." \
                   " Here you can see current gas and gas chart, set gas alert."

    current_gas = InlineKeyboardButton("Current ethereum gas", callback_data="current_gas")
    set_gas_alert = InlineKeyboardButton("Set gas alert", callback_data="set_gas_alert")
    show_gas_chart = InlineKeyboardButton("Show gas chart", callback_data="show_gas_chart")

    reply_markup = InlineKeyboardMarkup([[current_gas, set_gas_alert], [show_gas_chart]])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=reply_markup
    )

    await execute_once(update, context)

async def message_handler(update, context):
    text = update.message.text
    if text == "Current ethereum gas":
        await current_gas_callback(update, context)
        return None
    elif text == "Set gas alert":
        await set_gas_alert_callback(update, context)
        St.change_status(1)
        return None
    elif text == "Show gas chart":
        await show_gas_chart_callback(update, context)
        return None

    if St.get_status() == 1:
        try:
            number = int(update.message.text)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'You should write here only integer numbers. Try again set your alert!')
            St.change_status(0)
            return None
        conn = sqlite3.connect('database.db')

        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, value, value2) VALUES (?, ?, ?)", (update.message.from_user.username, update.message.text, update.effective_chat.id))

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your gas Alert successfully set to: {number} Gwei \n')

        except:
            cursor.execute("REPLACE INTO users (username, value, value2) VALUES (?, ?, ?)", (update.message.from_user.username, update.message.text, update.effective_chat.id))

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Your gas Alert successfully changed to: {number} Gwei \n')
        conn.commit()
        conn.close()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Set your alerts cooldown in minutes. If you do not answer, the cooldown will be automatically set to 60 minutes.')
        St.change_status(2)
        return None
    if St.get_status()==2:
        try:
            number = int(update.message.text)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'You should write here only integer numbers. Try again set your alert!')
            St.change_status(0)
            return None
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET CD = ?, time_to_alert = ? WHERE username = ?", (number*60, number*60, update.message.from_user.username))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Your Alert cooldown successfully set to: {number} minutes\n')
        conn.commit()
        conn.close()
        show_data()
async def button_callback(update, context):
    query = update.callback_query
    data = query.data

    if data == "current_gas":
        await current_gas_callback(update, context)
    elif data == "set_gas_alert":
        await set_gas_alert_callback(update, context)
    elif data == "show_gas_chart":
        await show_gas_chart_callback(update, context)


async def set_gas_alert_callback(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='At what gas do you want to be notified?')


async def current_gas_callback(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=get_gas_price()
    )


async def show_gas_chart_callback(update, context):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        caption="Current gas price: " + get_gas_price(),
        photo=show_graph()
    )
