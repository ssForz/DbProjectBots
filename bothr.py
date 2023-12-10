from aiogram import Bot, Dispatcher, types
from bhrconfig import BOT_TOKEN
from aiogram.utils import executor

import psycopg2
from bdconfig import host, user, password, db_name

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

start = ''
end = ''
ans = ''
cur_query = ''
q1 = 0
q2 = 0
q3 = 0
checkq1 = 0
add = 0
update = 0


def exec_query():
	global ans
	try:
		connection = psycopg2.connect(
			host=host,
			user=user,
			password=password,
			database=db_name
		)

		with connection.cursor() as cursor:
			cursor.execute(
					cur_query
				)
			connection.commit()
			ans = cursor.fetchall()
	except Exception as _ex:
		ans = "Error connection"
	finally:
		if connection:
			connection.close()
			print("Connection closed")

@dp.message_handler(commands=['start'])
async def echo_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("/add")
	item2 = types.KeyboardButton("/update")
	item3 = types.KeyboardButton("/queries")
	markup.add(item1, item2, item3)
	await bot.send_message(
			chat_id=message.chat.id,
			text="Выберите действие:\n - add - добавление нового работника в реестр\n - update - обновление информации о работнике\n - queries - запрос информации",
			reply_markup=markup
		)


@dp.message_handler(commands=['add'])
async def echo_message(message):
	global add
	add = 1
	await bot.send_message(
		chat_id=message.chat.id,
		text="Введите данные в формате: Имя Отчество Фамилия yyyy-mm-dd ИНН(12) Паспорт(10) Номер телефона(без пробелов)"
	)

@dp.message_handler(commands=['update'])
async def echo_message(message):
	global update
	update = 1
	await bot.send_message(
		chat_id=message.chat.id,
		text="Введите id работника, которого уволили"
	)
@dp.message_handler(commands=['queries'])
async def echo_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("/all")
	item2 = types.KeyboardButton("/q1")
	item3 = types.KeyboardButton("/q2")
	item4 = types.KeyboardButton("/q3")
	markup.add(item1, item2, item3, item4)
	await bot.send_message(
		chat_id=message.chat.id,
		text="Выберите запрос:\n - all - показать всех сотрудников\n - q1 - сотрудники, работавшие в определенный период\n - q2 - найти номер телефона сотрудника\n - q3 - сотрудники, родившиеся позже указанной даты",
		reply_markup=markup
	)

@dp.message_handler(commands=['all'])
async def echo_message(message):
	global cur_query
	cur_query = "SELECT * FROM cashier"
	exec_query()
	answer = ''
	for i in ans:
		answer += (str(i)[1:-1] + "\n" + "\n")
	await bot.send_message(
		chat_id=message.chat.id,
		text=answer,
	)
	cur_query = ''

@dp.message_handler(commands=['q1'])
async def echo_message(message):
	global q1
	q1 = 1
	await bot.send_message(
		chat_id=message.chat.id,
		text='Введите начало в формате yyyy-mm-dd hh:mm:ss',
	)

@dp.message_handler(commands=['q2'])
async def echo_message(message):
	global q2
	q2 = 1
	await bot.send_message(
		chat_id=message.chat.id,
		text='Введите фамилию сотрудника',
	)

@dp.message_handler(commands=['q3'])
async def echo_message(message):
	global q3
	q3 = 1
	await bot.send_message(
		chat_id=message.chat.id,
		text='Введите дату в формате dd.mm.yyyy',
	)



@dp.message_handler()
async def echo_message(message):
	global q1
	global q2
	global q3
	global add
	global update
	global cur_query
	# if (checkadd == 0 and checkupdate == 0 and checkqueries == 0):
	# 	await message.answer(text='Используйте /start')
	if (q1 == 1):
		global checkq1
		global start
		global end
		if (checkq1 == 0):
			start = message.text
			await bot.send_message(
				chat_id=message.chat.id,
				text='Введите конец в формате yyyy-mm-dd hh:mm:ss ',
			)
			checkq1 += 1
			return;
		if (checkq1 == 1):
			end = message.text
			checkq1 = 0
		cur_query = f"SELECT session.id_cashier, name, second_name, surname FROM session JOIN cashier ON session.id_cashier = cashier.id_cashier WHERE time_in between '{start}' and '{end}'"
		exec_query()
		answer = '(id, name, second_name, surname)\n'
		for i in ans:
			answer += (str(i)[1:-1] + "\n" + "\n")
		if (answer == ''):
			answer = 'Not found'
		await bot.send_message(
			chat_id=message.chat.id,
			text=answer,
		)
		start = ''
		end = ''
		q1 = 0
		cur_query = ''
	if (q2 == 1):
		cur_query = f"SELECT phone_num FROM cashier WHERE surname = '{message.text}'"
		exec_query()
		answer = str(ans[0])
		await bot.send_message(
			chat_id=message.chat.id,
			text=answer[2:-3],
		)
		q2 = 0
	if (q3 == 1):
		cur_query = f"SELECT name, surname FROM cashier GROUP BY birth, name, surname HAVING birth > '{message.text}' ORDER BY name desc"
		exec_query()
		answer = ''
		for i in ans:
			answer += str(i)[1:-1] + "\n"
		if (answer == ''):
			answer = 'Not found'
		await bot.send_message(
			chat_id=message.chat.id,
			text=answer,
		)
		q3 = 0
	if (add == 1):
		cur_query = "SELECT max(id_cashier) FROM cashier"
		exec_query()
		id_cas = int(str(ans[0])[1:-2]) + 1
		name, second_name, surname, date, inn, passport, phone = message.text.split(' ')
		cur_query = f"INSERT INTO cashier VALUES({id_cas}, '{name}', '{second_name}', '{surname}', '{date}', '{inn}', '{passport}', '{phone}')"
		exec_query()
		await bot.send_message(
			chat_id=message.chat.id,
			text=surname + " добавлен в реестр",
		)
		add = 0
	if (update == 1):
		id_fired = int(message.text)
		cur_query = f"SELECT surname FROM cashier WHERE id_cashier = {id_fired}"
		exec_query()
		surname = str(ans[0])[2:-3]
		cur_query = f"UPDATE cashier SET surname = (surname || text('(FIRED)')) WHERE id_cashier = {id_fired}"
		exec_query()
		await bot.send_message(
			chat_id=message.chat.id,
			text=surname + " помечен как уволенный",
		)
		update = 0
if __name__ == "__main__":
	executor.start_polling(dp)