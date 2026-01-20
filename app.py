<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Noticias Relevantes</title>
  <style>
    body { font-family: Arial, sans-serif; }
    .news-item { margin-bottom: 15px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
  </style>
</head>
<body>

<h1>Noticias Relevantes</h1>

<input type="text" id="keyword" placeholder="Palabra clave (USA, Estados Unidos, Groenlandia, Venezuela, tren, economía...)">
<button onclick="fetchNews()">Buscar</button>

<div id="news-container"></div>

<script src="app.js"></script>

</body>
</html>
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
