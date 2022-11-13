
import json
import telebot
from telebot import types
import data_app as da
from datetime import datetime



API_TOKEN= "ID"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'База запущена')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Добавить ученика"))
    markup.add(types.KeyboardButton("Вывод данных"))
    bot.send_message(message.chat.id,'Что Вы хотите сделать:',reply_markup=markup)

@bot.message_handler(func= lambda message: message.text =='Добавить ученика' or message.text =='/app')
def message_ID(message):

    bot.register_next_step_handler(message, message_name)
    global ID
    ID = message.chat.id
    print(message.chat.id)
    bot.send_message(message.from_user.id, 'Введите имя ученика:')


def message_name(message):
    bot.register_next_step_handler(message, message_family)
    global name
    name = message.text
    print(name)
    bot.send_message(message.from_user.id, 'Введите фамилию ученика:')

def message_family(message):
    bot.register_next_step_handler(message, message_birthdate)
    global family
    family = message.text
    print(family)
    bot.send_message(message.from_user.id, 'Введите дату рождения ученика:')

def message_birthdate(message):
    bot.register_next_step_handler(message, message_classroom)
    global birthdate
    birthdate = message.text
    print(birthdate)

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"))
    markup.add(types.KeyboardButton("4"), types.KeyboardButton("5"), types.KeyboardButton("6"))
    markup.add(types.KeyboardButton("7"), types.KeyboardButton("8"), types.KeyboardButton("9"))
    markup.add(types.KeyboardButton("10"), types.KeyboardButton("11"), types.KeyboardButton("подготовительный"))

    bot.send_message(message.from_user.id, 'Введите класс',reply_markup=markup)

def message_classroom(message):
    bot.register_next_step_handler(message, message_achievement)
    global classroom
    classroom = message.text
    print(classroom)
    global time_
    now = datetime.now()
    time_ = now.strftime("%d.%m.%Y, %H:%M:%S")
    print(time_)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Отличник"), types.KeyboardButton("Хорошист"))
    markup.add(types.KeyboardButton("Троичник"), types.KeyboardButton("Неуспевающий"))

    bot.send_message(message.from_user.id, 'Введите успеваемость ученика', reply_markup=markup)

def message_achievement(message):
    global achievement
    achievement = message.text
    print(achievement)
    da.data_entry(name, family, birthdate, classroom, achievement, time_, ID)
    bot.send_message(message.from_user.id, 'Данные успешно записаны в базу')
    bot.send_message(message.from_user.id, f"{name} {family} {birthdate}, класс {classroom}, успеваемость: {achievement}")


@bot.message_handler(func= lambda message: message.text =='Вывод данных' or message.text =='/print')

