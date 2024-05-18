import streamlit as st
from authentication import authenticate
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

# Buscar dados das ações
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Analisar os dados das ações
def analyze_stock(data):
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['Volatility'] = data['Close'].rolling(window=50).std() * (252 ** 0.5)
    return data

# Versão Matplotlib
def plot_matplotlib_stock_data(data):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(data.index, data['Close'], label='Preço de Fechamento', color='blue')
    ax.plot(data.index, data['MA50'], label='Média Móvel de 50 dias', color='red')
    ax.set_title('Evolução do Preço da Ação (Matplotlib)')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço (USD)')
    ax.legend()
    st.pyplot(fig)

# Versão Plotly
def plot_plotly_stock_data(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Preço de Fechamento', line=dict(color='blue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='Média Móvel de 50 dias', line=dict(color='red')), secondary_y=False)
    fig.update_layout(title='Evolução do Preço da Ação', xaxis_title='Data', yaxis_title='Preço', hovermode='x')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

# Home
def homepage():
    st.title('Fast Invest')
    st.markdown("""
    Bem-vindo ao Fast Invest, a plataforma que torna mais fácil do que nunca investir no mercado financeiro! 

    Você já imaginou ter acesso a análises detalhadas de ações e recomendações de investimento em apenas alguns cliques?
    
    Com o Fast Invest, isso é possível!

    Não importa se você é um investidor experiente ou está apenas começando sua jornada no mundo dos investimentos, o Fast Invest está aqui para ajudar você a tomar decisões informadas e obter sucesso financeiro.
    
    Comece a explorar nossos recursos hoje mesmo e descubra como podemos ajudá-lo(a) a alcançar seus objetivos de investimento!
    """)
    st.markdown('---')

# Página de login
def login_page():
    st.title('Página de Login')

    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Login'):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success('Login realizado com sucesso!')
        else:
            st.error('Usuário ou senha incorretos.')

# Filtros gráficos
def app_content():
    st.title('Fast Invest - Análise de Ações e Recomendações de Investimento')
    st.sidebar.header('Filtros')
    symbol_options = ['PETR4.SA']
    symbol = st.sidebar.selectbox('Selecione o símbolo da ação', symbol_options)
    start_date = st.sidebar.date_input('Selecione a data de início', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('Selecione a data de fim', pd.to_datetime('2024-01-01'))

    if st.sidebar.button('Analisar'):
        data = get_stock_data(symbol, start_date, end_date)
        analyzed_data = analyze_stock(data)
        st.write(analyzed_data)
        st.subheader('Versão Matplotlib:')
        plot_matplotlib_stock_data(analyzed_data)
        st.subheader('Versão Plotly:')
        plot_plotly_stock_data(analyzed_data)

# Menu de navegação
def navbar():
    #if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    #if st.session_state.authenticated:
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Gráficos"],
                icons=["house", "activity"],
                menu_icon="cast",
                default_index=0,
            )
        if selected == "Home":
            homepage()
        elif selected == "Gráficos":
            app_content()
    #else:
    #    login_page()

def main():
    navbar()

if __name__ == '__main__':
    main()
