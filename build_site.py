import os
import urllib.parse

# Настройки
HTML_OUTPUT = 'index.html'
PHOTOS_DIR = 'photos'
VIDEO_DIR = 'TO_VK'
LINKS_FILE = 'video_links.txt'

def get_video_links():
    links = {}
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    title, url = line.strip().split('|')
                    links[title.strip()] = url.strip()
    return links

def build():
    links_map = get_video_links()
    
    # 1. СБОРКА ФОТОГРАФИЙ (Оригинал + Превью)
    photo_html = ""
    if os.path.exists(PHOTOS_DIR):
        # Берем только оригиналы (без _thumb)
        files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith('.jpg') and '_thumb' not in f.lower()]
        for p in sorted(files):
            thumb = p.replace('.jpg', '_thumb.jpg')
            # Если превью нет, используем сам оригинал
            thumb_path = thumb if os.path.exists(os.path.join(PHOTOS_DIR, thumb)) else p
            
            enc_orig = urllib.parse.quote(f"photos/{p}")
            enc_thumb = urllib.parse.quote(f"photos/{thumb_path}")
            
            photo_html += f'''
            <div class="photo-card">
                <a href="{enc_orig}" target="_blank">
                    <img src="{enc_thumb}" loading="lazy" alt="Фото">
                </a>
            </div>'''

    # 2. СБОРКА ВИДЕО (Превью + Ссылка на ВК)
    video_html = ""
    if os.path.exists(VIDEO_DIR):
        v_thumbs = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith('.jpg')]
        for vt in sorted(v_thumbs):
            # Ищем название видео в ключе ссылки (убираем _thumb.jpg из имени файла)
            base_name = vt.replace('.mp4_thumb.jpg', '').replace('.mp4_t humb.jpg', '').strip()
            link = links_map.get(base_name, "#") # Если не нашли, ссылка будет пустой
            
            enc_vt = urllib.parse.quote(f"TO_VK/{vt}")
            video_html += f'''
            <div class="video-card">
                <img src="{enc_vt}" class="video-thumb">
                <div class="video-info">
                    <div class="video-title">{base_name}</div>
                    <a class="video-btn" href="{link}" target="_blank">СМОТРЕТЬ В ВК</a>
                </div>
            </div>'''

    # 3. HTML ШАБЛОН (Тёмная тема)
    full_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Архив ВПК Юный Десантник</title>
    <style>
        body {{ background: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        h1, h2 {{ text-align: center; color: #4a76a8; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-bottom: 40px; }}
        .photo-card img {{ width: 100%; height: 150px; object-fit: cover; border-radius: 8px; border: 1px solid #333; transition: 0.3s; }}
        .photo-card img:hover {{ transform: scale(1.05); border-color: #4a76a8; }}
        
        .video-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .video-card {{ background: #1e1e1e; border-radius: 10px; overflow: hidden; border: 1px solid #333; }}
        .video-thumb {{ width: 100%; height: 160px; object-fit: cover; }}
        .video-info {{ padding: 15px; text-align: center; }}
        .video-title {{ font-size: 14px; margin-bottom: 10px; height: 40px; overflow: hidden; }}
        .video-btn {{ display: inline-block; background: #4a76a8; color: #fff; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; }}
        .video-btn:hover {{ background: #3b5d85; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ВПК «ЮНЫЙ ДЕСАНТНИК»</h1>
        <h2>🎥 Видеоархив</h2>
        <div class="video-grid">{video_html}</div>
        <h2>📸 Фотогалерея</h2>
        <div class="grid">{photo_html}</div>
    </div>
</body>
</html>'''

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Сайт успешно собран!")

if __name__ == "__main__":
    build()