import pandas as pd
import datetime
import os
import sys
import multiprocessing
from multiprocessing import Pool
import time
import logging
import math

# backward = 180
# CAP_Limit = 10000000000
Price_Limit = 9.5
base_days = 59

def cal_Max_Min(df):

    EMA5_Max = []
    EMA10_Max = []
    EMA20_Max = []
    EMA60_Max = []
    EMA120_Max = []
    EMA250_Max = []
    OBV_Max = []
    Close_Max = []

    EMA5_Min = []
    EMA10_Min = []
    EMA20_Min = []
    EMA60_Min = []
    EMA120_Min = []
    EMA250_Min = []
    OBV_Min = []
    Close_Min = []
    
    for startindex in range(0,len(df)-base_days):
        endindex = startindex + base_days
        EMA5_Max.append(max(df.loc[startindex:endindex,'EMA5']))
        EMA10_Max.append(max(df.loc[startindex:endindex,'EMA10']))
        EMA20_Max.append(max(df.loc[startindex:endindex,'EMA20']))
        EMA60_Max.append(max(df.loc[startindex:endindex,'EMA60']))
        EMA120_Max.append(max(df.loc[startindex:endindex,'EMA120']))
        EMA250_Max.append(max(df.loc[startindex:endindex,'EMA250']))
        OBV_Max.append(max(df.loc[startindex:endindex,'OBV']))
        Close_Max.append(max(df.loc[startindex:endindex,'close']))
        EMA5_Min.append(min(df.loc[startindex:endindex,'EMA5']))
        EMA10_Min.append(min(df.loc[startindex:endindex,'EMA10']))
        EMA20_Min.append(min(df.loc[startindex:endindex,'EMA20']))
        EMA60_Min.append(min(df.loc[startindex:endindex,'EMA60']))
        EMA120_Min.append(min(df.loc[startindex:endindex,'EMA120']))
        EMA250_Min.append(min(df.loc[startindex:endindex,'EMA250']))
        OBV_Min.append(min(df.loc[startindex:endindex,'OBV']))
        Close_Min.append(min(df.loc[startindex:endindex,'close']))

    df.loc[base_days:len(df)-1,'EMA5_Max'] = EMA5_Max
    df.loc[base_days:len(df)-1,'EMA10_Max'] = EMA10_Max
    df.loc[base_days:len(df)-1,'EMA20_Max'] = EMA20_Max
    df.loc[base_days:len(df)-1,'EMA60_Max'] = EMA60_Max
    df.loc[base_days:len(df)-1,'EMA120_Max'] = EMA120_Max
    df.loc[base_days:len(df)-1,'EMA250_Max'] = EMA250_Max
    df.loc[base_days:len(df)-1,'OBV_Max'] = OBV_Max
    df.loc[base_days:len(df)-1,'Close_Max'] = Close_Max

    df.loc[base_days:len(df)-1,'EMA5_Min'] = EMA5_Min
    df.loc[base_days:len(df)-1,'EMA10_Min'] = EMA10_Min
    df.loc[base_days:len(df)-1,'EMA20_Min'] = EMA20_Min
    df.loc[base_days:len(df)-1,'EMA60_Min'] = EMA60_Min
    df.loc[base_days:len(df)-1,'EMA120_Min'] = EMA120_Min
    df.loc[base_days:len(df)-1,'EMA250_Min'] = EMA250_Min
    df.loc[base_days:len(df)-1,'OBV_Min'] = OBV_Min
    df.loc[base_days:len(df)-1,'Close_Min'] = Close_Min

    return df.loc[base_days:]

def cal_OBV(df):
    startindex = 0
    endindex = len(df)

    OBV = []
    OBV.append(0)
    # OBV_MAX = []
    # OBV_MAX.append(0)

    for i in range(startindex+1, endindex):
        high = df.high[i-1]
        low = df.low[i-1]
        mid = (high+low)/2
        if df.close[i] > mid:
            OBV.append(OBV[-1] + df.volume[i])
        elif df.close[i] < mid:
            OBV.append( OBV[-1] - df.volume[i])
        else:
            OBV.append(OBV[-1])
        # OBV_MAX.append(max(OBV))

    df['OBV'] = OBV
    # df['OBV_MAX'] = OBV_MAX

    return df

