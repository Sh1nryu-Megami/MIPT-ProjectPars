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


def get_all_no_ingredient(message):
    selected_entity = message
    responce_entity = requests.get(f'{f_const.backend_url}/select_all_entity/{selected_entity}')
    try:
        entity = responce_entity.json()
    except:
        entity = None
    return entity

def get_no_ingredient(message, selected_type):
    selected_entity = message
    responce_entity = requests.get(f'{f_const.backend_url}/select_entity/{selected_entity}/{selected_type}')
    try:
        entity = responce_entity.json()
    except:
        entity = None
    return entity

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
    btn = types.KeyboardButton("Все блюда без ингредиента")
    markup.add(btn)
    bot.send_message(message.chat.id, "Выберите тип блюда:", reply_markup=markup)


   
@bot.message_handler(func=lambda message: message.text == 'Все блюда без ингредиента')
def ask_all_for_entity(message):
    msg = bot.send_message(message.chat.id, "Введите ингредиент:")
    bot.register_next_step_handler(msg, send_all_dishes_without_entity)


def send_all_dishes_without_entity(message):
    entity = message.text
    data = get_all_no_ingredient(entity)
    if data:
        dishes_info = ""
        id = 1
        dishes_info += f"Следующие блюда не содержат указанные ингредиент. Вы можете выбрать их в меню кнопками:\n\n"
        for dish in data:
            dish_type, dish_name, dish_grams, dish_price = dish
            dishes_info += f"№{id} Тип блюда: {dish_type} Название: '{dish_name}' Цена: {dish_price}\n"
            if id % 10 == 0:
                bot.send_message(message.chat.id, dishes_info)
                dishes_info = ""
            id += 1
        if dishes_info:
            bot.send_message(message.chat.id, dishes_info)
    else:
        bot.send_message(message.chat.id, "Нет блюд без этого ингредиента.")

@bot.message_handler(func=check_dishes_types)
def show_positions(message):
    global selected_type
    selected_type = message.text
    response = requests.get(f'{f_const.backend_url}/select_selected_type/{selected_type}')
    positions = response.json()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for position in positions:
        btn = types.KeyboardButton(position)
        markup.add(btn)
    btn = types.KeyboardButton('Без ингредиента.')
    markup.add(btn)
    btn = types.KeyboardButton('Вернуться к выбору позиций.')
    markup.add(btn)
    response_names = requests.get(f'{f_const.backend_url}/select_all_dishes_names')
    all_dishes_names = response_names.json()
    bot.send_message(message.from_user.id, f'Блюда категории "{selected_type}":', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Без ингредиента.')
def ask_for_entity(message):
    msg = bot.send_message(message.chat.id, "Введите ингредиент:")
    bot.register_next_step_handler(msg, send_dishes_without_entity)


def send_dishes_without_entity(message):
    entity = message.text
    data = get_no_ingredient(entity, selected_type)
    if data:
        dishes_info = ""
        id = 1
        dishes_info += f"Следующие блюда не содержат указанные ингредиент. Вы можете выбрать их в меню кнопками:\n\n"
        for dish in data:
            dish_type, dish_name, dish_grams, dish_price = dish
            dishes_info += f"№{id} Тип блюда: {dish_type} Название: '{dish_name}' Цена: {dish_price}\n"
            if id % 10 == 0:
                bot.send_message(message.chat.id, dishes_info)
                dishes_info = ""
            id += 1
        if dishes_info:
            bot.send_message(message.chat.id, dishes_info)
    else:
        bot.send_message(message.chat.id, "Нет блюд без этого ингредиента.")



@bot.message_handler(func=check_dishes_names)
def about_position(message):
    selected_dish = message.text
    response = requests.get(f'{f_const.backend_url}/select_about_dish/{selected_dish}')
    position_info = response.json()[0]
    dish_details, dish_grams, dish_price, dish_image = position_info
    response = requests.get(dish_image)
    response.raise_for_status()
    try:
        response_text = f"Информация о блюде '{selected_dish}':\n\nОписание: {dish_details}\n\n"
        response_text += f"Вес: {dish_grams}\nЦена: {dish_price}"
        image_data = BytesIO(response.content)
        bot.send_photo(message.from_user.id, photo=image_data, caption=response_text)
    except:
        response_text = f"""К сожалению, сет настолько огромный, что телеграм не дает загрузить его описание... 
                            Подробное описание этого сета можно посмотреть на сайте Ёбисан!"""
        image_data = BytesIO(response.content)
        bot.send_photo(message.from_user.id, photo=image_data, caption=response_text)


bot.polling(none_stop=True)
