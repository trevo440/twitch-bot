from irc.bot import SingleServerIRCBot
from requests import get
from lib import cmds, react
from lib.cmds import db

NAME = 'trevobot'
OWNER = 'HIDDEN'

class Bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = 'irc.chat.twitch.tv'
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = 'HIDDEN'
        self.TOKEN = 'HIDDEN'
        self.CHANNEL = f'#{OWNER}'
        
        url = f'https://api.twitch.tv/kraken/users?login={self.USERNAME}'
        headers = {'CLIENT-ID': self.CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        resp = get(url, headers=headers).json()
        self.channel_id = resp['users'][0]['_id']
        
        super().__init__([(self.HOST, self.PORT, f'oauth:{self.TOKEN}')], self.USERNAME, self.USERNAME)
        
    def on_welcome(self, cxn, event):
        for req in ('membership', 'tags', 'commands'):
            cxn.cap('REQ', f':twitch.tv/{req}')
        db.build()    
        cxn.join(self.CHANNEL)
        self.send_message('Now online.')
    @db.with_commit    
    def on_pubmsg(self, cxn, event):
        tags = {kvpair['key']: kvpair['value'] for kvpair in event.tags}
        user = {'name': tags['display-name'], 'id': tags['user-id']}
        message = event.arguments[0]
        
        if user['name'] != NAME:
            react.process(bot, user, message)
            cmds.process(bot, user, message)
        
    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)
        
if __name__ == '__main__':
    bot = Bot()
    bot.start()
