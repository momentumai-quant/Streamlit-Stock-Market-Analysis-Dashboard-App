import streamlit as st
import pandas as pd
import plotly.graph_objects
from plotly.subplots import make_subplots
from utilities.stock_analyzer import StockAnalyzer
from utilities.visualization import ChartVisualizer

class TechnicalAnalysisPage:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        self.visualizer = ChartVisualizer()
        
    def show_page(self, loc_config):
        st.title(loc_config.get_text("technical_analysis_title"))
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            symbol = st.text_input(
                loc_config.get_text("symbol_input"),
                value="AAPL",
                help=loc_config.get_text("symbol_help")
            ).strip().upper()
            
        with col2:
            period = st.selectbox(
                loc_config.get_text("period_select"),
                options=['3mo','6mo','1y', '2y', '5y'],
                index=0
            )
        
        if st.button(loc_config.get_text("analyze_btn")):
            self._perform_analysis(symbol, period, loc_config)
            
    def _perform_analysis(self, symbol, period, loc_config):
        if not symbol:
            st.error(loc_config.get_text("symbol_input"))
            return
            
        with st.spinner(loc_config.get_text("analyzing_data")):
            try:
                if self.analyzer.fetch_data(symbol, period=period):
                    self._display_comprehensive_analysis(loc_config)
            except Exception as e:
                st.error(f"{loc_config.get_text('calculation_error')}: {str(e)}")
                
    def _display_comprehensive_analysis(self, loc_config):
        data = self.analyzer.data
        
        fig = make_subplots(
            rows=3, 
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2]
        )
        
        self._add_candlestick_plot(fig, data, 1, 1)
        self._add_volume_plot(fig, data, 2, 1)
        self._add_rsi_plot(fig, data, 3, 1)
        
        fig.update_layout(
            height=800,
            title_text=f"{self.analyzer.symbol} {loc_config.get_text('technical_analysis_title')}",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        self._display_technical_metrics(loc_config)
        
    def _add_candlestick_plot(self, fig, data, row, col):
        fig.add_trace(
            plotly.graph_objects.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=self.analyzer.symbol
            ),
            row=row, col=col
        )
        
        for ma in ['SMA_20', 'SMA_50', 'SMA_200']:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=data.index,
                    y=data[ma],
                    name=ma,
                    line=dict(width=1)
                ),
                row=row, col=col
            )
            
        bb_bands = ['BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0']
        for band in bb_bands:
            fig.add_trace(
                plotly.graph_objects.Scatter(
                    x=data.index,
                    y=data[band],
                    name=f'BB {band}',
                    line=dict(width=1, dash='dash')
                ),
                row=row, col=col
            )
            
    def _add_volume_plot(self, fig, data, row, col):
        fig.add_trace(
            plotly.graph_objects.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume'
            ),
            row=row, col=col
        )
        
    def _add_rsi_plot(self, fig, data, row, col):
        fig.add_trace(
            plotly.graph_objects.Scatter(
                x=data.index,
                y=data['RSI'],
                name='RSI'
            ),
            row=row, col=col
        )
        
        fig.add_hline(y=70, line_width=1, line_dash="dash", line_color="red", row=row, col=col)
        fig.add_hline(y=30, line_width=1, line_dash="dash", line_color="green", row=row, col=col)
        
    def _display_technical_metrics(self, loc_config):
        data = self.analyzer.data
        signals = self.analyzer.get_current_signals()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                loc_config.get_text("ma_trend"),
                signals['sma_cross']
            )
        
        with col2:
            st.metric(
                loc_config.get_text("rsi_title"),
                f"{data['RSI'].iloc[-1]:.1f}",
                signals['rsi']
            )
            
        with col3:
            st.metric(
                loc_config.get_text("macd_title"),
                signals['macd']
            )
            
        with col4:
            bb_position = "Middle"
            if data['Close'].iloc[-1] > data['BBU_5_2.0'].iloc[-1]:
                bb_position = "Above Upper"
            elif data['Close'].iloc[-1] < data['BBL_5_2.0'].iloc[-1]:
                bb_position = "Below Lower"
                
            st.metric(
                loc_config.get_text("bb_position"),
                bb_position
            )