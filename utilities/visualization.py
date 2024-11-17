import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartVisualizer:
    @staticmethod
    def create_candlestick_chart(data, symbol, indicators=None):
        fig = go.Figure()
        
        #candlestick base chart
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        ))
        
        #add indicators
        if indicators:
            for ind in indicators:
                if ind in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data[ind],
                        name=ind,
                        line=dict(width=1)
                    ))
        
        fig.update_layout(
            title=f'{symbol} Price Chart',
            yaxis_title='Price',
            template='plotly_white',
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_indicator_chart(data, indicator_name, **kwargs):
        fig = go.Figure()
        
        if indicator_name == 'RSI':
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['RSI'],
                name='RSI',
                line=dict(color='purple')
            ))
            #add  lines for sensetive levels
            fig.add_hline(y=70, line_dash="dash", line_color="red")
            fig.add_hline(y=30, line_dash="dash", line_color="green")
            
        elif indicator_name == 'MACD':
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MACD_12_26_9'],
                name='MACD'
            ))
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MACDs_12_26_9'],
                name='Signal'
            ))
            fig.add_trace(go.Bar(
                x=data.index,
                y=data['MACDh_12_26_9'],
                name='Histogram'
            ))
             
            
        fig.update_layout(
            title=f'{indicator_name} Chart',
            height=300,
            template='plotly_white'
        )
        
        return fig