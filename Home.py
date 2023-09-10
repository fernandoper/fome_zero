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
import pydeck as pdk

# Libs necessárias
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title='Main Page',    
    layout= 'wide'
)

# rodar o streamlit no cmd: python -m streamlit run Home.py

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

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

df['Price_type'] = df['Price range'].map(create_price_type)

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

# Crie a coluna 'main_cuisine' pegando apenas o primeiro valor (até a primeira vírgula) da coluna 'cuisines'
df['main_cuisine'] = df['cuisines'].str.split(',').str[0]

# ====================================================================
# MAP FUNCTION
# ====================================================================

def display_map(df):

# Mapa inicial
    m = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)
    
    # Mapeamento de cores
    colors = {
        "cheap": "lightgreen",
        "normal": "blue",
        "expensive": "orange",
        "gourmet": "darkred"
    }

    for _, row in df.iterrows():
        popup_content = f"""
        <div style="width:250px;">
            <strong>{row['restaurant_name']}</strong><br>
            Price: {row['average_cost_for_two']} ({row['currency']}) for two<br>
            Type: {row['main_cuisine']}<br>
            Rating: {row['aggregate_rating']}/5.0<br>
            Price Type: {row['price_type']}
        </div>
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_content,
            icon=folium.Icon(color=colors.get(row['price_type'], "blue"), icon='home', prefix='glyphicon')
        ).add_to(marker_cluster)
 
    # Controlando a exibição do mapa (centralizado)
    col1, col2, col3 = st.columns([1,2,1])  # Ajustando a proporção das colunas
    with col2:
        folium_static(m)
        
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

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 14px">
        Peça, Saboreie, Transforme: Juntos por um mundo sem fome!
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
# SIDEBAR CUISINE TYPE - MAP
# ====================================================================

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 16px">
        Select the price type you want to filter
    </div>
""", unsafe_allow_html=True)

# Price type list
price_type_list = df['price_type'].unique().tolist()

# Multiple price types selection
price_types_options = st.sidebar.multiselect(
    'Select price types',
    price_type_list, default=['cheap', 'normal', 'expensive', 'gourmet'])

# Cuisine filter
selected_price_types = df['price_type'].isin(price_types_options)
df = df.loc[selected_price_types, :]


# ====================================================================
# PAGE CONTENT
# ====================================================================

(st.markdown('<div style="text-align: center"><h1>Fome Zero</h1></div>',
            unsafe_allow_html=True))
(st.markdown('<div style="text-align: center;font-size: 1.5em;">The best place to find your newest favorite restaurant!</div>',
            unsafe_allow_html=True))

# CHART 1: Platforms Metrics
with st.container():
    
    st.markdown('### Platform Metrics')
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
            unique_restaurants = df.loc[:, 'restaurant_name'].nunique()
            col1.metric('Number os Restaurants', unique_restaurants)

    with col2:
            country_number = df.loc[:, 'country'].nunique()
            col2.metric('Number of Countries', country_number)

    with col3:
            cities_number = df.loc[:, 'city'].nunique()
            col3.metric('Number of Cities', cities_number)

    with col4:
            votes_number = df.loc[:, 'votes'].sum()
            formatted_votes = "{:,}".format(votes_number)
            col4.metric('Number of Votes', formatted_votes)

    with col5:
            cuisine_number = df.loc[:, 'main_cuisine'].nunique()
            col5.metric('Number of Cuisines', cuisine_number)

# CHART2: Map
with st.container():
    
    display_map(df)

#### Streamlist detecta a pasta "pages" e coloca dentro #####