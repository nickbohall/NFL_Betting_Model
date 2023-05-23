# NFL_Betting_Model

The point of this was to create a model that predicts spreads and totals better than vegas. 
Data was scraped from nfl_py_api and modified in pycharm. The main adjustments to the data are below:
1. Import epa for every play for every team for the last 20 years
2. Create a rolling average epa offset by 1 week
3. Turn that rolling average into a dynamic rolling average to weight more recent games higher
4. Added the EPAs onto an NFL schedule df and outputted to csv

The feature engineering and data analysis was done in google collab notebooks since that was a better place to work with the data.
Other features were brought in and the data was run through a linear and logisitc regression

# Results
The results from my model: 
![image](https://github.com/nickbohall/NFL_Betting_Model/assets/104167338/f4ccaf4c-2998-4ae1-a5f4-0aacfadb0f5a)

Compared to the results from vegas models: 
![image](https://github.com/nickbohall/NFL_Betting_Model/assets/104167338/6abbfa6f-a476-42f6-a5f5-bd7dd0cc8c3f)

The same analysis was done for totals. My model:
![image](https://github.com/nickbohall/NFL_Betting_Model/assets/104167338/763b8980-3634-4a77-808c-254956d53e06)

And vegas model again: 
![image](https://github.com/nickbohall/NFL_Betting_Model/assets/104167338/d8461385-4ba1-45a7-b1b6-f4aaaae0a70e)

As you can see, we haven't beat vegas yet, but there are more features that I have in mind and are in progress for implementation.


