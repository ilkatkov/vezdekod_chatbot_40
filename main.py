# Вездекод Чатбот by Илья Катков
# https://vk.com/ilkatkov/
# Сообщество с ботом - https://vk.com/vezdekod22_katkov
# Задание 30

# import modules
import vk_api
import random
import json
import sqlite3


def db_startup():
    # подключение к db.sqlite
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    print("DB connect: OK")

    # создание таблицы в db.sqlite
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(64),
            surname VARCHAR(64),
            last_seen VARCHAR(256)
            )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS memes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link VARCHAR(128) UNIQUE
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS users_memes (
        user_id INTEGER,
        mem INTEGER,
        mark INTEGER
        )""")

    # закрываем соединение с db.sqlite
    conn.commit()


def add_user(user_id):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    vk_info = vk.method("users.get", {"user_ids": int(user_id)})
    name = vk_info[0].get('first_name')
    surname = vk_info[0].get('last_name')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", [
                   user_id, name, surname, ''])
    conn.commit()


def update_memes():
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    # разобраться с загрузкой наименований пикч
    for i in range(18, 68):
        cursor.execute("INSERT OR IGNORE INTO memes (link) VALUES (?)", [
                       "photo-212549341_4572390" + str(i)])
    conn.commit()


def seen_memes(user_id):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT mem FROM users_memes WHERE user_id = ?", [user_id])
    temp_memes = cursor.fetchall()
    memes = []
    for mem in temp_memes:
        memes.append(mem[0])
    return memes


def getRandMem(user_id):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    seen = seen_memes(user_id)
    cursor.execute("SELECT link FROM memes ORDER BY RANDOM() LIMIT 1")
    mem = cursor.fetchall()[0][0]
    while mem in seen:
        cursor.execute("SELECT link FROM memes ORDER BY RANDOM() LIMIT 1")
        mem = cursor.fetchall()[0][0]
    return mem


def update_last_seen_mem_user(user_id, mem):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_seen = ?", [mem])
    conn.commit()


def set_mark(user_id, mark):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT last_seen FROM users WHERE id = ?", [user_id])
    last_seen = cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO users_memes VALUES (?, ?, ?)",
                   [user_id, last_seen, mark])
    conn.commit()


def getUserStat(user_id):
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(mark) FROM users_memes WHERE user_id = ? AND mark = 1", [user_id])
    likes = cursor.fetchall()[0][0]
    cursor.execute(
        "SELECT COUNT(mark) FROM users_memes WHERE user_id = ? AND mark = 0", [user_id])
    dislikes = cursor.fetchall()[0][0]
    return {"likes": likes, "dislikes": dislikes}


def memes_count():
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM memes")
    count = cursor.fetchall()[0][0]
    return count


# ---SETTINGS VK---#
token = "6bb80dcfd9c8329a03c620366157137d550ec388577582ff5d4d13927b72934164244b1551de74749d62b"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
admin = 142446929  # id админа в ВК
memes_count = memes_count()
# ---SETTINGS VK---#


def get_button(label, color, b_type, payload=''):  # функция вызова клавиатуры
    return {
        "action": {
            "type": b_type,
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def get_link_button(label, link='', payload=''):
    return {
        "action": {
            "type": "open_link",
            "link": link,
            "payload": json.dumps(payload),
            "label": label
        }
    }


main_keyboard = {"one_time": False, "buttons": [
    [get_button(label="Показать мем 🤣", color="positive", b_type='text')],
    [get_button(label="Автор 😎", color="negative", b_type="text")],
    [get_button(label="Статистика 📈", color="primary", b_type="text")],
    [get_button(label="Привет 👋🏻", color="secondary", b_type="text")]
]
}
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode('utf-8')
main_keyboard = str(main_keyboard.decode('utf-8'))

memes_keyboard = {"one_time": False, "buttons": [
    [get_button(label="Ещё мемас 😂", color="positive", b_type='text')],
    [get_button(label="Загрузить мем 📥", color="primary", b_type='text')],
    [get_button(label="Лайк 👍🏻", color="positive", b_type="text"), get_button(
        label="Дизлайк 👎🏻", color="negative", b_type="text")],
    [get_button(label="Назад", color="secondary",
                b_type='text', payload='{"command":"start"}')]
]
}
memes_keyboard = json.dumps(memes_keyboard, ensure_ascii=False).encode('utf-8')
memes_keyboard = str(memes_keyboard.decode('utf-8'))

author_keyboard = {"one_time": False, "buttons": [
    [get_link_button(label="Открыть страницу",
                     link="https://vk.com/ilkatkov/")],
    [get_link_button(label="Открыть сайт", link="https://ilkatkov.ru/")],
    [get_button(label="Назад", color="negative",
                b_type='text', payload='{"command":"start"}')]
]
}
author_keyboard = json.dumps(
    author_keyboard, ensure_ascii=False).encode('utf-8')
author_keyboard = str(author_keyboard.decode('utf-8'))

stat_keyboard = {"one_time": False, "buttons": [
    [get_button(label="Назад", color="negative",
                b_type='text', payload='{"command":"start"}')]
]
}
stat_keyboard = json.dumps(stat_keyboard, ensure_ascii=False).encode('utf-8')
stat_keyboard = str(stat_keyboard.decode('utf-8'))


def bot_start():
    print("Bot started!")
    while True:
        try:
            messages = vk.method("messages.getConversations", {
                                 "offset": 0, "count": 20, "filter": "unanswered"})
            if messages["count"] >= 1:
                user_id = messages["items"][0]["last_message"]["from_id"]
                user_words = messages["items"][0]["last_message"]["text"].lower(
                )
                add_user(user_id)
                if user_words == "привет 👋🏻" or user_words == "начать":
                    add_user(user_id)
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Привет вездекодерам!", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "автор 😎":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Катков Илья\nhttps://vk.com/ilkatkov", "keyboard": author_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "статистика 📈":
                    stat = getUserStat(user_id)
                    likes = stat["likes"]
                    dislikes = stat["dislikes"]
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Всего смешнявок вы оценили: " + str(likes + dislikes) + "\nЛайков: " + str(likes) + "\nДизлайков: " + str(dislikes), "keyboard": stat_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "показать мем 🤣" or user_words == "ещё мемас 😂":
                    if len(seen_memes(user_id)) == memes_count:
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "На сегодня мемесы закончились.", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                    else:
                        mem = getRandMem(user_id)
                        update_last_seen_mem_user(user_id, mem)
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "Мемас :D", "attachment": mem, "keyboard": memes_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "загрузить мем 📥":
                    if len(seen_memes(user_id)) == memes_count:
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "На сегодня мемесы закончились.", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                    else:
                        mem = getRandMem(user_id)
                        update_last_seen_mem_user(user_id, mem)
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "Совсем скоро эта возможность станет доступна.\nА сейчас давай смеяться над приколдесами!", "attachment": mem, "keyboard": memes_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "назад":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Выберите раздел:", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "лайк 👍🏻":
                    if len(seen_memes(user_id)) == memes_count:
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "На сегодня мемесы закончились.", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                    else:
                        mem = getRandMem(user_id)
                        update_last_seen_mem_user(user_id, mem)
                        set_mark(user_id, 1)
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "Я тоже ору с того мема, а как тебе этот?", "attachment": mem, "keyboard": memes_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "дизлайк 👎🏻":
                    if len(seen_memes(user_id)) == memes_count:
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "На сегодня мемесы закончились.", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                    else:
                        mem = getRandMem(user_id)
                        update_last_seen_mem_user(user_id, mem)
                        set_mark(user_id, 0)
                        vk.method("messages.send", {
                            "peer_id": user_id, "message": "Да нормальный был мем, чего ты :(\nА как тебе этот?", "attachment": mem, "keyboard": memes_keyboard, "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Я даже не знаю, что ответить :(", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
        except Exception as e:
            vk.method("messages.send", {"peer_id": admin, "message": str(e),
                      "random_id": random.randint(1, 2147483647)})


if __name__ == "__main__":
    db_startup()  # настройка бд
    update_memes()  # подгружаем мемесы
    bot_start()
