import os
from urllib.parse import quote

# Настройки
HTML_OUTPUT = 'Index.html'
PHOTOS_DIR = 'photos'
PREVIEW_DIR = 'TO_VK'
LINKS_FILE = 'video_links.txt'

def build():
    # Собираем видео
    video_html = ""
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    title, link = line.strip().split('|')
                    thumb = f"{PREVIEW_DIR}/{title}.mp4_thumb.jpg"
                    img_src = quote(thumb) if os.path.exists(thumb) else "https://via.placeholder.com/260x150/252525/cccccc?text=Video"
                    video_html += f'''
        <div class="video-card">
            <img class="video-thumb" src="{img_src}">
            <div class="video-info">
                <div class="video-title">{title}</div>
                <a class="video-btn" href="{link}" target="_blank">СМОТРЕТЬ</a>
            </div>
        </div>'''

    # Собираем фото (только оригиналы, без _thumb)
    photo_html = ""
    if os.path.exists(PHOTOS_DIR):
        files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith('.jpg') and '_thumb' not in f.lower()]
        for p in sorted(files):
            # КРИТИЧЕСКИЙ МОМЕНТ: кодируем @ и прочее для интернета
            encoded_path = quote(f"{PHOTOS_DIR}/{p}")
            photo_html += f'''
        <div class="msg">
            <img class="msg-photo" src="{encoded_path}" loading="lazy">
        </div>'''

    # Шаблон страницы
    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Архив ВПК «Юный Десантник»</title>
    <style>
        body {{ background: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{ text-align: center; padding: 40px 0; border-bottom: 1px solid #333; }}
        .video-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .video-card {{ background: #1e1e1e; border-radius: 8px; overflow: hidden; border: 1px solid #333; }}
        .video-thumb {{ width: 100%; height: 150px; object-fit: cover; }}
        .video-info {{ padding: 15px; }}
        .video-title {{ font-size: 13px; height: 35px; overflow: hidden; color: #bbb; margin-bottom: 10px; }}
        .video-btn {{ display: block; text-align: center; background: #4a76a8; color: white; text-decoration: none; padding: 8px; border-radius: 4px; }}
        .msg {{ background: #1e1e1e; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #333; }}
        .msg-photo {{ max-width: 100%; border-radius: 5px; display: block; }}
        h2 {{ border-left: 4px solid #4a76a8; padding-left: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>Архив ВПК «Юный Десантник»</h1></div>
        <h2>🎥 Видеоархив</h2>
        <div class="video-grid">{video_html}</div>
        <h2>📸 Фотоархив</h2>
        <div class="photo-list">{photo_html}</div>
    </div>
</body>
</html>'''

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Готово! Index.html исправлен для GitHub.")

if __name__ == "__main__":
    build()