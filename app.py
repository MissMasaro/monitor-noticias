import streamlit as st
import feedparser
import urllib.request
import google.generativeai as genai
import time

# --- 1. CONFIGURACIÓN DE IA (CONEXIÓN SEGURA) ---
try:
    # Busca la clave en los Secrets de Streamlit
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_activa = True
except Exception as e:
    ia_activa = False

# --- 2. ESTILO VISUAL (ATLÁNTICA AGRÍCOLA) ---
st.set_page_config(page_title="Global Intelligence Monitor", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    h1 { color: #004d40; font-family: 'Segoe UI', sans-serif; }
    h2 { color: #2e7d32; }
    .news-card {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        border-left: 5px solid #2e7d32; margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%;
    }
    .badge {
        padding: 2px 8px; border-radius: 4px; font-size: 10px; 
        font-weight: bold; color: white; margin-bottom: 5px; display: inline-block;
    }
    .badge-log { background-color: #0277bd; }
    .badge-eco { background-color: #2e7d32; }
    .badge-war { background-color: #c62828; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Global Strategic Monitor")
st.write("Panel de inteligencia logística y económica en tiempo real.")

# --- 3. DATOS Y FUNCIONES ---
continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

temas = 'actualidad'

def obtener_badge(titulo):
    t = titulo.lower()
    if any(w in t for w in ["puerto", "logística", "transporte"]): return '<span class="badge badge-log">⚓ LOGÍSTICA</span>'
    if any(w in t for w in ["moneda", "economía", "dólar"]): return '<span class="badge badge-eco">💰 ECONOMÍA</span>'
    if any(w in t for w in ["guerra", "conflicto", "crisis"]): return '<span class="badge badge-war">⚠️ ALERTA</span>'
    return ""

def buscar_noticias(pais):
    query = f'"{pais}" {temas}'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        time.sleep(0.1) # Pausa para evitar bloqueos
        with urllib.request.urlopen(req, timeout=10) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:3]
    except:
        return []

# --- 4. ESTRUCTURA DE LA WEB ---
todos_los_titulares = []

# Pestañas de Continentes
tabs = st.tabs(list(continentes.keys()))

for i, (nombre_continente, lista_paises) in enumerate(continentes.items()):
    with tabs[i]:
        for pais in lista_paises:
            st.markdown(f"### 📍 {pais}")
            noticias = buscar_noticias(pais)
            if noticias:
                cols = st.columns(len(noticias))
                for idx, n in enumerate(noticias):
                    todos_los_titulares.append(f"{pais}: {n.title}")
                    with cols[idx]:
                        badge = obtener_badge(n.title)
                        titulo_limpio = n.title.rsplit(" - ", 1)[0]
                        st.markdown(f"""
                            <div class="news-card">
                                {badge}<br>
                                <a style="color: #004d40; font-weight:bold; text-decoration:none;" href="{n.link}" target="_blank">{titulo_limpio}</a>
                                <p style="color: gray; font-size: 11px; margin-top:10px;">📅 {n.published[:16]}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.caption("No se detectan noticias relevantes hoy.")
            st.write("")

# --- 5. BARRA LATERAL: IA Y CONTROLES ---
st.sidebar.image("https://www.atlanticaagricola.com/wp-content/uploads/2021/05/logo-atlantica-agricola.png", width=200)
st.sidebar.header("🤖 Inteligencia Artificial")

if st.sidebar.button("Generar Resumen Estratégico"):
    if not ia_activa:
        st.sidebar.error("Configura la GEMINI_KEY en los Secrets de Streamlit.")
    elif not todos_los_titulares:
        st.sidebar.warning("No hay datos para analizar.")
    else:
        with st.sidebar:
            with st.spinner("Analizando situación global..."):
                texto = "\n".join(todos_los_titulares[:40])
                prompt = f"Eres un analista de riesgos. Resume estos titulares en un párrafo de 100 palabras enfocado en logística y economía para una empresa agrícola: {texto}"
                try:
                    response = model.generate_content(prompt)
                    st.success("Análisis del día:")
                    st.write(response.text)
                except:
                    st.error("Error al conectar con la IA.")

if st.sidebar.button('🔄 Refrescar Noticias'):
    st.rerun()            
