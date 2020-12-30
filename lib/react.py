from collections import defaultdict
from lib.cmds import db
from random import randint
from datetime import datetime, timedelta

welcomed = []
messages = defaultdict(int)

def process(bot, user, message):
    update_records(bot, user)
    if user["id"] not in welcomed:
        welcome(bot, user)
    elif "bye" in message:
        say_goodbye(bot, user)
        
    check_activity(bot, user)
    
def update_records(bot, user):
    db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)",
        user["id"])
    db.execute("UPDATE users SET MessagesSent = MessagesSent + 1 WHERE UserID = ?",
        user["id"])
    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?",
        user["id"])
    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        
        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?",
            randint(1, 50), coinlock, user["id"])
    
def welcome(bot, user):
    bot.send_message(f'Welcome to the stream {user["name"]}')
    welcomed.append(user["id"])
    
def say_goodbye(bot, user):
    bot.send_message(f'Goodbye {user["name"]}!')
    
def check_activity(bot, user):
    messages[user["id"]] +=1
    if (count := messages[user["id"]]) % 25 == 0:
        bot.send_message(f'interesting point but imma disagree {user["name"]}')
