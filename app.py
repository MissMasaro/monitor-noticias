import streamlit as st
import feedparser
import urllib.request

# 1. Configuración de pantalla
st.set_page_config(page_title="Monitor Logístico Mediterráneo", layout="wide", page_icon="⚓")
st.title("⚓ Monitor Estratégico de Noticias")
st.markdown("---")

# 2. Definición de parámetros
paises = ["Irán", "Libia", "Marruecos", "Túnez", "Francia"]

# Esta es la "fórmula mágica" para filtrar:
temas = '(puertos OR logística OR conflicto OR economía OR transporte OR "valor moneda")'

def buscar_noticias(pais):
    # Buscamos el país + los temas elegidos
    query = f"{pais} {temas}"
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:5] # Máximo 5 noticias por país
    except:
        return []

# 3. Mostrar los resultados en columnas para que se vea ordenado
col1, col2 = st.columns(2)

for i, pais in enumerate(paises):
    # Alternamos entre columna izquierda y derecha
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        st.subheader(f"📍 {pais}")
        noticias = buscar_noticias(pais)
        
        if noticias:
            for n in noticias:
                # Quitamos el nombre del diario del título para que sea más corto
                titulo_limpio = n.title.rsplit(" - ", 1)[0]
                st.markdown(f"🔗 **[{titulo_limpio}]({n.link})**")
                st.caption(f"📅 {n.published[:16]}")
                st.divider()
        else:
            st.info(f"Sin noticias de impacto logístico hoy para {pais}.")

# 4. Botón de actualización
if st.sidebar.button('🔄 Refrescar Noticias'):
    st.rerun()
