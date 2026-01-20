import streamlit as st
import feedparser
import urllib.request

st.set_page_config(page_title="Monitor Estratégico", page_icon="⚓")

st.title("⚓ Monitor de Noticias: Mediterráneo")

paises = ["Irán", "Libia", "Marruecos", "Túnez", "Francia"]
temas = '(conflicto OR guerra OR "transporte marítimo" OR puerto OR moneda OR divisa)'

def buscar_noticias(pais):
    query = f"{pais} {temas}"
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    
    # ESTA ES LA MEJORA: Configuramos una identidad de navegador (User-Agent)
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(request) as response:
            datos = response.read()
            feed = feedparser.parse(datos)
            return feed.entries[:5]
    except Exception as e:
        return []

# Diseño de la web
col1, col2 = st.columns(2)

for i, pais in enumerate(paises):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.subheader(f"📍 {pais}")
        noticias = buscar_noticias(pais)
        
        if noticias:
            for n in noticias:
                # Limpiamos el título (Google suele añadir el nombre del medio al final)
                titulo_limpio = n.title.split(" - ")[0]
                st.markdown(f"**[{titulo_limpio}]({n.link})**")
                st.caption(f"📅 {n.published[:16]}")
                st.divider()
        else:
            st.warning(f"No se detectan noticias recientes para {pais}.")

if st.button('🔄 Forzar Actualización'):
    st.rerun()
