import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
clan_ranks = ['Clan Leader','Clan Co-Leader','Clan Lieutenant','Clan Sergeant','Clan General']
overdue_days = timedelta(days=30) 
def read_file(path):
    with open(path, "r+") as file1:
        return file1.read()
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please supply the path to the GoS clanpage HTML")
        exit()
    data = read_file(sys.argv[1])
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
    for x in active_characters:
        print(x)
                

