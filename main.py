import os
import requests
import feedparser

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AMAZON_TAG = os.environ.get("AMAZON_TAG")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    print(f"Respuesta de Telegram: {response.status_code} - {response.text}")

def main():
    print(f"Canal configurado: {CHANNEL_ID}")
    # RSS específico para la categoría de Hogar y Casa
    rss_url = "https://www.chollometro.com/rss/categorias/hogar"
    feed = feedparser.parse(rss_url)
    print(f"Entradas encontradas en el RSS: {len(feed.entries)}")
    
    # Procesa solo el chollo más reciente de cada revisión
    for entry in feed.entries[:1]:
        titulo = entry.title
        link = entry.link
        
        # Añadir etiqueta de afiliado de Amazon si aplica
        if "amazon" in link:
            link = f"{link}?tag={AMAZON_TAG}"
            
        mensaje = f"🏠 <b>{titulo}</b>\n\n🔗 <a href='{link}'>Ver Chollo</a>"
        enviar_mensaje(mensaje)

if __name__ == "__main__":
    main()
