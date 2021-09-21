from menus import horario_menu
from menus import gerador
from menus import info
from menus import timeframe_menu
from menus import analise_menu
from menus import cont_dias
from menus import direcao_menu

from menus import sub_configs
from menus import volatividade
from menus import dif_noticia
from menus import choose_moeda
from menus import comunidade
from menus import payout_menu

from dateutil import parser

import pytz
from datetime import datetime
import random
import datetime as dt
import time



infovip = ''' '''

frases = ['“Quando a volatilidade e o momento se tornarem insanos, pule fora” - Michael Marcus.',
 '“Operar é emoção. É psicologia de massa, ganância e medo” - Michael Marcus',
 '“Se ocorrer uma perda desestabilizante, ponha um pouco de tempo entre a perda e sua próxima decisão” - Richard Dennis',
 '“Quanto mais disciplinado você puder ser, melhor você irá funcionar no mercado” - David Ryan',
 '“Estabeleça pontos de entrada e saída e entenda a relação entre risco e recompensa” - Jesse Livermore',
 '“Eu nunca falhei. Eu apenas encontrei 10 mil maneiras que não funcionam. - Thomas Edison”',
 '“Operar é como qualquer emprego. Se você permanecer o tempo necessário, terá o que colher” - Tom Baldwin']
 

