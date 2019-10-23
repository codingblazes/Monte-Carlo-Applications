# -*- coding: utf-8 -*- Unicode Transformation Format
"""
Created on Tue Oct 22 21:57:06 2019

@author: Ashwin Prakash Nalwade
"""

import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import math
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

class monte_carlo:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def get_asset(self, symbol):
        start = self.start
        end = self.end
      
        prices = web.DataReader(symbol, 'google', start, end)['Close']
        returns = prices.pct_change()
      
        self.returns = returns
        self.prices = prices
   
    
    def get_portfolio(self, symbols, weights):
        start = self.start
        end = self.end
        
        #Get Price Data
        df = web.DataReader(symbols, 'google',start, end)['Close']
        #Percent Change
        returns = df.pct_change()
        returns += 1
        
        #Define dollar amount in each asset
        port_val = returns * weights
        port_val['Portfolio Value'] = port_val.sum(axis=1)
        
        #Portfolio Dollar Values
        prices = port_val['Portfolio Value']
        
        #Portfolio Returns
        returns = port_val['Portfolio Value'].pct_change()
        returns = returns.replace([np.inf, -np.inf], np.nan)
                
        self.returns = returns
        self.prices = prices  
      
        
    def monte_carlo_sim(self, num_simulations, predicted_days):
        returns = self.returns
        prices = self.prices
        
        last_price = prices[-1]
        
        simulation_df = pd.DataFrame()

        #Create Each Simulation as a Column in df
        for x in range(num_simulations):
            count = 0
            daily_vol = returns.std()
            
            price_series = []
            
            #Append Start Value
            price = last_price * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            
            #Series for Preditcted Days
            for i in range(predicted_days):
                if count == 251:
                    break
                price = price_series[count] * (1 + np.random.normal(0, daily_vol))
                price_series.append(price)
                count += 1
        
            simulation_df[x] = price_series
            self.simulation_df = simulation_df
            self.predicted_days = predicted_days     
            
            
           