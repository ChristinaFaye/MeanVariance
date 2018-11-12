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
import math

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
        G=spmatrix(-1.0,range(dm),range(dm))
        #G=matrix(0.0,(dm,dm),'d')
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
         
    
    def frontierCurve(self,lower=-400,upper=3000):
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
        print('minimum variance point:')
        print('mu0=',mu0)
        print('sigma=',sigma)
        print(self.weight(mu0))
#find effective frontier curve
        efc=goals[index:]
      
        plt.plot(goals["sigma"],goals["mu0"],'b-')
        plt.plot(efc["sigma"],efc["mu0"],'r-',linewidth=2)
        plt.plot(efc.iloc[0,1],efc.iloc[0,0],'r*',markersize=15.0)
        plt.xlabel("sigma")
        plt.ylabel("Expected Return")
        return efc
    
    def random_portfolios(self,rf):
        exmean=[]
        var2=[]
        sharp=[]
        for i in range(1,5000):
            w=np.random.rand(self.returns.columns.size)
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
        plt.grid(True)
        plt.scatter(n_portfolios['sigma'],n_portfolios['mu0'],s=1.0,c=n_portfolios['sharp'],marker='o')
        plt.colorbar(label = 'Sharpe Ratio')
        
        return n_portfolios
    
    
    def weight_rf(self,goalRet,rf):
        dm=self.returns.columns.size
#covariance matrix
        sigma=np.array(self.returns.cov())
        P=matrix(sigma)
    
        q=matrix(0.0,(dm,1),'d')
    
#to restrict weights>=0:
        G=spmatrix(-1.0,range(dm),range(dm))
#if you allow short selling, please use:
        #G=matrix(0.0,(dm,dm),'d')
        h=matrix(0.0,(dm,1))  
        
        mu=np.array(self.returns.mean()-rf)
        A=matrix(mu,(1,dm),'d')
        b=matrix(goalRet-rf)
#get results
        sol=solvers.qp(P, q, G, h, A, b)
        res=sol['x']
        w=pd.DataFrame(np.array(res),index=self.returns.columns,columns=['weight'])
        return w
    

    def CML(self,rf,lower,upper):
      goals=pd.DataFrame([x/500000 for x in range(lower,upper)],columns=['mu0'])
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
    stock='600004.SH,600015.SH,600023.SH,600033.SH,600183.SH'
    field='close'
    startdate='2014-1-1'
    enddate='2016-1-1'
    fm=get_data(stock,field,startdate,enddate)
    r=log_return(fm)
    varMinimizer=MeanVariance(r)
    rf=(1+0.04)**(1/250)-1
    n_portfolios=varMinimizer.random_portfolios(rf)
    min_mu0=n_portfolios['mu0'].min()
    max_mu0=n_portfolios['mu0'].max()
    plt.ylim(min_mu0-0.0002,max_mu0+0.0002)
    print('The range of mu0:',min_mu0,'~',max_mu0)

    mu0=0.001
       
    w=varMinimizer.weight(mu0)
    mu=varMinimizer.meanRet(w)
    vol=varMinimizer.calVar(w)
    print('when mu=',mu[0])
    print('sigma=',vol)
    print(w)
    print('when risk-free asset is added:')
    wrf=varMinimizer.weight_rf(mu0,rf)
    print(wrf)    
    lower=int(n_portfolios['mu0'].min()*500000)
    upper=int(n_portfolios['mu0'].max()*500000)
    efc=varMinimizer.frontierCurve(lower,upper)
    lower=int(efc.iloc[0,0]*500000)
    goals=varMinimizer.CML(rf,lower,upper)
    varMinimizer.Mpoint(efc,goals)

main()

