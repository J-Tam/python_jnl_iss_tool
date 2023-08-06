# coding: UTF-8
import pandas as pd
from pandas import DataFrame
from pandas import Series
import datetime as dt
import numpy as np
import math

def cnv_amt_str_2_int(sr_amt: Series) -> Series:

    sr_amt = sr_amt.str.replace(',','')
    sr_amt = sr_amt.astype('int')

    return sr_amt

def cnv_amt_str_2_float(sr_amt: Series) -> Series:

    sr_amt = sr_amt.str.replace(',','')
    sr_amt = sr_amt.astype('float')

    return sr_amt

def cnv_date_str_zfill(sr_date: Series) -> Series:

    sr_date = pd.to_datetime(sr_date)
    sr_date = sr_date.apply(lambda x: x.strftime('%Y/%m/%d').zfill(10))

    return sr_date

def get_min_dt_fr_series(sr_dt: Series) -> dt.datetime:

    sr_sorted = sr_dt.sort_values()
    sr_sorted = sr_sorted.reset_index(drop=True)

    min_dt_fr_series = dt.datetime.strptime(sr_sorted[0], "%Y/%m/%d")

    return min_dt_fr_series