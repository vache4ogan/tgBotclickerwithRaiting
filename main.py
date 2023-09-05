from aiogram import Bot, Dispatcher, types
import logging
import asyncio
from config import token
import database

# initialization
database.init()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)

dp = Dispatcher(bot)

#Keyboard

click_but = types.KeyboardButton(text='Клик')
show_reyting = types.KeyboardButton(text='Рейтинг')
score_btn = types.KeyboardButton(text='Счет')

keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.add(click_but)
keyboard1.add(show_reyting)
keyboard1.add(score_btn)

conti = types.KeyboardButton(text='Продолжить')

keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.add(conti)

#variables

i = 1
RaitList = []
RateNameList = []
RateIDlist = []

#handlers

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    prov = database.check(message.from_user.id)
    if prov == True:
        database.insert(message.from_user.id, message.from_user.first_name, 0)
    elif prov == False:
        scoreFromFunc = database.score_show(message.from_user.id)
        database.insert(message.from_user.id, message.from_user.first_name, scoreFromFunc)
    database.commit()
    await message.answer('Привет ! Это бот кликер, кликай на кнопку и становись выше в рейтинге!',
                         reply_markup=keyboard1)


@dp.message_handler()
async def mess(message: types.Message):
    global i
    global RaitList
    global RateNameList
    global RateIDlist
    if message.text.lower() == 'клик':
        scoreFromFunc = database.score_show(message.from_user.id)
        scoreFromFunc += 1
        database.update_score(scoreFromFunc, message.from_user.id)
        database.commit()
        await message.answer('Счет: + 1')
    if message.text.lower() == 'рейтинг':
        await message.answer('Рейтинг: ', reply_markup=keyboard2)
        all = database.rait_show()
        for row in all:
            RateIDlist.append(row[0])
            RateNameList.append(row[1])
            RaitList.append(row[2])

        RateNameList1 = list(set(RateNameList))
        RateIDlist1 = list(set(RateIDlist))

        RaitList.sort()
        RaitList.reverse()
        print(RateIDlist1)
        print(RateNameList1)
        print(RaitList)

        for y in RaitList:
            Name = database.knowtop1(y)
            if len(RateNameList1) >= 2 and len(RaitList) >= 2:
                await message.answer(f'{i}. {Name}. Счет: {y}')
            else:
                await message.answer(f'{i}. {Name}. Счет: {RaitList[0]}')
            i = i + 1
        else:
            i = 1
            RaitList.clear()
            RateNameList1.clear()
            RateIDlist1.clear()
            RateIDlist.clear()
            RateNameList.clear()


    if message.text.lower() == 'счет':
        scoreFromFunc = database.score_show(message.from_user.id)
        await message.answer(f'Счет: {scoreFromFunc}')
    if message.text.lower() == 'продолжить':
        await message.answer('Продолжаю...', reply_markup=keyboard1)

async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
