# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import re
import datetime as dt
from PIL import Image
import inflection
import io
import base64

# Libs necessárias
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title= 'Cities', page_icon='🌇', layout= 'wide')

# ====================================================================
# FUNCTIONS
# ====================================================================

def clean_code(df):
    """
    FUNÇÃO DE DATA CLEANSING:  
    1. EXCLUSÃO LINHAS NAN
   
    INPUT: DATAFRAME
    OUTPUT: DATAFRAME
    """
    # Substituir 'Nan ' por np.nan usando lambda
    df = df.applymap(lambda x: np.nan if x == 'Nan ' else x)

    # Excluir linhas contendo np.nan
    df.dropna(inplace=True)
    return df

# ====================================================================
# FUNCTION 1 - Top 10 cities with the most registered restaurants
# ====================================================================

def top_cities(df):
    df_aux = (df.loc[:,['city','restaurant_id','country']].groupby(['city','country'])
                                                .nunique()                                                
                                                .reset_index()
                                                .sort_values('restaurant_id', ascending = False)
                                                .head(10))
    
    df_aux.columns = ['Cities','Country','Number of Restaurants']

    fig = px.bar(df_aux,
                 x='Cities',
                 y='Number of Restaurants',
                 title='Top 10 Cities with the Most Registered Restaurants',
                 labels={'Cities': 'Number of Restaurants'},
                 color='Country',  # Adiciona uma escala de cor com base na quantidade
                 color_continuous_scale='Blues',  # Define uma paleta de cor azul
                 hover_name='Cities',  # Mostra o nome do país no hover
                 hover_data={'Country': True, 
                             'Number of Restaurants': ':,.2f'}  # Mostra o nome do país e a quantidade no hover
                 )
    
