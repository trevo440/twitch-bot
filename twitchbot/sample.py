"""
    COPYRIGHT INFORMATION
    ---------------------
Python Twitch bot (twitch_tut.py)
    Copyright � Parafoxia 2020.
    Copyright � Carberra 2020.
This bot was created on the Carberra YouTube channel. The tutorial series it featured in can be found here:
    https://www.youtube.com/playlist?list=PLYeOw6sTSy6ZFDkfO9Kl8d37H_3wLyNxO
This bot can be freely copied and modified without permission, but not sold as is.
Some code in this file is licensed under the Apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/
    NOTES
    -----
You will obviously need to modify `NAME`, `OWNER`, `bot.CLIENT_ID`, and `bot.TOKEN` to your own info before running the bot.
Otherwise, the modifications to this code, and all the code in the /lib directory, are copyright � Carberra 2020.
"""

from irc.bot import SingleServerIRCBot
from requests import get

from lib import db, cmds, react, automod

NAME = "your bot's name here"
OWNER = "your channel's name here"


class Bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = "your bot's Client ID here"
        self.TOKEN = "your bot's token here"
        self.CHANNEL = f"#{OWNER}"

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        db.build()
        self.send_message("Now online.")

    @db.with_commit
    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        react.add_user(bot, user)

        if user["name"] != NAME and automod.clear(bot, user, message):
            react.process(bot, user, message)
            cmds.process(bot, user, message)

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
    bot = Bot()
    bot.start()