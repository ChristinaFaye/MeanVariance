# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 22:26:22 2018

@author: Christina_Faye
"""

import numpy as np
import pandas as pd
from cvxopt import matrix,solvers,spmatrix
from winddata import get_data
from get_return import log_return
import matplotlib.pyplot as plt

solvers.options['show_progress'] = False

class MeanVariance:
    def __init__(self,returns):
        self.returns=returns
        
    def weight(self,goalRet='null'):
        dm=self.returns.columns.size
#covariance matrix
        sigma=np.array(self.returns.cov())
        P=matrix(sigma)
    
        q=matrix(0.0,(dm,1),'d')
    
#to restrict weights>=0:
        #G=spmatrix(-1.0,range(dm),range(dm))
        G=matrix(0.0,(dm,dm),'d')
        h=matrix(0.0,(dm,1))
    
#restriction:mu0=E(rp),w1+w2+...+wn=1
        if goalRet!='null':
            mu=np.array(self.returns.mean())
            l=np.ones(dm)
            a=np.vstack((mu,l))
            A=matrix(a)
            b=matrix([goalRet,1.0],tc='d')
        else:
            A=matrix(np.ones(dm),(1,dm),'d')
            b=matrix(1.0)

#get results
        sol=solvers.qp(P, q, G, h, A, b)
        res=sol['x']
        w=pd.DataFrame(np.array(res),index=self.returns.columns,columns=['weight'])
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
        goals=[x/5000000 for x in range(-4000,3000)]
        variance=[]
        for i in goals:
            w=self.weight(i)
            variance.append(self.calVar(w))
          
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
        dm=self.returns.columns.size
#covariance matrix
        sigma=np.array(self.returns.cov())
        P=matrix(sigma)
    
        q=matrix(0.0,(dm,1),'d')
    
#to restrict weights>=0:
        #G=spmatrix(-1.0,range(dm),range(dm))
#if you allow short selling, please use:
        G=matrix(0.0,(dm,dm),'d')
        h=matrix(0.0,(dm,1))  
        
        mu=np.array(self.returns.mean()-rf)
        A=matrix(mu,(1,dm),'d')
        b=matrix(goalRet-rf)
#get results
        sol=solvers.qp(P, q, G, h, A, b)
        res=sol['x']
        w=pd.DataFrame(np.array(res),index=self.returns.columns,columns=['weight'])
        return w
    
    def CML(self):
        goals=[x/5000000 for x in range(500,3000)]
        variance=[]
        for i in goals:
            w=self.weight_rf(i,0.0001)
            variance.append(self.calVar(w))
        plt.plot(variance,goals,'r-')
    
def main():
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
    print(w)
    print('mu=',mu[0])
    print('sigma=',vol)
    wrf=varMinimizer.weight_rf(mu0,rf)
    print(wrf)
    #varMinimizer.frontierCurve()
    #varMinimizer.random_portfolios()

main()

