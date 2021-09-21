from iqoptionapi.stable_api import IQ_Option
import datetime as dt
from datetime import datetime
import time
from dateutil import parser, tz

from pytz import timezone


API = IQ_Option('', '')
print(API.connect())
#API.change_balance('PRACTICE')

class Generator:
    
    
    def check_open(self, time, ativo):
        pares = API.get_all_open_time()
        if pares[time][ativo]['open'] == {}:
            return False
        else:
            return pares[time][ativo]['open']
    
    def check_buy(self, id):
        compra = API.get_async_order(id)
        while len(compra)==0:
            compra = API.get_async_order(id)

        try:
            valor = compra['option-opened']['msg']['amount']
            direcao = compra['option-opened']['msg']['direction']
            ativo = compra['option-opened']['msg']['active']
            abertura = compra['option-opened']['msg']['value']
            expiracao = compra['option-opened']['msg']['expiration_time']
            payout = (compra['option-opened']['msg']['profit_percent']-100)/100
        
        except KeyError:
            try:
                self.check_buy(id)
            except RecursionError:
                return None
                
    
        return {'valor':valor,
                'ativo':ativo,
                'open':abertura,
                'exp':expiracao,
                'dir':direcao,
                'payout':payout}
    
    def buy(self, ativo, timeframe, quantia = 1, direc = 'call'):
        check, id = API.buy(quantia, ativo, direc, timeframe)
        if check == False:
            API.sell_option(id)
            return {'payout': 'Sem payout'}
        else:
            API.sell_option(id)
            return self.check_buy(id)
    
    def check_aovivo(self, ativo, tf, dias, horario):
          """
              Função responsável por verificar sinais
              num horário específico em função da quantidade
              de dias
          """
          # tf: Timeframe
          # horario: Horário em que a vela surgiu
          # dias: Quantidade de dias (Para o passado) /** Dia 0 -> Dial atual **\\
            
          # Quantidade de velas do passado
          if tf == 1:
              qt_velas = 5
              VL = ['0', '1', '2', '3', '4']
          elif tf == 5:
              qt_velas = 3
              VL = ['0', '1', '2']
                
          hoje = (parser.parse(horario)).timestamp()
          velas = API.get_candles(ativo, tf*60, qt_velas, hoje - (dias * 24 * 3600))
                
          sinal = {}
          for s, vela in zip(VL, velas):
              if vela['open'] < vela['close']:
                  sinal[s] = 'call'
              elif vela['open'] == vela['close']:
                  sinal[s] = 'doji'
              elif vela['open'] > vela['close']:
                  sinal[s] = 'put'
                
          return sinal
    
    
    def check(self, ativo, tf, dias, horario):
        """
            Função responsável por verificar sinais
            num horário específico em função da quantidade
            de dias
        """
        # tf: Timeframe
        # horario: Horário em que a vela surgiu
        # dias: Quantidade de dias (Para o passado) /** Dia 0 -> Dial atual **\\

        # Quantidade de velas do passado
        qt_velas = 3
        
        hoje = (parser.parse(horario)).timestamp()
        velas = API.get_candles(ativo, tf*60, qt_velas, hoje - (dias * 24 * 3600))
        
        sinal = {}
        for s, vela in zip(['0', '1', '2'], velas):
            if vela['open'] < vela['close']:
                sinal[s] = ['call']
            elif vela['open'] == vela['close']:
                sinal[s] = ['doji']
            elif vela['open'] > vela['close']:
                sinal[s] = ['put']
        
        return sinal

    def check_one(self, ativo, tf, dias = 0, horario = ''):
        qt_velas = 3
        
        hoje = (parser.parse(horario)).timestamp()
        velas = API.get_candles(ativo, tf*60, qt_velas, hoje - (dias * 24 * 3600))
        
        sinal = {}
        for s, vela in zip(['0', '1', '2'], velas):
            now = datetime.now()
            vl = parser.parse(horario)
            
            if vl > now:
                sinal[s] = ['close']
            elif vela['open'] < vela['close']:
                sinal[s] = ['call']
            elif vela['open'] == vela['close']:
                sinal[s] = ['doji']
            elif vela['open'] > vela['close']:
                sinal[s] = ['put']
            
        return sinal

    def catalogacao(self, ativo, horario, dias, tf = 1, getTrend = False):
        catalago = None
        for dia in range(1, dias+1):
            cat = self.check(ativo, tf, dia, horario)
            if dia != 1:
                for h in cat:
                    catalago[h].append(cat[h][0])
            else:
                catalago = cat
        if getTrend: #Pega catalogação passada de M5, pra ver a Trend
            return catalago[list(catalago)[len(catalago)-1]]
        else:
            return catalago
        
    def trend_maior(self, ativo, horario, dias, timeframe):
        maior = 30 if timeframe == 5 else 5
        
        hk = parser.parse(horario)
        hk = str(hk.hour)+':'+str(hk.minute)
        
        hora = parser.parse(horario) + dt.timedelta(minutes = -2*timeframe)
        trend_hora = str(hora.hour)+':'+str(hora.minute)
        past_trend = self.catalogacao(ativo, trend_hora, dias, maior, True)
        
        
        if past_trend.count('call') > past_trend.count('put'):
            past_trend = 'alta'
        elif past_trend.count('put') > past_trend.count('call'):
            past_trend = 'baixa'
        else:
            past_trend = None
            
        return trend_hora, past_trend, hk
            
        
    def probabilidade(self, ativo, horario, dias, timeframe, last_dir, vivo=False, last_pay=70):
        
        if dias == 'default':
            layer_two = self.trend_maior(ativo, horario, 7, timeframe)
            trend_hora, past_trend, hk = layer_two
            dias = 7
            criterio = 70
        else:
            hk = parser.parse(horario)
            hk = str(hk.hour)+':'+str(hk.minute)
            hora = parser.parse(horario) + dt.timedelta(minutes = -2*timeframe)
            trend_hora = str(hora.hour)+':'+str(hora.minute)
            past_trend = last_dir
            criterio = 100 if last_pay == 200 else 0 #Porcetangem da primeira entrada
            last_pay = 100 if last_pay == 200 else last_pay
        
        assert_gale = 40 if vivo == True else last_pay #Porcentagem dos martingales
        backtest = ''
        sinal = self.catalogacao(ativo, horario, dias, timeframe)
        last = None
        direc = None
        
        for step, horario in zip(['✅ ', '✅🐔 ', '✅🐔🐔 '], sinal):
            total = len(sinal[horario])
            calls = sinal[horario].count('call')
            puts = sinal[horario].count('put')

            if past_trend == 'alta':
                assertividade = (calls/dias)*100
                
                '''
                if vivo:
                    backtest += step + '('+str(round(assertividade, 2)) + '%)\n'
                '''
                if last != None:    
                    good = last <= assertividade
                    if not(good):
                        return None
                    else:
                        if assertividade >= assert_gale:
                            backtest += step + '('+str(round(assertividade, 2)) + '%)\n'
                            last = assertividade
                        else:
                            return None
                else:
                    last = assertividade
                    if not(last >= criterio):
                        return None
                    backtest += '🔰 ('+ativo+') - M'+str(timeframe)+'\n\n'
                    backtest += '♻️ Direção: CALL\n'
                    backtest += '⏱ Horário: '+trend_hora+'\n\n'+ step+'('+str(round(last, 2)) + '%)\n'
                    direc = 'call'                

                
            elif past_trend == 'baixa':
                assertividade = (puts/dias)*100
                '''
                if vivo:
                    backtest += step + '('+str(round(assertividade, 2)) + '%)\n'
                '''
                if last != None:
                    good = last <= assertividade
                    if not(good):
                        return None
                    else:
                        if assertividade >= assert_gale:
                            backtest += step + '('+str(round(assertividade, 2)) + '%)\n'
                            last = assertividade
                        else:
                            return None
                else:
                    last = assertividade
                    if not(last >= criterio):
                        return None
                    backtest += '🔰 ('+ativo+') - M'+str(timeframe)+'\n\n'
                    backtest += '♻️ Direção: PUT\n'
                    backtest += '⏱ Horário: '+trend_hora+'\n\n' + step + '('+str(round(last, 2)) + '%)\n'
                    direc = 'put'
                    
        
        
        return {'text':backtest, 'dados':{'ativo':ativo, 'hora':hk, 'dir':direc, 'tf':timeframe}}
