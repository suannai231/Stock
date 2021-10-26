#from pandas_datareader import data
from yahoo_fin import stock_info as si
import yfinance as yf
#import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
# import numpy as np
import datetime
import time
import os
# import threading
# import multiprocessing
# from multiprocessing import Pool
# import string
import concurrent.futures as cf
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from multiprocessing import Pool
# from multiprocessing import Value
from multiprocessing import Process, Manager

days=365*10

def run(ticker):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
    shares = -1
    try:
        quote_data = si.get_quote_data(ticker)
        shares = quote_data['sharesOutstanding']
    except Exception as e:
        if (str(e) == "'sharesOutstanding'") | (str(e) == 'Invalid response from server.  Check if ticker is\n                              valid.'):
            try:
                info = yf.Ticker(ticker).info
                shares = info['sharesOutstanding']
            except Exception as e:
                if str(e) == "'sharesOutstanding'":
                    return 0
                elif str(e).startswith('HTTPSConnectionPool') | str(e).startswith("('Connection aborted.'"):
                    return -1
                else:
                    return 0
        elif str(e).startswith('HTTPSConnectionPool') | str(e).startswith("('Connection aborted.'"):
            return -1
        else:
            return 0
    if (shares is None):
        return 0
    else:
        if int(shares) < 1:
            return 0
    try:
        df = si.get_data(ticker,start, end)
    except Exception as e:
        if (str(e) == "'timestamp'") | (str(e) == "'NoneType' object is not subscriptable"):
            return 0
        elif str(e).startswith('HTTPSConnectionPool') | str(e).startswith("('Connection aborted.'"):
            return -1
        else:
            return 0
    if df.empty:
        return 0
    df["shares"] = shares
    df["marketCap"] = df["close"]*shares
    df.to_csv(path+'/'+ticker+'.csv')
    return 1

# result_list = []
# def log_result(result):
#     result_list.append(result)

start = datetime.datetime.now() - datetime.timedelta(days)
end = datetime.date.today()

# path=f"C:/Python/{end}"
path = f'//jack-nas/Work/Python/RawData/{end}'

if __name__ == '__main__':
    isPathExists = os.path.exists(path)
    if not isPathExists:
        os.makedirs(path)
    # else:
    #     files = os.listdir(path)
    #     for f in files:
    #         os.remove(os.path.join(path,f))

    nasdaq = si.tickers_nasdaq()
    other = si.tickers_other()
    tickers = nasdaq + other #+ dow + sp500
    files = os.listdir(path)
    # thread_number = 100
    # i = 10
    # while True:
    #     if thread_number-i != 0:
    #         with ThreadPoolExecutor(thread_number-i) as tp:
    #             jobs = [tp.submit(run_thread,ticker) for ticker in tickers]
    #             success_num = 0
    #             for job in cf.as_completed(jobs):
    #                 if job.result() == -1:
    #                     i+=10
    #                     break
    #                 success_num += job.result()
    #         print(str(success_num)+' tickers raw data have been saved.\n')
    #         break
    #     else:
    #         break

    cores = multiprocessing.cpu_count()
    i = 0
    Loop = True
    while Loop:
        if cores-i != 0:
            with Pool(cores-i) as p:
                async_result_list = []
                for ticker in tickers:
                    # isTickerExists = os.path.exists(path+'/'+ticker+'.csv')
                    # if not isTickerExists:
                    file = ticker+'.csv'
                    if file in files:
                        continue
                    async_result = p.apply_async(run, args=(ticker,))
                    async_result_list.append(async_result)
                p.close()
                p.join()
                Loop = False
                success_num = 0
                for async_result in async_result_list:
                    result = async_result.get()
                    if result == -1:
                        i+=1
                        Loop = True
                        print(str(cores-i)+' processes didn\'t work, restarting...\n')
                        break
                    else:
                        Loop = False
                    success_num += result
                print(str(success_num)+' tickers raw data have been saved.\n')
        else:
            Loop = False
    os.popen(f'python C:/Users/jayin/OneDrive/Code/prepare_data_MP.py')