import pandas as pd 
import numpy as np 
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt

def getTop12():
    """ returns top 12 most minutes played players per team per season
    Input: None (hardcoded filename)
    Output: CSV file
    Return: Dataframe 
    """
    df_players = pd.read_csv('2013-2023-Player-Per_Calc.csv',decimal='.')

    # drop index from previous dataframe manipulation
    # df_players.drop(columns={'Unnamed: 0', 'Unnamed: 0.1'}, inplace=True)

    df_players.sort_values(['Season', 'Tm', 'MP', 'PER_calc'], ascending=[False, True, False, False], inplace=True)
    df_test = df_players.groupby(['Season', 'Tm']).head(12)
    df_test.to_csv('1_top12_player.csv')
    return df_test

def hist_SeasonPlayerPER():
    """Frequency distribution for top 12 players of each team per season
    Input: None (hardcoded dataframe from getTop12())
    returns: histogram with of player PER across different season
    """
    df_players = getTop12()
    
    PER_values = {}

    fig, ax = plt.subplots(2, 5, figsize=(16, 8), tight_layout=True, sharey='all')
    
    for i in range(2):
        for j in range(5):
            ax[int('{}'.format(i)), int('{}'.format(j))].set_xticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].set_yticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].tick_params(axis='both', which='both', length=0)
    years = [year for year in range(2012, 2023) if year != 2020]

    for i, (year, y)  in enumerate(zip(years, range(1, 11))):
        PER_values['{}-{}'.format(year, year+1)] = df_players[df_players['Season'] == '{}-{}'.format(year, year+1)]['PER_calc']
   
    
        mean_val = round(PER_values['{}-{}'.format(year, year+1)].mean(), 1)
        std_val = round(np.std(PER_values['{}-{}'.format(year, year+1)]), 1)

        fig.add_subplot(2, 5, y)
        n, bins, patches = plt.hist(x=PER_values['{}-{}'.format(year, year+1)], 
                                    bins='auto',
                                    alpha=0.7, 
                                    rwidth=0.85, 
                                    range=(0, 39)
                                    )

        plt.grid(axis='y', alpha=0.7)
        plt.xlabel('PER Value', labelpad=5, fontsize=8)
        plt.title('{}-{}'.format(year, year+1), fontsize=12)
        plt.yticks([10, 20, 30, 40, 50, 60, 70])
        plt.text(22, 50, 'mean: {}\nstd: {}'.format(mean_val, std_val), fontsize=8)
    plt.show()


def qq_SeasonPlayerPER():
    """Q-Q plot for player PER rating per season
    Input: None (hardcoded dataframe from getTop12())
    returns: Q-Q plot of player PER from all seasons"""
    df_players = getTop12()

    PER_values = {}
    fig, ax = plt.subplots(2, 5, figsize=(16, 8), tight_layout=True, sharey='all')
    
    title_list = []
    years = [year for year in range(2012, 2023) if year != 2020]
    for i in years: # to make title list 
        title_list.append('{}-{}'.format(i, i+1))

    for i in range(2):
        for j in range(5):
            ax[int('{}'.format(i)), int('{}'.format(j))].set_xticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].set_yticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].tick_params(axis='both', which='both', length=0)
            ax[int('{}'.format(i)), int('{}'.format(j))].set_title(title_list.pop(0))

    for i, (year,y)  in enumerate(zip(years, range(1, 11))):
        PER_values['{}-{}'.format(year, year+1)] = df_players[df_players['Season'] == '{}-{}'.format(year, year+1)]['PER_calc']

        sm.qqplot(PER_values['{}-{}'.format(year, year+1)], line='q', ax=fig.add_subplot(2, 5, y), markersize=1)
    
    plt.show()


