from dataclasses import dataclass
from typing import Dict, Literal

@dataclass
class LocalizationConfig:
    def __init__(self, lang='en'):
        self.current_language: Literal['en', 'fa'] = lang
        self._translations = {
            #ui elements
            'dashboard_title': {
                'en': 'Advanced Stock Analysis Dashboard',
                'fa': 'داشبورد پیشرفته تحلیل سهام'
            },
            'nav_stock_info': {
                'en': 'Stock Information',
                'fa': 'اطلاعات سهام'
            },
            'nav_technical': {
                'en': 'Technical Analysis',
                'fa': 'تحلیل تکنیکال'
            },
            'nav_indicators': {
                'en': 'Custom Indicators',
                'fa': 'اندیکاتورهای سفارشی'
            },
            'language_selector': {
                'en': 'Switch Language',
                'fa': 'تغییر زبان'
            },
            
            #stock info page labels and titles
            'stock_info_title': {
                'en': 'Stock Information',
                'fa': 'اطلاعات سهام'
            },
            'symbol_input': {
                'en': 'Enter Stock Symbol',
                'fa': 'نماد سهام را وارد کنید'
            },
            'symbol_help': {
                'en': 'Enter the stock symbol (e.g., AAPL for Apple)',
                'fa': 'نماد سهام را وارد کنید (مثال: AAPL برای اپل)'
            },
            'period_select': {
                'en': 'Select Time Period',
                'fa': 'انتخاب بازه زمانی'
            },
            'interval_select': {
                'en': 'Select Interval',
                'fa': 'انتخاب فاصله زمانی'
            },
            'fetch_data_btn': {
                'en': 'Fetch Data',
                'fa': 'دریافت اطلاعات'
            },
            'loading_data': {
                'en': 'Loading data...',
                'fa': 'در حال بارگذاری اطلاعات...'
            },
            'company_info_expander': {
                'en': 'Company Information',
                'fa': 'اطلاعات شرکت'
            },
            'market_cap': {
                'en': 'Market Cap',
                'fa': 'ارزش بازار'
            },
            'pe_ratio': {
                'en': 'P/E Ratio',
                'fa': 'نسبت P/E'
            },
            'beta': {
                'en': 'Beta',
                'fa': 'بتا'
            },
            'dividend_yield': {
                'en': 'Dividend Yield',
                'fa': 'بازده سود سهام'
            },
            '52w_high': {
                'en': '52-Week High',
                'fa': 'سقف 52 هفته'
            },
            '52w_low': {
                'en': '52-Week Low',
                'fa': 'کف 52 هفته'
            },
            'business_summary': {
                'en': 'Business Summary',
                'fa': 'خلاصه کسب و کار'
            },
            
            #tech analysis page labels
            'technical_analysis_title': {
                'en': 'Technical Analysis',
                'fa': 'تحلیل تکنیکال'
            },
            'analyze_btn': {
                'en': 'Analyze',
                'fa': 'تحلیل'
            },
            'trend_analysis_tab': {
                'en': 'Trend Analysis',
                'fa': 'تحلیل روند'
            },
            'momentum_analysis_tab': {
                'en': 'Momentum Analysis',
                'fa': 'تحلیل مومنتوم'
            },
            'volatility_analysis_tab': {
                'en': 'Volatility Analysis',
                'fa': 'تحلیل نوسان'
            },
            'moving_averages_title': {
                'en': 'Moving Averages',
                'fa': 'میانگین‌های متحرک'
            },
            'select_ma_periods': {
                'en': 'Select Moving Averages',
                'fa': 'انتخاب میانگین‌های متحرک'
            },
            'trend_summary_title': {
                'en': 'Trend Summary',
                'fa': 'خلاصه روند'
            },
            'trend_strength': {
                'en': 'Trend Strength',
                'fa': 'قدرت روند'
            },
            'ma_trend': {
                'en': 'MA Trend',
                'fa': 'روند میانگین متحرک'
            },
            'price_trend': {
                'en': 'Price Trend',
                'fa': 'روند قیمت'
            },
            
          
            #messages
            'info_fetch_error': {
                'en': 'Error fetching stock information',
                'fa': 'خطا در دریافت اطلاعات سهام'
            },
            'calculation_error': {
                'en': 'Error in calculations',
                'fa': 'خطا در محاسبات'
            },
       
            'rsi_title': {
                'en': 'Relative Strength Index (RSI)',
                'fa': 'شاخص قدرت نسبی (RSI)'
            },
            'macd_title': {
                'en': 'MACD',
                'fa': 'واگرایی/همگرایی میانگین متحرک'
            },
            'bb_title': {
                'en': 'Bollinger Bands',
                'fa': 'باندهای بولینگر'
            },
            'atr_title': {
                'en': 'Average True Range',
                'fa': 'میانگین دامنه واقعی'
            },
            'momentum_summary_title': {
                'en': 'Momentum Summary',
                'fa': 'خلاصه مومنتوم'
            },
            'volatility_summary_title': {
                'en': 'Volatility Summary',
                'fa': 'خلاصه نوسانات'
            },
            'bb_position': {
                'en': 'Bollinger Band Position',
                'fa': 'موقعیت باند بولینگر'
            },
            'volatility_trend': {
                'en': 'Volatility Trend',
                'fa': 'روند نوسانات'
            }, 
            'analyzing_data': {
                'en': 'Analyzing data...',
                'fa': 'در حال تحلیل داده‌ها...'
            },
            'update_complete': {
                'en': 'Update complete',
                'fa': 'به‌روزرسانی کامل شد'
            },
            'no_data_available': {
                'en': 'No data available',
                'fa': 'داده‌ای موجود نیست'
            },
            
            
            #sginals and indicator related labels
            'signal_sma_cross': {
                'en': 'SMA Cross Signal',
                'fa': 'سیگنال تقاطع SMA'
            },
            'signal_rsi': {
                'en': 'RSI Signal',
                'fa': 'سیگنال RSI'
            },
            'signal_macd': {
                'en': 'MACD Signal',
                'fa': 'سیگنال MACD'
            },
            'price_chart_title': {
                'en': 'Price Chart',
                'fa': 'نمودار قیمت'
            },
            'select_indicators': {
                'en': 'Select Indicators',
                'fa': 'انتخاب شاخص‌ها'
            },
            'summary_metrics_title': {
                'en': 'Summary Metrics',
                'fa': 'خلاصه معیارها'
            },
            
            # advn analysis labels
            'divergence_analysis': {
                'en': 'Divergence Analysis',
                'fa': 'تحلیل واگرایی'
            },
            'support_resistance': {
                'en': 'Support & Resistance',
                'fa': 'حمایت و مقاومت'
            },
            'fibonacci_levels': {
                'en': 'Fibonacci Levels',
                'fa': 'سطوح فیبوناچی'
            },
            
            #charts releated labels
            'pattern_analysis': {
                'en': 'Chart Pattern Analysis',
                'fa': 'تحلیل الگوهای نموداری'
            },
            'detected_patterns': {
                'en': 'Detected Patterns',
                'fa': 'الگوهای شناسایی شده'
            },
             
            'volume_analysis': {
                'en': 'Volume Analysis',
                'fa': 'تحلیل حجم'
            },
            'volume_profile': {
                'en': 'Volume Profile',
                'fa': 'پروفایل حجم'
            },
             
         
            # timeframe  and time periods
            'period_1d': {
                'en': '1 Day',
                'fa': '1 روز'
            },
            'period_1w': {
                'en': '1 Week',
                'fa': '1 هفته'
            },
            'period_1m': {
                'en': '1 Month',
                'fa': '1 ماه'
            },
            'period_3m': {
                'en': '3 Months',
                'fa': '3 ماه'
            },
            'period_6m': {
                'en': '6 Months',
                'fa': '6 ماه'
            },
            'period_1y': {
                'en': '1 Year',
                'fa': '1 سال'
            },
            'period_2y': {
                'en': '2 Years',
                'fa': '2 سال'
            },
            'period_5y': {
                'en': '5 Years',
                'fa': '5 سال'
            }
        }
        
    def get_text(self, key: str) -> str: 
        return self._translations.get(key, {}).get(self.current_language, key)
    
    def switch_language(self): 
        self.current_language = 'fa' if self.current_language == 'en' else 'en'
        
    def get_current_language(self) -> str: 
        return self.current_language
    
    def is_rtl(self) -> bool: 
        return self.current_language == 'fa'