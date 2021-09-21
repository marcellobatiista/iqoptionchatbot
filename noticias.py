from bs4 import BeautifulSoup
import requests
from pprint import pprint
from dateutil import parser
import datetime as dt


class Investing:
    
    soup = None
    
    def __init__(self):
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329'})
        pagina = requests.get('http://br.investing.com/economic-calendar/', headers = headers)
        self.soup = BeautifulSoup(pagina.content, 'html.parser')
    
    def get_noticias(self):
        noticia = self.soup.find('td', {'class':'theDay'}).get_text() + '\n\n'

        k_hora = k_moeda = k_volat = {}
        
        for horario in zip(self.soup.find_all('td', {'class':'first left time js-time'}),
                           self.soup.find_all('td', {'class':'left flagCur noWrap'}),
                           self.soup.find_all('td', {'class':'left textNum sentiment noWrap'})
                                                                                        ):
            hora = horario[0].get_text()
            moeda = horario[1].get_text(strip = True)
            volat = horario[2].get('data-img_key').replace('bull1', '⭐️').replace('bull2', '⭐️⭐️').replace('bull3', '⭐️⭐️⭐️')

            if hora in k_hora:
                k_hora[hora].append({'moeda':moeda, 'volat':volat})
            else:
                k_hora[hora] = [{'moeda':moeda, 'volat':volat}]

            if moeda in k_moeda:
                k_moeda[moeda].append({'hora':hora, 'volat':volat})
            else:
                k_moeda[moeda] = [{'hora':hora, 'volat':volat}]

            if volat in k_volat:
                k_volat[volat].append({'hora':hora, 'moeda':moeda})
            else:
                k_volat[volat] = [{'hora':hora, 'moeda':moeda}]
            
            linha = hora+'  '+moeda+'  '+volat+'\n'
            
            noticia += linha
        
        return {'all':noticia, 'hora':k_hora, 'moeda':k_moeda, 'volat':k_volat}

    def get(self, arg, raw):
        n = raw
        arg = str(arg)
        
        if arg.isdigit():
            if arg == '1':
                arg = '⭐️'
            elif arg == '2':
                arg = '⭐️⭐️'
            else:
                arg = '⭐️⭐️⭐️'
            return n['volat'][arg]
        elif 'all' in arg:
            return n['all']
        elif not(arg.islower()):
            try:
                return n['moeda'][arg]
            except KeyError:
                pass
                
        elif ':' in arg:
            return n['hora'][arg]
        
                
    def search(self, ativo = '', horario = '', volat = '', raw = ''):
        if ativo == horario == volat:
            return self.get('all')
        
        volat = str(volat)
        tmp = []
        
        if volat == '1':
            volat = '⭐️'
        elif volat == '2':
            volat = '⭐️⭐️'
        else:
            volat = '⭐️⭐️⭐️'
        
        take = self.get(ativo, raw)
        if take == None:
            return -1
        for all in take:
            if all['hora'] == horario and all['volat'] == volat:
                tmp.append(all)
        return len(tmp)

    def noticia(self, ativo, horario, volat, limite, dir, raw):    
        horario = parser.parse(horario)
        dir = -1 if dir < 0 else 1

        for n in range(limite):
            novo = horario.strftime('%H:%M')
            isSearch = self.search(ativo, horario=novo, volat=volat, raw=raw)
            if isSearch > 0:
                if volat == 1:
                    return '⭐️', isSearch
                if volat == 2:
                    return '⭐️⭐️', isSearch
                else:
                    return '⭐️⭐️⭐️', isSearch
            
            horario = horario + dt.timedelta(minutes=dir)

#inv = Investing()
#raw = inv.get_noticias()
#print(inv.noticia('USD', '08:22', 1, limite=30, dir=-1, raw=raw))
        
        
