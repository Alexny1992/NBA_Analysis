import pandas as pd
import numpy as np
import csv 

def dataClean():
    # Cleaning up data from the scraped data from ESPN
    # Output it as a csv
    df = pd.read_csv("2013-2023-Regular-PlayerStats-raw.csv")
    # Remove missing values
    df.dropna(inplace=True) 
    # Reset Index
    df.reset_index(drop= True, inplace=True)
    # Change team to Team abbreviation
    df.rename(columns={'Team': 'Team Abbreviation'}, inplace=True)
    # Update to csv
    df.to_csv('ESPN_2002-2019-Regular-PlayerStats-edit.csv')
    return df

            
dataClean()