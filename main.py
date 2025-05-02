import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configurar Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# URL de la noticia (puedes cambiar esto o hacer input dinámico)
url = "https://example.com/noticia"

# Obtener HTML
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# Extraer og:image
og_img = soup.find("meta", property="og:image")
img_url = og_img["content"] if og_img else None

# Extraer título y texto (simplificado)
title = soup.title.string.strip() if soup.title else "Noticia"
paragraphs = soup.find_all("p")
text = " ".join(p.get_text() for p in paragraphs[:5])  # Los primeros 5 párrafos

# Llamar a Gemini para resumir
prompt = f"Resume en 3 frases este texto de noticia:\n\n{text}"
response = model.generate_content(prompt)
summary = response.text.strip()
print("Resumen:", summary)

# Guardar texto en archivo
with open("resumen.txt", "w") as f:
    f.write(summary)

# Descargar imagen
if img_url:
    img_data = requests.get(img_url).content
    with open("imagen.jpg", "wb") as f:
        f.write(img_data)
else:
    print("No se encontró imagen destacada")

# Crear audio (solo texto de momento, puede ser TTS en otra fase)
with open("voz.mp3", "wb") as f:
    f.write(b"")  # Placeholder (puedes generar con ElevenLabs o TTS local)

# Crear video con FFmpeg
os.system("ffmpeg -loop 1 -i imagen.jpg -i voz.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -pix_fmt yuv420p video.mp4")
