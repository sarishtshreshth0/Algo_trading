import os
import pandas as pd
path = r'C:\Users\JIT DAS\trading\trading_data.csv'
def section_wise_check(name_of_section):
    if not os.path.exists(path):
        return "path doesn't exsits"
    else:
        df=pd.read_csv(path)
        filter = df[df['Ticker'] == name_of_section]

        filter.to_csv(f'{name_of_section[0:-3]}.csv' , index = False)
        return 'done'
print('section_wise_check' , section_wise_check('RELIANCE.NS'))