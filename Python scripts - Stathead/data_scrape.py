import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

CURRENT_YEAR = datetime.today().year

class WeeklyStats:
    def __init__(self):
        options = Options()
        options.headless = False  # This is to not actually open the webpage
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    def flatten(self,l):
        return [item for sublist in l for item in sublist]

    # Helper function to get the headers only
    def get_column_headers(self,year):
        # Go to the url for the specified season
        url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
        self.driver.get(url)
        time.sleep(2)

        # get the data table and pull out the column headers first
        data_table = self.driver.find_element(By.ID, "games")
        column_headers = data_table.find_element(By.CSS_SELECTOR, "tr").find_elements(By.CSS_SELECTOR, "th")
        headers = [item.text for item in column_headers]

        # Adding in year column
        headers.append("year")

        return headers

    # Main function that gets the bulk of the data
    def get_scoring_table(self, year):
        url = f"https://www.pro-football-reference.com/years/{year}/games.htm"
        self.driver.get(url)
        time.sleep(2)

        data = []
        data_table = self.driver.find_element(By.ID, "games").find_elements(By.CSS_SELECTOR, "tr")
        for row in data_table[1:]:
            if row.get_attribute("class") == "thead":
                continue
            else:
                row_week = row.find_element(By.CSS_SELECTOR, "th")
                row_data = row.find_elements(By.CSS_SELECTOR, "td")
                row_data_list = [item.text for item in row_data]
                row_data_list.insert(0,row_week.text)
                data.append(row_data_list)

        data_with_year = [game + [year] for game in data]

        return data_with_year


    def get_all_data(self, years):

        headers = self.get_column_headers(CURRENT_YEAR-1)
        table_data = []

        start_year = CURRENT_YEAR - years
        end_year = CURRENT_YEAR

        for year in range(start_year, end_year):
            data = self.get_scoring_table(year)
            table_data.append(data)

        data = self.flatten(table_data)
        return headers, data


    def get_scores_df(self, years):
        df_input = self.get_all_data(years)

        df = pd.DataFrame(df_input[1], columns=df_input[0])
        return df







