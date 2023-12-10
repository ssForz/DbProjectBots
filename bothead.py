from aiogram import Bot, Dispatcher, types
from headconfig import BOT_TOKEN
from aiogram.utils import executor
from bdconfig import host, user, password, db_name
import psycopg2
import psycopg2.extras

ans = ''
cur_query = ''
flag = 0



def exec_query():
    global ans
    try:
        connection = psycopg2.connect(dbname=db_name, user=user, password=password, host=host)
 
        with connection.cursor() as cursor:
            cursor.execute(
                    cur_query
                )
            connection.commit()
            ans = cursor.fetchall()
    except Exception as _ex:
        ans = "Неверно введенные данные"
    finally:
        if connection:
            connection.close()
            print("Connection closed")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

tocheckpass = ''

@dp.message_handler(commands=['start'])
async def echo_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/revenue_calculation")
    item2 = types.KeyboardButton("/availability_check")
    item3 = types.KeyboardButton("/add_to_registry")
    item4 = types.KeyboardButton("/price_check")
    item5 = types.KeyboardButton("/change_the_price")
    item6 = types.KeyboardButton("/add_item")
    markup.add(item1, item2, item3, item4, item5, item6)
    await bot.send_message(
            chat_id=message.chat.id,
            text="Выберите что хотите сделать сегодня :):\n - /revenue_calculation - Вывод общей выручки\n - /availability_check - Проверка наличия товара\n - /add_to_registry - Увеличить количество товара в реестре\n - /price_check - Просмотр стоимости товара\n - /change_the_price - Изменение стоимости товара\n - /add_item - Добавление нового товара в реестр",
            reply_markup=markup
        )

@dp.message_handler(commands=['revenue_calculation'])
async def echo_message(message):
    global cur_query
    cur_query = f"SELECT SUM(scan.amount * item.price) as total FROM scan, item WHERE scan.id_item = item.id_item"
    exec_query()
    answer = ''
    for i in ans:
        answer += (str(i)[1:-1])
    num1, num2, num3 = answer.split("'")
    await bot.send_message(
        chat_id=message.chat.id,
        text=num2,
    )
    

@dp.message_handler(commands=['availability_check'])
async def echo_message(message):
    global flag
    flag = 2
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите товар, наличие которого хотите проверить"

    )
@dp.message_handler(commands=['add_to_registry'])
async def echo_message(message):
    global flag
    flag = 3
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите товар, для которого хотите отметить завоз и введите количество надбавки"

    )

@dp.message_handler(commands=['price_check'])
async def echo_message(message):
    global flag
    flag = 4
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите товар, цену которого хотите узнать"
    )

@dp.message_handler(commands=['change_the_price'])
async def echo_message(message):
    global flag
    flag = 5
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите товар, для которого хотите поменять цену и его новую цену"
    )

@dp.message_handler(commands=['add_item'])
async def echo_message(message):
    global flag
    flag = 6
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите товар, который хотите добавить, его стоимость и количество"

    )

@dp.message_handler()
async def echo_message(message):
    global cur_query
    if (flag == 2):
        cur_query = f"SELECT totalamount FROM item WHERE nameitem = '{message.text}'"
        exec_query()
        answer = ''
        for i in ans:
            answer += (str(i)[1:-1])
        answerr = answer.rstrip(",")
        await bot.send_message(
            chat_id=message.chat.id,
            text=answerr,
        )
    elif (flag == 3):
        vvod = message.text
        num1, num2 = vvod.split(' ')
        num22 = int(num2)
        cur_query = f"UPDATE item SET totalamount = item.totalamount + {num22} WHERE nameitem = '{num1}'"
        exec_query()
        await bot.send_message(
            chat_id=message.chat.id,
            text="Добавлено",
        )
    elif (flag == 4):
        cur_query = f"SELECT price FROM item WHERE nameitem = '{message.text}'"
        exec_query()
        answer = ''
        for i in ans:
            answer += (str(i)[1:-1])
        answerr = answer.rstrip(",")
        await bot.send_message(
            chat_id=message.chat.id,
            text=answerr,
        )
    elif (flag == 5):
        vvod = message.text
        num1, num2 = vvod.split(' ')
        num22 = int(num2)
        cur_query = f"UPDATE item SET price = {num22} WHERE nameitem = '{num1}'"
        exec_query()
        await bot.send_message(
            chat_id=message.chat.id,
            text="Цена изменена",
        )
    elif (flag == 6):
        vvod = message.text
        num1, num2, num3 = vvod.split(' ')
        num22 = int(num2)
        num33 = int(num3)
        cur_query = "SELECT max(id_item) FROM item;"
        exec_query()
        id_itemm = int(str(ans[0])[1:-2]) + 1
        cur_query = f"INSERT INTO item VALUES({id_itemm}, '{num1}', {num22}, {num33})"
        exec_query()
        await bot.send_message(
            chat_id=message.chat.id,
            text="Товар добавлен",
        )
    else:
        await message.answer(text='Выберите, что вы хотите сделать')


if __name__ == "__main__":
    executor.start_polling(dp)

