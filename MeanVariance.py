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
         
    def frontierCurve(self,lower,upper):
        goals=pd.DataFrame([x/500000 for x in range(lower,upper)],columns=["mu0"])
        goals["sigma"]=0
        for i in range(len(goals)):
            mu0=goals.loc[i,"mu0"]
            w=self.weight(mu0)
            sigma=math.sqrt(self.calVar(w))
            goals.loc[i,"sigma"]=sigma
        
        #find the point with minimum variance
        index=goals["sigma"].idxmin()
        mu0=goals.loc[index,'mu0']
        sigma=goals.loc[index,'sigma']
        print('minimum variance portfolio:')
        print('mu0=',mu0)
        print('sigma=',sigma)
        print(self.weight(goals.loc[index,"mu0"]))
        #find effective frontier curve
        efc=goals[index:]
          
        plt.plot(goals["sigma"],goals["mu0"],'b-')
        plt.plot(efc["sigma"],efc["mu0"],'r-',linewidth=2)
        plt.plot(efc.iloc[0,1],efc.iloc[0,0],'r*',markersize=15.0)
        plt.xlabel("sigma")
        plt.ylabel("Expected Return")
        return efc
    

#rf:to calculate sharp ratio
    def random_portfolios(self,rf):
        exmean=[]
        var2=[]
        sharp=[]
        for i in range(1,5000):
            w=np.random.uniform(-1,1,self.returns.columns.size)
            weights=pd.DataFrame(w/sum(w))
            mu0=self.meanRet(weights)
            sigma=math.sqrt(self.calVar(weights))
            sharp_ratio=(mu0-rf)/sigma
            exmean.append(mu0)
            var2.append(sigma)
            sharp.append(sharp_ratio)            
       
        n_portfolios=pd.DataFrame(exmean,columns=['mu0'])
        n_portfolios['sigma']=var2
        n_portfolios['sharp']=sharp
# to control sigma in a certain range
        limits=3*n_portfolios['sigma'].min()
        n_portfolios=n_portfolios[n_portfolios['sigma']<limits]
        
        plt.grid(True)
        plt.scatter(n_portfolios['sigma'],n_portfolios['mu0'],s=1.0,c=n_portfolios['sharp'],marker='o')
        plt.colorbar(label = 'Sharpe Ratio')
    
        return n_portfolios        
    
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
        goals=pd.DataFrame([x/500000 for x in range(int(rf*500000),3000)],columns=['mu0'])
        goals['sigma']=0
        for i in range(len(goals)):
            mu=goals.loc[i,'mu0']
            w=self.weight_rf(mu,rf)
            sigma=math.sqrt(self.calVar(w))
            goals.loc[i,'sigma']=sigma
        
        plt.plot(goals['sigma'],goals['mu0'],'r-')
        plt.xlabel("sigma")
        plt.ylabel("Expected Return")
        
        return goals
    
    def Mpoint(self,efc,goals):
        EFC=pd.DataFrame(efc['sigma'].values,index=efc['mu0'],columns=['sigma'])
        CML=pd.DataFrame(goals['sigma'].values,index=goals['mu0'],columns=['sigma'])
        diff=abs(CML-EFC).dropna()
        print("The efficient portfolio M:")
        Vdiff=diff.min().values[0]
        if Vdiff<=0.000001:
            mu0=diff.idxmin().values[0]
            weights=self.weight(mu0)
            sigma=math.sqrt(self.calVar(weights))
            print("mu0=",mu0)
            print("sigma=",sigma)
            print(weights)
            print("difference:",Vdiff)
            plt.plot(sigma,mu0,'k*',markersize=15.0)
        else:
            print("Please adjust lower and upper limits of frontier curve!")
            
            
  
def main():
    #stock='600000.SH,600004.SH'
    #stock='600004.SH,600015.SH,600023.SH,600033.SH,600183.SH'
    stock='601919.SH,000063.SZ,002508.SZ,600016.SH,601012.SH,600585.SH'
    field='close'
    startdate='2014-1-1'
    enddate='2015-1-1'
    fm=get_data(stock,field,startdate,enddate)
    r=log_return(fm)
    mu0=0.0001
    rf=0.000083
    varMinimizer=MeanVariance(r)
    w=varMinimizer.weight(mu0)
    mu=varMinimizer.meanRet(w)
    vol=varMinimizer.calVar(w)
    wrf=varMinimizer.weight_rf(mu0,rf)
    print('when mu=',mu[0],':')
    print('sigma=',vol)
    print(w)
    print('when risk-free asset is added:\n',wrf)
    n_p=varMinimizer.random_portfolios(rf)
    
    lower=int(n_p['mu0'].min()*500000)
    upper=int(n_p['mu0'].max()*500000)
    efc=varMinimizer.frontierCurve(lower,upper)
    goals=varMinimizer.CML(rf)
    varMinimizer.Mpoint(efc,goals)

main()

