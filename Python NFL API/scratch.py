# from api_calls import *
# from data_manipulation_helpers import *
# from side_analysis import *
# from main_analysis import *
import nfl_data_py as nfl
import pandas as pd

pd.set_option('display.max_columns', 15)

seasons = list(range(2022, 2023))
test = nfl.clean_nfl_data(seasons)
print(test)
print(test.columns)
