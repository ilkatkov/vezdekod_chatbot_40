# Вездекод Чатбот by Илья Катков
# https://vk.com/ilkatkov/
# Сообщество с ботом - https://vk.com/vezdekod22_katkov
# Задание 10

# import modules
import vk_api
import random

admin = 142446929  # id админа в ВК

# ---SETTINGS VK---#
token = "6bb80dcfd9c8329a03c620366157137d550ec388577582ff5d4d13927b72934164244b1551de74749d62b"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---SETTINGS VK---#


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
                if user_words == "привет":
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Привет вездекодерам!", "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {
                              "peer_id": user_id, "message": "Я даже не знаю, что ответить :(", "random_id": random.randint(1, 2147483647)})
        except Exception as e:
            vk.method("messages.send", {"peer_id": admin, "message": str(e),
                      "random_id": random.randint(1, 2147483647)})


if __name__ == "__main__":
    main()