def boxplot_PlayerPER():
    """boxplot of player PER
    Input: None (hardcoded dataframe from getTop12())
    returns: boxplot of player PER across different season"""
    df_players = getTop12()

    PER_values = {}
    positions = ['C', 'PF', 'PG', 'SF', 'SG']
    for pos in positions: 
        PER_values[pos] = df_players[df_players['Pos'] == pos]['PER_calc']

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.boxplot(PER_values.values())
    ax.set_xticklabels(PER_values.keys(), fontsize=16)
    ax.set_title('PER For Different Basketball Positions',  fontsize=20)
    ax.set_ylabel('PER Value', fontsize=16)

    plt.show()

def boxcox_PlayerPER():
    """Boxcox normality test for player PER
    Input: None (hardcoded dataframe from getTop12())
    returns: lambda value to figure out how to transform data"""

    df_players = getTop12()

    # There is a single negative PER value. Need to transform so that all 
    # values are positive for scipy BoxCox function 
    df_players['PER_calc'] += 1 
    df_players = df_players[df_players['PER_calc'] >  0]

    transformed_val, lambda_val = stats.boxcox(df_players['PER_calc']) 
    transformed_val = transformed_val.tolist()
    df_players.insert(5, 'Trans_PER', transformed_val)
    df_players['PER_calc'] -= 1

    # df_players.to_csv('test_trans.csv')
    print('lambda:', lambda_val)
    return df_players, lambda_val

def teamPER_calc():
    """calculates team PER value
    Input: None (hardcoded dataframe from getTop12())
    Output: CSV file"""
    df_players = getTop12()
    df_players = df_players[['Season', 'Player', 'PER_calc', 'Tm', 'MP']]
    print(df_players)
    PER_MP = df_players['PER_calc'] * df_players['MP']
    df_players.insert(2, 'log(PER * MP)', PER_MP)

    df_players.sort_values(['Season', 'Tm'], inplace=True)

    # log transformation based on BoxCox lambda value
    teamPER = np.log(df_players.groupby(['Season', 'Tm'])['log(PER * MP)'].sum())

    teamPER.reset_index().to_csv('2_teamPER.csv')



def teamRatio_calc():
    """calculates team win ratio
    Input: None (hardcoded filename)
    returns: CSV file
    """
    df_teams = pd.read_csv('2013-2023-Team-edit.csv', index_col=0)

    team_tm = {
            'Atlanta Hawks': 'ATL',
            'Boston Celtics': 'BOS',
            'Brooklyn Nets': 'BRK',
            'Charlotte Bobcats': 'CHA',
            'Charlotte Hornets': ['CHH', 'CHO'],
            'Chicago Bulls': 'CHI',
            'Cleveland Cavaliers': 'CLE',
            'Dallas Mavericks': 'DAL',
            'Denver Nuggets': 'DEN',
            'Detroit Pistons': 'DET',
            'Golden State Warriors': 'GSW',
            'Houston Rockets': 'HOU',
            'Indiana Pacers': 'IND',
            'Los Angeles Clippers': 'LAC',
            'Los Angeles Lakers': 'LAL',
            'Memphis Grizzlies': 'MEM',
            'Miami Heat': 'MIA',
            'Milwaukee Bucks': 'MIL',
            'Minnesota Timberwolves': 'MIN',
            'New Jersey Nets': 'NJN',
            'New Orleans Hornets': 'NOH',
            'New Orleans/Oklahoma City Hornets': 'NOK',
            'New Orleans Pelicans': 'NOP',
            'New York Knicks': 'NYK',
            'Oklahoma City Thunder': 'OKC',
            'Orlando Magic': 'ORL',
            'Philadelphia 76ers': 'PHI',
            'Phoenix Suns': 'PHO',
            'Portland Trail Blazers': 'POR',
            'Sacramento Kings': 'SAC',
            'San Antonio Spurs': 'SAS',
            'Seattle SuperSonics': 'SEA',
            'Toronto Raptors': 'TOR',
            'Utah Jazz': 'UTA',
            'Vancouver Grizzlies': 'VAN',
            'Washington Wizards': 'WAS',
        }

    # Charlotte Hornets name splits 
    CHH_season = []
    for i in range(1998, 2002):
        CHH_season.append('{}-{}'.format(i, i+1))

    CHO_season = []
    for i in range(2014, 2019):
        CHO_season.append('{}-{}'.format(i, i+1))

    # adding tm col to df_teams_inst 
    tm_list = []
    for each_team, season in zip(df_teams['Team'], df_teams['Season']):
        if each_team == 'Charlotte Hornets':
            if season in CHH_season:
                tm_list.append(team_tm['Charlotte Hornets'][0])
            else: 
                tm_list.append(team_tm['Charlotte Hornets'][1])
        else:
            tm_list.append(team_tm[each_team])
        
    df_teams.insert(3, 'Tm', tm_list)

    # calculate win ratio 
    win_ratio = df_teams['W'] / (df_teams['W'] + df_teams['L'])
    df_teams.insert(5, 'Win Ratio', win_ratio)
    
    df_teams.to_csv('3_team_data.csv')


