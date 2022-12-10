import pandas as pd
import os


def read_folder_rows(path, range_start, range_end):

    print(range_start, range_end)

    train_data = []
    SMA_ARR = [7, 30]
    files_read = 0
    count = range_start
    # Date,Open,High,Low,Close,Volume,OpenInt
    for filename in os.listdir(path):
        if count < range_start or count > range_end:
            count += 1
            continue

        try:
            read_file = os.path.join(path, filename)
            ticker_data = pd.read_csv(read_file)
            new_pd_table = pd.DataFrame()
            new_pd_table['HIGH/LOW'] = (ticker_data['High'] /
                                        ticker_data['Low'] - 1) * 1000

            new_pd_table['TARGET'] = (ticker_data['Close'].shift(
                -30) / ticker_data['Close'] - 1) * 1000

            for sma_type in SMA_ARR:
                new_pd_table['SMA{}_HIGH/LOW'.format(sma_type)] = (new_pd_table['HIGH/LOW'].rolling(
                    sma_type).mean() - 1) * 1000

                new_pd_table['{}D_HIGH/LOW'.format(sma_type)] = (ticker_data['High'].rolling(
                    sma_type).max() / ticker_data['Low'].rolling(
                    sma_type).min() - 1) * 1000

                # SMA
                SMA_MEAN = ticker_data['Close'].rolling(sma_type).mean()

                new_pd_table['{}D_SMA/{}D_CLOSE'.format(sma_type, sma_type)
                             ] = (SMA_MEAN / ticker_data['Close'].shift(sma_type) - 1) * 1000

                new_pd_table['{}D_SMA/{}D_HIGH'.format(sma_type, sma_type)
                             ] = (SMA_MEAN / ticker_data['High'].shift(sma_type) - 1) * 1000

                new_pd_table['{}D_SMA/{}D_LOW'.format(sma_type, sma_type)
                             ] = (SMA_MEAN / ticker_data['Low'].shift(sma_type) - 1) * 1000

                new_pd_table['{}D_SMA/LAST_CLOSE'.format(sma_type)
                             ] = (SMA_MEAN / ticker_data['Close'] - 1) * 1000

                new_pd_table['{}D_AVG_GAIN'.format(sma_type)
                             ] = new_pd_table['{}D_SMA/LAST_CLOSE'.format(sma_type)
                                              ].rolling(sma_type).mean()

                for sma in SMA_ARR:
                    if sma != sma_type:
                        new_pd_table['{}D_SMA/{}D_SMA'.format(sma, sma_type)
                                     ] = (SMA_MEAN / ticker_data['Close'].rolling(sma).mean() - 1) * 1000

            train_data.append(new_pd_table)
            files_read += 1
            print(files_read)

        except Exception as e:
            print(e)

        count += 1
    return train_data
