# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 00:12:25 2018

@author: Christina_Faye
"""

import pandas as pd
import numpy as np

def log_return(fm):
    r=np.log(fm[1:].values/fm[:-1].values)
    logr=pd.DataFrame(r,index=fm.index[1:],columns=fm.columns)
    return logr

def simple_return(fm):
    r=fm[1:].values/fm[:-1].values-1
    sr=pd.DataFrame(r,index=fm.index[1:],columns=fm.columns)
    return sr

def cum_return(r):
    return r.cumsum()

def annual_return(r):
    cumr=r.cumsum()
    lcumr=cumr.iloc[-1:]
    t=r.count()
    
    ar=(1+lcumr.values)**(250/t)-1
        
    return ar
