import streamlit as st
import feedparser
import urllib.request

# Configuración profesional de la página
st.set_page_config(page_title="Monitor Logístico", page_icon="⚓", layout="wide")

st.markdown("# ⚓ Monitor de Noticias Estratégicas")
st.write("Seguimiento de puertos, moneda y conflictos en el Mediterráneo e Irán.")

paises = ["Irán", "Libia", "Marruecos", "Túnez", "Francia"]
# Filtro optimizado para asegurar resultados relevantes
temas = "(puertos OR logística OR conflicto OR economía OR transporte OR moneda)"

def buscar_noticias(pais):
    # La búsqueda ahora es más precisa
    query = f'"{pais}" {temas}'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:8] # Aumentamos a 8 noticias por país
    except:
        return []

# Creamos pestañas para una navegación limpia
tabs = st.tabs(paises)

for i, pais in enumerate(paises):
    with tabs[i]:
        st.subheader(f"Últimos titulares de {pais}")
        noticias = buscar_noticias(pais)
        
        if noticias:
            for n in noticias:
                # Diseño de cada noticia
                with st.container():
                    # Título más grande y limpio
                    titulo = n.title.split(" - ")[0]
                    st.markdown(f"### [{titulo}]({n.link})")
                    
                    # Detalles de la noticia
                    col_info1, col_info2 = st.columns([1, 4])
                    with col_info1:
                        st.caption(f"📅 {n.published[:16]}")
                    with col_info2:
                        # Extraemos el nombre del medio si está disponible
                        fuente = n.source.title if hasattr(n, 'source') else "Fuente externa"
                        st.markdown(f"*{fuente}*")
                    
                    st.divider()
        else:
            st.info(f"No se han encontrado noticias específicas de logística o conflicto para {pais} en las últimas horas.")

# Botón de actualización manual al final
st.sidebar.markdown("---")
if st.sidebar.button('🔄 Actualizar Todo Ahora'):
    st.cache_data.clear()
    st.rerun()

st.sidebar.write("Actualizado por última vez:", st.session_state.get('last_update', "Recién cargado"))
