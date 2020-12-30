from lib.cmds import db
import random

def coins(bot, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?",
        user["id"])
    bot.send_message(f'{user["name"]}, you have {coins:,} coins.')
    
def gamble(bot, user, *args):
    coin = db.field("SELECT Coins FROM users WHERE UserID = ?",
        user["id"])
    
    try: 
        arg = args[0]        
        if coin >= abs(int(arg)):
            i = random.randrange(1, 15)
            if i <= 3:
                db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                    abs(int(arg)), user["id"])
                bot.send_message(f'Congrats {user["name"]}! You won {arg} Coins')
            else: 
                db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
                    abs(int(arg)), user["id"])
                bot.send_message(f'Sorry {user["name"]}... You lost {arg} Coins')
        
    except (IndexError, ValueError):       
        if coin >= 10:
            i = random.randrange(1, 15)
            if i <= 3:
                db.execute("UPDATE users SET Coins = Coins + 10 WHERE UserID = ?",
                    user["id"])
                bot.send_message(f'Congrats {user["name"]}! You won 10 Coins')
            else: 
                db.execute("UPDATE users SET Coins = Coins - 10 WHERE UserID = ?",
                    user["id"])
                bot.send_message(f'Sorry {user["name"]}... You lost 10 Coins')
            
        else:
            bot.send_message(f'You do not have enough coins {user["name"]}')
    