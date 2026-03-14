import telebot
import requests

BOT_TOKEN = "8797797157:AAFAKZ9UsCvfxhyOMNDRTg4Nl6LhqpI7wyc"
DEEPSEEK_API = "sk-4777a1d00435460fa5774d300d49996d"

bot = telebot.TeleBot(BOT_TOKEN)

channels = ["@ProTech43", "@Pro43Zone", "@SQ_BOTZ"]


def check_join(user_id):
    for ch in channels:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


def ask_deepseek(text):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]


@bot.message_handler(commands=['start'])
def start(msg):

    if not check_join(msg.from_user.id):

        join_text = """
لومړی دا چینلونه Join کړئ 👇

https://t.me/ProTech43
https://t.me/Pro43Zone
https://t.me/SQ_BOTZ

بیا /start ولیکئ
"""
        bot.send_message(msg.chat.id, join_text)
        return

    bot.send_message(msg.chat.id, "🤖 AI Bot تیار دی! هر څه ولیکئ.")


@bot.message_handler(func=lambda message: True)
def chat(message):

    if not check_join(message.from_user.id):
        bot.send_message(message.chat.id, "لومړی چینلونه Join کړئ!")
        return

    try:
        reply = ask_deepseek(message.text)
        bot.send_message(message.chat.id, reply)
    except:
        bot.send_message(message.chat.id, "AI جواب کې ستونزه ده.")


bot.infinity_polling()
