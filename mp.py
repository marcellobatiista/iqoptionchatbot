import mercadopago

class MercadoPago:

    sdk = pays = result = None
  
    def __init__(self):
        self.sdk = mercadopago.SDK('')
        self.pays = self.sdk.payment()
        self.result = self.pays.search()['response']['results'] #Lista    

    def status(self, client):
        return client['status']  

    def bank(self, client):
        point = client['point_of_interaction']
        for k in point:
            if 'transaction_data' in k:
                return point[k]['bank_info']['payer']['long_name']

    def details(self, client):
        detalhes = client['transaction_details']
        d = {}
        for e, k in enumerate(detalhes):
            d[k] = detalhes[k]
            if e >= 1:
                break
        return d


    def search(self, transaction):
        for client in self.result:
            try:
                tran = self.details(client)['transaction_id'].replace('PIXE', '')
            except KeyError:
                continue
            if tran.lower() in transaction.lower():
                 if self.status(client) == 'approved':
                     return {'status':'aprovado',
                             'banco':self.bank(client),
                             'valor':self.details(client)['total_paid_amount']}

#mp = MercadoPago()
#print(mp.search('PIXE228964312021061001002971031445'))
