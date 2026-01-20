import streamlit as st
import feedparser
import urllib.request
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE IA ---
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_activa = True
except:
    ia_activa = False

# --- ESTILO VISUAL ATLÁNTICA AGRÍCOLA ---
st.set_page_config(page_title="Global Intelligence Monitor", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    h1 { color: #004d40; font-family: 'Segoe UI', sans-serif; }
    .news-card {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        border-left: 5px solid #2e7d32; margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 180px;
    }
    .badge { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; }
    .badge-log { background-color: #0277bd; }
    .badge-war { background-color: #c62828; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Global Strategic Monitor")

continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

def obtener_badge(titulo):
    t = titulo.lower()
    if any(w in t for w in ["puerto", "logística", "marítimo"]): return '<span class="badge badge-log">⚓ LOGÍSTICA</span>'
    if any(w in t for w in ["guerra", "conflicto", "crisis"]): return '<span class="badge badge-war">⚠️ ALERTA</span>'
    return ""

def buscar_noticias(pais):
    # Simplificado a 'actualidad' temporalmente para asegurar que salgan noticias
    query = f'"{pais}" actualidad'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        time.sleep(0.1)
        with urllib.request.urlopen(req, timeout=10) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:2]
    except:
        return []

todos_los_titulares = []
tabs = st.tabs(list(continentes.keys()))

for i, (nombre_continente, lista_paises) in enumerate(continentes.items()):
    with tabs[i]:
        cols = st.columns(3)
        for idx, pais in enumerate(lista_paises):
            with cols[idx % 3]:
                st.subheader(f"📍 {pais}")
                noticias = buscar_noticias(pais)
                if noticias:
                    for n in noticias:
                        todos_los_titulares.append(f"{pais}: {n.title}")
                        st.markdown(f"""
                            <div class="news-card">
                                {obtener_badge(n.title)}<br>
                                <a style="color: #004d40; font-weight:bold; text-decoration:none;" href="{n.link}" target="_blank">{n.title.split(' - ')[0]}</a>
                                <p style="color: gray; font-size: 11px; margin-top:10px;">📅 {n.published[:16]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.caption("Sin novedades.")

# BARRA LATERAL
st.sidebar.header("🤖 Inteligencia Artificial")
if st.sidebar.button("Generar Resumen Estratégico"):
    if not ia_activa:
        st.sidebar.error("Falta la clave GEMINI_KEY.")
    else:
        with st.sidebar:
            with st.spinner("Analizando..."):
                texto = "\n".join(todos_los_titulares[:30])
                prompt = f"Resume estos titulares en un párrafo estratégico para Atlántica Agrícola: {texto}"
                response = model.generate_content(prompt)
                st.write(response.text)

if st.sidebar.button('🔄 Refrescar'):
    st.rerun()
