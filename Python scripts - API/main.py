# ------------------------------------ IMPORTS ------------------------------------#
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

from api_calls import *
from sql_database import *
from data_manipulation_helpers import *
from side_analysis import *

# ------------------------------------ HOUSEKEEPING ------------------------------------#

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12,8)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 300)

# ------------------------------------ SET INPUTS AND CONSTANTS ------------------------------------#

seasons = list(range(2018, 2024))

# ------------------------------------ GET DATA - API CALL ------------------------------------#

play_data = get_play_data(seasons)

# ------------------------------------ CLEANING AND TRANSFORMING DATA ------------------------------------#

# Create a DF for each EPA we're looking at
rushing_offense_epa = create_epa_df(play_data, 'rush_attempt', 'posteam')
rushing_defense_epa = create_epa_df(play_data, 'rush_attempt', 'defteam')
passing_offense_epa = create_epa_df(play_data, 'pass_attempt', 'posteam')
passing_defense_epa = create_epa_df(play_data, 'pass_attempt', 'defteam')

# lag EPA one period back
rushing_offense_epa['epa_shifted'] = lag_df(rushing_offense_epa, 'posteam')
rushing_defense_epa['epa_shifted'] = lag_df(rushing_defense_epa, 'defteam')
passing_offense_epa['epa_shifted'] = lag_df(passing_offense_epa, 'posteam')
passing_defense_epa['epa_shifted'] = lag_df(passing_defense_epa, 'defteam')

# In each case, calculate EWMA with a static window and dynamic window and assign it as a column
rushing_offense_epa['ewma_dynamic_window'] = create_ewma_dynamic(rushing_offense_epa, 'posteam')
rushing_defense_epa['ewma_dynamic_window'] = create_ewma_dynamic(rushing_defense_epa, 'defteam')
passing_offense_epa['ewma_dynamic_window'] = create_ewma_dynamic(passing_offense_epa, 'posteam')
passing_defense_epa['ewma_dynamic_window'] = create_ewma_dynamic(passing_defense_epa, 'defteam')

# Merge all the data together
offense_epa = rushing_offense_epa.merge(passing_offense_epa, on=['posteam', 'season', 'week'],
                                        suffixes=('_rushing', '_passing')) \
    .rename(columns={'posteam': 'team'})

defense_epa = rushing_defense_epa.merge(passing_defense_epa, on=['defteam', 'season', 'week'],
                                        suffixes=('_rushing', '_passing')) \
    .rename(columns={'defteam': 'team'})

epa = offense_epa.merge(defense_epa, on=['team', 'season', 'week'], suffixes=('_offense', '_defense'))
epa_final_cols = [column for column in epa.columns if 'ewma' in column and 'dynamic' in column]
epa_final_cols.extend(['team', 'season', 'week'])
epa = epa[epa_final_cols]


# ------------------------------------ GET SCHEDULE DATA ------------------------------------ #

schedule = play_data[['game_id', 'season', 'week', 'home_team', 'away_team', 'home_score', 'away_score']] \
    .drop_duplicates().reset_index(drop=True).assign(home_team_win=lambda x: (x.home_score > x.away_score).astype(int))


df = schedule.merge(epa.rename(columns={'team': 'home_team'}), on=['home_team', 'season', 'week']) \
    .merge(epa.rename(columns={'team': 'away_team'}), on=['away_team', 'season', 'week'], suffixes=('_home', '_away'))

# ------------------------------------ NEW MAIN DF ------------------------------------ #

# Trying to create a df where each matchup is duplicated and there's a hero team and opponent with the respective EPAs

schedule_test = pd.DataFrame(np.repeat(schedule.values, 2, axis=0))
schedule_test.columns = schedule.columns
schedule_test["team"] = np.where(schedule_test.index % 2 == 0, schedule_test.home_team, schedule_test.away_team)
schedule_test["opponent"] = np.where(schedule_test.index % 2 != 0, schedule_test.home_team, schedule_test.away_team)
schedule_test["score"] = np.where(schedule_test.index % 2 == 0, schedule_test.home_score, schedule_test.away_score)
schedule_test["home"] = np.where(schedule_test.index % 2 == 0, 1, 0)

df_new = schedule_test.merge(epa, on=['team', 'season', 'week'])\
    .merge(epa.rename(columns={'team': 'opponent'}), on=['opponent', 'season', 'week'], suffixes=('_team', '_opp'))

# Adding team id to include H/A so everything is unique
df_new["team_id"] = np.where(df_new.home == 1, df_new.game_id + "_H", df_new.game_id + "_A")

df_new.drop(['home_team', 'away_team', 'home_score', 'away_score', 'home_team_win'], axis=1, inplace=True)

# Add in score diff column
df.insert(6, "score_diff", df.home_score - df.away_score)
df.insert(7, "score_total", df.home_score + df.away_score)
df.sort_values("game_id", inplace=True)

# Get a separate df for vegas data and add the game_id
vegas = get_vegas_data(seasons)
vegas.drop("game_id", axis=1, inplace=True)
vegas["game_id"] = vegas.season.astype(str) + "_" + vegas.week.astype(str).apply(lambda x: x.zfill(2)) \
                   + "_" + vegas.away_team + "_" + vegas.home_team
vegas.drop(vegas[vegas.side == vegas.away_team].index, inplace=True)
vegas = vegas[["game_id", "line"]].sort_values("game_id").reset_index()

# Let's also do it for win totals. Probably need those later.
win_totals = get_vegas_win_totals(seasons)

# Also just a blank schedule
schedule = get_schedule(seasons)

# ------------------------------------ OUTPUT TO CSV ------------------------------------ #

# Okay nice, now lets output this bitch to a csv and move over to notebooks to data science
df.to_csv(f"../API Data Out/data_{seasons[0]}_to_{seasons[-1]}.csv")
vegas.to_csv(f"../API Data Out/vegas_{seasons[0]}_to_{seasons[-1]}.csv")
win_totals.to_csv(f"../API Data Out/win_totals_{seasons[0]}_to_{seasons[-1]}.csv")
schedule.to_csv(f"../API Data Out/schedule_{seasons[0]}_to_{seasons[-1]}.csv")
df_new.to_csv(f"../API Data Out/test_{seasons[0]}_to_{seasons[-1]}.csv")





