import telebot
from telebot import types
import time
from first.models import *

training_time = ["8:00-9:30", "9:30-11:00", "11:00-12:30", "13:00-14:30", "14:30-16:00", "16:00-17:30", "17:30-19:00"]
training_day = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Субота", "Воскресенье"]

config = {
    "name": "gym_bot",
    "token": "5844930593:AAFFqE9CKylQpr3ppR5sll_BJuzqwFs0zRE"
}
inlines = telebot.types.InlineKeyboardMarkup()
product = Product.objects.all()
for elem in product:
    inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem} ₴", callback_data=elem.name))
inlines.add(
    telebot.types.InlineKeyboardButton(text="------------------------------------------------",
                                       callback_data="-"))
inlines.add(telebot.types.InlineKeyboardButton(text="Проверить счет",
                                               callback_data="Проверить счет"))
inlines.add(
    telebot.types.InlineKeyboardButton(text="Просмотреть корзину", callback_data="Просмотреть корзину"))
inlines.add(telebot.types.InlineKeyboardButton(text="Оплатить",
                                               callback_data="Оплатить"))
inlines.add(telebot.types.InlineKeyboardButton(text="Очистить корзину", callback_data="Очистить корзину"))

free_access = types.ReplyKeyboardMarkup(resize_keyboard=True)
free_access.add(types.InlineKeyboardButton("Регистрация"),
                types.InlineKeyboardButton("Авторизация"))

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.InlineKeyboardButton("Работа со счетом"),
                  types.InlineKeyboardButton("Покупка товаров"),
                  types.InlineKeyboardButton("Тренеровки"))

work_with_a_cash_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
work_with_a_cash_keyboard.add(types.InlineKeyboardButton("Проверить счет"),
                              types.InlineKeyboardButton("Пополнить счет"),
                              types.InlineKeyboardButton("Вернутся в главное меню"))

trainer_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Вывод всех тренеров в кнопки
name_trainer = Trainer.objects.all()
for i in name_trainer:
    trainer_keyboard.add(types.InlineKeyboardButton(f"{i}", f"{i}"))
trainer_keyboard.add(types.InlineKeyboardButton("Вернутся в главное меню"),
                     types.InlineKeyboardButton("Просмотреть заказаные тренировки"))

trainer_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Вывод всех тренеров на кнопки
name_trainer = Trainer.objects.all()
name_trainer_all = []
for i in name_trainer:
    trainer_keyboard.add(types.InlineKeyboardButton(f"{i}", f"{i}"))
    name_trainer_all.append(i.name)
trainer_keyboard.add(types.InlineKeyboardButton("Вернутся в главное меню"),
                     types.InlineKeyboardButton("Просмотреть заказаные тренировки"))

max_gum = telebot.TeleBot(config["token"])


@max_gum.message_handler(commands=["start"])
def start(message):
    max_gum.send_message(message.chat.id,
                         "Приветствуем в системе спротзала, если вы зарегестрированы то войдите в систему,"
                         " если нет то сначала зарегстрируйтесь",
                         reply_markup=free_access)


@max_gum.message_handler(content_types=["text"])
def get_text(message):
    if message.text.lower() == "регистрация":
        max_gum.register_next_step_handler(max_gum.send_message(message.chat.id, "Придумайте пароль"), registration)
    elif message.text.lower() == "авторизация":
        max_gum.register_next_step_handler(max_gum.send_message(message.chat.id, "Введите пароль для входа"),
                                           authorization)
    # добавляем основной функционал
    var_step = 0
    client = User.objects.filter(login_id=message.chat.id)
    if len(client) > 0:
        client_time = client[0].time_auto
        if time.time() - client_time < 86400:  # Проверка на длинну сесии, если пользователь авторезирован менее суток
            var_step = 1  # назад то его перекидывает обратно на авторизацию
    if var_step == 1:
        if message.text.lower() in ["работа со счетом", "проверить счет"]:
            max_gum.send_message(message.chat.id, f"Состояние вашего счета - {client[0].cash_account}₴",
                                 reply_markup=work_with_a_cash_keyboard)
        elif message.text.lower() == "пополнить счет":
            max_gum.register_next_step_handler(
                max_gum.send_message(message.chat.id, "На какую сумму хотите пополнить счет?"), add_money)
        elif message.text.lower() == "вернутся в главное меню":
            max_gum.send_message(message.chat.id, 'Возвращение в главное меню', reply_markup=main_keyboard)
        elif message.text.lower() == "покупка товаров":
            # inlines = telebot.types.InlineKeyboardMarkup()
            # product = Product.objects.all()
            # for elem in product:
            #     inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem} ₴", callback_data=elem.name))
            # inlines.add(
            #     telebot.types.InlineKeyboardButton(text="------------------------------------------------",
            #                                        callback_data="-"))
            # inlines.add(telebot.types.InlineKeyboardButton(text="Проверить счет",
            #                                                callback_data="Проверить счет"))
            # inlines.add(
            #     telebot.types.InlineKeyboardButton(text="Просмотреть корзину", callback_data="Просмотреть корзину"))
            # inlines.add(telebot.types.InlineKeyboardButton(text="Оплатить",
            #                                                callback_data="Оплатить"))
            # inlines.add(telebot.types.InlineKeyboardButton(text="Очистить корзину", callback_data="Очистить корзину"))
            max_gum.send_message(message.chat.id, "Товары на сегодня:", reply_markup=inlines)
        elif message.text.lower() == "тренеровки":
            max_gum.send_message(message.chat.id, "Выберете одно из наших тренеров", reply_markup=trainer_keyboard)

        elif message.text in name_trainer_all:
            trainer_time(message)
        elif message.text.lower() == "просмотреть заказаные тренировки":
            us_roz(message)
            max_gum.send_message(message.chat.id, f"Назначинные тренеровки на следующюю неделлю:",
                                 reply_markup=us_roz(message))
    # else:
    # if message.text.lower() == "регистрация":
    #     max_gum.register_next_step_handler(max_gum.send_message(message.chat.id, "Придумайте пароль"), registration)
    # elif message.text.lower() == "авторизация":
    #     max_gum.register_next_step_handler(max_gum.send_message(message.chat.id, "Введите пароль для входа"),
    #                                        authorization)
    # else:
    #     max_gum.send_message(message.chat.id,
    # "Время сессии завершено, для доступа к функционалу бота пройдите авторизацию",
    # reply_markup=free_access)
    #


