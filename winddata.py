# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 00:11:17 2018

@author: Christina_Faye
"""

from WindPy import*
w.start()
import pandas as pd

def get_data(stock,field,startdate,enddate):
    #get data from wind, then transfer to dataframe
    data=w.wsd(stock,field,startdate,enddate)
    stock=stock.strip(',').split(',')
    fm=pd.DataFrame(data.Data,index=stock,columns=data.Times)
    fm=fm.T
    return fm