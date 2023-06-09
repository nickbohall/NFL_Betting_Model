import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime as dt
import numpy as np
import time


URL = "https://stathead.com/"
USERNAME = "sleepycornbread"
PASSWORD = "statheadLK0!"


class teamStats():
    def __init__(self):
        options = Options()
        options.headless = False  # This is to not actually open the webpage
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # Lets make a separate function to login. This will be called each time a new URL is presented, which should be fine
    def login(self):
        # Go to the stathead URL
        self.driver.get(URL)
        time.sleep(2)

        # Click the login button
        login = self.driver.find_element(By.CLASS_NAME, "login")
        login.click()
        time.sleep(2)

        # Enter username & password and click login
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "sh-login-button")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        login_button.click()
        time.sleep(2)

    # The website is very nice, so this is a generic function that will turn any table to df given the URL
    def get_table(self, url):
        time.sleep(2)
        self.driver.get(url)

        # Initialize blank list
        data = []

        # Get the headers first and add them to data list
        table_headers = self.driver.find_element(By.CSS_SELECTOR, "table thead")\
            .find_elements(By.CSS_SELECTOR, "tr")[1]\
            .find_elements(By.CSS_SELECTOR, "th")

        headers = [header.text for header in table_headers[1:]]
        data.append(headers)

        for page in range(13):
            try:
                # Now get the body table
                table_rows = self.driver.find_element(By.CSS_SELECTOR, "table tbody")\
                    .find_elements(By.CSS_SELECTOR, "tr")\

                # Now iterate through the rows
                for row in table_rows:
                    if row.get_attribute("class") == "thead" or row.get_attribute("class") == "over_header thead":
                        continue
                    else:
                        row_items = row.find_elements(By.CSS_SELECTOR, "td")
                        items = [item.text for item in row_items]
                        data.append(items)

                next_page = self.driver.find_element(By.CLASS_NAME, "next")
                self.driver.execute_script("arguments[0].click();", next_page)
            except selenium.common.exceptions.NoSuchElementException: # Keep going to the end
                continue

            time.sleep(3)
        return data

    def create_season(self, df):
        year = pd.to_datetime(df.Date).dt.year
        df["month"] = pd.to_datetime(df.Date).dt.month
        df["Season"] = np.where(df["month"] < 5, year - 1, year)
        df.drop("month", axis=1, inplace=True)
        return df

    # Helper function to create a unique ID for every game to use on each DF
    def create_ID(self, df):
        # First we have to create a season column for everyone
        self.create_season(df)
        team = df["Team"]
        opponent = df["Opp"]
        season = df["Season"]
        week = df["Week"]
        df["game_id"] = season.astype(str) + "_" + week.astype(str).apply(lambda x: x.zfill(2)) \
                        + "_" + team + "_" + opponent
        return df

    # Now we can start calling the individual tables we want to turn to dfs
    def get_stats_df(self, url_trigger, year_min, year_max):
        # the url trigger tells the driver what part of the website to go to. This will be called multiple times
        url = f"{URL}/football/team-game-finder.cgi?request=1&order_by={url_trigger}&year_min={year_min}&year_max={year_max}"

        data = self.get_table(url)
        game_df = pd.DataFrame(data)

        # set first row as header
        game_df.columns = game_df.iloc[0]
        game_df = game_df[1:]

        # Use helper to create unique identifier
        game_df = self.create_ID(game_df)
        print(f"{url_trigger} df scraped!")
        return game_df
