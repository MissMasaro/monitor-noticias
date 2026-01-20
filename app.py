import streamlit as st
import feedparser
import urllib.request

st.set_page_config(page_title="Monitor Logístico", page_icon="⚓", layout="wide")

st.markdown("# ⚓ Monitor de Noticias Estratégicas")
st.write("Actualización en tiempo real para logística y conflictos.")

paises = ["Irán", "Libia", "Marruecos", "Túnez", "Francia"]
# Filtro optimizado: busca una cosa O la otra
temas = "(puertos OR logística OR conflicto OR economía OR transporte)"

def buscar_noticias(pais):
    # Usamos comillas para asegurar que el país sea el centro de la búsqueda
    query = f'"{pais}" {temas}'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
