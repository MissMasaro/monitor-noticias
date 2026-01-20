import feedparser
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "097761fa694c4b468d1fcd47964bc941" 
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash") # Modelo rápido y económico

def classify_headline(headline):
    prompt = f"""
    Classify the following news headline into one of these categories: 
    [Business, crisis, war, Middle East, maritime transport].
    
    Headline: "{headline}"
    
    Category:
    """
    response = model.generate_content(prompt)
    return response.text.strip()


rss_url = "https://news.google.com/rss/search?q=technology&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(rss_url)

print(f"--- Procesando {len(feed.entries[:5])} noticias ---\n")


    title = entry.title
    category = classify_headline(title)
    
    print(f"📰 Titular: {title}")
    print(f"🏷️ Categoría: {category}")
    print("-" * 30)
