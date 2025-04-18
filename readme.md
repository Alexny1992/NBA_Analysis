# NBA Analysis (Tableau At the end)

## Description
The objective of this analysis was to investigate the relationship between the calculated team PER and win ratio, with a specific focus on forecasting playoff qualification. To accomplish this, regression analysis was employed utilizing the Ordinary Least Squares (OLS) method.

The data consisted of team PER values and win ratios from a given set of seasons. The regression analysis aimed to determine if there was a statistically significant relationship between team PER and win ratio, and whether the team PER could serve as a predictor for playoff qualification.

By applying the OLS method, the regression model was developed to estimate the impact of team PER on win ratio. This allowed us to examine the strength and significance of the relationship between these variables. Additionally, the model provided insights into the predictive power of team PER for forecasting playoff qualification.

Through this regression analysis, we aimed to uncover valuable information about the influence of team PER on win ratio and its potential for predicting playoff qualification. The findings from this study contribute to a better understanding of the relationship between team performance metrics and success in basketball.

**Tableau at the end**

## Introduction
Basketball is an exhilarating sport that has accumulated a wealth of data on players and teams over the past 20+ years. Throughout its history, team managements and statisticians have devised various metrics to assess the impact of players on the court. One such metric, the Player Efficiency Rating (PER), was created by John Hollinger to provide insight into a player's successes and shortcomings during a particular season. PER condenses multiple offensive and defensive player statistics into a single value, allowing for a comparison of a player's performance to that of their peers. On average, an ordinary player will have a PER of 15, while a rating near 30 indicates exceptional performance relative to other players.

Presently, the NBA consists of 30 teams divided into two conferences, with each team aiming to secure a spot in the NBA playoffs by playing 82 regular-season games. To qualify for the postseason, teams must maintain a win ratio above 0.5 and rank among the top 8 teams in their respective conferences. Although PER serves as a useful metric for quantifying an individual player's abilities on the court, it fails to capture the collective abilities of an entire team. This project endeavors to explore the correlation between players' PER ratings and their team's win ratio, examining whether PER can serve as a predictive factor for securing a playoff berth.


## Questions
1. Is there a significant disparity in PER (Player Efficiency Rating) across different basketball positions
    * Box plot

2. Is there a correlation between the Team PER value and win ratio?
    * Correlation

3. Can regular season Team PER values be utilized as a predictor for identifying post-season teams?
    * Regression Analysis

## Methods
### Data Source
We employed webscrapers to gather data from Basketball Reference and ESPN websites. The data collected included player and team information from Basketball Reference for seasons ranging from 2012 to 2023. Additionally, PER data was scraped from ESPN to aid in validating the PER calculations derived from Basketball Reference's data.

It is worth noting that the PER values generated from Basketball Reference's player and team data may differ from the PER values obtained from ESPN. This discrepancy can be attributed to the variation in PACE values used by Basketball Reference and ESPN in their calculations.

By utilizing webscrapers, we were able to extract the necessary data from these sources, enabling us to conduct analyses and investigations related to basketball player and team performance across multiple seasons.

### Data Clean & Prep
PER calculations were performed for all players between the years 2012 and 2023. However, for the purpose of this project, the focus was narrowed down to the top 12 individuals in terms of minutes played (MP) for each team. This approach was adopted to account for any roster changes or periods of inactivity that may occur throughout the season due to factors such as trades, injuries, and other circumstances.

By considering only the top 12 MP players, the analysis aims to capture the core contributors and minimize the impact of outliers or players with limited playing time. This approach provides a more comprehensive representation of each team's performance and allows for a more accurate assessment of the relationship between PER and other factors of interest.
### Player Efficiency Rating Formula 
```
uPER = (1 / MP) *
     [ 3P
     + (2/3) * AST
     + (2 - factor * (team_AST / team_FG)) * FG
     + (FT *0.5 * (1 + (1 - (team_AST / team_FG)) + (2/3) * (team_AST / team_FG)))
     - VOP * TOV
     - VOP * DRB% * (FGA - FG)
     - VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA - FT)
     + VOP * (1 - DRB%) * (TRB - ORB)
     + VOP * DRB% * ORB
     + VOP * STL
     + VOP * DRB% * BLK
     - PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP) ]


factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
VOP    = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)
DRB%   = (lg_TRB - lg_ORB) / lg_TRB

Source: BasketBall Reference
```
### Regression Analysis
For the simplicity of this personal project, only the last 3 seasons were used to investigate whether team PER correlated with win ratio. 

