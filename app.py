import time

# --- 1. CONFIGURACIÓN PREVIA (Simulación de tus datos) ---

# Clase simple para simular lo que te devuelve una librería como 'feedparser'
class Noticia:
    def __init__(self, title):
        self.title = title

# Lista de noticias falsas para probar el código
entries = [
    Noticia("El Real Madrid gana el partido en el último minuto"),
    Noticia("El Bitcoin alcanza un nuevo máximo histórico hoy"),
    Noticia("Nueva receta de pasta viral en TikTok"),
    Noticia("Apple anuncia el nuevo iPhone 16 con IA integrada"),
    Noticia("El tiempo para mañana: lluvias en el norte")
]

# --- 2. TU FUNCIÓN DE CLASIFICACIÓN ---
# He creado una lógica básica. Tú puedes cambiar las palabras clave.
def classify_headline(text):
    text = text.lower()
    if any(x in text for x in ["madrid", "gol", "partido", "fútbol"]):
        return "Deportes ⚽"
    elif any(x in text for x in ["bitcoin", "dinero", "bolsa", "economía"]):
        return "Finanzas 💰"
    elif any(x in text for x in ["iphone", "ia", "tecnología", "google"]):
        return "Tecnología 💻"
    else:
        return "General 🌍"

# --- 3. EL BUCLE PRINCIPAL (Tu código) ---

print("--- INICIANDO LECTOR DE NOTICIAS ---\n")

for entry in entries:
    # -- Aquí empieza la parte de tu imagen --
    
    title = entry.title
    category = classify_headline(title)

    print(f"📰 Titular: {title}")
    print(f"🏷️ Categoría: {category}")
    print("-" * 30)

    # -- Aquí está la pausa para que puedas leer --
    input(">> Presiona ENTER para ver la siguiente noticia...")
    print("\n") # Espacio extra para limpiar visualmente

print("--- FIN DE LAS NOTICIAS ---")
