import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import argparse
parser = argparse.ArgumentParser(prog="GoS Clan Viewer",description="displays info about your GoS clan!")
parser.add_argument("filename",help="the filepath to the HTML of the clan members")
parser.add_argument("-a","--active",action="store_true",help="shows all active players (default days is 30)")
parser.add_argument("-i","--inactive",action="store_true",help="shows all inactive players (default days is 30)")
parser.add_argument("-al","--all",action="store_true",help="Shows all players")
parser.add_argument("-d","--days",help="number of days a player needs to be inactive before they count as inactive",type=int,default=30)
args = parser.parse_args()
clan_ranks = ['Clan Leader','Clan Co-Leader','Clan Lieutenant','Clan Sergeant','Clan General']
overdue_days = timedelta(days=args.days) 
def read_file(path):
    with open(path, "r+") as file1:
        return file1.read()
if __name__ == "__main__":
    data = read_file(args.filename)
    soup = BeautifulSoup(data, 'lxml')
    characters = soup.find_all(id=re.compile("myForm"))
    expired_characters = []
    active_characters = []
    online_player_count = 0
    for character in characters:
        user_id = character.find("input",{"type":"hidden","name":"id"}).get("value")
        username = character.find("input",{"type":"hidden","name":"user"}).get("value")
        chat_rank = character.find("img").get("src").split("files/")[1][6:-4]
        stats = character.text.strip().split("  ")
        if "Last Activity" not in stats[0] and stats[0] not in clan_ranks:
            player_activity = stats[0]
        else:
            player_activity = None
        for x in stats:
            if "Last Activity" in x:
                active_date = x.split(": ")
                if "@" in x:
                    status = 'ONLINE'
                    online_player_count+=1
                    date = datetime.strptime(active_date[1],"%m/%d/%Y @ %I:%M:%S %p")
                else:
                    date = datetime.strptime(active_date[1],"%m/%d/%y %I:%M %p")
                    status= 'OFFLINE'
        if datetime.now()-overdue_days > date:
            expired_characters.append(f"Rank: {chat_rank} Username: {username}, ID: {user_id} {date.strftime('%m/%d/%y')} {status}")
        else:
            active_characters.append(f"Rank: {chat_rank} Username: {username}, ID: {user_id} {date.strftime('%m/%d/%y')}  Activity: {player_activity} {status}")
            
    
    print(f"Clan Members Online: {online_player_count} \nActive in last {overdue_days.days} days: {len(active_characters)}\nNot logged in for {overdue_days.days} days: {len(expired_characters)}")
    if args.active:
        for x in active_characters:
            print(x)
    if args.all:
        players = active_characters + expired_characters
        for x in players:
            print(x)
    if args.inactive:
        for x in expired_characters:
            print(x)
                

