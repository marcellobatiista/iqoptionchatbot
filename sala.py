class SalaDeSinais:
  
    client = message = db = None
    admins = None

    def __init__(self, client, message, collection):
        self.client = client
        self.message = message
        self.db = collection
        
        self.list_admins()
        found = self.search_db()
        self.verify(found)
        
    def list_admins(self):
        self.admins = []
        for admin in self.client.get_chat_members(self.message.chat.id, filter="administrators"):
            self.admins.append(admin.user.id)
      
    def search_db(self):
        found = False
        for user in self.db.find():
            if user['_id'] in self.admins and user['plano'] == '🍀 Plus':
                found = self.send_update(user)
                break
        return found
      
    def send_update(self, user):
        sala = {'nome':self.message.chat.title, 'id':self.message.chat.id}
        self.db.update_one({'_id':user['_id']}, {'$set': {'sala':sala}})
        self.client.send_message(self.message.chat.id, 'Ligado!')
        return True
      
    def verify(self, found):
        if found == False:
            self.client.send_message(self.message.chat.id, 'Fuizz!')
            self.client.leave_chat(self.message.chat.id)
