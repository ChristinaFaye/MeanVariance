# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 00:14:05 2018

@author: Christina_Faye
"""
from scipy.stats import norm

#volatility
def vol(r):
    return r.std()

def annual_vol(vol):
    n=vol.count()
    avar=vol*((250/n)**0.5)
    return avar

#downside risk
def downside_risk(r,marr):
    temp=r[r<marr]
    temp=temp.dropna()
    dev=(sum((temp-marr)**2)/len(r))**0.5
    return dev

#Vaule at Risk
def VaR_history(r,alpha):
    return r.quantile(alpha)

def VaR_cov(r,alpha):
    return  norm.ppf(alpha,r.mean(),r.std())

#Expected Shortfall
def ES(r,VaR):
    return r[r<=VaR].mean()


#max drawdown
def max_drawdown(r):
    value=(1+r).cumprod()
    D=value.cummax()-value
    d=D/(D+value)
    MDD=D.max()
    MDD_rate=d.max()
    return MDD.values,MDD_rate.values

def covariance(r):
    return r.cov()



    