@max_gum.callback_query_handler(func=lambda call: True)
def callback_data(call):
    product = Product.objects.filter(name=call.data)
    if product:
        max_gum.register_next_step_handler(
            max_gum.send_message(call.message.chat.id,
                                 f"Товар \"{call.data}\" выбран."
                                 f"\n\nВведите количество товара: "), add_product_cart)
    global name_product
    name_product = call.data
    # prod = Product.objects.all()
    # if call.data in prod:  # Ще не працює, проблема з forenkey
    #     product = Product.objects.filter(name=call.data)
    #     try:
    #         _, created = User_product.objects.get_or_create(
    #             user=User.objects.get(login_id=call.message.chat.id),
    #             name=Product.objects.get(name=product[0].name),
    #             price=product[0].price,
    #         )
    #     except:
    #         pass
    # if call.data == "back":
    #     max_gum.send_message(call.message.chat.id, "назад", reply_markup=)
    if call.data == "Проверить счет":
        client = User.objects.filter(login_id=call.message.chat.id)
        max_gum.send_message(call.message.chat.id, f"Состояние вашего счета - {client[0].cash_account} ₴",
                             reply_markup=main_keyboard)
    elif call.data == "Просмотреть корзину":
        inlines = telebot.types.InlineKeyboardMarkup()
        products = User_product.objects.all()
        suma = 0.0
        for elem in products:
            suma += int(elem.price)
            inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem.name} ₴", callback_data=f"{elem.name}"))
        inlines.add(
            telebot.types.InlineKeyboardButton(text="------------------------------------------------",
                                               callback_data="-"))
        inlines.add(telebot.types.InlineKeyboardButton(text="Оплатить",
                                                       callback_data="Оплатить"))
        inlines.add(telebot.types.InlineKeyboardButton(text="Очистить корзину", callback_data="Очистить корзину"))

        max_gum.send_message(call.message.chat.id, f"Общая сумма: {suma}₴", reply_markup=inlines)
    elif call.data == "Очистить корзину":
        User_product.objects.all().delete()
    elif call.data == "Оплатить":
        sum_1 = User.objects.filter(login_id=call.message.chat.id)
        products = User_product.objects.all()
        sum_all = 0
        for elem in products:
            sum_all += int(elem.price)
        User.objects.filter(login_id=call.message.chat.id).update(
            cash_account=sum_1[0].cash_account - sum_all)
        client = User.objects.filter(login_id=call.message.chat.id)
        User_product.objects.all().delete()
        max_gum.send_message(call.message.chat.id,
                             f"Оплату проведено. Состояние вашего счета - {client[0].cash_account} ₴",
                             reply_markup=main_keyboard)
    elif call.data.split(",")[0] in training_day and call.data.split(",")[1] in training_time \
            and call.data.split(",")[2] in name_trainer_all:  # Прверка формата вывода продуктов
        try:
            Schedule_trainer.objects.get_or_create(
                weekday=call.data.split(",")[0],
                trainer_name=Trainer.objects.get(name=call.data.split(",")[2]),
                time_training=call.data.split(",")[1],
                clients=User.objects.get(login_id=call.message.chat.id)
            )
        except:
            pass