class Inline:
    client = None
    db = None
    generator = None
    
    def __init__(self, client, mongodb, gerate):
        self.client = client        
        self.db = mongodb
        self.generator = gerate

    def managedb(self, retorno):
        now = datetime.now()
        acesso = '{}/{}/{}'.format(now.day, now.month, now.year)
        usuario = self.db.find_one(retorno.from_user.id)


        if usuario['ult_acess'] != acesso: #CleanDBSinais
            self.db.update_one(
                {'_id':retorno.from_user.id},
                {
                    '$set': {
                        'sinais': []}})
        

        if usuario['vip'] > 0:
            dias = usuario['vip']
            if (usuario['ult_acess'] != acesso):
                dias = usuario['vip']-1
                
            self.db.update_one(
                {'_id':retorno.from_user.id},
                {
                    '$set': {
                            'ult_acess':acesso,
                            'last_asset':retorno.data,
                            'vip': dias
                            }
                },
                upsert = True)
            return True

        else:
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'plano':'Free'}})
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'sala':'Sem registro'}})
          
            turn = (usuario['max_geracao'] <=0 and usuario['ult_acess'] != acesso)
             
            if (turn == True) or (usuario['max_geracao'] > 0):
                x = 5 if turn == True else usuario['max_geracao']#-1
               
                self.db.update_one(
                    {'_id':retorno.from_user.id},
                    {
                        '$set': {
                                'ult_acess':acesso,
                                'last_asset':retorno.data,
                                'max_geracao': x
                                }
                    },
                    upsert = True)
                return True

            elif turn == False:
                return False

    def limite(self, retorno, level = True):
        usuario = self.db.find_one(retorno.from_user.id)
        if usuario['vip'] <= 0:
            if usuario['max_geracao'] <= 0:
                return True
            else:
                if level:
                    self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'max_geracao':usuario['max_geracao']-1}})
                    return False
                elif level == False and usuario['max_geracao'] <= 0:
                    return True
      
    def gerar(self, ativo, horario, retorno, last_tf):
        usuario = self.db.find_one(retorno.from_user.id)
        dias = usuario['last_dias'] 
        last_dir = usuario['last_dir']
        last_payout = usuario['last_pay']
        
        horario = str(int(horario)+1) if last_tf > 5 else horario
        if last_tf > 5 and int(horario) >= 24:
            return None
        
        antes = 1
        for minute in range(0, 58, last_tf):
            self.client.send_chat_action(retorno.from_user.id, 'typing')
            sinal = self.generator.probabilidade(ativo, horario+':'+str(minute), dias, last_tf, last_dir, last_pay = last_payout)
            
            if sinal != None:
                if sinal['text'] != '':
                    
                    depois = int(sinal['dados']['hora'].split(':')[1])
                    if (depois-antes) == 1: #Sinais com horário consecutivos em m1(Descarta)
                        antes = depois
                        continue
                    elif (depois-antes) < 0:
                        antes = 1
                    else:
                        antes = depois
                      
                    if self.limite(retorno):
                        break
                    self.client.send_message(retorno.from_user.id, sinal['text'])
                    self.db.update_one(
                        {'_id':retorno.from_user.id},
                        {'$push':{'sinais':sinal['dados']}})
    
    
    def mod(self, text, imp = None):
        lista = text.split('\n')
        for lin in lista:
            if 'Status' in lin:
                lista.pop(len(lista)-1)
                break
        if imp != None:
            q = '\n\n' if imp == 'Configurações' else '\n'
            return '\n'.join(lista) + q+'**Status:** __'+imp+'__'
        else:
            return '\n'.join(lista)
    
    def perfil(self, retorno):
        usuario = self.db.find_one(retorno.from_user.id)
        perfil = 'ID: '+str(retorno.from_user.id)+'\n'
        perfil += 'Nome: '+str(retorno.from_user.first_name)+' '+str(retorno.from_user.last_name)+'\n'
        perfil += 'Username: @'+str(retorno.from_user.username)+'\n\n'
        perfil += 'Indicações: '+str(len(usuario['indicacoes']))+'\n'
        perfil += 'Gerações restantes: '+str(usuario['max_geracao'])+'x\n'
        perfil += 'Sinais gerados hoje: '+str(len(usuario['sinais']))+'\n'
        volat = str(usuario['volat']).replace('1', '⭐️').replace('2', '⭐️⭐️').replace('3', '⭐️⭐️⭐️')
        perfil += 'Filtro de notícias: '+str(volat)+' | '+str(usuario['dif_volat'])+' min | '+str(usuario['moeda'])+'ª\n\n'
        perfil += 'Pacote: '+str(usuario['plano'])+'\n'
        if str(usuario['plano']) == '🍀 Plus':
            try:
                perfil += 'Minha sala: '+usuario['sala']['nome']+'\n'
            except TypeError:
                perfil += 'Minha sala: '+usuario['sala']+'\n'
        perfil += 'Assinatura: '+str(usuario['vip'])+' dia (s)'
        
        return perfil
    
    def feedback(self, retorno, trend):
        
        if 'configs' in retorno.data:
            old_text = retorno.message.text
            if retorno.data == 'configs':
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(old_text, 'Configurações'))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      sub_configs)
            elif retorno.data == 'back-configs':
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(old_text))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      comunidade)
            elif retorno.data == 'noticias-configs':
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(old_text, 'Nível de volatividade que deseja filtrar'))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      volatividade)
            elif 'volat' in retorno.data:
                nivel = int(retorno.data.split('-')[1])
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'volat':nivel}})
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(old_text, 'Minutos de diferença entre o sinal e a notícia'))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      dif_noticia)
            elif 'min' in retorno.data:
                dif = int(retorno.data.split('-')[0])
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'dif_volat':dif}})
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(old_text, 'Moeda do ativo que será filtrada'))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      choose_moeda)
            elif 'moeda' in retorno.data:
                moeda = int(retorno.data.split('-')[1])
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'moeda':moeda}})
                self.client.edit_message_text(retorno.message.chat.id, 
                                              retorno.message.message_id, 
                                              self.mod(self.perfil(retorno)))
                self.client.edit_message_reply_markup(retorno.message.chat.id, 
                                                      retorno.message.message_id, 
                                                      comunidade)
            return None
              
        else:
            try:
                self.client.delete_messages(retorno.message.chat.id,
                                                retorno.message.message_id)
            except AttributeError:
                print('Erro cabuloso no chat.id')
          
        if retorno.data == 'InfoVIP':
            self.client.send_message(retorno.from_user.id, infovip)
            return None
          
        if '+' in retorno.data:
            self.client.send_message(retorno.from_user.id, 'Aguarde, só um segundo...')
            ativo = retorno.data.split('+')[1]
            resultado = trend.tendencia(ativo)
            self.client.send_message(retorno.from_user.id, 'Tendência de '+ativo+': '+resultado)
            return None
        
        if 'vivo' in retorno.data:
            if retorno.data == 'm1_vivo_ON':
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'insvivo': 'M1'}})
                self.client.send_message(retorno.from_user.id, 'M1 ativado. Agora é só aguardar os sinais chegarem')
            elif retorno.data == 'm5_vivo_ON':
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'insvivo': 'M5'}})
                self.client.send_message(retorno.from_user.id, 'M5 ativado. Agora é só aguardar os sinais chegarem')
            elif retorno.data == 'ao_vivo_OFF':
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'insvivo': 'OFF'}})
                self.client.send_message(retorno.from_user.id, 'Live desativada')
        
        elif 'pay' in retorno.data:
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_pay':int(retorno.data.split('-')[1])}})
            usuario = self.db.find_one(retorno.from_user.id)
            
            if usuario['last_analise'] == '#parcial':
                self.client.send_message(retorno.from_user.id, 'Agora escolha o intervalo de horário, que deseja gerar os sinais', reply_markup = horario_menu)
              
            elif usuario['last_analise'] == '#lista':
             
                self.client.send_message(retorno.from_user.id,
                                 '♻️ Aguarde, gerando sinais...')
                self.client.send_chat_action(retorno.from_user.id, 'typing')
               
                direcao = trend.tendencia(usuario['last_asset'])
                if 'VENDA' in direcao:
                    direcao = 'baixa'
                elif 'COMPRA' in direcao:
                    direcao = 'alta'
                else:
                     self.client.send_message(retorno.from_user.id, 'Escolha outro ativo ou volte daqui a 1h')
                     return None
                  
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_dir':direcao}})
                self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_dias':2}})
                
                self.client.send_chat_action(retorno.from_user.id, 'typing')
             
                now = datetime.now()
                for quatr4 in range( now.hour, (now + dt.timedelta(hours = 4)).hour ):
                    if self.limite(retorno, False):
                        break
                    self.gerar(usuario['last_asset'], str(quatr4), retorno, usuario['last_tf'])
                
                self.client.send_message(retorno.from_user.id,
                                     random.choice(frases),
                                     reply_markup=gerador)
                
            else:
                self.client.send_message(retorno.from_user.id,
                                 '♻️ Aguarde, gerando sinais...')
               
                for vinte4 in range(24):
                    if self.limite(retorno, False):
                        break
                    self.gerar(usuario['last_asset'], str(vinte4), retorno, usuario['last_tf'])
            
                self.client.send_message(retorno.from_user.id,
                                         random.choice(frases),
                                         reply_markup=gerador)
            
        elif 'tf' in retorno.data:
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_tf':int(retorno.data.split('-')[1])}})
            self.client.send_message(retorno.from_user.id, 'Escolha a porcentagem de assertividade', reply_markup = payout_menu)
            
        elif '=' in retorno.data:
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_dir':retorno.data.split('=')[0]}})
            self.client.send_message(retorno.from_user.id,
                                         'Escolha um timeframe',
                                         reply_markup = timeframe_menu)
           
        elif '-d' in retorno.data:
            dias = retorno.data.split('-')[0]
            
            if dias != 'default':
                dias = int(dias)
            
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_dias':dias}})
              
            if dias != 'default':
                self.client.send_message(retorno.from_user.id, 'Escolha a direção dos sinais', reply_markup = direcao_menu)
            else:
                self.client.send_message(retorno.from_user.id,
                                         'Escolha um timeframe',
                                         reply_markup = timeframe_menu)
           
        elif '#' in retorno.data:
            dia = datetime.now().isoweekday()
          
            self.db.update_one({'_id':retorno.from_user.id}, {'$set': {'last_analise':retorno.data}})
           
            if dia >= 6 and retorno.data == '#lista':
                self.client.send_message(retorno.from_user.id, 'Indisponível para OTC')
                return None
            elif retorno.data == '#lista':
                self.client.send_message(retorno.from_user.id,
                                         'Escolha um timeframe',
                                         reply_markup = timeframe_menu)
                return None
            
            self.client.send_message(retorno.from_user.id,
                                     'Deseja realizar o backtest de quantos dias?',
                                     reply_markup = cont_dias)
        
        elif not(retorno.data.isdigit()):
            if retorno.data == 'GBPJPY-OTC':
                self.client.send_message(retorno.from_user.id, 'Ativo indisponível')
                return None
            
            if not(self.managedb(retorno)):
                convite = 'https://t.me/IQOptionGenerator_bot?start='+str(retorno.from_user.id)
                self.client.send_message(retorno.from_user.id,
                                         '''Infelizmente, a quantidade de sinais que você pode gerar acabou. 😔\n
Você só pode gerar 5 sinais/dia.\n\nMas não se preocupe, amanhã tem mais. 😍\n\n
Ganhe 3 dias de assinatura grátis ao indicar um amigo com o seu link de convite:\n'''+convite+'''\n\n
Obs: Assinantes têm acesso ilimitado.\nPara mais informações clique aqui 👇''', reply_markup=info)
                return False
            
            self.client.send_message(retorno.from_user.id, 
                                     'De que forma deseja gerar os sinais do dia?',
                                     reply_markup = analise_menu)
           
        else:
            self.client.send_message(retorno.from_user.id,
                                 '♻️ Aguarde, gerando sinais...')

            usuario = self.db.find_one(retorno.from_user.id)
            self.gerar(usuario['last_asset'], retorno.data, retorno, usuario['last_tf'])
            
            self.client.send_message(retorno.from_user.id,
                                     random.choice(frases),
                                     reply_markup=gerador)