def teamPER_winRatio():
    """creates dataframe with teamPER and team win ratio
    Input: None (hardcoded filename)
    Output: CSV file
    """
    df_team_data = pd.read_csv('3_team_data.csv', index_col=0)
    df_teamPER = pd.read_csv('2_teamPER.csv', index_col=0)

    df_team_data.sort_values(['Season', 'Tm'], ascending=[True, True], inplace=True)
    df_teamPER.sort_values(['Season', 'Tm'], ascending=[True, True], inplace=True)

    df_teamPER.index = df_team_data.index # align index of dataframes
    df_team_data.insert(5, 'Team PER', df_teamPER['log(PER * MP)'])

    # for colormapping in corr_teamPER_winRatio()
    western = {
        'LAL',
        'LAC', 
        'DEN', 
        'DAL', 
        'HOU', 
        'UTA', 
        'OKC', 
        'SAC', 
        'POR', 
        'PHO', 
        'MIN', 
        'SAS', 
        'MEM', 
        'NOP', 
        'GSW', 
        'SEA', 
        'VAN', 
    }

    tm_conf_list = []
    for each in df_team_data['Tm']:
        if each in western:
            tm_conf_list.append('Western')
        else: 
            tm_conf_list.append('Eastern')

    df_team_data.insert(4, 'Conference', tm_conf_list)

    df_team_data.to_csv('4_team_data_final.csv')


def corr_teamPER_winRatio():
    """correlation of team PER and win ratio for each season
    Input: None (hardcoded filename)
    Returns: Scatter plot"""

    df_teams = pd.read_csv('4_team_data_final.csv')

    for each in range(2016, 2019):
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = list(ind_season['Team PER'])
        y_data = list(ind_season['Win Ratio'])
        names = list(ind_season['Tm'])
        
        colormap = []
        for each in ind_season['Conference']:
            if each == 'Western':
                colormap.append('tab:red')
            else: 
                colormap.append('tab:blue')

        fig = plt.figure(figsize=(10, 8))
        ax = plt.subplot(111)
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.05)

        # legend
        plt.scatter([], [], color='r', label='Western')
        plt.scatter([], [], color='b', label='Eastern')
        plt.legend(loc="lower right")

        for i,type in enumerate(names):
            x = x_data[i]
            y = y_data[i]
            plt.scatter(x, y, color=colormap[i], s=15)
            plt.text(x, y-0.01, type, fontsize=7)

        # trendline
        trend = np.polyfit(x_data,y_data,1)
        trendpoly = np.poly1d(trend) 
        ax.plot(x_data,trendpoly(x_data), c='orange')

        plt.title('Team PER v. Win Ratio During Regular Season: {}'.format(ind_season['Season'].iloc[0]))
        plt.ylabel('Win Ratio (Games Won / Total Games)')
        plt.xlabel('Team PER (log(Player PER * Player MP))')

    plt.show()

