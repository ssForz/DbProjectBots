import psycopg2
from aiogram import Bot, Dispatcher, types
from cashierconfig import BOT_TOKEN
from aiogram.utils import executor
from bdconfig import host, user, password, db_name

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


ans = ''
cur_query = ''
flag = 0;
 
def exec_query():
    try:
        global ans
        #global cur_query
    # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name    
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                cur_query
            )
            connection.commit()
            ans = cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")
            print("Connection closed")

@dp.message_handler(commands=['start'])
async def echo_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Register_session")
    item2 = types.KeyboardButton("/Add_scan")
    item3 = types.KeyboardButton("/Add_purchase")
    item4 = types.KeyboardButton("/Check")
    markup.add(item1, item2, item3, item4)
    await bot.send_message(
            chat_id=message.chat.id,
            text="Ваше действие:\nRegister_session - зарегистрировать сессию\nAdd_scan - отсканировать товар\nAdd_purchase - отсканировать покупку\nCheck - чек ",
            reply_markup=markup
        )

@dp.message_handler(commands=['Register_session'])
async def echo_message(message):

    global cur_query
    global flag
    global id_ses
    flag = 2
    cur_query = "SELECT max(id_session) FROM session;"
    exec_query()
    #print(ans)
    id_ses = int(str(ans[0])[1:-2]) + 1
    #print(id_ses)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите данные сессии\nНеобходимо ввести:\nНомер кассы\nНомер кассира\nВремя начала работы\n Время конца работы"

    )




@dp.message_handler(commands=['Add_scan'])
async def echo_message(message):
    global cur_query
    global flag
    global id_scann
    flag = 3
    cur_query = """SELECT max(id_scan) FROM scan;"""
    exec_query()
    #print(ans)
    id_scann = int(str(ans[0])[1:-2]) + 1
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите данные об отсканированном товаре\nНеобходимо ввести:\nСессию покупки\nНазвание товара\nКоличество"

    )
    


@dp.message_handler(commands=['Add_purchase'])
async def echo_message(message):
    global cur_query
    global flag
    global id_pur
    flag = 4
    cur_query = """SELECT max(id_purchase) FROM purchase;"""
    exec_query()
    #print(ans)
    id_pur = int(str(ans[0])[1:-2]) + 1
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите данные об отсканированной покупке\nНеобходимо ввести:\nНомер сессии\nВремя покупки\nСпособ оплаты"

    )

@dp.message_handler(commands=['Check'])
async def echo_message(message):
    global cur_query
    global flag
    global id_pur
    flag = 5
    
    exec_query()
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите номер покупки"
    )

@dp.message_handler()
async def echo_message(message):
    global cur_query
    if(flag == 2):
        id_sess = id_ses
        print(id_sess)
        session_data = message.text
        par1, par2, par3, par4, par5, par6 = session_data.split(' ')
        par34 = " ".join((par3,par4))
        par56 = " ".join([par5,par6])
        cur_query = f"INSERT INTO session VALUES( {id_sess}, '{par1}', '{par2}', '{par34}', '{par56}');"
        exec_query()
        await bot.send_message(
                chat_id=message.chat.id,
                text="Данные введены, ваша сессия: "+str(id_sess)
        )

    if(flag == 3):
        id_scan1 = id_scann
        scan_data = message.text
        par1, par2, par3 = scan_data.split(' ')
        #par22 = int(par2)
        cur_query = f"select id_item from item  where nameitem = {par2};"
        exec_query()
        par34 = str(ans[0])
        cur_query = f"INSERT INTO scan VALUES( {id_scan1}, '{par1}'', '{par34}', '{par3}');"
        exec_query()
        await bot.send_message(
                chat_id=message.chat.id,
                text="Данные введены, сессия покупки "+str(par1)
        )

    if(flag == 4):
        id_pur1 = id_pur
        purchase_data = message.text
        par1, par2, par3, par4, = purchase_data.split(' ')
        par23 = " ".join((par2,par3))
        cur_query = f"INSERT INTO purchase VALUES( {id_pur1}, '{par1}', '{par23}', '{par4}');"
        exec_query()
        await bot.send_message(
                chat_id=message.chat.id,
                text="Данные введены, сессия покупки "+str(id_pur)
        )

    if(flag == 5):
        pur_data=message.text
        par1 = int(pur_data)
        cur_query = f"""SELECT SUM(totalprice) FROM (SELECT purchase.id_purchase, item.nameitem, item.price * scan.amount as totalprice FROM purchase JOIN scan ON purchase.id_purchase = scan.id_purchase JOIN item ON scan.id_item = item.id_item) as save WHERE save.id_purchase = {par1}"""
        exec_query()
        sm = int(str(ans[0])[10:-4])
        print(sm)
        await bot.send_message(
                chat_id=message.chat.id,
                text="Чек "+ str(sm) + " рублей"
        )




@dp.message_handler()
async def echo_message(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Используйте команду /start"
    )

if __name__ == "__main__":
    executor.start_polling(dp)