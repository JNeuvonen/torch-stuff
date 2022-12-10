
import pandas as pd
import utility.functions as F

PATH_STOCKS = 'data/archive/Stocks'
PATH_ETF = 'data/archive/ETFs'
SAVED_DATA_PATH = 'processed-data'


stock_data = F.read_folder_rows(PATH_STOCKS, 0, 10000)
etf_data = F.read_folder_rows(PATH_ETF, 0, 10000)

result = stock_data + etf_data
data = pd.concat(result)


data.to_csv(SAVED_DATA_PATH, index=False)
