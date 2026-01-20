import feedparser # O la librería que uses
import time       # Necesario para el input/sleep

def classify_headline(title):
    # ... lógica de clasificación ...
    return "Categoría X"

feed = feedparser.parse("https://elpais.com/rss/...") 
entries = feed.entries

for entry in entries:
    
    # 1. Procesar datos
    title = entry.title
    category = classify_headline(title)

    # 2. Mostrar en pantalla
    print(f"📰 Titular: {title}")
    print(f"🏷️ Categoría: {category}")
    print("-" * 30)

    # 3. PAUSA PARA LEER (Lo nuevo)
    input(">> Dale a Enter para la siguiente...")
