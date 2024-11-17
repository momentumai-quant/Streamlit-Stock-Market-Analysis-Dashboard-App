import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta
 

def apply_rtl_styles(self, loc_config): 
    if loc_config.is_rtl():
        st.markdown(
            """
            <style>
                .element-container {
                    direction: rtl;
                }
                .stTextInput input {
                    direction: ltr;
                }
                .stSelectbox select {
                    direction: ltr;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

def format_number(self, value, precision=2): 
    try:
        return f"{value:,.{precision}f}"
    except:
        return "N/A"
 