def message_choice(message):

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("всю базу данных (/1)"))
    markup.add(types.KeyboardButton("данные ученика (/2)"), types.KeyboardButton("список учеников одного класса (/3)"))
    markup.add(types.KeyboardButton("учеников по году рождения (/4)"), types.KeyboardButton("учеников по успеваемости (/5)"))

    bot.send_message(message.from_user.id, 'Выберите, что вы хотите вывести?',reply_markup=markup)



    @bot.message_handler(func=lambda message: message.text == 'всю базу данных (/1)' or message.text == '/1')
    def message_everyone_students(message):
        with open("student_info.json", "r", encoding="utf-8") as f:
            text = json.load(f)
        for tex in text["stud_card"]:
            everyone_students = f'{tex["name"]} {tex["family"]}, {tex["birthdate"]}, {tex["classroom"]} класс, {tex["achievement"]}'
            bot.send_message(message.from_user.id, everyone_students)
        f.close()



    @bot.message_handler(func=lambda message: message.text == 'данные ученика (/2)' or message.text == '/2')
    def one_student(message):
        bot.register_next_step_handler(message, print_one_student)
        bot.send_message(message.from_user.id, 'Введите фамилию ученика:')

    def print_one_student(message):
        fam = message.text
        print(fam)
        with open("student_info.json", "r", encoding="utf-8") as f:
            text = json.load(f)
        for tex in text["stud_card"]:
            if fam == tex["family"]:
                print(f'{tex["name"]} {tex["family"]}, {tex["birthdate"]},класс:{tex["classroom"]}, {tex["achievement"]}')
                print_students = f'{tex["name"]} {tex["family"]}, {tex["birthdate"]}, {tex["classroom"]} класс, {tex["achievement"]}'
                bot.send_message(message.from_user.id, print_students)
        f.close()

    @bot.message_handler(func=lambda message: message.text == 'список учеников одного класса (/3)' or message.text == '/3')
    def students_class(message):
        bot.register_next_step_handler(message, print_students_class)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"))
        markup.add(types.KeyboardButton("4"), types.KeyboardButton("5"), types.KeyboardButton("6"))
        markup.add(types.KeyboardButton("7"), types.KeyboardButton("8"), types.KeyboardButton("9"))
        markup.add(types.KeyboardButton("10"), types.KeyboardButton("11"), types.KeyboardButton("подготовительный"))

        bot.send_message(message.from_user.id, 'Введите класс', reply_markup=markup)

    def print_students_class(message):
        clas = message.text
        print(clas)
        with open("student_info.json", "r", encoding="utf-8") as f:
            text = json.load(f)
        for tex in text["stud_card"]:
            if clas == tex["classroom"]:
                print(f'{tex["name"]} {tex["family"]}, {tex["birthdate"]},класс:{tex["classroom"]}, {tex["achievement"]}')
                print_studs_class = f'{tex["name"]} {tex["family"]}, {tex["birthdate"]}, {tex["classroom"]} класс, {tex["achievement"]}'
                bot.send_message(message.from_user.id, print_studs_class)
        f.close()


    @bot.message_handler(func=lambda message: message.text == 'учеников по году рождения (/4)' or message.text == '/4')
    def students_years(message):
        bot.register_next_step_handler(message, print_students_years)
        bot.send_message(message.from_user.id, 'Введите год рождения:')

    def print_students_years(message):
        year = int(message.text)
        print(year)
        with open("student_info.json", "r", encoding="utf-8") as f:
            text = json.load(f)
        for tex in text["stud_card"]:
            yyyy = int(str(tex["birthdate"])[6:10])
            if year <= yyyy <= year:
                print(f'{tex["name"]} {tex["family"]}, {tex["birthdate"]},класс:{tex["classroom"]}, {tex["achievement"]}')
                print_studs_years = f'{tex["name"]} {tex["family"]}, {tex["birthdate"]}, {tex["classroom"]} класс, {tex["achievement"]}'
                bot.send_message(message.from_user.id, print_studs_years)
        f.close()

    @bot.message_handler(func=lambda message: message.text == 'учеников по успеваемости (/5)' or message.text == '/5')
    def students_achievement(message):
        bot.register_next_step_handler(message, print_students_achievement)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Отличник"), types.KeyboardButton("Хорошист"))
        markup.add(types.KeyboardButton("Троичник"), types.KeyboardButton("Неуспевающий"))

        bot.send_message(message.from_user.id, 'Введите успеваемость ученика', reply_markup=markup)

    def print_students_achievement(message):
        achiev = message.text
        print(achiev)
        with open("student_info.json", "r", encoding="utf-8") as f:
            text = json.load(f)
        for tex in text["stud_card"]:
            if achiev == tex["achievement"]:
                print(f'{tex["name"]} {tex["family"]}, {tex["birthdate"]},класс:{tex["classroom"]}, {tex["achievement"]}')
                print_studs_achievement = f'{tex["name"]} {tex["family"]}, {tex["birthdate"]}, {tex["classroom"]} класс, {tex["achievement"]}'
                bot.send_message(message.from_user.id, print_studs_achievement)
        f.close()


bot.infinity_polling()