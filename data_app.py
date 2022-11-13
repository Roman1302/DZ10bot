
import json

def data_entry(name, family, birthdate, classroom, achievement, time_, ID):
    # Функция приглашает пользователя внести данных учеников и сохранить их в файл


    print(f'Вы ввели данные: {name} {family} {birthdate} {classroom} {achievement}\n')

    stud_card = { 
        "name" : name,
        "family": family,
        "birthdate" : birthdate,
        "classroom": classroom,
        "achievement" : achievement,
        "time" : time_,
        "ID" : ID}
    with open("student_info.json", encoding='utf-8') as f:
        data=json.load(f)
        data["stud_card"].append(stud_card)
        with open("student_info.json", "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.close()
        f.close()