def registration(message):
    password = message.text
    try:
        User.objects.get_or_create(
            login_id=message.chat.id,
            password=password,
            time_auto=0.0,
            cash_account=0
        )
    except Exception as ex:
        print(ex)
    max_gum.send_message(message.chat.id, "Позровляю вы зарегестрировались в системе")


def authorization(message):
    clients = User.objects.filter(login_id=message.chat.id, password=message.text)
    if clients:
        User.objects.update(time_auto=time.time())
        max_gum.send_message(message.chat.id, "Авторизация успешна", reply_markup=main_keyboard)
    else:
        max_gum.send_message(message.chat.id, "Не правильный пароль")


def add_money(message):
    inlines = types.InlineKeyboardMarkup()
    client = User.objects.filter(login_id=message.chat.id)
    User.objects.filter(login_id=message.chat.id).update(cash_account=client[0].cash_account + int(
        float(message.text)))  # Без флоат бьет ошибку привводе цифр через точку
    push_money = "https://www.portmone.com.ua/popovnyty-rakhunok-mobilnoho?gclid=Cj0KCQiA45qdBhD-ARIsAOHbVdFrlNp" \
                 "38FMOhwif78In6fNRi-hlSVrfjlOp6US5LeP3dsr37Z9OzjQaAvNyEALw_wcB"
    inlines.add(types.InlineKeyboardButton(text="Пополнение счета", url=push_money))
    max_gum.send_message(message.chat.id, "Нажмите чтобы оплатить", reply_markup=inlines)


def trainer_time(message):
    if message.text.lower() == "вернутся в главное меню":
        max_gum.send_message(message.chat.id, 'Возвращение в главное меню', reply_markup=main_keyboard)
    elif message.text.lower() == "просмотреть заказаные тренировки":
        us_roz(message)
        max_gum.send_message(message.chat.id, f"Назначинные тренеровки на следующюю неделлю:",
                             reply_markup=us_roz(message))
    else:
        trainer = Trainer.objects.filter(name=message.text)
        trainer_id = ""
        for el in trainer:
            trainer_id = el.id
        trainer_data = Schedule_trainer.objects.filter(trainer_name=trainer_id)
        dict_schedule_trainer = {}
        for elem in trainer_data:
            dict_schedule_trainer[elem.weekday] = elem.time_training
        inlines = telebot.types.InlineKeyboardMarkup()
        for elem_day in training_day:
            inlines.add(telebot.types.InlineKeyboardButton(text=f"-----------------    {elem_day}    -----------------",
                                                           callback_data=f"{1}"))
            for elem_time in training_time:
                if elem_day in dict_schedule_trainer:
                    if elem_time == dict_schedule_trainer[elem_day]:
                        continue
                    else:
                        inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem_time}",
                                                                       callback_data=f"{elem_day},{elem_time},"
                                                                                     f"{message.text}"))
                else:
                    inlines.add(telebot.types.InlineKeyboardButton(text=f"{elem_time}",
                                                                   callback_data=f"{elem_day},{elem_time},"
                                                                                 f"{message.text}"))
        max_gum.send_message(message.chat.id, f'Вы выбрали тренера {message.text}. Выберете день тренировок и время',
                             reply_markup=inlines)
        return inlines


def us_roz(message):
    us_tr = Schedule_trainer.objects.filter(clients=User.objects.get(login_id=message.chat.id))
    inlines = telebot.types.InlineKeyboardMarkup()
    count = 1
    for item in us_tr:
        inlines.add(telebot.types.InlineKeyboardButton(text=f"{count}. {item.weekday}, "
                                                            f"тренер: {item.trainer_name}, "
                                                            f"время: {item.time_training}", callback_data=f"{1}"))
        count += 1
    return inlines


def add_product_cart(message):
    if message.text.isdigit():
        if int(message.text) >= 1:
            User_product.objects.get_or_create(
                name=Product.objects.get(name=name_product),
                user=User.objects.get(login_id=message.chat.id),
                price=float(int(message.text))
            )
            max_gum.send_message(message.chat.id, f"Добавлено в корзину в количестве {message.text} шт.",
                                 reply_markup=inlines)


# def add_product_cart(message):
#     price_prod = Product.objects.filter(nameProd=name_product)
#     for i in price_prod:
#         price_prod_var = i.price
#     User_product.objects.get_or_create(
#         name=Product.objects.get(name=name_product),
#         user=User.objects.get(login_id=message.chat.id),
#         price=float(int(name_product) * float(price_prod_var)))
#     max_gum.send_message(message.chat.id, f"Добавлено в корзину в количестве {message.text} шт.",
#                            reply_markup=keyboard_basket)
#

max_gum.polling(none_stop=True, interval=0)