Team PER was calculated by taking the PERs of the top 12 MP players and multiplying it with their respective minutes played. PER is a per-minute rating so by multiplying it with minutes played, it gives players with more minutes played more weight in the team PER value. If a high PER player doesn't play as many minutes, he may not contribute as much to team PER relative to a teammate who has average PER but has played a higher number of minutes. 

Because preliminary data showed that our data were heteroscedastic, a BoxCox test and transformation were applied to team PER values to make it more homoscedastic. BoxCox test returned a lambda of ~0.446, which corresponds to a log transformation of the data. 

Linear models were created using Ordinary Least Squares and evaluated using adjusted R^2, F-statistic from Wald test, residual, and Q-Q plots. 

## Results and Data Analysis
When examining the distribution of PER for players across each season, we see that most distributions are right-skewed. 
![Frequency Histogram](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/hist_SeasonPlayerPER.png)

![Q-Q Plot](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/qq_SeasonPlayerPER.png)

As a preliminary investigation, PER values for different positions were also examined. 
![Boxplot](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/boxplot_PlayerPER.png)
All of the PER for different positions seem similar to each other with extreme PER values in the upper range.



### 2019 - 2020 Regular Season
There is a distinct linear trend when examining the correlation between Team PER and win ratio. When comparing teams belonging to different conferences, the Western Conference comparatively has stronger teams indicated by the cluster representing high team PER and win ratio. 
![Corr_2019-2020](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2019-2020-TeamPER-vs-Winrate.png) 

The summary of our linear model showed an adjusted R^2 of 0.022 and a significant F-statistic. However, when evaluating our model with residuals, we can see there are extreme residuals with an overestimation for lower team PER. Our probability value for Omnibus is low which supports that residuals are not normally distributed. Extreme deviations at the tails will skew distribution as observed in the Q-Q plot. 


<p float="center">
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2019-2020-Normal_QQ.png" width="290" /> 
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2019-2020-OLS.png" width="290" />
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2019-2020-Regression.png" width="290" />
</p>

### 2021 - 2022 Regular Season
In the 2021-2022 regular season, there has been a shift in the team with the highest PER, as the Golden State Warriors no longer hold that position. Instead, the Milwaukee Bucks, Washington Wizards, and The Indiana Pacers seem to have similar team PER values but exhibit different win ratios. Once again, we observe a notable trend in the Western Conference, with teams having higher PER scores also showcasing higher win ratios, resulting in a concentrated cluster in the upper-right portion of the graph.
![Corr_2021-2022](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2021-2022-TeamPER-vs-WinRate.png)

There is an improvement for this season's linear model with an adjusted R^2 of 0.703 and significant F-statistic explaining the variability in data. Omnibus probability 1.235 can further support it, indicating the data are typically distributed. 

<p float="center">
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2021-2022_Normal_QQ.png" width="290" />
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2021-2022-Residuals-vs-Fitted.png" width="290" /> 
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2021-2022-OLS.png" width="290" />
</p>

### 2022 - 2023 Regular Season
"![Corr_2021-2022](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2022-2023-TeamPER-vs-WinRate.png)
 
The summary of our linear model indicated that our model had an adjusted R^2 of 0.532 and was significant according to F-statistics. With Omnibus probability value of 0.961 it is indicating our residuals are normally distributed. 

<p float="center">
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2022-2023-Normal_QQ.png" width="290" /> 
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2022-2023-Residuals-vs-Fitted.png" width="290" />
  <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2022-2023-OLS.png" width="290" />
</p>


