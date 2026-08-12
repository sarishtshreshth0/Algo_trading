import pandas as pd
import os
data = []
path = 'trading_data.csv'
def make_data(r):
    data.append(r)

def make_csv(data):
    if not data:
        return 'no data to save'
    new_data = pd.DataFrame(data)
    if os.path.exists(path):
        old_df = pd.read_csv(path)
        new_data = pd.concat([old_df , new_data] , ignore_index= True)
        new_data.drop_duplicates(['Ticker' , 'Date'] ,keep='last', inplace =True)
    new_data.to_csv(path, index=False)
    return 'Check trading_data.csv'