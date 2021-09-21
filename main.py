from pyrogram import Client
from pyrogram import filters
from body import Body
from inline import Inline
from pymongo import MongoClient
from Vinte import Generator
from aovivo import AOVIVO
import pyrogram
import threading
from tendencia import Tendencia
from sala import SalaDeSinais
from mp import MercadoPago

mp = MercadoPago()
gerador = Generator()

mongodb = MongoClient('')
collection = mongodb['BOT']['usuarios']

bot_token = ''
api_id = -1
api_hash = ''

bot = Client(session_name='generator_iqoption',
             bot_token=bot_token, api_id=api_id,
             api_hash=api_hash)

trend = Tendencia()
botoes = Inline(bot, collection, gerador)
ao_vivo = AOVIVO(bot, collection, gerador, trend)

threading.Thread(target = ao_vivo.RUN).start()

# ========== Retorno ========== 
@bot.on_callback_query()
def answer(client, query):
    botoes.feedback(query, trend)
    
# ========== Principal ========== 
@bot.on_message(filters.private)
def updates(client, message):
    try:
        client.send_chat_action(message.from_user.id, "typing")
    except pyrogram.errors.exceptions.bad_request_400.UserIsBot:
        print('Um bot tentou conversar')
        return None  
      
    Body(client, message, collection, gerador, mp)

# ========== SalaDeSinais ========== 
@bot.on_message(filters.regex('Só win na IQ!') & (filters.channel | filters.group))
def updates(client, message):
    SalaDeSinais(client, message, collection)
        
        
bot.run()
