import streamlit as st
import yfinance as yf
from utilities.stock_analyzer import StockAnalyzer
from utilities.visualization import ChartVisualizer
from utilities.pages_utilities import *

class StockInfoPage:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        self.visualizer = ChartVisualizer()
        
    def show_page(self, loc_config):
        st.title(loc_config.get_text("stock_info_title"))
        
        st.success("Please enter a symbol name : AAPL , BTC-USD , or other yahoo finance symbols")
        # symbols input
        symbol = st.text_input(
            loc_config.get_text("symbol_input"),
            value="AAPL",
            help=loc_config.get_text("symbol_help")
        )
        
        col1, col2 = st.columns(2)
        with col1:
            period = st.selectbox(
                loc_config.get_text("period_select"),
                options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
                index=3
            )
        
        with col2:
            interval = st.selectbox(
                loc_config.get_text("interval_select"),
                options=['1d' ],
                index=0
            )
            
        if st.button(loc_config.get_text("fetch_data_btn")):
            with st.spinner(loc_config.get_text("loading_data")):
                if self.analyzer.fetch_data(symbol, period=period):
                    self._display_stock_info(symbol, loc_config)
                    self._display_price_chart(symbol, loc_config)
                    self._display_summary_metrics(loc_config)
                    
    def _display_stock_info(self, symbol, loc_config):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            with st.expander(loc_config.get_text("company_info_expander"), expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        loc_config.get_text("market_cap"),
                        f"${info.get('marketCap', 'N/A'):,}"
                    )
                    st.metric(
                        loc_config.get_text("pe_ratio"),
                        round(info.get('trailingPE', 0), 2)
                    )
                
                with col2:
                    st.metric(
                        loc_config.get_text("beta"),
                        round(info.get('beta', 0), 2)
                    )
                    st.metric(
                        loc_config.get_text("dividend_yield"),
                        f"{info.get('dividendYield', 0)*100:.2f}%"
                    )
                
                with col3:
                    st.metric(
                        loc_config.get_text("52w_high"),
                        f"${info.get('fiftyTwoWeekHigh', 0):.2f}"
                    )
                    st.metric(
                        loc_config.get_text("52w_low"),
                        f"${info.get('fiftyTwoWeekLow', 0):.2f}"
                    )
                
                st.markdown(f"**{loc_config.get_text('business_summary')}**")
                st.write(info.get('longBusinessSummary', 'N/A'))
        
        except Exception as e:
            st.error(loc_config.get_text("info_fetch_error"))
            
    def _display_price_chart(self, symbol, loc_config):
        data = self.analyzer.data
        if data is not None:
            st.subheader(loc_config.get_text("price_chart_title")) 
            indicators=['SMA_20', 'SMA_50', 'EMA_20', 'BB_UPPER', 'BB_LOWER']
            fig = self.visualizer.create_candlestick_chart(data, symbol, indicators)
            st.plotly_chart(fig, use_container_width=True)
            
    def _display_summary_metrics(self, loc_config):
        data = self.analyzer.data
        if data is not None:
            st.subheader(loc_config.get_text("summary_metrics_title"))
            
            signals = self.analyzer.get_current_signals()
            
            cols = st.columns(len(signals))
            for col, (signal_name, value) in zip(cols, signals.items()):
                col.metric(
                    loc_config.get_text(f"signal_{signal_name}"),
                    value,
                    delta=None,
                    delta_color="normal"
                )