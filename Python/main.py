from datetime import datetime
from functools import reduce

import numpy as np
import pandas as pd

from stathead_scrape import teamStats

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ------------------------------------ CONSTANTS ------------------------------------#

CURRENT_YEAR = datetime.today().year
YEAR_MIN = 2017
YEAR_MAX = 2022

POINTS = "points"
VEGAS = "vegas_line"
PASSING = "pass_cmp"
RUSHING = "rush_att"
TOTALS = "tot_yds"
PENALTIES = "penalties"
DOWNS = "first_down"
SCORING = "all_td_team"
OPP_PASSING = "pass_cmp_opp"
OPP_RUSHING = "rush_att_opp"
OPP_TOTALS = "tot_yds_opp"
OPP_DOWNS = "first_down_opp"
OPP_SCORING = "all_td_opp"
# ------------------------------------ GET THE DFS ------------------------------------#

stats = teamStats()
stats.login()

# Create a list of all the constants we're going to pass into the df function
attribute_list = [POINTS, VEGAS, PASSING , RUSHING, TOTALS, PENALTIES, DOWNS, OPP_PASSING, OPP_RUSHING, OPP_TOTALS,
                  OPP_DOWNS, OPP_SCORING]
df_names = ["points", "vegas", "pass", "rush", "total", "penalty", "downs", "opp_passing", "opp_rushing", "opp_totals",
            "opp_downs", "opp_scoring"]

# Initialize a list for the dfs to go into
df_list = []

# Loop through the constants list and create dfs for all of them.
for attribute in attribute_list:
    df = stats.get_stats_df(attribute, YEAR_MIN, YEAR_MAX)
    df_list.append(df)
    df.to_csv(f"../Data out/{attribute}.csv", index=False)

# Create base df to merge them all onto
base_df = df_list[0][["game_id", "Team", "Date", "Day", "G#", "Week", "", "Opp", "Result"]]
base_df["home"] = np.where(base_df[""] == "@", 0, 1)
base_df.drop("", axis=1, inplace=True)

# Remove all duplicate columns from each subsequent df
for df in df_list:
    df.drop(["Team", "Date", "Day", "G#", "Week", "", "Opp", "Result"], axis=1, inplace=True)
    # Drop that weird dup column from the website
    df.drop(df.columns[1], axis=1, inplace=True)

    # Rearrange the columns so that game_id is in front
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

# Ok now name the columns something specific to their metric so there's no dups
for i in range(len(df_list)):
    df_list[i] = df_list[i].set_index(["game_id"]).add_suffix(f"_{df_names[i]}").reset_index()
    print(df_list[i].head())

# Now add back in the base df to the list to merge them all
df_list.insert(0, base_df)

# Combine the dfs on game_id and out to csv
master = reduce(lambda left, right: pd.merge(left, right, on=['game_id'],
                                             how='left'), df_list)

master.to_csv(f"../Data out/master_data_{YEAR_MIN}-{YEAR_MAX}.csv")