def ols_teamPER_winRatio():
    """OLS summary table
    Input: None (hardcoded filename)
    Returns: Standardized Residuals {dict} used in qq_teamPER()"""
    df_teams = pd.read_csv('4_team_data_final.csv')

    stand_residual_dict = {}
    constant_coef = {}
    winR_coef = {}
    years = {year for year in range(2013, 2023) if year != 2020}
    for each in years:
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        ols_model = sm.OLS(y_data, x_data)
        results = ols_model.fit()
        # print('{}-{} Season \n'.format(each, each+1), results.summary())

        # get parameters
        constant_coef['{}-{}'.format(each, each+1)] = results.params[0]
        winR_coef['{}-{}'.format(each, each+1)] = results.params[1]

        # create instance of influence
        influence = results.get_influence()
        

        # residuals
        standardized_residuals = influence.resid_studentized_internal
        studentized_residuals = influence.resid_studentized_external
        #print('Standardized residuals \n', standardized_residuals)
        #print('Studentized residuals \n',  studentized_residuals)

        stand_residual_dict['{}-{}'.format(each, each+1)] = standardized_residuals
    return stand_residual_dict, constant_coef, winR_coef
    




def glm_teamPER_winRatio():
    """returns table of GLM metrics"""
    df_teams = pd.read_csv('4_team_data_final.csv')
    years = {year for year in range(2013, 2023) if year != 2020}
    for each in years:
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        glm_model = sm.GLM(y_data, x_data)
        results = glm_model.fit()
        print(results.summary())


def huber_teamPER_winRatio():
    """returns table of RLM using Huber's"""
    df_teams = pd.read_csv('4_team_data_final.csv')
    years = {year for year in range(2013, 2023) if year != 2020}
    for each in years:
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        glm_model = sm.RLM(y_data, x_data)
        results = glm_model.fit()
        print(results.summary())


def residuals_fitted_teamPER(constant, X1_coefficient, start_year):
    """Residual plot
    Input Parameters:
    * constant (intercept) {float}
    * X1 coefficient {float}
    * start_year - beginning year of season {int}
    """
    df_teams = pd.read_csv('4_team_data_final.csv')

    ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(start_year, start_year+1)]

    x_actual = list(ind_season['Win Ratio'])
    y_actual = list(ind_season['Team PER'])
    names = list(ind_season['Tm'])

    # generating y-predicted values from regression model
    y_pred = []
    for x_val in x_actual:
        y_pred_val = constant + (X1_coefficient * x_val)
        y_pred.append(y_pred_val)
    
    # calculating residuals
    residual_vals = []
    for obs, pred in zip(y_actual, y_pred):
        res_val = obs - pred
        residual_vals.append(res_val)

    #automate later?
    #residual_dict['{}-{}'.format(each, each+1)] = residual_vals #alt use ind_season['Season'].iloc[0]

    colormap = []
    for each in ind_season['Conference']:
        if each == 'Western':
            colormap.append('tab:red')
        else: 
            colormap.append('tab:blue')
    
    fig = plt.figure(figsize=(10, 8))
    ax = plt.subplot(111)
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.05)

    plt.scatter([], [], color='r', label='Western')
    plt.scatter([], [], color='b', label='Eastern')
    plt.legend(loc="lower right")

    for i,type in enumerate(names):
        x = y_actual[i]
        y = residual_vals[i]
        plt.scatter(x, y, color=colormap[i], s=15)
        plt.text(x+0.002, y-0.002, type, fontsize=7)

    plt.hlines(0, linestyles='dashed', xmin=min(y_actual), xmax=max(y_actual))

    plt.title('Residuals v. Fitted Model: {} Season'.format(ind_season['Season'].iloc[0]))
    plt.ylabel('Residuals')
    plt.xlabel('Fitted Values')

    plt.show()


