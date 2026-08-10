import pandas as pd
import os
data = []
def make_data(r):
    data.append(r)

def make_csv(data):
    if not data:
        return 'no data to save'
    new_data = pd.DataFrame(data)
    if os.path.exists(r'C:\Users\JIT DAS\trading\trading_data.csv'):
        old_df = pd.read_csv(r'C:\Users\JIT DAS\trading\trading_data.csv')
        new_data = pd.concat([old_df , new_data] , ignore_index= True)
        new_data.drop_duplicates(inplace =True)
    new_data.to_csv(r"C:\Users\JIT DAS\trading\trading_data.csv", index=False)
    return 'Check trading_data.csv'