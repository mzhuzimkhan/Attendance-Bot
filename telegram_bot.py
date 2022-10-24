import logging
import geopy.distance
from aiogram import Bot, Dispatcher, executor, types
from pymongo import MongoClient


connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client["telegram_bot"]
users_of_bot = db["users"]
attendance = db["attendance"]
API_TOKEN = ''# Your Token


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="html")
dp = Dispatcher(bot)
def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton("Share Position", request_location=True)
    keyboard.add(button)
    return keyboard

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    coords_1 = (51.139598, 71.432995)## Coordinates of the office 
    coords_2 = (lat, lon)
    checker = 0
    if geopy.distance.geodesic(coords_1, coords_2).m < 50: 
        reply = True
    else:
        reply = False
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())
    if reply == True:
        date = str(message.date).strip().split(' ')
        weekdays ={
            '0' : 'Monday',
            '1' : 'Tuesday',
            '2' : 'Wednesday',
            '3' : 'Thursday',
            '4' : 'Friday',
            '5' : 'Saturday',
            '6' : 'Sunday'
        }
        n = users_of_bot.find({})
        name = ""
        for nm in n:
            if str(message.chat.id) in nm:
                name = nm[str(message.chat.id)]
                break
        d = attendance.find({},{"_id":0})
        for dm in d:
            if (dm['name'] == name and dm['date'] == date[0]) or (message.date.weekday() == 6):
                checker = 1
                break
        
        if checker == 0:
            inf = {
                "name" : name,
                "date" : date[0],
                "time" : message.date.strftime('%H:%M:%S'),                
                "Weekday" : weekdays[str(message.date.weekday())]
                }
            attendance.insert_one(inf)

@dp.message_handler(commands=['start'])
async def get_fullname(message: types.Message):
    reply = "Hello! The purpose of the bot is to check the attendance.\n In order to start press /get_location"
    await message.answer(reply)
    masked = {
        "chat_id" : message.chat.id,
        "fullname" : message.from_user.full_name
    }
    users_of_bot.insert_one(masked)

@dp.message_handler(commands=['get_location'])
async def cmd_locate_me(message: types.Message):
    reply = "Click on the the button below to share your location"
    await message.answer(reply, reply_markup=get_keyboard())

@dp.message_handler(commands=['menu'])
async def get_fullname(message: types.Message):
    reply = "This bot was constructed in order to check the attendance of the workers and to checck it press the button /get_location"
    await message.answer(reply)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
