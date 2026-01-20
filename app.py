import streamlit as st
import feedparser
import google.generativeai as genai
import time
from datetime import datetime

# 1. CONEXIÓN SEGURA CON LA IA
def configurar_ia():
    try:
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return None
    return None

ia_model = configurar_ia()

# 2. CONFIGURACIÓN DE LA INTERFAZ (ESTILO ATLÁNTICA AGRÍCOLA)
st.set_page_config(page_title="Monitor Global 2.0", layout="wide", page_icon="🌱")

st.markdown("""
    <style>
    .main { background-color: #f8faf9; }
    .stHeading h1 { color: #004d40; border-bottom: 3px solid #2e7d32; }
    .news-card {
        background-color: #ffffff; border-radius: 12px; padding: 15px;
        border-left: 6px solid #2e7d32; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px; min-height: 150px;
    }
    .pais-tag { background-color: #004d40; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Monitor Global Estratégico 2.0")
st.caption(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# 3. PAÍSES Y CONTINENTES
continentes = {
    "AMÉRICA": ["Costa Rica", "Panamá", "Paraguay", "Brasil", "Uruguay", "Argentina", "Chile", "México", "Guatemala"],
    "EUROPA": ["España", "Francia", "Italia", "Rusia", "Turquía"],
    "ÁFRICA": ["Marruecos", "Túnez", "Argelia", "Egipto", "Senegal"],
    "ORIENTE": ["Dubái", "Kuwait", "Yeda", "Vietnam", "Myanmar"]
}

# 4. MOTOR DE BÚSQUEDA DE NOTICIAS
def traer_noticias(pais):
    # Buscamos términos clave de logística y economía
    busqueda = f'"{pais}" (puertos OR logística OR economía OR conflicto)'
    url = f"https://news.google.com/rss/search?q={busqueda}&hl=es&gl=ES&ceid=ES:es"
    
    try:
        # Usamos feedparser directamente (más estable)
        feed = feedparser.parse(url)
        return feed.entries[:3] # Traer 3 noticias
    except:
        return []

# 5. ESTRUCTURA DE LA APP
titulares_para_ia = []

tabs = st.tabs(list(continentes.keys()))

for i, (nombre_cont, lista_paises) in enumerate(continentes.items()):
    with tabs[i]:
        cols = st.columns(3)
        for idx, pais in enumerate(lista_paises):
            with cols[idx % 3]:
                st.markdown(f"### <span class='pais-tag'>{pais}</span>", unsafe_allow_html=True)
                noticias = traer_noticias(pais)
                
                if noticias:
                    for n in noticias:
                        titulares_para_ia.append(f"{pais}: {n.title}")
                        # Limpiar título
                        t_limpio = n.title.split(" - ")[0]
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{n.link}" target="_blank" style="text-decoration:none; color:#004d40; font-weight:bold;">{t_limpio}</a>
                                <p style="font-size:11px; color:#666; margin-top:10px;">🕒 {n.published[:16]}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No hay noticias críticas hoy.")

# 6. RESUMEN INTELIGENTE EN BARRA LATERAL
st.sidebar.image("https://www.atlanticaagricola.com/wp-content/uploads/2021/05/logo-atlantica-agricola.png", width=180)
st.sidebar.header("🤖 Inteligencia de Mercado")

if st.sidebar.button("Generar Resumen Global"):
    if ia_model and titulares_para_ia:
        with st.sidebar:
            with st.spinner("Analizando situación..."):
                texto = "\n".join(titulares_para_ia[:50])
                prompt = f"Analiza estos titulares y genera un resumen ejecutivo de un párrafo para Atlántica Agrícola sobre riesgos logísticos y económicos: {texto}"
                respuesta = ia_model.generate_content(prompt)
                st.success("Análisis Estratégico:")
                st.write(respuesta.text)
    else:
        st.sidebar.warning("Configura la clave GEMINI_KEY o espera a que carguen noticias.")

if st.sidebar.button("🔄 Refrescar Todo"):
    st.rerun()
