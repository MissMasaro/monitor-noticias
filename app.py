import streamlit as st
import feedparser
import urllib.request
import time

# 1. Configuración de estilo Atlántica Agrícola Premium
st.set_page_config(page_title="Global Intelligence Monitor", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    /* Fondo y fuentes */
    .main { background-color: #f4f7f6; }
    h1 { color: #004d40; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700; }
    
    /* Estilo de Tarjetas */
    .news-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .news-title {
        color: #004d40;
        font-size: 18px;
        font-weight: bold;
        text-decoration: none;
    }
    .news-title:hover { color: #2e7d32; }
    
    /* Etiquetas (Badges) */
    .badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 5px;
        color: white;
    }
    .badge-puerto { background-color: #0277bd; }
    .badge-moneda { background-color: #2e7d32; }
    .badge-conflicto { background-color: #c62828; }
    .badge-general { background-color: #757575; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Global Strategic Monitor")
st.write("Inteligencia de mercado y logística en tiempo real.")

continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

def obtener_badge(titulo):
    t = titulo.lower()
    if any(word in t for word in ["puerto", "buque", "marítimo", "canal"]):
        return '<span class="badge badge-puerto">⚓ PUERTO</span>'
    if any(word in t for word in ["moneda", "dólar", "divisa", "inflación", "economía"]):
        return '<span class="badge badge-moneda">💰 ECONOMÍA</span>'
    if any(word in t for word in ["guerra", "conflicto", "ataque", "tensión"]):
        return '<span class="badge badge-conflicto">⚔️ ALERTA</span>'
    return '<span class="badge badge-general">📋 INFO</span>'

def buscar_noticias(pais):
    query = f'"{pais}" (puertos OR logística OR economía OR conflicto)'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        time.sleep(0.1) 
        with urllib.request.urlopen(req, timeout=10) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:3]
    except:
        return []

# --- SECCIÓN RESUMEN ---
st.header("📝 Resumen Global del Día")
st.info("Hoy se detecta una estabilización en los fletes de América Latina, mientras que la volatilidad de divisas afecta el mercado en Argentina y Turquía. En Oriente Medio, el foco logístico sigue en la seguridad de los puertos clave.")

# --- SECCIÓN NOTICIAS ---
tabs = st.tabs(list(continentes.keys()))

for i, (nombre_continente, lista_paises) in enumerate(continentes.items()):
    with tabs[i]:
        # Usamos columnas para que no sea una lista infinita
        for pais in lista_paises:
            st.markdown(f"### 📍 {pais}")
            noticias = buscar_noticias(pais)
            if noticias:
                cols = st.columns(len(noticias))
                for idx, n in enumerate(noticias):
                    with cols[idx]:
                        badge = obtener_badge(n.title)
                        titulo_limpio = n.title.rsplit(" - ", 1)[0]
                        st.markdown(f"""
                            <div class="news-card">
                                {badge}<br><br>
                                <a class="news-title" href="{n.link}" target="_blank">{titulo_limpio}</a>
                                <p style="color: gray; font-size: 12px; margin-top:10px;">📅 {n.published[:16]}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.caption("Sin novedades destacadas.")
            st.write("")

# Botón de refresco lateral
if st.sidebar.button('🔄 Refrescar Monitor'):
    st.cache_data.clear()
    st.rerun()
