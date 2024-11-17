import streamlit as st
import pandas as pd
import numpy as np
from utilities.stock_analyzer import StockAnalyzer
from utilities.visualization import ChartVisualizer


from utilities.pages_utilities import *
class IndicatorsPage:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        self.visualizer = ChartVisualizer()
        
    def show_page(self, loc_config):
        st.title(loc_config.get_text("custom_indicators_title"))
        
        # Stock Symbol Input
        symbol = st.text_input(
            loc_config.get_text("symbol_input"),
            value="AAPL",
            help=loc_config.get_text("symbol_help")
        )
        
        if st.button(loc_config.get_text("calculate_indicators_btn")):
            with st.spinner(loc_config.get_text("loading_data")):
                if self.analyzer.fetch_data(symbol):
                    self._show_custom_indicators(loc_config)
                    
    def _show_custom_indicators(self, loc_config):
        indicator_options = {
            'Custom MA Cross': self._calculate_ma_cross,
            'Volume Price Trend': self._calculate_vpt,
            'Price Channels': self._calculate_price_channels,
            'Custom Momentum': self._calculate_custom_momentum
        }
        
        selected_indicators = st.multiselect(
            loc_config.get_text("select_custom_indicators"),
            options=list(indicator_options.keys()),
            default=['Custom MA Cross', 'Volume Price Trend']
        )
        
        if selected_indicators:
            for indicator in selected_indicators:
                indicator_options[indicator](loc_config)
                
    def _calculate_ma_cross(self, loc_config):
        st.subheader(loc_config.get_text("ma_cross_title"))
        
        col1, col2 = st.columns(2)
        with col1:
            fast_period = st.slider(
                loc_config.get_text("fast_ma_period"),
                min_value=5,
                max_value=50,
                value=10
            )
        with col2:
            slow_period = st.slider(
                loc_config.get_text("slow_ma_period"),
                min_value=10,
                max_value=200,
                value=30
            )
            
        data = self.analyzer.data.copy()
        data[f'FastMA'] = data['Close'].rolling(window=fast_period).mean
        data[f'SlowMA'] = data['Close'].rolling(window=slow_period).mean()
        data['CrossSignal'] = np.where(data['FastMA'] > data['SlowMA'], 1, -1)
        
        # Create visualization
        fig = self.visualizer.create_candlestick_chart(
            data, 
            data.index[-1], 
            [f'FastMA', f'SlowMA']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display signals
        last_signal = "Bullish" if data['CrossSignal'].iloc[-1] > 0 else "Bearish"
        st.metric(
            loc_config.get_text("current_signal"),
            last_signal,
            delta=None,
            delta_color="normal"
        )
        
    def _calculate_vpt(self, loc_config):
        st.subheader(loc_config.get_text("vpt_title"))
        
        data = self.analyzer.data.copy()
        data['VPT'] = self._calculate_vpt_values(data)
        
        # Create VPT visualization
        fig = make_subplots(rows=2, cols=1, shared_xaxis=True)
        
        # Price chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # VPT indicator
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['VPT'],
                name='VPT',
                line=dict(color='purple')
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=800)
        st.plotly_chart(fig, use_container_width=True)
        
    def _calculate_vpt_values(self, data):
        close = data['Close']
        volume = data['Volume']
        
        price_change = close.pct_change()
        vpt = (volume * price_change).cumsum()
        return vpt
        
    def _calculate_price_channels(self, loc_config):
        st.subheader(loc_config.get_text("price_channels_title"))
        
        period = st.slider(
            loc_config.get_text("channel_period"),
            min_value=10,
            max_value=100,
            value=20
        )
        
        data = self.analyzer.data.copy()
        data['Upper_Channel'] = data['High'].rolling(window=period).max()
        data['Lower_Channel'] = data['Low'].rolling(window=period).min()
        data['Middle_Channel'] = (data['Upper_Channel'] + data['Lower_Channel']) / 2
        
        fig = self.visualizer.create_candlestick_chart(
            data,
            data.index[-1],
            ['Upper_Channel', 'Middle_Channel', 'Lower_Channel']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate channel width and trend
        channel_width = ((data['Upper_Channel'] - data['Lower_Channel']) / data['Middle_Channel'] * 100).iloc[-1]
        price_position = self._calculate_price_position(data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                loc_config.get_text("channel_width"),
                f"{channel_width:.2f}%"
            )
        with col2:
            st.metric(
                loc_config.get_text("price_position"),
                price_position
            )
            
    def _calculate_custom_momentum(self, loc_config):
        st.subheader(loc_config.get_text("custom_momentum_title"))
        
        col1, col2 = st.columns(2)
        with col1:
            momentum_period = st.slider(
                loc_config.get_text("momentum_period"),
                min_value=5,
                max_value=50,
                value=14
            )
        with col2:
            smoothing_period = st.slider(
                loc_config.get_text("smoothing_period"),
                min_value=2,
                max_value=20,
                value=3
            )
            
        data = self.analyzer.data.copy()
        
        # Calculate custom momentum
        data['Momentum'] = self._calculate_momentum_indicator(
            data,
            momentum_period,
            smoothing_period
        )
        
        # Create visualization
        fig = make_subplots(rows=2, cols=1, shared_xaxis=True)
        
        # Price chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Momentum indicator
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Momentum'],
                name='Momentum',
                line=dict(color='orange')
            ),
            row=2, col=1
        )
        
        fig.update_layout(height=800)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display momentum signals
        momentum_signal = self._interpret_momentum(data)
        st.metric(
            loc_config.get_text("momentum_signal"),
            momentum_signal
        )
        
    def _calculate_momentum_indicator(self, data, period, smoothing):
        # Calculate rate of change
        roc = data['Close'].pct_change(period) * 100
        
        # Apply smoothing
        smooth_momentum = roc.rolling(window=smoothing).mean()
        return smooth_momentum
        
    def _interpret_momentum(self, data):
        current_momentum = data['Momentum'].iloc[-1]
        if current_momentum > 2:
            return "Strong Bullish"
        elif current_momentum > 0:
            return "Weak Bullish"
        elif current_momentum > -2:
            return "Weak Bearish"
        else:
            return "Strong Bearish"
            
    def _calculate_price_position(self, data):
        current_price = data['Close'].iloc[-1]
        upper_channel = data['Upper_Channel'].iloc[-1]
        lower_channel = data['Lower_Channel'].iloc[-1]
        middle_channel = data['Middle_Channel'].iloc[-1]
        
        if current_price > upper_channel:
            return "Above Channel"
        elif current_price < lower_channel:
            return "Below Channel"
        elif current_price > middle_channel:
            return "Upper Half"
        else:
            return "Lower Half"