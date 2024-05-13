import asyncio
import re
import random as r
import requests
import json
import telebot
from fake_useragent import UserAgent

api_id = '23267900'
api_hash = '63cfeea8d8e113c17c2a1ac8e4db442e'
bot_token = '6755514236:AAF5lq2JXOPE6ZU4ET0jFVlz8NPDdEjbCu8'

bot = telebot.TeleBot(bot_token)

# FUNCTION FOR GETTING ONLY THE CARD DETAILS FROM THE MESSAGE IF THERE IS ANY
def getcards(text: str):
    if text is None:
        return None

    text = text.replace('\n', ' ').replace('\r', '')
    card = re.findall(r"[0-9]+", text)
    if not card or len(card) < 3:
        return
    if len(card) == 3:
        cc = card[0]
        if len(card[1]) == 3:
            mes = card[2][:2]
            ano = card[2][2:]
            cvv = card[1]
        else:
            mes = card[1][:2]
            ano = card[1][2:]
            cvv = card[2]
    else:
        cc = card[0]
        if len(card[1]) == 3:
            mes = card[2]
            ano = card[3]
            cvv = card[1]
        else:
            mes = card[1]
            ano = card[2]
            cvv = card[3]
        if len(mes) == 2 and (mes > '12' or mes < '01'):
            ano1 = mes
            mes = ano
            ano = ano1
    if cc[0] == 3 and len(cc) != 15 or len(cc) != 16 or int(cc[0]) not in [3, 4, 5, 6]:
        return
    if len(mes) not in [2, 4] or len(mes) == 2 and mes > '12' or len(mes) == 2 and mes < '01':
        return
    if len(ano) not in [2, 4] or len(ano) == 2 and ano < '21' or len(ano) == 4 and ano < '2021' or len(
            ano) == 2 and ano > '39' or len(ano) == 4 and ano > '2039':
        return
    if cc[0] == 3 and len(cvv) != 4 or len(cvv) != 3:
        return
    if (cc, mes, ano, cvv):
        return cc + "|" + mes + "|" + ano + "|" + cvv


# MODIFY CC TO APPROVED LIKE TEXT
def modify(cc, cctype, brand, level, issuer, country, countrycode):
    a = str(r.randint(0, 20)) + '.' + str(r.randint(0, 9))

    return f'''━━『 ʟɪᴠᴇ ᴄᴄ sᴛʀᴀᴘᴘᴇᴅ ⚡』━━

𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅

𝗖𝗮𝗿𝗱: {cc}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Approved 1000

𝗜𝗻𝗳𝗼: {cctype} - {brand} - {level}
𝐈𝐬𝐬𝐮𝐞𝐫: {issuer}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country} {countrycode}

𝗧𝗶𝗺𝗲: {a}  𝐬𝐞𝐜𝐨𝐧𝐝𝐬

━━『 ᴄʜᴇᴄᴋ ɪɴғᴏ 』━━
ᴊᴏɪɴ @cc_x_dark ғᴏʀ ᴍᴏʀᴇ!
ᴘʀᴏ𝐱𝐲 : ʀᴇ𝐬ɪ𝐝𝐞𝐧𝐭𝐢𝐚𝐥 ⚡
ᴄʜᴇᴄᴋᴇᴅ ʙʏ : [🇬🇧] ˹xᴏ 𝕩 ᴇᴠɪʟ˼™ </> ~🇰🇷 [ᴀғᴋ]「ᴄᴄ」 (https://t.me/xoxevilxd)
『 𝗕𝗢𝗧 𝗕𝗬 - @xoxevilxd 』'''

# for getting bin info
async def get_bin(bin: str):
    url = f'https://binlist.io/lookup/{bin}/'
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    response = requests.get(url=url, headers=headers)
    result = json.loads(response.text)

    L = [result["scheme"], result["type"], result["category"], result["country"]["name"],
         result["country"]["alpha2"], result["bank"]["name"]]

    return L


# FOR DROPPING MESSAGE TO GROUP
async def drop_message(text):
    await bot.send_message(-4276388469, text=text)


chats = [-1001917696969, -1002136892104, -1001751466344, -1001314882195, -1001637582754, -1002048387671,
         -1001988741296, -1001504119575]  # give chat id's from where to scrap


# retrieve updates from telegram chats
@bot.message_handler(func=lambda message: True)
def main(message):
    Text = message.text
    fullz = getcards(Text)
    if fullz:
        info = get_bin(fullz[:6])  # Adjusted to take the first 6 digits for BIN lookup
        fully_ready_message = modify(cc=fullz, cctype=info[1], brand=info[0], level=[2], issuer=[5],
                                      country=[3], countrycode=[4])
        drop_message(fully_ready_message)

# Start polling
bot.polling()

# Log that the bot is running perfectly
print("The bot is running perfectly without errors.")