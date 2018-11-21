# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 13:29:00 2018

@author: zxwan
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
from pytz import timezone 
import tushare as ts 
import pandas_datareader.data as web  

class auto_combination:
    nums = np.array([])
    codes = []
    names = []
    prices = np.array([])
    values = np.array([])
    currency = 0.88
    date = ""
    combn_data = None #combination information
    value = 0.0
    ratios = np.array([])
    net_v = 1.0
    init = 100000.0


    def __init__(self,curr_input):
        self.get_date()
        self.init = self.read_initial()
        if curr_input == 0:
            self.currency = self.read_currency()    # HK vs rmb
        else:
            self.currency = curr_input
        self.combn_data = self.read_comb_info()
        self.codes = self.combn_data['code'].tolist()
        self.nums = np.float_(self.combn_data['num'].tolist())
        self.names = self.combn_data['name'].tolist()
        
        
        i = 0
        for s_code in self.codes:
            price = self.get_price(s_code)
            print(self.names[i])
            print(price)
            self.prices = np.append(self.prices, price)
            value = price*self.nums[i]
            self.values = np.append(self.values,value)
            i = i+1
        self.update_combi_data()
                    

    def update_combi_data(self):
        self.value = self.values.sum()
        self.ratios = self.values/self.value
        self.net_v = self.value/self.init
               
    def get_date(self):
        # date of beijing
        bj = timezone('Asia/Hong_Kong')
        bj_time = datetime.now(bj)
        bj_date = bj_time.strftime('%Y-%m-%d')
        self.date = bj_date
        
    def read_comb_info(self,*filename):
        # Read the detailed info of the combination
        if len(filename) == 0:
            file = u"Real_combination_info.xlsx"
        else:
            file = filename
        comb_info = pd.read_excel(file,dtype = str)
        return comb_info
    
    def read_currency(self,*filename):
        # Read the exchange currency between HKD and CNY
        if len(filename) == 0:
            file = u"Currency.xlsx"
        else:
            file = filename
        currency = pd.read_excel(file,dtype = str)
        return float(currency['price'].iat[0])

    def read_initial(self,*filename):
        # Read the initial capital
        if len(filename) == 0:
            file = u"Initial_invest.xlsx"
        else:
            file = filename
        init = pd.read_excel(file,dtype = str)
        return float(init['price'].iat[0])
    
    def get_price(self,s_code):
        #Get the price of a certain stock from its code
        try:
            tmp = int(s_code)
        except:
            pass
        else:
            if tmp == 0:
                # this is the item of Cash
                return 1.0
        if len(s_code) != 6:
            # 港股
            pdate = date.today() - timedelta(10)
            pdatet = pdate.strftime('%Y-%m-%d')
            data_Df=web.get_data_yahoo(s_code,pdatet,self.date)
            price = data_Df['Close'].iloc[-1]*self.currency
        else:
            # A股
            df = ts.get_k_data(s_code)
            price = df.iloc[-1]['close']    # price of the latest closing trading day, numpy.float
        return price
    
    def save(self, **kwargs):
        # Write to files
        default = {'daily_file': 'Simple_Auto_combination_date_info',\
                   'date_file': 'Latest_combination_ratio'}
        for item in default:
            if item in kwargs:
                default[item] = kwargs[item]

        dic_day = {'Total_value':self.value, \
                   'Date':self.date, \
                   "Net value":self.net_v}
        df_day = pd.DataFrame(dic_day,index = [0])
        try:
            day_in = pd.read_excel(default['daily_file']+ '.xlsx')
        except: # file not exist
            day_all = df_day
        else:
            day_all = day_in.append(df_day, ignore_index=True)#,sort=False)
        day_all.to_excel(default['daily_file'] + '.xlsx')
        print(u'总市值:')
        print(self.value)
        print(u"净值:")
        print(self.net_v)
      
        
        dic = {'code':self.codes, 'name': self.names, 'num': self.nums,\
               'value':self.values,'radio':self.ratios}
        df = pd.DataFrame.from_dict(dic)
        df.to_excel(default['date_file'] + '.xlsx')

