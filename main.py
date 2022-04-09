# Вездекод Чатбот by Илья Катков
# https://vk.com/ilkatkov/
# Сообщество с ботом - https://vk.com/vezdekod22_katkov
# Задание 20

# import modules
import vk_api
import random
import json

admin = 142446929  # id админа в ВК

# ---SETTINGS VK---#
token = "6bb80dcfd9c8329a03c620366157137d550ec388577582ff5d4d13927b72934164244b1551de74749d62b"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
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
    [get_button(label="Лайк 👍🏻", color="positive", b_type="text"), get_button(label="Дизлайк 👎🏻", color="negative", b_type="text")],
    [get_button(label="Назад", color="secondary", b_type='text', payload='{"command":"start"}')]
    ]
}
memes_keyboard = json.dumps(memes_keyboard, ensure_ascii=False).encode('utf-8')
memes_keyboard = str(memes_keyboard.decode('utf-8'))

author_keyboard = {"one_time": False, "buttons": [
    [get_link_button(label="Открыть страницу", link="https://vk.com/ilkatkov/")], 
    [get_link_button(label="Открыть сайт", link="https://ilkatkov.ru/")], 
    [get_button(label="Назад", color="negative", b_type='text', payload='{"command":"start"}')]
    ]
}
author_keyboard = json.dumps(author_keyboard, ensure_ascii=False).encode('utf-8')
author_keyboard = str(author_keyboard.decode('utf-8'))

stat_keyboard = {"one_time": False, "buttons": [ 
        [get_button(label="Назад", color="negative", b_type='text', payload='{"command":"start"}')]
    ]
}
stat_keyboard = json.dumps(stat_keyboard, ensure_ascii=False).encode('utf-8')
stat_keyboard = str(stat_keyboard.decode('utf-8'))

def main():
    print("Bot started!")
    while True:
        try:
            messages = vk.method("messages.getConversations", {
                                 "offset": 0, "count": 20, "filter": "unanswered"})
            if messages["count"] >= 1:
                user_id = messages["items"][0]["last_message"]["from_id"]
                user_words = messages["items"][0]["last_message"]["text"].lower(
                )
                if user_words == "привет 👋🏻" or user_words == "начать":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Привет вездекодерам!", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "автор 😎":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Катков Илья\nhttps://vk.com/ilkatkov", "keyboard": author_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "статистика 📈":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Тут будет статистика :)", "keyboard": stat_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "показать мем 🤣":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Мемас :D", "keyboard": memes_keyboard, "random_id": random.randint(1, 2147483647)})
                elif user_words == "назад":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Выберите раздел:", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Я даже не знаю, что ответить :(", "keyboard": main_keyboard, "random_id": random.randint(1, 2147483647)})
        except Exception as e:
            vk.method("messages.send", {"peer_id": admin, "message": str(e),
                      "random_id": random.randint(1, 2147483647)})


if __name__ == "__main__":
    main()
