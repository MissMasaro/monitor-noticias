import streamlit as st
import requests

# Leer la llave desde los Secrets de Streamlit
API_KEY = st.secrets["news_key"]

# Configuración de la página
st.set_page_config(page_title="Global News Radar", page_icon="🌎")

st.title("🌎 Radar de Noticias Globales")
st.subheader("Los 5 titulares más importantes de la prensa internacional")

# Tu API Key de NewsAPI.org
API_KEY = "TU_API_KEY_AQUI" 

# Lista de periódicos influyentes (IDs de NewsAPI)
sources = "the-new-york-times,the-guardian,al-jazeera-english,le-monde,the-times-of-india"

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?sources={sources}&apiKey={API_KEY}"
    response = requests.get(url)
    return response.json()

if st.button('Actualizar Noticias'):
    data = get_news()
    
    if data.get("status") == "ok":
        articles = data.get("articles", [])
        
        # Diccionario para asegurar 1 titular por medio
        seen_sources = set()
        count = 0
        
        for art in articles:
            source_name = art['source']['name']
            if source_name not in seen_sources and count < 5:
                st.markdown(f"### 📰 {source_name}")
                st.write(f"**Titular:** {art['title']}")
                st.write(f"[Leer noticia completa]({art['url']})")
                st.divider()
                
                seen_sources.add(source_name)
                count += 1
    else:
        st.error("Error al conectar con la API. Verifica tu API Key.")

st.info("Esta app filtra noticias de NYT, The Guardian, Al Jazeera, Le Monde y Times of India.")