### Prediction: OLS (StatsModel)
In spite of the varying goodness-of-fit of linear models when applied to past season data, they were employed to assess their predictive capability regarding win ratio in the subsequent season using data from 2019 to 2023. Upon examining the graph, it becomes apparent that beyond the top 10 rankings, the residuals notably escalate for both the 2019-2020 and 2021-2022 seasons.

![Pred_22-23](https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/2022-2023-Regular-Season-Pred.png)

### Top 16 teams 
Using the linear regression generated from data of 2022 - 2023, 11 out of 16 (68.5%) teams were correctly predicted to qualify for playoffs using the 2021-2022 model (bolded team abbreviations were not predicted).  

####                        Eastern Conference                     
|      Actual  2022 - 2023      |  Prediction 21-22, 19-20 model  |
|:-----------------------------:|:-------------------------------:|
|              BOS              |                BOS              | 
|            **CLE**            |                MIL              |
|              PHI              |                TOR              |
|              MIL              |              **MIA**            |
|            **NYK**            |                MIL              |
|              TOR              |                PHI              |
|            **CHI**            |              **IND**            |
|            **BRK**            |                TOR              | 

####                         Western Conference                      
|      Actual  2022 - 2023      |  Prediction 21-22, 19-20 model  |
|:-----------------------------:|:-------------------------------:|
|              MEM              |                PHO              |
|              DEN              |              **LAC**            |
|            **SAC**            |              **UTA**            |
|              PHO              |                MEM              |
|            **NOP**            |                LAL              |
|              GSW              |                GSW              |
|            **OKC**            |              **DAL**            |
|              LAL              |                DEN              |

## Discussion
Based on the data from the last 3 seasons, a clear linear relationship can be observed between Team PER and win ratio. It is logical to expect that teams with higher PER would perform better and win more games during the season. The linear models used in our analysis showed statistical significance, with supporting adjusted R^2 and F-statistic values from the Wald test. However, it is important to note that there were outliers present in the data, which increased the variability in our model.

The outliers in our analysis can be explained in various ways. For teams with high PER but underperforming, this could be attributed to individual players with high PER who play a significant number of minutes but do not consistently contribute to winning games. These teams may rely heavily on one or two-star players who perform efficiently but lack a strong supporting bench, resulting in a lower win ratio. On the other hand, teams with low PER but overperforming may have high-performing players who are not on the court for extended periods, while the bench players contribute significantly during the game. This situation can occur when a team secures a substantial lead early in the game, leading to star players being benched for injury prevention or rest in preparation for future games.

It is worth noting that while team PER from the previous season can predict the majority of teams that will make the playoffs in the subsequent season, its reliability is limited to an accuracy of 62.5%.

One important consideration is that PER may not be the most reliable indicator for defensive statistics. As pointed out by John Hollinger, PER does not adequately capture a player's defensive acumen since it primarily incorporates active stats such as blocks and steals, which do not always reflect a player's overall contribution to the team's defense. By incorporating another metric that provides a better description of a player's defensive performance, we may be able to reduce unexplained variability in our model and improve its predictive accuracy.

In summary, while the relationship between Team PER and win ratio demonstrates a linear trend, outliers and limitations in the PER metric suggest the need for additional factors and metrics, particularly for assessing defensive performance, to enhance the accuracy and reliability of our models.



## Tableau Dashboard (Click Image for Interactive View)
<a href="https://public.tableau.com/app/profile/alex.wang3519/viz/2022-2023NBA_Analysis/Dashboard1">
   <img src="https://github.com/Alexny1992/NBA_Analysis/blob/main/NBA_Analysis/Images/Tableau_Dashboard.jpg" alt="NBA PER Analysis Tableau Dashboard">
</a>

## Notes

| Team Name                         | Season    | Team Abbrev |
|:----------------------------------|:---------:|:-----------:|
| Charlotte Bobcats                 | 2004-2014 | CHA         |
| Charlotte Hornets                 | 2014-2019 | CHO         |
| New Orleans Hornets               | 2007-2013 | NOH         |
| New Orleans Pelicans              | 2013-2019 | NOP         |

