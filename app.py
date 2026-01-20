import streamlit as st
import feedparser
import urllib.request

# 1. Configuración básica
st.set_page_config(page_title="Monitor", layout="wide")
st.title("⚓ Monitor de Noticias")

paises = ["Irán", "Libia", "Marruecos", "Túnez", "Francia"]

# 2. Función de búsqueda ultra-simple
def buscar(pais):
    # Buscamos noticias generales del país para asegurar que salga ALGO
    url = f"https://news.google.com/rss/search?q={pais}+actualidad&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:5]
    except:
        return []

# 3. Mostrar noticias
for pais in paises:
    st.header(f"📍 {pais}")
    noticias = buscar(pais)
    if noticias:
        for n in noticias:
            st.markdown(f"**[{n.title}]({n.link})**")
            st.caption(f"Publicado: {n.published}")
            st.divider()
    else:
        st.error(f"Error de conexión para {pais}")

# 4. Botón de reinicio
if st.button('Actualizar'):
    st.rerun()
