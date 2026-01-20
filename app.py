import streamlit as st
import google.generativeai as genai

# El código buscará automáticamente GEMINI_KEY en los Secrets que acabas de guardar
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("No se pudo configurar la IA. Revisa los Secrets en Streamlit.")

# --- CONFIGURACIÓN DE IA ---
# SUSTITUYE AQUÍ TU LLAVE
API_KEY_GEMINI = "PEGA_AQUÍ_TU_API_KEY" 
genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Global Intelligence Monitor", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    h1 { color: #004d40; font-family: 'Segoe UI'; font-weight: 700; }
    .news-card {
        background-color: #ffffff; padding: 15px; border-radius: 10px;
        border-left: 5px solid #2e7d32; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 180px;
    }
    .badge { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; }
    .badge-alert { background-color: #c62828; }
    .badge-log { background-color: #0277bd; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Global Strategic Monitor (AI Powered)")

continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

def buscar_noticias(pais):
    query = f'"{pais}" (puertos OR logística OR economía OR conflicto)'
    url = f"https://news.google.com/rss/search?q={query}&hl=es&gl=ES&ceid=ES:es"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            feed = feedparser.parse(response.read())
            return feed.entries[:2] # 2 noticias por país para no saturar a la IA
    except: return []

# --- LÓGICA DE RECOLECCIÓN PARA IA ---
todos_los_titulares = []

# Mostramos los países y recolectamos titulares para el resumen
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
                                <a style="color: #004d40; font-weight:bold; text-decoration:none;" href="{n.link}" target="_blank">{n.title.rsplit(" - ", 1)[0]}</a>
                                <p style="color: gray; font-size: 11px; margin-top:10px;">📅 {n.published[:16]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else: st.caption("Sin novedades.")

# --- SECCIÓN RESUMEN IA (Aparecerá en la barra lateral o al final) ---
st.sidebar.header("🤖 Resumen Inteligente")
if st.sidebar.button("Generar Resumen con IA"):
    if API_KEY_GEMINI == "PEGA_AQUÍ_TU_API_KEY":
        st.sidebar.error("Falta la API KEY")
    else:
        with st.sidebar:
            with st.spinner("Analizando noticias..."):
                texto_titulares = "\n".join(todos_los_titulares[:30]) # Enviamos los primeros 30 titulares
                prompt = f"Eres un analista experto en logística y economía. Basándote en estos titulares, escribe un resumen ejecutivo de un párrafo sobre la situación global actual, destacando riesgos en puertos o moneda: {texto_titulares}"
                try:
                    response = model.generate_content(prompt)
                    st.success("Análisis completado:")
                    st.write(response.text)
                except Exception as e:
                    st.error("Error con la IA")

if st.sidebar.button('🔄 Refrescar Noticias'):
    st.rerun()