# Values taken from OLS summary table
# residuals_fitted_teamPER(12.4639, 0.4199, 2022) # 18-19
# residuals_fitted_teamPER(12.3923, 0.6228, 2021) # 17-18
# residuals_fitted_teamPER(12.5184, 0.4662, 2019) # 16-17

def qq_teamPER():
    """normal Q-Q plot for standardized residuals for each season
    Input: standardized residuals (ols_teamPER_winRatio()) {dict}"""
    stand_residual_dict, _ , _ = ols_teamPER_winRatio()
    print(type(stand_residual_dict))
    years = [2019,2021,2022]
    for each in years:
        fig = sm.qqplot(stand_residual_dict['{}-{}'.format(each, each+1)], line='q', markersize=1)
        fig.suptitle('Normal Q-Q: {}-{}'.format(each, each+1))
    plt.show()
qq_teamPER()


def recent_2022_vs_21_19():
    """Using 2016-2017 and 2017-2018 season predictions using OLS coefficients 
    to test with 2018-2019 actual season win ratios.
    
    Input: None (hardcoded filename)
    Returns: 
    * graph
    * CSV file 
    """
    df_teams = pd.read_csv('4_team_data_final.csv')

    # 2022 - 2023 Western
    west_teams = df_teams[(df_teams['Season']=='2022-2023') & (df_teams['Conference']=='Western')]
    y_22_west = list(west_teams['Win Ratio'])
    x_22_west = list(west_teams['Rk'])
    names_west = west_teams['Tm']

    # 2022-2023 Eastern
    east_teams = df_teams[(df_teams['Season']=='2022-2023') & (df_teams['Conference']=='Eastern')]
    y_22_east = list(east_teams['Win Ratio'])
    x_22_east = list(east_teams['Rk'])
    names_east = east_teams['Tm']

    rk = list(df_teams[df_teams['Season']=='2022-2023']['Rk'])
    teamPER_pred = df_teams[df_teams['Season']=='2022-2023']['Team PER']

    winR_19_pred = []
    winR_21_pred = []

    for i in teamPER_pred:
        res = (i - 12.4674)/0.4974 # 2019
        winR_19_pred.append(res)
        res = (i - 12.4140)/0.5646 # 2021
        winR_21_pred.append(res)
    
    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot(111)
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.05)

    plt.scatter(x_22_west, y_22_west, color='r', label='Western')
    plt.scatter(x_22_east, y_22_east, color='b', label='Eastern')
    plt.scatter(rk, winR_19_pred, color='c', label='2019 predicted')
    plt.scatter(rk, winR_21_pred, color='m', label='2021 predicted')
    plt.legend(loc="upper right")

    for i, txt in enumerate(names_west):
        ax.annotate(txt, (x_22_west[i]+0.05, y_22_west[i]), size=10)
    
    for i, txt in enumerate(names_east):
        ax.annotate(txt, (x_22_east[i]+0.05, y_22_east[i]), size=10)

    plt.title('2022-2023 Regular Season Prediction')
    plt.ylabel('Win Ratio (Games Won / Total Games)')
    plt.xlabel('Season Ranking')
    plt.tight_layout()
    plt.show()

    conf = list(df_teams[df_teams['Season']=='2022-2023']['Conference'])
    names_2022 = list(df_teams[df_teams['Season']=='2022-2023']['Tm'])
    winR_22 = list(df_teams[df_teams['Season']=='2022-2023']['Win Ratio'])

    pred_rankings = pd.DataFrame([conf, names_2022, rk, winR_22, winR_21_pred, winR_19_pred])
    pred_rankings = pred_rankings.transpose()
    pred_rankings.columns = ['Conference', 'Tm', '2022 Rk', '2022 WR', 'Pred 2021 WR', 'Pred 2019 WR']

    pred_rankings.to_csv('5_2022_validation.csv')

