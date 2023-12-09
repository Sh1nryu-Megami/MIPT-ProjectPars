import telebot
from telebot import types
import requests
from io import BytesIO
import f_const

bot = telebot.TeleBot(f_const.TOKEN)



def get_dishes_types():
   response_types = requests.get(f'{f_const.backend_url}/select_all_dishes_types')
   all_dishes_types = response_types.json()	
   return all_dishes_types

def get_dishes_names():
   response_names = requests.get(f'{f_const.backend_url}/select_all_dishes_names')
   all_dishes_names = response_names.json()	
   return all_dishes_names
   
def check_dishes_types(message):
   all_dishes_types = get_dishes_types()
   return message.text in all_dishes_types or message.text == "Вернуться к выбору типа блюд."
   
def check_dishes_names(message):
   all_dishes_names = get_dishes_names()
   return message.text in all_dishes_names or message.text == "Вернуться к выбору блюда."
   
   
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poz_btn = types.KeyboardButton("Посмотреть позиции.")
    markup.add(poz_btn)
    text = "👋 Здравствуйте, это телеграм-бот доставки Ёбисан. Здесь вы можете ознакомиться с блюдами заведения."
    bot.send_message(message.from_user.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Посмотреть позиции.'
                                          or message.text == 'Вернуться к выбору позиций.')
def show_types(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    all_dishes_types = get_dishes_types()
    for dish_type in all_dishes_types:
        btn = types.KeyboardButton(dish_type)
        markup.add(btn)
    bot.send_message(message.chat.id, "Выберите тип блюда:", reply_markup=markup)


   
   
@bot.message_handler(func=check_dishes_types)
def show_positions(message):
    
    selected_type = message.text
    response = requests.get(f'{f_const.backend_url}/select_selected_type/{selected_type}')
    positions = response.json()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for position in positions:
        btn = types.KeyboardButton(position)
        markup.add(btn)
    btn = types.KeyboardButton('Вернуться к выбору позиций.')
    markup.add(btn)
    response_names = requests.get(f'{f_const.backend_url}/select_all_dishes_names')
    all_dishes_names = response_names.json()
    bot.send_message(message.from_user.id, f'Блюда категории "{selected_type}":', reply_markup=markup)


@bot.message_handler(func=check_dishes_names)
def about_position(message):

    selected_dish = message.text
    response = requests.get(f'{f_const.backend_url}/select_about_dish/{selected_dish}')
    position_info = response.json()[0]
    dish_details, dish_grams, dish_price, dish_image = position_info
    response = requests.get(dish_image)
    response.raise_for_status()
    if selected_dish == "СЕТ №34 ВАБИСАБИ (180шт)":
        response_text = f"""К сожалению, сет настолько огромный, что телеграм не дает загрузить его описание... 
                            Подробное описание этого сета можно посмотреть на сайте Ёбисан!"""
    else:
        response_text = f"Информация о блюде '{selected_dish}':\n\nОписание: {dish_details}\n\n"
        response_text += f"Вес: {dish_grams}\nЦена: {dish_price}"
    image_data = BytesIO(response.content)
    bot.send_photo(message.from_user.id, photo=image_data, caption=response_text)
bot.polling(none_stop=True)
    
