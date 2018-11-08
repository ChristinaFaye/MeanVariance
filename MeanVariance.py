# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 22:26:22 2018

@author: Christina_Faye
"""

import numpy as np
import pandas as pd
from winddata import get_data
from get_return import log_return
import matplotlib.pyplot as plt
import math

#solvers.options['show_progress'] = False

class MeanVariance:
    def __init__(self,returns):
        self.returns=returns
    
    def weight(self,goalRet=0):
        covs=np.array(self.returns.cov())
        means=np.array(self.returns.mean())
        n=len(means)
        L1=np.append(np.append(covs,means.reshape((n,1)),1),np.ones((n,1)),1)
        L2=np.append(np.append([means],np.ones((1,n)),0),np.zeros((2,2)),1)
        L=np.append(L1,L2,0)
        B=np.zeros((n+2,1))
        B[-1,:]=1
        B[-2,:]=goalRet
        X=np.linalg.solve(L,B)
        w=pd.DataFrame(X[0:n,:],index=self.returns.columns,columns=['weight'])
        return w
        
        
        
    def meanRet(self,weights):
        w=np.array(weights)
        mu=np.array(self.returns.mean())
        return np.dot(mu,w)
    
    def calVar(self,weights):
        w=np.array(weights)
        sigma=np.array(self.returns.cov())
        v=np.dot(np.dot(w.T,sigma),w)
        return v[0,0]
         
    def frontierCurve(self):
        goals=[x/500000 for x in range(-4000,3000)]
        variance=[]
        for i in goals:
            w=self.weight(i)
            sigma=math.sqrt(self.calVar(w))
            variance.append(sigma)
          
        plt.plot(variance,goals,'r-')
        plt.xlabel("sigma")
        plt.ylabel("Expected Return")


    
    def random_portfolios(self):
        exmean=[]
        var2=[]
        for i in range(1,500):
            w=np.random.rand(self.returns.columns.size)
            weights=pd.DataFrame(w/sum(w))
            exmean.append(self.meanRet(weights))
            var2.append(self.calVar(weights))
             
        plt.plot(var2,exmean,'o')
        plt.show()
    
    def weight_rf(self,goalRet,rf):
        covs=np.array(self.returns.cov())
        means=np.array(self.returns.mean())-rf
        n=len(means)
        L1=np.append(covs,means.reshape((n,1)),1)
        L2=np.append([means],np.zeros((1,1)),1)
        L=np.append(L1,L2,0)
        B=np.zeros((n+1,1))
        B[-1,:]=goalRet-rf
        X=np.linalg.solve(L,B)
        w=pd.DataFrame(X[0:n,:],index=self.returns.columns,columns=['weight'])
        return w       

    def CML(self,rf):
        goals=[x/500000 for x in range(40,3000)]
        variance=[]
        for i in goals:
            w=self.weight_rf(i,rf)
            sigma=math.sqrt(self.calVar(w))
            variance.append(sigma)
          
        plt.plot(variance,goals,'r-')
        plt.xlabel("sigma")
        plt.ylabel("Expected Return")

  
def main():
    #stock='600000.SH,600004.SH'
    stock='600000.SH,600004.SH,600006.SH,600007.SH,600008.SH'
    field='close'
    startdate='2017-1-1'
    enddate='2018-1-1'
    fm=get_data(stock,field,startdate,enddate)
    r=log_return(fm)
    mu0=0.0001
    rf=0.000083
    varMinimizer=MeanVariance(r)
    w=varMinimizer.weight(mu0)
    mu=varMinimizer.meanRet(w)
    vol=varMinimizer.calVar(w)
    wrf=varMinimizer.weight_rf(mu0,rf)
    print(w)
    print('mu=',mu[0])
    print('sigma=',vol)
    print(wrf)
    #varMinimizer.frontierCurve()
    #varMinimizer.random_portfolios()
    #varMinimizer.CML(rf)

main()