def cal_basics(df):

    lastindex = len(df)-1

    df['Breakout'] = 0
    df['Breakout_Cum'] = 0
    df['Wait'] = 0
    df['Wait_Cum'] = 0

    df['change'] = (df.close - df.close.shift(1))/df.close.shift(1)
    # df['change_1days'] = (df.close.shift(-1)- df.close)/df.close
    # df['change_2days'] = (df.close.shift(-2)- df.close)/df.close
    # df['change_3days'] = (df.close.shift(-3)- df.close)/df.close
    # df['change_4days'] = (df.close.shift(-4)- df.close)/df.close
    # df['change_5days'] = (df.close.shift(-5)- df.close)/df.close
    # df['change_6days'] = (df.close.shift(-6)- df.close)/df.close
    # df['change_7days'] = (df.close.shift(-7)- df.close)/df.close
    # df['change_8days'] = (df.close.shift(-8)- df.close)/df.close
    # df['change_9days'] = (df.close.shift(-9)- df.close)/df.close
    # df['change_10days'] = (df.close.shift(-10)- df.close)/df.close
    # df['change_11days'] = (df.close.shift(-11)- df.close)/df.close
    # df['change_12days'] = (df.close.shift(-12)- df.close)/df.close
    # df['change_13days'] = (df.close.shift(-13)- df.close)/df.close
    # df['change_14days'] = (df.close.shift(-14)- df.close)/df.close
    # df['change_15days'] = (df.close.shift(-15)- df.close)/df.close
    # df['change_16days'] = (df.close.shift(-16)- df.close)/df.close
    # df['change_17days'] = (df.close.shift(-17)- df.close)/df.close
    # df['change_18days'] = (df.close.shift(-18)- df.close)/df.close
    # df['change_19days'] = (df.close.shift(-19)- df.close)/df.close
    # df['change_20days'] = (df.close.shift(-20)- df.close)/df.close

    # shares = df.loc[lastindex,'shares']
    # df['turn'] = df.volume/shares

    ema5 = df['close'].ewm(span = 5, adjust = False).mean()
    ema10 = df['close'].ewm(span = 10, adjust = False).mean()
    ema20 = df['close'].ewm(span = 20, adjust = False).mean()
    ema60 = df['close'].ewm(span = 60, adjust = False).mean()
    ema120 = df['close'].ewm(span = 120, adjust = False).mean()
    ema250 = df['close'].ewm(span = 250, adjust = False).mean()
    df['EMA5'] = ema5
    df['EMA10'] = ema10
    df['EMA20'] = ema20
    df['EMA60'] = ema60
    df['EMA120'] = ema120
    df['EMA250'] = ema250

    return df

def run(ticker_chunk_df):
    return_ticker_chunk_df = pd.DataFrame()
    tickers= ticker_chunk_df.ticker.unique()
    for ticker in tickers:
        df = ticker_chunk_df[ticker_chunk_df.ticker==ticker].reset_index(drop=True)
        lastindex = df.index[-1]

        if df['close'][lastindex] > Price_Limit:
            continue
        elif(len(df)<=base_days):
            # print(ticker+" length is less than base_days business days.")
            continue

        df = cal_basics(df)
        df = cal_OBV(df)
        df = cal_Max_Min(df)

        if not df.empty:
            return_ticker_chunk_df = pd.concat([return_ticker_chunk_df,df],ignore_index=True)
    return return_ticker_chunk_df

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == '__main__':

    raw_data_path='//jack-nas/Work/Python/RawData/'
    processed_data_path='//jack-nas/Work/Python/ProcessedData/'

    logpath = '//jack-nas/Work/Python/'
    logfile = logpath + datetime.datetime.now().strftime("%m%d%Y") + "_process.log"
    logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO)

    isPathExists = os.path.exists(processed_data_path)
    if not isPathExists:
        os.makedirs(processed_data_path)

    while True:
        now = datetime.datetime.now()
        # today3pm = now.replace(hour=15,minute=5,second=0,microsecond=0)
        # if(now>today3pm):
        #     logging.info("time passed 3:05pm.")
        #     break
        start_time = now.strftime("%m%d%Y-%H%M%S")
        logging.info("start time:" + start_time)
        raw_data_files = os.listdir(raw_data_path)
        if len(raw_data_files) == 0:
            logging.warning("raw data not ready, sleep 10 seconds...")
            time.sleep(10)
            continue
        # date_time = datetime.datetime.now() 
        # datetime_str = date_time.strftime("%m%d%Y-%H")
        # processed_data_file = datetime_str + '.feather'

        processed_data_files = os.listdir(processed_data_path)
        if raw_data_files[-1] in processed_data_files:
            logging.warning("error: " + raw_data_files[-1] + " existed, sleep 10 seconds...")
            time.sleep(10)
            continue
        
        logging.info("processing "+raw_data_files[-1])
        try:
            time.sleep(10)
            df = pd.read_feather(raw_data_path + raw_data_files[-1])
        except Exception as e:
            logging.critical(e)
            continue

        tickers = df.ticker.unique()

        cores = multiprocessing.cpu_count()
        ticker_chunk_list = list(chunks(tickers,math.ceil(len(tickers)/cores)))
        pool = Pool(cores)
        async_results = []
        for ticker_chunk in ticker_chunk_list:
            ticker_chunk_df = df[df['ticker'].isin(ticker_chunk)]
            async_result = pool.apply_async(run, args=(ticker_chunk_df,))
            async_results.append(async_result)
        pool.close()
        del(df)

        df = pd.DataFrame()
        for async_result in async_results:
            result = async_result.get()
            if not result.empty:
                df = pd.concat([df,async_result.get()])
        
        if(not df.empty):
            df.reset_index(drop=True,inplace=True)
            try:
                df.to_feather(processed_data_path + raw_data_files[-1])
            except Exception as e:
                logging.critical("to_feather:"+str(e))
            # df.to_csv(processed_data_path + raw_data_files[-1] + '.csv')
            stop_time = datetime.datetime.now().strftime("%m%d%Y-%H%M%S")
            logging.info("stop time:" +stop_time)
            # os.popen(f'python C:/Code/One/screen_data_One_Wait.py')
            # os.popen(f'python C:/Code/One/screen_data_One_Breakout.py')
        else:
            logging.error("df empty")