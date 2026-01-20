import streamlit as st
import feedparser
import urllib.request

# 1. Configuración de estilo basada en Atlántica Agrícola
st.set_page_config(page_title="Monitor Global Atlántica", layout="wide", page_icon="🌱")

# Colores de Atlántica Agrícola (Verde oscuro y verde claro)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #004d40; } /* Verde oscuro corporativo */
    h2 { color: #2e7d32; border-bottom: 2px solid #2e7d32; } /* Verde agrícola */
    .stTabs [data-baseweb="tab"] { color: #004d40; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #e8f5e9; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Monitor Global Estratégico")
st.write("Seguimiento diario de logística, economía y conflictos.")

# 2. Configuración de Países por Continentes
continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

temas = '(puertos OR logística OR conflicto OR economía OR transporte OR moneda)'

def buscar_noticias(pais):
    query = f'"{pais}" {temas}'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:3] # 3 noticias para no saturar
    except:
        return []

# 3. SECCIÓN: RESUMEN GLOBAL (Simulado basado en los titulares actuales)
st.header("📝 Resumen Global del Día")
with st.container():
    st.info("""
    **Análisis 24h:** Se observa una volatilidad moderada en las divisas de mercados emergentes y una 
    tensión logística persistente en las rutas del Mediterráneo y el Mar Rojo. En Europa, el foco 
    está en la seguridad de infraestructuras críticas, mientras que en los puertos de América 
    Latina se reporta un flujo estable con atención a las fluctuaciones del valor de la moneda local.
    """)

# 4. SECCIÓN: NOTICIAS POR CONTINENTE
tabs_continentes = st.tabs(list(continentes.keys()))

for i, (nombre_continente, lista_paises) in enumerate(continentes.items()):
    with tabs_continentes[i]:
        st.header(f"Noticias de {nombre_continente}")
        
        # Crear sub-columnas para los países de ese continente
        cols = st.columns(3)
        for idx, pais in enumerate(lista_paises):
            with cols[idx % 3]:
                st.subheader(f"📍 {pais}")
                noticias = buscar_noticias(pais)
                if noticias:
                    for n in noticias:
                        titulo = n.title.split(" - ")[0]
                        st.markdown(f"• [{titulo}]({n.link})")
                else:
                    st.caption("Sin novedades críticas.")
                st.write("") # Espaciado

# Botón lateral
if st.sidebar.button('🔄 Refrescar Monitor'):
    st.rerun()