def prev_season_pred_test():
    """For each season, predictions of previous season generated from OLS coefficients  are used to
    compare with actual season win ratios.
    
    Input: None (hardcoded filename)
    Returns: 
    * graph
    * CSV file"""
    df_teams = pd.read_csv('4_team_data_final.csv')
    stand_residual_dict, constant_coef, winR_coef = ols_teamPER_winRatio()

    season_list = []
    conference_list = []
    name_list = []
    rk_list = []
    winR_list = []
    pred_from_prev_list = []
    constant_coef_list = []
    winR_coef_list = []
    
    # start with actual 2013-2023 data to compare with previous year predictions
    years = [year for year in range(2013, 2023) if year != 2020]
    for i , year in enumerate(years):
        # Western Conference Teams for actual season data
        west_teams = df_teams[(df_teams['Season']=='{}-{}'.format(year, year+1)) & (df_teams['Conference']=='Western')]
        y_west = list(west_teams['Win Ratio'])
        x_west = list(west_teams['Rk'])
        names_west = west_teams['Tm']

        # Eastern Conference Teams for actual season data
        east_teams = df_teams[(df_teams['Season']=='{}-{}'.format(year, year+1)) & (df_teams['Conference']=='Eastern')]
        y_east = list(east_teams['Win Ratio'])
        x_east = list(east_teams['Rk'])
        names_east = east_teams['Tm']

        rk = list(df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Rk'])
        teamPER_pred = df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Team PER']

        prev_year_pred = []
        constant_coef_vals = []
        winR_coef_vals = []

        for i in teamPER_pred:
            res = (i - constant_coef['{}-{}'.format(year, year+1)])/winR_coef['{}-{}'.format(year, year+1)]
            prev_year_pred.append(res)

        fig = plt.figure(figsize=(12, 8))
        ax = plt.subplot(111)
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.05)

        plt.scatter(x_west, y_west, color='r', label='Western')
        plt.scatter(x_east, y_east, color='b', label='Eastern')
        plt.scatter(rk, prev_year_pred, color='c', label='{}-{} predicted'.format(year-1, year))
        plt.legend(loc="upper right")

        for i, txt in enumerate(names_west):
            ax.annotate(txt, (x_west[i]+0.05, y_west[i]), size=10)
    
        for i, txt in enumerate(names_east):
            ax.annotate(txt, (x_east[i]+0.05, y_east[i]), size=10)

        plt.title('{}-{} Regular Season Prediction'.format(year, year+1))
        plt.ylabel('Win Ratio (Games Won / Total Games)')
        plt.xlabel('Season Ranking')
        plt.tight_layout()
        plt.show()
        
        # TO DO
        # Make a dictionary outside of for loop and append to it to add to final csv file
        season = list(df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Season'])
        conf = list(df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Conference'])
        names = list(df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Tm'])
        winR = list(df_teams[df_teams['Season']=='{}-{}'.format(year, year+1)]['Win Ratio'])

        season_list.extend(season)
        conference_list.extend(conf)
        name_list.extend(names)
        rk_list.extend(rk)
        winR_list.extend(winR)
        pred_from_prev_list.extend(prev_year_pred)
        constant_coef_list.extend(constant_coef_vals)
        winR_coef_list.extend(winR_coef_vals)


    pred_rankings = pd.DataFrame([season_list, conference_list, name_list, rk_list, winR_list, pred_from_prev_list, constant_coef_list, winR_coef_list])
    pred_rankings = pred_rankings.transpose()
    pred_rankings.columns = ['Season', 'Conference', 'Tm', 'Actual Season Rk', 'Actual Win Ratio', 'Predicted Win Ratio (from previous)', 'Constant', 'Win Ratio Coefficient']

    pred_rankings.to_csv('6_winR_predictions.csv')

# prev_season_pred_test()
# prev_season_pred_test()
# recent_2022_vs_21_19()


