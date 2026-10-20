import os
import requests
import feedparser

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AMAZON_TAG = os.environ.get("AMAZON_TAG")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Palabras clave para filtrar productos de hogar/cocina
PALABRAS_CLAVE = [
    "hogar", "cocina", "aspirador", "cafetera", "freidora", "sarten", 
    "robot", "colchon", "almohada", "silla", "mesa", "luz", "led", 
    "enchufe", "herramienta", "bosh", "cecotec", "philips", "xiaomi"
]

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
    # Feed RSS general de Chollometro (este nunca falla)
    rss_url = "https://www.chollometro.com/rss"
    feed = feedparser.parse(rss_url)
    print(f"Entradas totales en el RSS general: {len(feed.entries)}")
    
    encontrado = False
    for entry in feed.entries:
        titulo = entry.title
        link = entry.link
        
        # Comprobar si el chollo coincide con el nicho de hogar/cocina
        texto_analizar = (titulo + " " + entry.get("summary", "")).lower()
        if any(palabra in texto_analizar for palabra in PALABRAS_CLAVE):
            # Añadir etiqueta de afiliado de Amazon si aplica
            if "amazon" in link:
                link = f"{link}?tag={AMAZON_TAG}"
                
            mensaje = f"🏠 <b>{titulo}</b>\n\n🔗 <a href='{link}'>Ver Chollo</a>"
            enviar_mensaje(mensaje)
            encontrado = True
            break # Publica 2 chollo y finaliza la ejecución

    if not encontrado:
        print("No se encontraron chollos de hogar en esta revisión.")

if __name__ == "__main__":
    main()
