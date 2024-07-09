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

# Função para criar gráficos com Matplotlib
def plot_matplotlib_graph(data, title, ylabel, xlabel='Data'):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Preço de Fechamento', color='blue')
    ax.plot(data.index, data['MA50'], label='Média Móvel de 50 dias', color='red')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    st.pyplot(fig)

# Função para criar gráficos com Plotly
def plot_plotly_graph(data, title, ylabel, xlabel='Data'):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Preço de Fechamento', line=dict(color='blue')), secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='Média Móvel de 50 dias', line=dict(color='red')), secondary_y=False)
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel, hovermode='x')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

# Histograma do Preço de Fechamento
def plot_histogram(data):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.hist(data['Close'], bins=50, color='blue', alpha=0.7)
    ax.set_title('Histograma do Preço de Fechamento')
    ax.set_xlabel('Preço (USD)')
    ax.set_ylabel('Frequência')
    st.pyplot(fig)

# Box Plot do Preço de Fechamento
def plot_boxplot(data):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.boxplot(data['Close'], vert=False)
    ax.set_title('Box Plot do Preço de Fechamento')
    ax.set_xlabel('Preço (USD)')
    st.pyplot(fig)

# Gráfico de Dispersão do Volume de Negociações
def plot_scatter_volume(data):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.scatter(data.index, data['Volume'], alpha=0.5, color='blue')
    ax.set_title('Gráfico de Dispersão do Volume de Negociações')
    ax.set_xlabel('Data')
    ax.set_ylabel('Volume')
    st.pyplot(fig)

# Home
def homepage():
    st.title('Fast Invest 📈')
        
    st.markdown("""
    ## Bem-vindo ao Fast Invest!
    **A plataforma que torna mais fácil do que nunca investir no mercado financeiro!**

    ### O que oferecemos:
    - **Análises detalhadas de ações**
    - **Recomendações personalizadas de investimento**
    - **Ferramentas interativas para acompanhar seu portfólio**

    ### Funcionalidades principais:
    - Acompanhe a evolução das suas ações favoritas
    - Descubra novas oportunidades de investimento
    - Utilize gráficos avançados para análises técnicas

    ### Por que escolher o Fast Invest?
    "O sucesso financeiro não é um destino, é uma jornada. E nós estamos aqui para guiá-lo em cada passo." 
    ### Estatísticas:
    - Mais de **10,000** usuários satisfeitos
    - Mais de **1,000** análises de ações realizadas
    - Mais de **500** recomendações de investimento personalizadas
    
    ---
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Segurança 🔒</h3>", unsafe_allow_html=True)
        st.write("Seu investimento protegido com a melhor tecnologia de segurança.")
    
    with col2:
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Confiabilidade 🤝🏻</h3>", unsafe_allow_html=True)
        st.write("Transparência e integridade em todas as nossas recomendações.")
    
    with col3:
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Facilidade ✅</h3>", unsafe_allow_html=True)
        st.write("Interface intuitiva e fácil de usar para todos os tipos de investidores.")
    
    st.markdown("---")
    
    st.write("""
    **Comece a explorar nossos recursos hoje mesmo e descubra como podemos ajudá-lo(a) a alcançar seus objetivos de investimento!**
    """)

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
    st.title('Análise de Ações e Recomendações de Investimento:')
    st.sidebar.header('Filtros')
    symbol_options = ['PETR4.SA']
    symbol = st.sidebar.selectbox('Selecione o símbolo da ação', symbol_options)
    start_date = st.sidebar.date_input('Selecione a data de início', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('Selecione a data de fim', pd.to_datetime('2024-01-01'))

    if st.sidebar.button('Analisar'):
        data = get_stock_data(symbol, start_date, end_date)
        analyzed_data = analyze_stock(data)
        st.write(analyzed_data)
        
        st.subheader('1. Evolução do Preço da Ação (Matplotlib):')
        plot_matplotlib_graph(analyzed_data, 'Evolução do Preço da Ação (Matplotlib)', 'Preço (USD)')
        
        st.subheader('2. Evolução do Preço da Ação (Plotly):')
        plot_plotly_graph(analyzed_data, 'Evolução do Preço da Ação (Plotly)', 'Preço (USD)')
        
        st.subheader('3. Histograma do Preço de Fechamento:')
        plot_histogram(analyzed_data)
        
        st.subheader('4. Box Plot do Preço de Fechamento:')
        plot_boxplot(analyzed_data)
        
        st.subheader('5. Gráfico de Dispersão do Volume de Negociações:')
        plot_scatter_volume(analyzed_data)

# Menu de navegação
def navbar():
    st.session_state.authenticated = False

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Gráficos"],
            icons=["house", "activity"],
            menu_icon="cast",
            default_index=0,
        )
        if selected == "Home":
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.image('logo_fast.png', width=200) 

    if selected == "Home":
        homepage()
    elif selected == "Gráficos":
        app_content()


def main():
    navbar()

if __name__ == '__main__':
    main()
