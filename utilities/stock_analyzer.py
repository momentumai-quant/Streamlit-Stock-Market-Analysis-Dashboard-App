import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import streamlit as st

class StockAnalyzer:
    def __init__(self):
        self.data = None
        self.symbol = None
        
    def fetch_data(self, symbol, period='1y'):
        try:
            stock = yf.Ticker(symbol)
            self.data = stock.history(period=period)
            self.symbol = symbol
            self.calculate_all_indicators()
            return True
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return False
            
    def calculate_all_indicators(self):
        self.calculate_moving_averages()
        self.calculate_advanced_indicators()
        self.calculate_volatility_indicators()
        
    def calculate_moving_averages(self):
        for period in [9, 20, 50, 200]:
            self.data[f'SMA_{period}'] = self.data['Close'].rolling(window=period).mean()
            self.data[f'EMA_{period}'] = self.data['Close'].ewm(span=period, adjust=False).mean()
            
    def calculate_advanced_indicators(self):
        #using pandas_ta for calculating indicators
        self.data['RSI'] = ta.rsi(self.data['Close'], length=14)
        macd = ta.macd(self.data['Close'])
        self.data = pd.concat([self.data, macd], axis=1)
        
        #oscillator
        stoch = ta.stoch(self.data['High'], self.data['Low'], self.data['Close'])
        self.data = pd.concat([self.data, stoch], axis=1)
        
        #adx
        adx = ta.adx(self.data['High'], self.data['Low'], self.data['Close'])
        self.data = pd.concat([self.data, adx], axis=1)
        
    def calculate_volatility_indicators(self):
        #add bollingar bands
        bb = ta.bbands(self.data['Close'])
        self.data = pd.concat([self.data, bb], axis=1)
        
        #atr
        atr = ta.atr(self.data['High'], self.data['Low'], self.data['Close'])
        self.data['ATR'] = atr
        
    def get_current_signals(self):
        signals = {}
        
        #simple sma 50 vs 20 cross signal
        signals['sma_cross'] = 'Bullish' if self.data['SMA_20'].iloc[-1] > self.data['SMA_50'].iloc[-1] else 'Bearish'
        
        #simple rsi signal (over 70 and under 30)
        rsi = self.data['RSI'].iloc[-1]
        if rsi > 70:
            signals['rsi'] = 'Overbought'
        elif rsi < 30:
            signals['rsi'] = 'Oversold'
        else:
            signals['rsi'] = 'Neutral'
            
        #macd signal
        signals['macd'] = 'Bullish' if self.data['MACD_12_26_9'].iloc[-1] > self.data['MACDs_12_26_9'].iloc[-1] else 'Bearish'
        
        return signals