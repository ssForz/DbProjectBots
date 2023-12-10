from aiogram import Bot, Dispatcher, types
from bconfig import BOT_TOKEN
from aiogram.utils import executor

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

tocheckpass = ''
tonamebot = ''

@dp.message_handler(commands=['start'])
async def echo_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("/hr")
	item2 = types.KeyboardButton("/head")
	item3 = types.KeyboardButton("/cashier")
	markup.add(item1, item2, item3)
	await bot.send_message(
			chat_id=message.chat.id,
			text="Выберите вашу должность для работы с базой данных: кадровик (hr), управляющий (head) или кассир (cashier)",
			reply_markup=markup
		)

@dp.message_handler(commands=['hr'])
async def echo_message(message):
	global tocheckpass
	tocheckpass = 'hr1234'
	global tonamebot
	tonamebot = '@hresBDbot'
	await bot.send_message(
		chat_id=message.chat.id,
		text="Введите код доступа"

	)

@dp.message_handler(commands=['head'])
async def echo_message(message):
	global tocheckpass
	tocheckpass = 'head1234'
	global tonamebot
	tonamebot = '@headBDbot'
	await bot.send_message(
		chat_id=message.chat.id,
		text="Введите код доступа"

	)
@dp.message_handler(commands=['cashier'])
async def echo_message(message):
	global tocheckpass
	tocheckpass = 'cashier1234'
	global tonamebot
	tonamebot = '@cashierBDbot'
	await bot.send_message(
		chat_id=message.chat.id,
		text="Введите код доступа"

	)
@dp.message_handler()
async def echo_message(message):
	if (message.text == tocheckpass):
		await bot.send_message(
			chat_id=message.chat.id,
			text= "Код принят, используйте: " + tonamebot
		)
	elif (tocheckpass == ''):
		await bot.send_message(
			chat_id=message.chat.id,
			text="Используйте команду /start"
		)
	else:
		await message.answer(text='Неверный код')

if __name__ == "__main__":
	executor.start_polling(dp)