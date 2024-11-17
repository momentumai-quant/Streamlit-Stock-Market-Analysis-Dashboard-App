import warnings
warnings.filterwarnings('ignore')

import streamlit as st
from streamlit_option_menu import option_menu

from utilities.localization import LocalizationConfig
from pages.stock_info import StockInfoPage
from pages.technical_analysis import TechnicalAnalysisPage 

class StockAnalysisApp:
    def __init__(self):
        self.loc_config = LocalizationConfig()
        self.setup_page()
        
    def setup_page(self):
        st.set_page_config(
            page_title=self.loc_config.get_text("dashboard_title"),
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        self.hide_sidebar()
        
    def hide_sidebar(self):
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {visibility: hidden;}
                [data-testid="stSidebarCollapsedControl"] {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)
        
    def run(self):
        lang_btn = st.button(
            "🌐 " + self.loc_config.get_text('language_selector'), 
            key="lang_btn"
        )
        if lang_btn:
            st.switch_page("pages/persian_page.py")

        selected_page = option_menu(
            menu_title=None,
            options=[
                self.loc_config.get_text("nav_stock_info"),
                self.loc_config.get_text("nav_technical"), 
            ],
            icons=["info-circle", "graph-up", "tools"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        
        if selected_page == self.loc_config.get_text("nav_stock_info"):
            StockInfoPage().show_page(self.loc_config)
        elif selected_page == self.loc_config.get_text("nav_technical"):
            TechnicalAnalysisPage().show_page(self.loc_config)
    

app = StockAnalysisApp()
app.run()
