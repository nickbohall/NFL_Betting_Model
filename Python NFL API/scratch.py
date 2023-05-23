# from api_calls import *
# from data_manipulation_helpers import *
# from side_analysis import *
# from main_analysis import *
import nfl_data_py as nfl
import pandas as pd
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

pd.set_option('display.max_columns', 50)

seasons = list(range(2022, 2023))
test = nfl.see_pbp_cols()
print(np.array(test))
