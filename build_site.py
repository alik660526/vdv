import os
import urllib.parse

# Настройки, которые работали
HTML_OUTPUT = 'index.html'
PHOTO_DIR = 'Фото'
VIDEO_FILE = 'video_links.txt'

def generate_site():
    photo_html = ""
    video_html = ""

    # 1. ОБРАБОТКА ФОТО (Ваш старый рабочий метод)
    if os.path.exists(PHOTO_DIR):
        photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for photo in photos:
            # Важно: используем кодирование пути, как в прошлый раз
            photo_url = urllib.parse.quote(f"{PHOTO_DIR}/{photo}")
            photo_html += f'''
            <div class="photo-card">
                <a href="{photo_url}" target="_blank">
                    <img src="{photo_url}" loading="lazy">
                </a>
            </div>'''

    # 2. ОБРАБОТКА ВИДЕО
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    title, link = line.strip().split('|')
                    video_html += f'''
                    <div class="video-card">
                        <div style="background:#333; height:100px; display:flex; align-items:center; justify-content:center; font-size:40px;">🎬</div>
                        <div class="video-info">
                            <div class="video-title">{title}</div>
                            <a class="video-btn" href="{link}" target="_blank">СМОТРЕТЬ В ВК</a>
                        </div>
                    </div>'''

    # 3. HTML (Возвращаем старую структуру, добавляем только лого)
    full_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>ВПК ЮНЫЙ ДЕСАНТНИК</title>
    <style>
        body {{ background: #121212; color: #e0e0e0; font-family: sans-serif; text-align: center; padding: 20px; }}
        .header-logo {{ width: 150px; height: 150px; object-fit: cover; border-radius: 50%; border: 3px solid #4a76a8; margin-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; }}
        .photo-card img {{ width: 100%; height: 150px; object-fit: cover; border-radius: 5px; }}
        .video-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .video-card {{ background: #1e1e1e; padding: 10px; border-radius: 8px; }}
        .video-btn {{ display: block; background: #4a76a8; color: white; padding: 8px; text-decoration: none; margin-top: 10px; border-radius: 4px; }}
        .video-title {{ font-size: 14px; height: 35px; overflow: hidden; }}
    </style>
</head>
<body>
    <img src="images/logo.jpg" class="header-logo">
    <h1>ВПК «ЮНЫЙ ДЕСАНТНИК»</h1>
    
    <h2>ВИДЕОАРХИВ</h2>
    <div class="video-grid">{video_html}</div>
    
    <h2>ФОТОГАЛЕРЕЯ</h2>
    <div class="grid">{photo_html}</div>
</body>
</html>'''

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Откат завершен. Сайт собран по старой схеме!")

if __name__ == "__main__":
    generate_site()