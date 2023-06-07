from nba_api.stats.endpoints import boxscoreadvancedv2
from nba_api.stats.static import teams
import pandas as pd
import csv
import json

# teams = teams.get_teams()
# print(teams)
teams = boxscoreadvancedv2.BoxScoreAdvancedV2(
    season = '2013-14',
    season_type_all_star = 'Regular Season'
).get_data_frames()[0]
print(teams)

# def nba_API():
#     yearStart=2013
#     yearEnd =2023
#     for yearStart in range(yearStart, yearEnd+1):
#         teams = teamgamelogs.TeamGameLogs(
#             season_nullable = f'{yearStart-1}-{str(yearStart)[2:4]}',
#             season_type_nullable = 'Regular Season'
#             per_mode_simple_nullable = 'PerGame'
#             # headers = SEASON_YEAR', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK'
#             ).get_data_frames()[0]

#         df = pd.DataFrame(teams)
        # avg = avg.groupby(['WL', 'MIN', 'FGM', 'FGA', 
        #                    'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
        #                    'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 
        #                    'PFD', 'PTS', 'PLUS_MINUS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 
        #                    'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 
        #                    'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 
        #                    'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 
        #                    'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK'])
#         df.to_csv('2013-2023-NBA_API-TeamStat-raw.csv')
# nba_API()

# top_500_avg = top_500.groupby(['player_name', 'player_id']).mean()[[
#     'min', 'fgm', 'fga', 'ftm', 'fta', 'pts', 'fg3m', 'fg3a', 'gp'

    
        