#Layout apenas para colocar o título no centro
    fig.update_layout( 
        title={
            'text': "Top 10 Cities with the Most Registered Restaurants", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
# Estiliza as barras
    fig.update_traces(marker_line_color='black',  # Contornos das barras
                      marker_line_width=1,
                      opacity=0.6)  # Transparência das barras
    
# Adiciona números em cima das barras
    fig.add_trace(go.Scatter(
        x=df_aux['Cities'],
        y=df_aux['Number of Restaurants'],
        text=df_aux['Number of Restaurants'],
        mode='text',  # Modo somente texto (sem linhas ou pontos)
        textposition='top center',  # Posição do texto
        showlegend=False  # Esconde o traço no legend
    ))

    # Atualiza o layout
    fig.update_layout(xaxis_title='Cities',
                      yaxis_title='Number of Restaurants',
                      xaxis={'categoryorder':'total descending'})    #ordenar as barras de forma decrescente
    
    return fig

# ====================================================================
# FUNCTION 2 - Top 7 Cities with Restaurants that have an Average Score Above 4
# ====================================================================
 
def avg_high_score(df):
    filtered_df = df[df['aggregate_rating'] > 4]
    df_aux = (filtered_df.groupby(['city', 'country'])['restaurant_id']
                      .nunique()
                      .reset_index()
                      .sort_values('restaurant_id', ascending=False)
                      .head(7))
    df_aux.columns = ['Cities','Country','Number of Restaurants']
        
    fig = px.bar(df_aux,
                 x='Cities',
                 y='Number of Restaurants',
                 title="Top 7 Cities with Restaurant's Score Above 4",
                 labels={'Cities': 'Number of Restaurants'},
                 color='Country',  # Adiciona uma escala de cor com base na quantidade
                 color_continuous_scale='Blues',  # Define uma paleta de cor azul
                 hover_name='Cities',  # Mostra o nome do país no hover
                 hover_data={'Country': True, 
                             'Number of Restaurants': ':,.2f'}  # Mostra o nome do país e a quantidade no hover
                 )
    
#Layout apenas para colocar o título no centro
    fig.update_layout( 
        title={
            'text': "Top 7 Cities with Restaurant's Score Above 4", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
# Estiliza as barras
    fig.update_traces(marker_line_color='black',  # Contornos das barras
                      marker_line_width=1,
                      opacity=0.6)  # Transparência das barras
    
# Adiciona números em cima das barras
    fig.add_trace(go.Scatter(
        x=df_aux['Cities'],
        y=df_aux['Number of Restaurants'],
        text=df_aux['Number of Restaurants'],
        mode='text',  # Modo somente texto (sem linhas ou pontos)
        textposition='top center',  # Posição do texto
        showlegend=False  # Esconde o traço no legend
    ))

    # Atualiza o layout
    fig.update_layout(xaxis_title='Cities',
                      yaxis_title='Number of Restaurants',
                      xaxis={'categoryorder':'total descending'})    #ordenar as barras de forma decrescente
    
    return fig

# ====================================================================
# FUNCTION 3 - Top 7 Cities with Restaurants that have an Average Score Under 2.5
# ====================================================================
 
def avg_low_score(df):
    filtered_df = df[df['aggregate_rating'] < 2.5]
    df_aux = (filtered_df.groupby(['city', 'country'])['restaurant_id']
                      .nunique()
                      .reset_index()
                      .sort_values('restaurant_id', ascending=False)
                      .head(7))
    df_aux.columns = ['Cities','Country','Number of Restaurants']
        
    fig = px.bar(df_aux,
                 x='Cities',
                 y='Number of Restaurants',
                 title="Top 7 Cities with Restaurant's Score Under 2.5",
                 labels={'Cities': 'Number of Restaurants'},
                 color='Country',  # Adiciona uma escala de cor com base na quantidade
                 color_continuous_scale='Blues',  # Define uma paleta de cor azul
                 hover_name='Cities',  # Mostra o nome do país no hover
                 hover_data={'Country': True, 
                             'Number of Restaurants': ':,.2f'}  # Mostra o nome do país e a quantidade no hover
                 )
    
#Layout apenas para colocar o título no centro
    fig.update_layout( 
        title={
            'text': "Top 7 Cities with Restaurant's Score Under 2.5", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
# Estiliza as barras
    fig.update_traces(marker_line_color='black',  # Contornos das barras
                      marker_line_width=1,
                      opacity=0.6)  # Transparência das barras
    
# Adiciona números em cima das barras
    fig.add_trace(go.Scatter(
        x=df_aux['Cities'],
        y=df_aux['Number of Restaurants'],
        text=df_aux['Number of Restaurants'],
        mode='text',  # Modo somente texto (sem linhas ou pontos)
        textposition='top center',  # Posição do texto
        showlegend=False  # Esconde o traço no legend
    ))

    # Atualiza o layout
    fig.update_layout(xaxis_title='Cities',
                      yaxis_title='Number of Restaurants',
                      xaxis={'categoryorder':'total descending'})    #ordenar as barras de forma decrescente
    
    return fig

# ====================================================================
# FUNCTION 4 - Top 10 Cities with Most Distinct Cuisines
# ====================================================================
 
def distinct_cuisines(df):
    df_aux = (round(df.loc[:,['city','country','cuisines']]
                    .groupby(['city','country'])
                    .nunique()
                    .sort_values('cuisines', ascending = False)
                    .reset_index()
                    .head(10),2))

    df_aux.columns = ['Cities','Country','Number of Cuisines']
    
    fig = px.bar(df_aux,
                 x='Cities',
                 y='Number of Cuisines',
                 title='Top 10 Cities with Most Distinct Cuisines',
                 labels={'Cities': 'Number of Cuisines'},
                 color='Country',  # Adiciona uma escala de cor com base na quantidade
                 color_continuous_scale='Blues',  # Define uma paleta de cor azul
                 hover_name='Country',  # Mostra o nome do país no hover
                 hover_data={'Cities': True, 'Number of Cuisines': False}  # Mostra a quantidade no hover
                 )
    
#Layout apenas para colocar o título no centro
    fig.update_layout( 
        title={
            'text': "Top 10 Cities with Most Distinct Cuisines", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
# Estiliza as barras
    fig.update_traces(marker_line_color='black',  # Contornos das barras
                      marker_line_width=1,
                      opacity=0.6)  # Transparência das barras
    
# Adiciona números em cima das barras
    fig.add_trace(go.Scatter(
        x=df_aux['Cities'],
        y=df_aux['Number of Cuisines'],
        text=df_aux['Number of Cuisines'],
        mode='text',  # Modo somente texto (sem linhas ou pontos)
        textposition='top center',  # Posição do texto
        showlegend=False  # Esconde o traço no legend
    ))

    # Atualiza o layout
    fig.update_layout(xaxis_title='Cities',
                    yaxis_title='Number of Cuisines',
                    xaxis={'categoryorder':'total descending'})    #ordenar as barras de forma decrescente

    return fig

# ====================================================================
# IMPORT DATASET
# ====================================================================
df = pd.read_csv("dataset/zomato.csv")

# rodar o streamlit no cmd: python -m streamlit run cities.py
# identar automaticamente: shift + alt + L

# ====================================================================
# DATA CLEANSING
# ====================================================================
df = clean_code(df)

# ====================================================================
# MODELAGEM DATASET
# ====================================================================

# Nome dos países e coluna
countries = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return countries[country_id]

# Criando uma coluna com base no country code
df['Country'] = df['Country Code'].map(country_name)

# Tipo de Categoria de Comida e Coluna

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

df['Price_type'] = df['Price range'].map(create_price_tye)

# Nome das cores

colors = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return colors[color_code]

# Renomear as colunas do df

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

df = rename_columns(df)

#Remoção valor Outlier
index_max = df['average_cost_for_two'].idxmax()
print(df.loc[index_max])
df.drop(index_max, inplace=True)

#Conversão de valores para Dólar:

exchange_rates = {
    'Dollar($)': 1,
    'Brazilian Real(R$)': 4.95,
    'Indonesian Rupiah(IDR)': 14300,
    'Sri Lankan Rupee(LKR)': 200,
    'Botswana Pula(P)': 11,
    'Indian Rupees(Rs.)': 75,
    'Rand(R)': 15,
    'Qatari Rial(QR)': 3.64,
    'Emirati Diram(AED)': 3.67,
    'Turkish Lira(TL)': 8.5,
    'Pounds(£)': 0.73,
    'NewZealand($)': 1.4
}

# Convertendo os valores
df['avg_cost_for_two_dol'] = df.apply(lambda row: row['average_cost_for_two'] / exchange_rates[row['currency']], axis=1)

# Arredondando os valores para 2 casas decimais
df['avg_cost_for_two_dol'] = df['avg_cost_for_two_dol'].round(2)

# ====================================================================
# LAYOUT SIDEBAR
# ====================================================================

# ====================================================================
# SIDEBAR LOGO
# ====================================================================

# Carregar a imagem
img = plt.imread('images/cuisine_logo.png')

# Converter a imagem para bytes
buf = io.BytesIO()
Image.fromarray((img * 255).astype('uint8')).save(buf, format='png')

# Codificar a imagem em base64
encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')

# Centralizar a imagem na barra lateral usando HTML/CSS
st.sidebar.markdown("""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{}" width="60"/>
    </div>
""".format(encoded_img), unsafe_allow_html=True)

# ====================================================================
# SIDEBAR TITLES
# ====================================================================

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 18px">
        Fome Zero
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown(""" ___ """)

# ====================================================================
# SIDEBAR COUNTRY FILTER
# ====================================================================

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 16px">
        Select the countries you want to filter
    </div>
""", unsafe_allow_html=True)

# Countries list
countries = df['country'].unique().tolist()

# Multiple country selection
country_options = st.sidebar.multiselect(
    "Select the countries",
    countries, default= 'Brazil')

# Countries filter
selected_countries = df['country'].isin(country_options)
df = df.loc[selected_countries, :]

# ====================================================================
# SIDEBAR BOTTOM TEXT
# ====================================================================

st.sidebar.markdown(""" ___ """)

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 16px">
        Powered by Comunidade DS
    </div>
""", unsafe_allow_html=True)

# ====================================================================
# CITIES PAGE HEADER
# ====================================================================

# Defina as colunas
col1, col2 = st.columns([1,20])  # Ajuste os números para alterar a proporção de largura entre colunas
# Na primeira coluna, adicione a imagem
col1.image('images/city_logo.png', use_column_width=True)
# Na segunda coluna, adicione o header
col2.header('Cities Analytics')

# ====================================================================
# GRAPHS
# ====================================================================

with st.container():
        # CHART1: Top 10 cities with the most registered restaurants
        fig = top_cities(df)        
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # CHART2: Top 7 Cities with Restaurants that have an Average Score Above 4
        fig = avg_high_score(df)        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # CHART3: average cost for two people per country
        fig = avg_low_score(df)
        st.plotly_chart(fig, use_container_width=True)
        
with st.container():
        #CHART4: Registered Cities by Country
        fig = distinct_cuisines(df)        
        st.plotly_chart(fig, use_container_width=True)        