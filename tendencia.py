import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Tendencia:
  browser = None
  
  def __init__(self):
      options = webdriver.ChromeOptions()
      options.add_argument("headless")
      options.add_argument('--disable-dev-shm-usage')
      options.add_argument("--no-sandbox")

      path = ChromeDriverManager().install()
      self.browser  = webdriver.Chrome(executable_path=path, options=options)

  def tendencia(self, ativo):
      self.browser.get('https://br.tradingview.com/symbols/'+ativo+'/technicals/')
      times = []
      for timeframe in ['//*[@id="technicals-root"]/div/div/div[1]/div/div/div/button[4]'
                        ,'//*[@id="technicals-root"]/div/div/div[1]/div/div/div/button[5]']: #H1 && H4
          btn = self.browser.find_element_by_xpath(timeframe)#.click()
          self.browser.execute_script("arguments[0].click();", btn)
          time.sleep(3)
          summary = self.browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[2]')
          tendencia = summary.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[2]/span[2]').text
          times.append(tendencia)
        
      if times[0] in times[1] or times[1] in times[0]:
          return times[0]
      else:
          return 'SEM CONFLUÊNCIA'


  def tendencia_tf(self, ativo, tf):
      self.browser.get('https://br.tradingview.com/symbols/'+ativo+'/technicals/')
      
      try:
          tfs = {'M1': '/html/body/div[3]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div/button[1]',
                 'M5': '/html/body/div[3]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div/button[2]',
                 'M15': '/html/body/div[3]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div/button[3]',
                 'H1': '/html/body/div[3]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div/button[5]',
                 'H4': '/html/body/div[3]/div[5]/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div/div/button[7]'}

          btn = self.browser.find_element_by_xpath(tfs[tf])#.click()
          self.browser.execute_script("arguments[0].click();", btn)
          time.sleep(3)
          summary = self.browser.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[2]')
          tendencia = summary.find_element_by_xpath('//*[@id="technicals-root"]/div/div/div[2]/div[2]/span[2]').text

          return tendencia
      except:
          return 'SEM CONFLUÊNCIA'
      
#print(Tendencia().tendencia_tf('USDJPY', 'M15'))
