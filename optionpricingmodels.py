# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class BlackScholes():
    """
    Black-Scholes PDE
    """
    def __init__(self,S,K,T,r,sigma):
        """
        S: Underlying spot price
        K: Strike price
        T: days to maturity
        r: Risk-free rate (%)
        sigma: volatility of log returns
        """
        self.T = T/365
        self.r = r/100
        self.sigma = sigma/100
        self.K = K
        self.S = S 
        
    def _call_price(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) 
              * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) *
              self.T) / (self.sigma * np.sqrt(self.T))
        return (self.S * norm.cdf(d1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0.0, 1.0))
   
    def _put_price(self): 
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0.0, 1.0) - self.S * norm.cdf(-d1, 0.0, 1.0))

class BinomialTree():
    """
    Cox-Ross-Rubenstein Binomial Tree
    """
    def __init__(self,S,K,T,r,sigma,N):
        """
        S: Underlying spot price
        K: Strike price
        T: days to maturity
        r: Risk-free rate (%)
        sigma: volatility of log returns
        N: number of time steps
        """
        self.T = T/365
        self.r = r/100
        self.sigma = sigma/100
        self.K = K
        self.S = S
        self.N = N
    
    def _call_price(self):
        dt = self.T/self.N
        u = np.exp(self.sigma)*np.sqrt(dt)
        d = 1.0/u
        
        tree = np.zeros(self.N + 1)                       

        S_t = np.array( [(self.S * u**j * d**(self.N - j)) for j in range(self.N + 1)])

        a = np.exp(self.r * dt)
        p = (a - d) / (u - d)        # risk-neutral up probability
        q = 1.0 - p                  # risk-neutral down probability   

        tree[:] = np.maximum(S_t - self.K, 0.0)
    
        #fill up tree backwards!
        for i in range(self.N - 1, -1, -1):
            tree[:-1] = np.exp(-self.r * dt) * (p * tree[1:] + q * tree[:-1])
        
        return tree[0]
    
    def _put_price(self):
        dt = self.T/self.N
        u = np.exp(self.sigma)*np.sqrt(dt)
        d = 1.0/u
        
        tree = np.zeros(self.N + 1)                       

        S_t = np.array( [(self.S * u**j * d**(self.N - j)) for j in range(self.N + 1)])

        a = np.exp(self.r * dt)
        p = (a - d) / (u - d)        # risk-neutral up probability
        q = 1.0 - p                  # risk-neutral down probability   

        tree[:] = np.maximum(self.K-S_t, 0.0)
    
        #fill up tree backwards!
        for i in range(self.N - 1, -1, -1):
            tree[:-1] = np.exp(-self.r * dt) * (p * tree[1:] + q * tree[:-1])
        
        return tree[0]

class MonteCarlo():
    """
    Simulate underlying price using Geometric Brownian Motion
    """
    def __init__(self,S,K,T,r,sigma,N):
        """
        S: Underlying spot price
        K: Strike price
        T: days to maturity
        r: Risk-free rate (%)
        sigma: volatility of log returns
        N: number of simulations
        """
        self.T = T
        self.r = r/100
        self.sigma = sigma/100
        self.K = K
        self.S = S
        self.N = N
        
        self.T_years = T/365
        self.dt = self.T_years/self.T
        
    def sim_prices(self):
        np.random.seed(20)
        self.result = None
        
        S_t = np.zeros((self.T, self.N))        
        S_t[0] = self.S

        for t in range(1, self.T):
            Z = np.random.standard_normal(self.N) 
            S_t[t] = S_t[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dt + (self.sigma * np.sqrt(self.dt) * Z))

        self.result = S_t
    
    def _call_price(self):
            if self.result is None:
                return "N/A"
            return np.exp(-self.r * self.T_years) * 1 / self.N * np.sum(np.maximum(self.result[-1] - self.K, 0))
    
    def _put_price(self):
            if self.result is None:
                return "N/A"
            return np.exp(-self.r * self.T_years) * 1 / self.N * np.sum(np.maximum(self.K- self.result[-1], 0))
    
    def _plot_paths(self,n_movement):
        arr = self.result[:,0:n_movement]
        figure,ax=plt.subplots()
        ax.plot(arr)
        ax.set_xlim([0,self.T])
        ax.set_ylabel('Price')
        ax.set_xlabel('Time (days)')
        return figure
        
    
    
        
        