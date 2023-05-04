from data_scrape import WeeklyStats
from stathead_scrape import teamStats
import pandas as pd
from functools import reduce
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ------------------------------------ CONSTANTS ------------------------------------#

CURRENT_YEAR = datetime.today().year
YEAR_MIN = 2018
YEAR_MAX = 2022

POINTS = "points"
VEGAS = "vegas_line"
PASSING = "pass_cmp"
RUSHING = "rush_att"
TOTALS = "tot_yds"
PENALTIES = "penalties"
DOWNS = "first_down"
SCORING = "all_td_team"

# ------------------------------------ GET THE DFS ------------------------------------#

stats = teamStats()
stats.login()

# Create a list of all the constants we're going to pass into the df function
attribute_list = [POINTS, VEGAS, PASSING, RUSHING, TOTALS, PENALTIES, DOWNS]

# Initialize a list for the dfs to go into
df_list = []

# Loop through the constants list and create dfs for all of them.
for attribute in attribute_list:
    df = stats.get_stats_df(attribute, YEAR_MIN, YEAR_MAX)
    df_list.append(df)
    df.to_csv(f"../Data out/{attribute}.csv", index=False)

# Remove all duplicate columns from each subsequent df
for df in df_list[1:]:
    df.drop(["Team", "Date", "Day", "G#", "Week", "", "Opp", "Result"], axis=1, inplace=True)

# Clean some of the columns
df_list[2].rename(columns={"Att": "pass_att", 'Yds': 'pass_yds', 'TD': "pass_TD", 'Y/A': "pass_Y/A"}, inplace=True)
df_list[3].rename(columns={"Att": "rush_att", 'Yds': 'rush_yds', 'TD': "rush_TD", 'Y/A': "rush_Y/A"}, inplace=True)
df_list[5].rename(columns={'Yds': 'pen_yds'}, inplace=True)

# Combine the dfs on game_id and out to csv
master = df_list[0]\
    .merge(df_list[1], on="game_id") \
    .merge(df_list[2], on="game_id") \
    .merge(df_list[3], on="game_id") \
    .merge(df_list[4], on="game_id") \
    .merge(df_list[5], on="game_id") \
    .merge(df_list[6], on="game_id")

master.to_csv(f"../Data out/master_data.csv")
