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

st.set_page_config( page_title= 'Cuisines', page_icon='🥗', layout= 'wide')

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
# FUNCTION 1 - Best Restaurants by Cuisine
# ====================================================================

def display_restaurant_metric(col, dataframe, index):
    """Display a restaurant's metric in a given Streamlit column using markdown with styled rating and centered content."""
    row = dataframe.iloc[index]
    title = f"<span style='font-size:0.8em;'>{row['main_cuisine']} : {row['restaurant_name']}</span>"
    location = f"<span style='font-size:0.8em;'>{row['city']}, {row['country']}</span>"
    value = f"<span style='font-size:2em;'>{row['aggregate_rating']} / 5.0</span>"
    
    metric_content = f"""
    <div style="text-align: center;">
        <strong>{title}</strong><br>
        {location}<br>
        {value}
    </div>
    """
    col.markdown(metric_content, unsafe_allow_html=True)

# ====================================================================
# FUNCTION 2 - Top 20 Restaurants
# ====================================================================
 
def top_restaurants(df, n_results=10): # Adicione n_results como um argumento padrão
    # Inserindo o título centralizado e em fonte grande
    st.markdown(f'<div style="text-align: center; font-size: 2em; margin-bottom: 20px;">Top {n_results} Restaurants</div>', unsafe_allow_html=True)
    
    # Usando colunas para centralizar a tabela
    col1, col2, col3 = st.columns((1,4,1))  # Ajuste os números para alterar a largura relativa das colunas
    
    with col2:
        rating = (df.loc[:, ['restaurant_id', 'restaurant_name','country','city','cuisines','average_cost_for_two', 'aggregate_rating','votes']]
                  .sort_values('aggregate_rating', ascending = False)
                  .reset_index()
                  .head(n_results))
        st.dataframe(rating)

# ====================================================================
# FUNCTION 3 - Top 20 Best Cuisines
# ====================================================================
 
def best_cuisines(df, n_results=10):
    df_aux = (round(df.groupby('main_cuisine')
          .aggregate_rating.mean() 
          .reset_index()
          .sort_values('aggregate_rating', ascending=False)
          .head(n_results),2))
    df_aux.columns = ['Cuisines','Average Rating']

    fig = px.bar(df_aux,
                 x='Cuisines',
                 y='Average Rating',
                 title="Top 20 Best Cuisines",               
                 color_continuous_scale='Blues',
                 hover_name='Cuisines',
                 hover_data={'Cuisines': True,                             
                             'Average Rating': ':,.2f'}
                 )
    
    fig.update_layout(
        title={
            'text': f"Top {n_results} Best Cuisines", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }        
    )
    
    fig.update_traces(marker_line_color='black',
                      marker_line_width=1,
                      opacity=0.8,
                      text=df_aux['Average Rating'],
                      textposition='inside')
    
    fig.update_layout(xaxis_title='Cuisines',
                      yaxis_title='Average Rating',
                      xaxis={'categoryorder':'total descending'})
    
    return fig

# ====================================================================
# FUNCTION 4 - Top 20 Worst Cuisines
# ====================================================================
 
def worst_cuisines(df, n_results=10):
    df_aux = (df.groupby('main_cuisine')
          .aggregate_rating.mean() 
          .reset_index()
          .query('aggregate_rating > 0')  # Filtra as entradas com aggregate_rating maior que 0
          .sort_values('aggregate_rating', ascending=True)
          .head(n_results))

    df_aux['aggregate_rating'] = df_aux['aggregate_rating'].round(2)  # Arredonda os valores após todos os cálculos
    df_aux.columns = ['Cuisines','Average Rating']

    fig = px.bar(df_aux,
                 x='Cuisines',
                 y='Average Rating',
                 title="Top 20 Worst Cuisines",               
                 color_continuous_scale='Blues',
                 hover_name='Cuisines',
                 hover_data={'Cuisines': True,                             
                             'Average Rating': ':,.2f'}
                 )
    
    fig.update_layout(
        title={
            'text': f"Top {n_results} Worst Cuisines", 
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }        
    )
    
    fig.update_traces(marker_line_color='black',
                      marker_line_width=1,
                      opacity=0.8,
                      text=df_aux['Average Rating'],
                      textposition='inside')
    
    fig.update_layout(xaxis_title='Cuisines',
                      yaxis_title='Average Rating',
                      xaxis={'categoryorder':'total ascending'})
    
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

# Crie a coluna 'main_cuisine' pegando apenas o primeiro valor (até a primeira vírgula) da coluna 'cuisines'
df['main_cuisine'] = df['cuisines'].str.split(',').str[0]  

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
# SLIDER RESTAURANTS FILTER
# ====================================================================

# Adicione um slider na barra lateral
number_of_results = st.sidebar.slider('Select number of results', min_value=1, max_value=20, value=10)

# ====================================================================
# SIDEBAR CUISINE FILTER
# ====================================================================

st.sidebar.markdown("""
    <div style="text-align: center; font-weight: bold; font-size: 16px">
        Select the cuisines you want to filter 
    </div>
""", unsafe_allow_html=True)

# Cuisine's List
unique_cuisines = df['main_cuisine'].unique().tolist()

# Multiple cuisine selection
cuisine_options = st.sidebar.multiselect(
    "Select the cuisines",
    unique_cuisines, 
    default=['Italian', 'American']
)

# Filtro Countries
selected_cuisines = df['main_cuisine'].isin(cuisine_options)
df = df.loc[selected_cuisines, :]

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
col1.image('images/cuisines.logo.png', use_column_width=True)
# Na segunda coluna, adicione o header
col2.header('Cuisines Analytics')

# ====================================================================
# GRAPHS
# ====================================================================

with st.container():
    
    # Inserindo o título centralizado, em fonte grande, e com espaço abaixo
    st.markdown('<div style="text-align: center; font-size: 2em; margin-bottom: 20px;">Best Restaurants by Cuisine</div>', unsafe_allow_html=True)
    
    # CHART 1: Best Restaurants by Cuisine
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Ordenando o dataframe pelos melhores ratings e pegando os top 5
    sorted_df = (df[['restaurant_name', 'main_cuisine', 'city', 'country', 'average_cost_for_two', 
                    'currency', 'aggregate_rating']]
                    .sort_values('aggregate_rating', ascending=False).head(5))

    # Exibindo os cinco melhores restaurantes usando a função
    display_restaurant_metric(col1, sorted_df, 0)
    display_restaurant_metric(col2, sorted_df, 1)
    display_restaurant_metric(col3, sorted_df, 2)
    display_restaurant_metric(col4, sorted_df, 3)
    display_restaurant_metric(col5, sorted_df, 4)
    
    # Criando espaço entre este container e o próximo
    st.markdown('\n\n\n\n', unsafe_allow_html=True)

with st.container():
        # CHART2: Top 20 Restaurants
        top_restaurants(df,number_of_results)

with st.container():
    col1, col2 = st.columns(2)
        
    with col1:
        # CHART1: Top 20 Best Cuisines
        fig = best_cuisines(df,number_of_results)        
        st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        # CHART1: Top 20 Worst Cuisines
        fig = worst_cuisines(df,number_of_results)        
        st.plotly_chart(fig, use_container_width=True)
       