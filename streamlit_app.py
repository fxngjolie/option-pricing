# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:32:23 2021

@author: jols
"""

import streamlit as st
from optionpricingmodels import BlackScholes,BinomialTree,MonteCarlo
from datetime import datetime

st.title('Option Pricing Models')
method = st.sidebar.radio("Select option pricing method",("Black-Scholes 🚀","Binomial Tree 🌴","Monte Carlo 🎲"))

st.header('Method: '+method)

if method == "Black-Scholes 🚀":
    
    #description
    st.subheader('Description')
    st.write("The idea behind the model is to hedge European options by buying or selling the underlying asset, \
             thereby eliminating the risk associated with volatility of the underlying asset. This involves solving \
             a partial differential equation that models the returns of the stock + options portfolio. From there, the option price is the expected value of the discounted \
            payoff of the option. Read more [here](https://www.cantorsparadise.com/the-black-scholes-formula-explained-9e05b7865d8a).")
    st.write(
        """
        Assumptions:
        - No dividends paid
        - Risk-free rate and volatility are constant
        - Underlying returns are lognormally distributed
        - No transaction or slippage costs
                    
        """
        )
    
    #params
    st.subheader('Calculator')
    S = st.number_input('Underlying Price', min_value = 0)
    K = st.number_input('Strike Price', min_value = 0)
    date = st.date_input('Expiry Date',min_value = datetime.today())
    T = (date - datetime.now().date()).days
    r = st.slider('Risk-free Rate (%)',0,100,5)
    sigma = st.slider('Volatility (%)',0,100,20)
    
    #calculation
    if st.button('Calculate'):
        BSM = BlackScholes(S,K,T,r,sigma)
        call = BSM._call_price()
        put = BSM._put_price()
        
        st.subheader('Call Option: $'+'{0:.2f}'.format(call))
        st.subheader('Put Option: $'+'{0:.2f}'.format(put))

elif method == "Binomial Tree 🌴":
    #description
    st.subheader('Description')
    st.write('This is a lattice-based method which discretizes time, calculates option payoff at each final node, \
            then works backwards at each time step to calculate payoffs at previous nodes based on the probability of an up or down \
            move in the underlying stock by a certain factor. Here, the [Cox-Ross-Rubenstein](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) binomial tree approximation \
                is used.')
    
    #params
    st.subheader('Calculator')
    S = st.number_input('Underlying Price', min_value = 0)
    K = st.number_input('Strike Price', min_value = 0)
    date = st.date_input('Expiry Date',min_value = datetime.today())
    T = (date - datetime.now().date()).days
    r = st.slider('Risk-free Rate (%)',0,100,5)
    sigma = st.slider('Volatility (%)',0,100,20)
    N = st.slider('Number of time steps',1,100)
    
    #calculation
    if st.button('Calculate'):
        BT = BinomialTree(S,K,T,r,sigma,N)
        call = BT._call_price()
        put = BT._put_price()
        
        st.subheader('Call Option: $'+'{0:.2f}'.format(call))
        st.subheader('Put Option: $'+'{0:.2f}'.format(put))

elif method == "Monte Carlo 🎲":
    #description
    col1, col2 = st.columns(2)
    col1.subheader('Description')
    col1.write('In this method, as the name suggests, we simulate many paths for underlying asset price using the Geometric Brownian Motion stochastic process. \
             For each path, we can calculate the payoff for the option. We then average all payoffs and discount the mean payoff at the risk-free \
             rate to get the value of the option.')
    col1.write('Use the slider on the right to visualise the simulation results for a specific number of price movements (after you have calculated the option prices).')
    col2.subheader('Visualisation')
    
    #params
    st.subheader('Calculator')
    S = st.number_input('Underlying Price', min_value = 0)
    K = st.number_input('Strike Price', min_value = 0)
    date = st.date_input('Expiry Date',min_value = datetime.today())
    T = (date - datetime.now().date()).days
    r = st.slider('Risk-free Rate (%)',0,100,5)
    sigma = st.slider('Volatility (%)',0,100,20)
    N = st.slider('Number of simulations',1,100)
    
    #calculation
    if st.button('Calculate'):
        MC = MonteCarlo(S,K,T,r,sigma,N)
        results = MC.sim_prices()
        call = MC._call_price()
        put = MC._put_price()
        
        st.subheader('Call Option: $'+'{0:.2f}'.format(call))
        st.subheader('Put Option: $'+'{0:.2f}'.format(put))

    n_movements = col2.slider('Number of random price movements',0,N)
    if st.button('Visualize'):
        MC = MonteCarlo(S,K,T,r,sigma,N)
        results = MC.sim_prices()
        figure = MC._plot_paths(n_movements)
        col2.pyplot(fig=figure)