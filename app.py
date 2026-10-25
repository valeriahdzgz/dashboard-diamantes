import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Diamantes", page_icon="💎", layout="wide")

st.title(" Dashboard Interactivo - Mercado de Diamantes")
st.markdown("Exploración de datos, filtros dinámicos y visualizaciones para la toma de decisiones.")

@st.cache_data
def load_data():
    return sns.load_dataset("diamonds")

df = load_data()

# Panel de filtros
st.sidebar.header(" Panel de Filtros Dinámicos")
min_price, max_price = int(df['price'].min()), int(df['price'].max())
selected_price = st.sidebar.slider("Selecciona el Rango de Precio (USD)", min_price, max_price, (min_price, 5000))

cuts = df['cut'].unique().tolist()
selected_cuts = st.sidebar.multiselect("Calidad de Corte (Cut)", cuts, default=cuts[:3])

filtered_df = df[
    (df['price'] >= selected_price[0]) & 
    (df['price'] <= selected_price[1]) & 
    (df['cut'].isin(selected_cuts))
]

# Métricas Clave (KPIs)
st.subheader("Métricas Clave del Negocio")
col1, col2, col3 = st.columns(3)
col1.metric("Registros Filtrados", f"{len(filtered_df):,}")
col2.metric("Precio Promedio", f"${filtered_df['price'].mean():,.2f}")
col3.metric("Peso Promedio (Carat)", f"{filtered_df['carat'].mean():.2f} ct")

st.markdown("---")

# Visualizaciones Interactivas
st.subheader(" Visualizaciones Interactivas")
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("### Figura 3.2a: Dispersión Precio vs Quilates")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='carat', y='price', hue='cut', alpha=0.5, palette='viridis', ax=ax)
    ax.set_title("Relación Carat vs Price")
    st.pyplot(fig)

with col_g2:
    st.markdown("### Figura 3.2b: Matriz de Correlación")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    numeric_cols = ['price', 'carat', 'depth', 'table', 'x']
    corr = filtered_df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax2, annot_kws={"size": 8})
    ax2.set_title("Matriz de Correlación Numérica")
    st.pyplot(fig2)
