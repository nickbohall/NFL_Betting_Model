import nfl_data_py as nfl

def get_play_data(seasons):
    play_data = nfl.import_pbp_data(years=seasons)
    return play_data

def get_week_data(seasons):
    week_data = nfl.import_weekly_data(seasons)
    return week_data

def get_schedule(seasons):
    schedule = nfl.import_schedules(seasons)
    return schedule

def get_vegas_data(seasons):
    vegas = nfl.import_sc_lines(seasons)
    return vegas

def get_vegas_win_totals(seasons):
    vegas_win_totals = nfl.import_win_totals(seasons)
    return vegas_win_totals


