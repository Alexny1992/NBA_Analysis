# from nba_api.stats.static import players
# import pandas as pd

# player_dict = players.get_players()

# # Use ternary operator or write function 
# # Names are case sensitive
# bron = [player for player in player_dict if player['full_name'] == 'Kobe Bryant'][0]
# bron_id = bron['id']

# # find team Ids
# from nba_api.stats.static import teams 
# teams = teams.get_teams()
# GSW = [x for x in teams if x['full_name'] == 'Golden State Warriors'][0]
# GSW_id = GSW['id']

# print(kobe_)
# print(GSW_id)


# First we import the endpoint
# We will be using pandas dataframes to manipulate the data
from nba_api.stats.endpoints import playergamelog
import pandas as pd 
import csv
import json 

# If you want all seasons, you must import the SeasonAll parameter 
from nba_api.stats.library.parameters import SeasonAll

#since API endpoint renders json we will have to convert json file to dict to csv
#csv is just for better visiualization
df_kobe = playergamelog.PlayerGameLog(player_id='977', season = SeasonAll.all)
df = df_kobe.get_data_frames()[0]
df.to_json('kobe.json')


with open('kobe.json') as json_file:
    data = json.load(json_file)
 
    # Print the type of data variable
    print("Type:", type(data))
 
    df = pd.DataFrame(data)

# df.to_csv('kobe.csv')
df_greater_than_30 = df[df['MIN'] > 30 ]
print(len(df_greater_than_30))

