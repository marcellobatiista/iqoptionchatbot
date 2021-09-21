from menus import gerador
from menus import inline_OTC
from menus import inline_NORMAL
from menus import menu_ativos
from menus import comunidade
from menus import m1_ON
from menus import m5_ON
from menus import ao_vivo_OFF
from menus import info
from menus import inline_TENDENCIA

import pytz
from datetime import datetime

from dateutil import parser
import datetime as dt

from noticias import Investing

class Body:
    client = None
    message = None
    db = None
    generator = None
    now = None
    acesso = None
    inv = Investing()
    mercadopago = None
    
    def __init__(self, client, message, mongodb, gerador, mp):
        self.now = datetime.now()
        self.acesso = '{}/{}/{}'.format(self.now.day, self.now.month, self.now.year)
        
        self.client = client
        self.message = message
        self.db = mongodb
        self.generator = gerador
        self.mercadopago = mp
        
        self.start()
        
        '''
        if not(self.message.from_user.id == 665448517):
            self.client.send_message(self.message.from_user.id, 'Em manutenção')
            return None
        '''
        
        self.comprovante()
        self.ativos()
        self.aovivo()
        self.tendencia()
        self.limpar()
        self.admin()
    
    def start(self):
        if self.message.text == None:
            pass
        elif '/start' in self.message.text or self.message.text == '🏠 Menu':
            self.client.send_message(self.message.from_user.id,
                                     'Seja bem-vindo!', reply_markup=gerador)
            self.registro()
            self.indicacao()
        else:
            self.db.update_one({'_id':self.message.from_user.id}, {'$set': {'last_hour':str(self.now.hour)+':'+str(self.now.minute)}})
    
    def registro(self):
        if self.db.find_one(self.message.from_user.id) == None:
            self.db.insert_one({'_id':self.message.from_user.id,
                                'username':'@'+str(self.message.from_user.username),
                                'max_geracao': 5,
                                'ult_acess':self.acesso,
                                'last_asset':None,
                                'last_tf':None,
                                'last_hour':None,
                                'last_dias': None,
                                'last_dir':None,
                                'vip': 0,
                                'sinais':[],
                                'indicacoes':[],
                                'last_analise': None,
                                'insvivo': 'OFF',
                                'volat': 2,
                                'dif_volat': 5,
                                'moeda': 1,
                                'plano': 'Free',
                                'sala': 'Sem registro',
                                'last_pay': 70})
            
            self.client.send_message(665448517, 'Novo usuário cadastrado: @'+str(self.message.from_user.username))
    
    
    def comprovante(self):
        if len(self.message.text) == 32:
            db = self.db.find_one(self.message.from_user.id)
            if self.message.text in self.db.find_one(665448517)['trans']:
                self.client.send_message(self.message.from_user.id, 'Transação em reuso negada.')
                return None
            
            pix = self.mercadopago.search(self.message.text) 
            if pix != None:
                if pix['valor'] == 5:
                    plano = '🏅Micro'
                    vip = 7
                elif pix['valor'] == 10:
                    plano = '🥉Mini'
                    vip = 15
                elif pix['valor'] == 20:
                    plano = '🥈Default'
                    vip = 30
                elif pix['valor'] == 40:
                    plano = '🥇 Premium'
                    vip = 60
                elif pix['valor'] == 50:
                    plano = '🍀 Plus'
                    vip = 30
                else:
                    plano = '🥈Default'
                    vip = int(pix['valor']/2)
                
                
                self.db.update_one({'_id':665448517}, 
                                   {
                                       '$push': {
                                            'trans':self.message.text
                                         }
                                   })
                
                self.db.update_one(
                            {'_id':self.message.from_user.id},
                            {
                                '$set': {
                                            'vip':db['vip'] + vip,
                                            'plano':plano
                                        }
                            },
                            upsert = True)
                self.client.send_message(self.message.from_user.id, 'Status: '+pix['status'].upper()+'\nBanco: '+pix['banco']+'\nValor: R$ '+str(pix['valor'])+' reais\n\nA assinatura de '+str(vip)+' dias foi adicionada em sua conta!\nPor favor, verifique seus dias clicando em [Perfil] no menu\n\nMuito obrigado! Sua contribuição será muito importante para o desenvolvimento contínuo do bot')
                self.client.send_message(665448517, str(self.message.from_user.id)+' fez uma transação no valor de R$ '+str(pix['valor'])+' reais pelo banco '+pix['banco'])
            else:
                self.client.send_message(self.message.from_user.id, 'Transação não encontrada. Por favor, verifique se o ID/Número está correto e tente mais uma vez ou envie o comprovante para @SP4CNE')
    
    def fhora(self, horario, timeframe=1):
        hora = parser.parse(horario) + dt.timedelta(minutes = -2*timeframe)
        hora = str(hora.hour)+':'+str(hora.minute)
        return hora

    def indicacao(self):
        msg = self.message.text
        if ('/start' in msg) and len(msg.split()) > 1:
            amigo_id = int(self.message.text.split()[1])
            indicado_id = self.message.from_user.id

            if amigo_id == indicado_id:
                self.client.send_message(indicado_id, 'Você não pode indicar a si mesmo')
                return None

            dbamigo = self.db.find_one(amigo_id)
            
            if dbamigo != None:
                dbindicado = self.db.find_one(indicado_id)
                if not(amigo_id in dbindicado['indicacoes']):
                    self.db.update_one(
                            {'_id':amigo_id},
                            {
                                '$push': {
                                            'indicacoes':indicado_id
                                         },
                                '$set': {
                                            'vip':dbamigo['vip'] + 3,
                                            'plano':dbamigo['plano'].replace('Free', 'Freemium')
                                        }
                            },
                            upsert = True)
                    
                    self.db.update_one(
                            {'_id':indicado_id},
                            {
                                '$push': {
                                            'indicacoes':amigo_id
                                         },
                                '$set': {
                                            'vip':dbindicado['vip'] + 1,
                                            'plano':'Freemium'
                                        }
                            },
                            upsert = True)
                    self.client.send_message(amigo_id, 'Você acabou de ganhar 3 dias\nde assinatura grátis por indicar @'+str(self.message.from_user.username))
                    self.client.send_message(indicado_id, 'Parabéns, você acaba de ganhar 1 dia de assinatura grátis\npor aceitar o convite do seu amigo')
                else:
                    self.client.send_message(indicado_id, 'Já houve indicação entre as partes')
            else:
                self.client.send_message(indicado_id, 'Seu amigo não é usuário do Bot ou o ID indicado não existe')

                
    def ativos(self):
        if self.message.text == '♻️ Gerar Sinais':
            self.client.send_message(self.message.from_user.id,
                                     'Escolha o tipo de mercado',
                                     reply_markup = menu_ativos)

        elif self.message.text == '✅ Check Sinais':
            usuario = self.db.find_one(self.message.from_user.id)
            bruto = self.inv.get_noticias()

            if usuario['ult_acess'] != self.acesso: #CleanDBSinais
                self.db.update_one(
                    {'_id':self.message.from_user.id},
                    {
                        '$set': {
                            'sinais': []}})
                self.client.send_message(self.message.from_user.id, '✋ Calma jovem, você ainda não gerou sinais hoje')
                return None

            
            if len(usuario['sinais']) != 0:
                texto = 'CheckList dos seus sinais\nData: '+self.acesso+'\n\n'     
                for sinal in usuario['sinais']:
                    
                    
                    isNoticia = None
                    if not('OTC' in sinal['ativo']):
                        moeda = sinal['ativo'][:3] if usuario['moeda'] == 1 else sinal['ativo'][3:]
                        isNoticia = self.inv.noticia(moeda, sinal['hora'], usuario['volat'], limite=usuario['dif_volat'], dir=-1, raw=bruto)
                        if isNoticia == None:
                            isNoticia = self.inv.noticia(moeda, sinal['hora'], usuario['volat'], limite=usuario['dif_volat'], dir=1, raw=bruto)
                        isNoticia = '' if isNoticia == None else ' - '+str(isNoticia[0])+' - '+str(isNoticia[1])+' notícia(s)'
                    else:
                        isNoticia = ''
                    
                    
                    R = self.generator.check_one(sinal['ativo'],
                                             sinal['tf'], 0,
                                             sinal['hora'])
                    
                    cw = False
                    for p, s in R.items():
                        if sinal['dir'] == s[0]:
                            sb = p.replace('0', '✅  ').replace('1', '✅¹ ').replace('2', '✅² ')
                            texto += sb+sinal['ativo']+' - '+self.fhora(sinal['hora'], sinal['tf'])+' - M'+str(sinal['tf'])+' - '+sinal['dir']+str(isNoticia)+'\n'
                            cw = True
                            break
                        elif s[0] == 'close':
                            texto += '🔒  '+sinal['ativo']+' - '+self.fhora(sinal['hora'], sinal['tf'])+' - M'+str(sinal['tf'])+' - '+sinal['dir']+str(isNoticia)+'\n'
                            cw = True
                            break
                    if cw == False:
                        texto += '❌  '+sinal['ativo']+' - '+self.fhora(sinal['hora'], sinal['tf'])+' - M'+str(sinal['tf'])+' - '+sinal['dir']+str(isNoticia)+'\n'
                
                texto += '\n\nLegenda:\n\n'
                texto += '⭐️ - Volat. Baixa\n'
                texto += '⭐️⭐️ - Volat. Moderada\n'
                texto += '⭐️⭐️⭐️ - Volat. Alta\n'
                texto += '— Filtro com '+str(usuario['dif_volat'])+' min de diferença'
                
                try:
                    self.client.send_message(self.message.from_user.id, texto)
                except: #Quando ultrapassa o limite de caracteres
                    quebra = texto.split('\n')
                    pedacos = 4
                    middle = int(len(quebra)/pedacos)

                    for parte, x in zip([quebra[:middle], quebra[middle::middle+1], quebra[len(quebra)-middle:]], range(pedacos)):
                        self.client.send_message(self.message.from_user.id, '\n'.join(parte))
            else:
                self.client.send_message(self.message.from_user.id, '✋ Calma jovem, você ainda não gerou sinais hoje')

        elif self.message.text == '🧙🏼‍♂️ Perfil':
            usuario = self.db.find_one(self.message.from_user.id)
            perfil = 'ID: '+str(self.message.from_user.id)+'\n'
            perfil += 'Nome: '+str(self.message.from_user.first_name)+' '+str(self.message.from_user.last_name)+'\n'
            perfil += 'Username: @'+str(self.message.from_user.username)+'\n\n'
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

            self.client.send_message(self.message.from_user.id, (perfil), reply_markup=comunidade)
            
        self.mercado_normal()
        self.mercado_otc()
        
    def mercado_normal(self):
        if self.message.text == '🚀 Normal':
            dia = datetime.now().isoweekday()
            if dia >= 6 or (dia == 5 and datetime.now().hour >= 17):
                self.client.send_message(self.message.from_user.id, 'O mercado está fechado')
                return None
            self.client.send_message(self.message.from_user.id,
                                     'Escolha um dos ativos',
                                     reply_markup = inline_NORMAL)
        
    def mercado_otc(self):
        if self.message.text == '⚔️ OTC':
            dia = datetime.now().isoweekday()
            if dia == 5 and datetime.now().hour >= 17:
                pass
            elif dia < 6:
                self.client.send_message(self.message.from_user.id, 'O mercado OTC está fechado')
                return None
            self.client.send_message(self.message.from_user.id,
                                     'Escolha um dos ativos',
                                     reply_markup = inline_OTC)
    
    def aovivo(self):
        if self.message.text == '🟢 Sinais 24h':
            user = self.db.find_one(self.message.from_user.id)
            usuario = user['insvivo']
            vip = user['vip']
            if vip > 0:
                label = 'Sinais 24h | Sinais 24h por dia, 7 dias por semana'
                if usuario == 'M1':
                     self.client.send_message(self.message.from_user.id, label, reply_markup = m1_ON)
                elif usuario == 'M5':
                     self.client.send_message(self.message.from_user.id, label, reply_markup = m5_ON)
                else:
                     self.client.send_message(self.message.from_user.id, label, reply_markup = ao_vivo_OFF)
            else:
                convite = 'https://t.me/IQOptionGenerator_bot?start='+str(self.message.from_user.id)
                self.client.send_message(self.message.from_user.id, 'Sinais 24h somente para assinantes.\n\nGanhe 3 dias de assinatura grátis ao indicar um amigo com o seu link de convite:\n'+convite+'\n\nPara mais informações clique aqui 👇', reply_markup = info)
    
    def tendencia(self):
        if self.message.text == '🏄🏼‍♂️ Tendência':
            self.client.send_message(self.message.from_user.id, 'Escolha um ativo para verificar a TENDÊNCIA de agora', reply_markup = inline_TENDENCIA)
    
    def limpar(self):
        if self.message.text == '🧹 Limpar Sinais':
            self.db.update_one(
                    {'_id':self.message.from_user.id},
                    {
                        '$set': {
                            'sinais': []}})
            self.client.send_message(self.message.from_user.id, 'CheckWin esvaziado')
    
    def admin(self):
        if not(self.message.from_user.id == 665448517):
            return None

        msg = self.message.text
        
        if ('/vip' in msg) and len(msg.split()) > 2:
            felizado_id = int(self.message.text.split()[1])
            dias = int(self.message.text.split()[2])
            plano = self.message.text.split()[3]
            
            plano = plano.replace('micro', '🏅Micro').replace('mini', '🥉Mini').replace('default', '🥈Default').replace('premium', '🥇 Premium').replace('plus', '🍀 Plus')

            dbfelizado = self.db.find_one(felizado_id)

            if dbfelizado == None:
                self.client.send_message(self.message.from_user.id, 'User não encontrado')
                return None
            
            self.db.update_one(
                            {'_id':felizado_id},
                            {
                                '$set': {
                                            'vip':dbfelizado['vip'] + dias
                                        }
                            })
            self.db.update_one({'_id':felizado_id}, {'$set': {'plano':plano}})
            
            if dias > 0:
                self.client.send_message(felizado_id, 'A assinatura de '+str(dias)+' dias foi adicionada em sua conta!\nPor favor, verifique seus dias clicando em [Perfil] no menu\n\nMuito obrigado! Sua contribuição será muito importante para o desenvolvimento contínuo do bot\n')
            self.client.send_message(self.message.from_user.id, str(dias)+' dias adicionados com sucesso')
        
        elif ('/geracao' in msg) and len(msg.split()) > 2:
            felizado_id = int(self.message.text.split()[1])
            vezes = int(self.message.text.split()[2])

            dbfelizado = self.db.find_one(felizado_id)

            if dbfelizado == None:
                self.client.send_message(self.message.from_user.id, 'User não encontrado')
                return None

            self.db.update_one(
                            {'_id':felizado_id},
                            {
                                '$set': {
                                            'max_geracao':dbfelizado['max_geracao'] + vezes
                                        }
                            })
            if vezes > 0:
                self.client.send_message(felizado_id, str(vezes)+' gerações foram adicionadas em sua conta!')
            self.client.send_message(self.message.from_user.id, str(vezes)+' gerações adicionado com sucesso')
        
        elif ('/mod' in msg) and len(msg.split()) > 2:
            felizado_id = int(self.message.text.split()[1])
            key = self.message.text.split()[2]
            value = self.message.text.split()[3].replace('_', ' ')
            tipo = self.message.text.split()[4]
            
            if tipo == 'array':
                value = [] if value == '[]' else list(value.strip('[').strip(']').split(','))
            elif tipo == 'dict':
                value = eval(value)
            elif tipo == 'int':
                value = int(value)
            elif tipo == 'str':
                pass

            dbfelizado = self.db.find_one(felizado_id)

            if dbfelizado == None:
                self.client.send_message(self.message.from_user.id, 'User não encontrado')
                return None
            try:
                self.db.update_one({'_id':felizado_id},{'$set': {key:value}})
                self.client.send_message(self.message.from_user.id, 'Modificação feita com sucesso.')
            except:
                self.client.send_message(self.message.from_user.id, 'Erro ao tentar modificar documento.')
        
        elif ('/buscar' in msg) and len(msg.split()) > 1:
            id = self.message.text.split()[1]
            if id.isdigit():
                dbfelizado = self.db.find_one(int(id))
            else:
                dbfelizado = self.db.find_one({'username':id})

            if dbfelizado == None:
                self.client.send_message(self.message.from_user.id, 'User não encontrado')
                return None
            
            log = ''

            for key, value in dbfelizado.items():
                if key == 'sinais' or key == 'indicacoes':
                    value = len(value)
                log += key+': '+str(value)+'\n'

            self.client.send_message(self.message.from_user.id, log)

        elif ('/msg' in msg) and len(msg.split()) > 1:
            usuarios = self.db.find()
            blockeds = ''
            for user in usuarios:
                try:
                    self.client.send_message((user['_id']), ' '.join(msg.split(' ')[1:]))
                except:
                    blockeds += str(user['_id'])+'\n'
                    continue
            self.client.send_message(self.message.from_user.id, 'Usuários que desistiram do bot:\n\n'+blockeds)
            
        elif '/usuarios' == msg:
            usuarios = self.db.find()
            cont = 0
            for user in usuarios:
                cont += 1
            self.client.send_message(self.message.from_user.id, str(cont)+' usuários cadastrados')
        
        elif ('/remover' in msg) and len(msg.split()) > 1:
            user_id = int(self.message.text.split()[1])
            
            dbuser_id = self.db.find_one(user_id)
            username = None

            if dbuser_id == None:
                self.client.send_message(self.message.from_user.id, 'User não encontrado')
                return None
            
            username = dbuser_id['username']
            self.db.delete_one({"_id": user_id})
            self.client.send_message(self.message.from_user.id, str(username)+' removido do db')
