This project created for parsing site https://ebisan.ru/

To start it:

git clone git@github.com:Sh1nryu-Megami/MIPT-ProjectPars.git

cd MIPT-ProjectPars

git checkout dev

bash ./build.sh

Телеграм-бот для доставки блюд "Ёбисан"

Этот проект представляет собой комплексное приложение для заказа и ознакомления с блюдами ресторана "Ёбисан". Проект включает в себя frontend (телеграм-бот), backend (Flask-приложение для взаимодействия с базой данных), парсер (скрипт для сбора данных с веб-сайта ресторана), и Docker-контейнеры для удобного развертывания.

Структура проекта

	Frontend
		front.py: Код телеграм-бота на Python с использованием библиотеки Telebot.
		f_const.py: Константы, такие как токен бота и URL бекенда.

	Backend

		backend.py: Flask-приложение для обработки запросов от телеграм-бота. Взаимодействует с базой данных.
		b_const.py: Константы для подключения к базе данных.

	Парсер
		parser.py: Скрипт для сбора данных о блюдах с веб-сайта ресторана.
		p_const.py: Константы для парсера, такие как URL сайта и номера разделов с блюдами.

	Database
		База данных, построенная на PostgreSQL
		
	Docker

		docker-compose.yml: Файл конфигурации Docker Compose для запуска PostgreSQL, парсера, бекенда и фронтенда, сборки все это в контейнеры.



Frontend (frontend.py){

	get_dishes_types(): --Делает GET-запрос к бэкенду для получения всех уникальных типов блюд. Возвращает список типов блюд.

	get_dishes_names(): --Делает GET-запрос к бэкенду для получения всех уникальных названий блюд. Возвращает список названий блюд.

 	def get_all_no_ingredient(message): --Делает GET-запрос к бэкэнду для получения всех уникальных блюд, исключающих ингредиент message

  	def get_no_ingredient(message, selected_type): --Делает GET-запрос к бэкэнду для получения всех уникальных блюд, исключающих ингредиент message в рамках определенного типа блюд

	check_dishes_types(message): --Функция, проверяющая, принадлежит ли текстовое сообщение одному из типов блюд или является ли оно командой "Вернуться к выбору типа блюд."

	check_dishes_names(message): --Функция, проверяющая, принадлежит ли текстовое сообщение одному из названий блюд или является ли оно командой "Вернуться к выбору блюда."

	start(message): --Обработчик команды /start. Создает клавиатуру с кнопкой "Посмотреть позиции" и отправляет приветственное сообщение.

	show_types(message): --Обработчик команды "Посмотреть позиции" или "Вернуться к выбору позиций." Создает клавиатуру с кнопками для каждого типа блюда и отправляет сообщение для выбора типа блюда.

 	def ask_all_for_entity(message): --Обработчик команды "Все блюда без ингредиента"

  	def send_all_dishes_without_entity(message): --Используя гетеры, выводит сообщения со всеми продуктами, в которых нет набранного пользователем продукта

	show_positions(message): --Обработчик выбора типа блюда. Делает GET-запрос к бэкенду для получения блюд выбранного типа, создает из них KeyboardButton и отправляет сообщение с клавиатурой для выбора блюда.

  	def ask_for_entity(message): --Обработчик команды "Без ингредиента." 

   	def send_dishes_without_entity(message): --тоже самое, что и def send_all_dishes_without_entity(message), только для конкретного типа блюд

	about_position(message): --Обработчик выбора блюда. Делает GET-запрос к бэкенду для получения информации о выбранном блюде и отправляет сообщение с фото и описанием блюда.
}



Backend (backend.py){

	select_about_dish(selected_dish): --Обработчик запроса на получение информации о выбранном блюде. Выполняет SQL-запрос к базе данных и возвращает информацию о блюде.

 	def select_all_entity(selected_entity): --Обработчик запроса на получение всех блюд, исключая те, в которых есть продукт, указанный пользователем. Выполняет SQL-запрос к базе данных и возвращает список.

  	def select_entity(selected_entity, selected_type=None): --Обработчик запроса на получение всех блюд, исключая те, в которых есть продукт, указанный пользователем, в рамках одного типа блюд. Выполняет SQL-запрос к базе данных и возвращает список.

	select_selected_type(selected_type): --Обработчик запроса на получение списка блюд выбранного типа. Выполняет SQL-запрос к базе данных и возвращает список названий блюд выбранного типа.

	select_all_dishes_types(): --Обработчик запроса на получение всех типов блюд. Выполняет SQL-запрос к базе данных и возвращает список всех уникальных типов блюд.

	select_all_dishes_names(): --Обработчик запроса на получение всех названий блюд. Выполняет SQL-запрос к базе данных и возвращает список всех уникальных названий блюд.
	}



Parser (parser.py){

	connect_to_database(): --Устанавливает соединение с базой данных PostgreSQL и возвращает объект соединения.

	update(cur, upd_dtype, upd_name, upd_details, upd_grams, upd_price, upd_image): --Обновляет запись о блюде в базе данных.

	insert(cur, ins_dtype, ins_name, ins_details, ins_grams, ins_price, ins_image): --Добавляет новое блюдо в базу данных.

	scrape_and_update_db(conn, cur, url, sections): --Парсит веб-страницу ресторана, обновляет базу данных информацией о блюдах (инсертит, если блюда нет, если есть, проверяет, сходится ли информация и обновляет ее при надобности)

	main(): --Главная функция, которая в бесконечном цикле обновляет данные о блюдах с использованием парсера и ожидает 1 час перед следующим обновлением.
	}



