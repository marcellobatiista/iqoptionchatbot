import datetime as dt
from datetime import datetime
import time
from dateutil import parser
from menus import info
from noticias import Investing
import pyrogram

class AOVIVO:
    client = None
    db = None
    gerador = None
    now = datetime.now()
    trend = None
    inv = Investing()
    bruto = None
    
    def __init__(self, client, db, gerador, trend):
        self.client = client
        self.db = db
        self.gerador = gerador
        self.trend = trend
        
        self.bruto = self.inv.get_noticias()

    def q_max(self, lista):
        c_max = lista.count('call')
        p_max = lista.count('put')

        if c_max > p_max:
            return 'call'
        elif c_max < p_max:
            return 'put'
        else:
            return None

    def quadrantes(self, ativo):
        q1 = datetime.now() + dt.timedelta(minutes = -1)
        qs1 = q1.strftime('%H:%M')
        quadrante1 = list(self.gerador.check_aovivo(ativo, 1, 0, qs1).values())

        q2 = q1 + dt.timedelta(minutes = -5)
        qs2 = q2.strftime('%H:%M')
        quadrante2 = list(self.gerador.check_aovivo(ativo, 1, 0, qs2).values())

        qmax1 = self.q_max(quadrante1)
        qmax2 = self.q_max(quadrante2)
            
        if (qmax1 == qmax2) and (qmax1 != None):
            entrada = (q1 + dt.timedelta(minutes = 3)).strftime('%H:%M')
            direcao = qmax1
            
            texto = '🔰 ('+ativo+') - M1\n\n'
            texto += '♻️ Direção: '+direcao+'\n'
            texto += '⏱ Horário: '+entrada+'\n\n'
            
            if not('OTC' in ativo):
                texto += '🏄🏼‍♂️ Tendência: '+self.trend.tendencia_tf(ativo, 'M1').lower()+'\n'
            
            bpay = self.gerador.buy(ativo, 1)['payout']
            pay = '%' if type(bpay) == str else bpay*100
            texto += '💸 Payout: '+str(pay)+'%'
            
            return {'dados':{'ativo':ativo, 'horario':entrada, 'dir':direcao, 'tf':1}, 'texto':texto}
        else:
            return None

    def quadrantes_m5(self, ativo):
        q1 = datetime.now() + dt.timedelta(minutes = -5)
        qs1 = q1.strftime('%H:%M')
        quadrante1 = list(self.gerador.check_aovivo(ativo, 5, 0, qs1).values())

        q2 = q1 + dt.timedelta(minutes = -15)
        qs2 = q2.strftime('%H:%M')
        quadrante2 = list(self.gerador.check_aovivo(ativo, 5, 0, qs2).values())

        qmax1 = self.q_max(quadrante1)
        qmax2 = self.q_max(quadrante2)
            
        if (qmax1 == qmax2) and (qmax1 != None):
            entrada = (q1 + dt.timedelta(minutes = 15)).strftime('%H:%M')
            direcao = qmax1
            
            texto = '🔰 ('+ativo+') - M5\n'
            texto += '♻️ Direção: '+direcao+'\n'
            texto += '⏱ Horário: '+entrada+'\n\n'
            
            if not('OTC' in ativo):
                texto += '🏄🏼‍♂️ Tendência: '+self.trend.tendencia_tf(ativo, 'M5').lower()+'\n'
                
            bpay = self.gerador.buy(ativo, 5)['payout']
            pay = '%' if type(bpay) == str else bpay*100
            texto += '💸 Payout: '+str(pay)+'%'
            
            return {'dados':{'ativo':ativo, 'horario':entrada, 'dir':direcao, 'tf':5}, 'texto':texto}
        else:
            return None
    
    def noticia(self, usuario, sinal, bruto):
        sinal = sinal['dados']
        isNoticia = None
        if not('OTC' in sinal['ativo']):
            moeda = sinal['ativo'][:3] if usuario['moeda'] == 1 else sinal['ativo'][3:]
            isNoticia = self.inv.noticia(moeda, sinal['horario'], usuario['volat'], limite=usuario['dif_volat'], dir=-1, raw=bruto)
            if isNoticia == None:
                isNoticia = self.inv.noticia(moeda, sinal['horario'], usuario['volat'], limite=usuario['dif_volat'], dir=1, raw=bruto)
            isNoticia = '\n📣 Notícia: nenhuma' if isNoticia == None else '\n📣 Notícia: '+str(isNoticia[0])+' - '+str(isNoticia[1])+' notícia(s)'
        else:
            isNoticia = ''
            
        hk = parser.parse(sinal['horario']) + dt.timedelta(minutes=2)
        hk = str(hk.hour)+':'+str(hk.minute)
        direcao = sinal['dir'].replace('call', 'alta').replace('put', 'baixa')
        proba = self.gerador.probabilidade(sinal['ativo'], hk, 15, sinal['tf'], direcao, vivo = True)
        pbs = ''
        if proba != None:
            if proba['text'] != '':
                for txt in proba['text'].split('\n'):
                    if '✅' in txt:
                        pbs += txt + '\n'
                        
        isNoticia = (isNoticia + '\n\n' + pbs)
                
        return isNoticia
        
    def RUN(self):
        future = None
        sinal = None
        flag = False
        c = 0
        ativos = ['EURUSD', 'AUDCAD', 'EURGBP', 'EURJPY', 'NZDUSD']
        otc = ['EURUSD-OTC', 'EURGBP-OTC', 'AUDCAD-OTC', 'EURJPY-OTC', 'NZDUSD-OTC']
        ativo = None
        
        sinalm5 = None
        flag_m5 = None
        future_m5 = None
        
        last_dia = self.now.isoweekday()
        
        while 1:
            self.now = datetime.now()
            now_min = self.now.minute
            
            if self.filtro(self.now):
                continue
            
            if flag:
                if now_min >= future:
                    self.checkwin('M1')
                    future = sinal = None
                    flag = False
                    
            if flag_m5:
                if now_min >= future_m5:
                    self.checkwin('M5')
                    future_m5 = sinalm5 = None
                    flag_m5 = False
                
            if now_min % 5 == 0:
                dia = self.now.isoweekday()
                
                if last_dia != dia:
                    self.bruto = self.inv.get_noticias()
                    last_dia = dia
                
                if dia >= 6:
                    ativo = otc
                else:
                    if dia == 5 and self.now.hour >= 17:
                        ativo = otc
                    else:
                        ativo = ativos
                
                sinal = self.quadrantes(ativo[c])
                
                if sinal != None:
                    #-------------------------TMP------------------------------#
                    if self.gerador.check_open('turbo', ativo[c]) == False:
                        c += 1
                        if c >= 5:
                            c = 0
                        continue
                    #-------------------------TMP------------------------------#
                    self.db.update_one({'_id':665448517}, {'$set': {'aovivo':sinal['dados']}})
                    self.inscritos(sinal, 'M1')
                    future = ( parser.parse(sinal['dados']['horario']) + dt.timedelta(minutes = 3) ).minute
                    flag = True
                    
                    
                if now_min == 0 or now_min == 30:
                    sinalm5 = self.quadrantes_m5(ativo[c])
                    if sinalm5 != None:
                        #-------------------------TMP------------------------------#
                        if self.gerador.check_open('binary', ativo[c]) == False:
                            c += 1
                            if c >= 5:
                                c = 0
                            continue
                        #-------------------------TMP------------------------------#
                        self.db.update_one({'_id':665448517}, {'$set': {'aovivo_m5':sinalm5['dados']}})
                        self.inscritos(sinalm5, 'M5')
                        future_m5 = ( parser.parse(sinalm5['dados']['horario']) + dt.timedelta(minutes = 15) ).minute
                        flag_m5 = True
                        
                
                c += 1
                if c >= 5:
                     c = 0
                time.sleep(60)
                
            time.sleep(1)
    
    def filtro(self, now):
        if now.isoweekday() == 5:
            if now.hour >= 17:
                return False
            return False
        elif now.isoweekday() < 6:
            if now.hour >= 18 and now.hour <= 23:
                time.sleep(60)
                return True
            else:
                return False
        elif now.isoweekday() == 7 and now.hour >= 21:
            time.sleep(60)
            return True
        else:
            return False
    
    def inscritos(self, sinal, timeframe):
        
        dados = sinal
        sinal = sinal['texto']
        usuarios = self.db.find()
        
        for user in usuarios:
            
            '''
            if user['_id'] != 665448517:
                self.db.update_one({'_id':user['_id']}, {'$set': {'insvivo':'OFF'}}) #MANUTENÇÃO
            '''
            
            if user['insvivo'] == timeframe:
                try:
                    ntc = self.noticia(user, dados, self.bruto)
                    self.client.send_message(user['_id'], sinal+ntc)
                    if user['plano'] == '🍀 Plus' and user['sala'] != 'Sem registro':
                        try:
                            self.client.send_message(user['sala']['id'], sinal+ntc)
                        except pyrogram.errors.exceptions.bad_request_400.ChannelPrivate:
                            self.db.update_one({'_id':user['_id']}, {'$set': {'sala':'Sem registro'}})
                        except pyrogram.errors.exceptions.bad_request_400.ChannelInvalid:
                            self.db.update_one({'_id':user['_id']}, {'$set': {'sala':'Sem registro'}})
                            
                except:
                    print('Error aqui, verificar')
                    continue
                
                acesso = '{}/{}/{}'.format(self.now.day, self.now.month, self.now.year)
                if user['ult_acess'] != acesso and user['vip'] > 0: #atualiza os dias de assinatura pra quem tá com a live ligada
                    
                    self.db.update_one({'_id':user['_id']}, {'$set': {'sinais': []}}) #CleanDBSinais
                    
                    self.db.update_one({'_id':user['_id']}, {'$set': {'ult_acess':acesso}})
                    self.db.update_one({'_id':user['_id']}, {'$set': {'vip':user['vip']-1}})
                    
                elif user['vip'] <= 0:
                    self.db.update_one({'_id':user['_id']}, {'$set': {'insvivo':'OFF'}})
                    self.db.update_one({'_id':user['_id']}, {'$set': {'plano':'Free'}})
                    self.db.update_one({'_id':user['_id']}, {'$set': {'sala':'Sem registro'}})
                    self.client.send_message(user['_id'], 'Seus dias de assinatura acabaram.\n\nPara mais informações clique aqui 👇', reply_markup=info)
    
    def checkwin(self, tf):
        
        if tf == 'M1':
            sinal = self.db.find_one(665448517)['aovivo']
        
            horario = (parser.parse(sinal['horario']) + dt.timedelta(minutes = 2)).strftime('%H:%M')
            resultado = self.gerador.check_one(sinal['ativo'], sinal['tf'], 0, horario)
        elif tf == 'M5':
            sinal = self.db.find_one(665448517)['aovivo_m5']
        
            horario = (parser.parse(sinal['horario']) + dt.timedelta(minutes = 10)).strftime('%H:%M')
            resultado = self.gerador.check_one(sinal['ativo'], sinal['tf'], 0, horario)
            
        texto = ''
        cw = False
        for p, s in resultado.items():
            if sinal['dir'] == s[0]:
                sb = p.replace('0', '✅  ').replace('1', '✅¹ ').replace('2', '✅² ')
                texto += sb+sinal['ativo']+' - '+sinal['horario']+' - M'+str(sinal['tf'])+' - '+sinal['dir']+' - WIN\n'
                cw = True
                break
            elif s[0] == 'close':
                texto += 'Sem CheckWin\n'
                cw = True
                break
        if cw == False:
            texto += '❌  '+sinal['ativo']+' - '+sinal['horario']+' - M'+str(sinal['tf'])+' - '+sinal['dir']+' - LOSS\n'
        
        
        usuarios = self.db.find()
        for user in usuarios:
            if user['insvivo'] == tf:
                self.client.send_message(user['_id'], texto)
                if user['plano'] == '🍀 Plus' and user['sala'] != 'Sem registro':
                    try:
                        self.client.send_message(user['sala']['id'], texto)
                    except pyrogram.errors.exceptions.bad_request_400.ChannelPrivate:
                        self.db.update_one({'_id':user['_id']}, {'$set': {'sala':'Sem registro'}})
