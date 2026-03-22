import os
import re
from datetime import datetime

PHOTO_DIR = 'photos'
VIDEO_FILE = 'video_links.txt'
OUTPUT_FILE = 'index.html'

def format_date(filename):
    """Извлекает дату из названия файла типа photo_100@31-05-2022_11-27-48.jpg"""
    match = re.search(r'@(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{2})', filename)
    if match:
        date_str, time_str = match.groups()
        time_formatted = time_str.replace('-', ':')
        return f"📅 {date_str} в {time_formatted}"
    return "Архив ВПК"

def get_video_data():
    videos = []
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    title = parts[0].replace('_', ' ')
                    url = parts[1]
                    match = re.search(r'video(\d+)_(\d+)', url)
                    if match:
                        oid, vid = match.groups()
                        videos.append({'title': title, 'oid': oid, 'id': vid})
    return videos

def get_photos():
    if not os.path.exists(PHOTO_DIR): return []
    # Берем только полные фото
    full_photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and '_thumb' not in f]
    # Сортируем: новые сверху
    full_photos.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTO_DIR, x)), reverse=True)
    return full_photos

def build():
    videos = get_video_data()
    photos = get_photos()

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ВПК Юный Десантник | Лента</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --bg: #f0f2f5; --blue: #0056b3; --card: #ffffff; --text: #1c1e21; }}
        body {{ font-family: -apple-system, system-ui, sans-serif; background: var(--bg); margin: 0; color: var(--text); }}
        
        header {{ background: white; padding: 20px; text-align: center; border-bottom: 1px solid #ddd; position: sticky; top:0; z-index:100; }}
        .logo {{ width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--blue); object-fit: cover; }}
        h1 {{ margin: 10px 0 0; font-size: 18px; text-transform: uppercase; }}

        .container {{ max-width: 600px; margin: 10px auto; padding: 0 8px; }}
        .section-header {{ font-size: 16px; font-weight: bold; margin: 25px 10px 10px; color: #65676b; text-transform: uppercase; }}
        
        .post-card {{ background: var(--card); border-radius: 8px; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.2); overflow: hidden; }}
        .post-header {{ padding: 12px; font-weight: 600; font-size: 15px; border-bottom: 1px solid #f0f2f5; }}
        
        .post-content img {{ width: 100%; display: block; height: auto; background: #eee; }}
        
        .post-footer {{ padding: 10px 12px; background: #fff; border-top: 1px solid #f0f2f5; font-size: 13px; color: #65676b; }}
        
        .video-wrapper {{ background: #000; }}
    </style>
</head>
<body>

<header>
    <img src="images/logo.jpg" alt="Лого" class="logo">
    <h1>ВПК «Юный Десантник»</h1>
</header>

<div class="container">
    <div class="section-header">🎬 Видеоархив</div>
    """

    for vid in videos:
        html_content += f"""
    <div class="post-card">
        <div class="post-header">{vid['title']}</div>
        <div class="video-wrapper">
            <div class="js-player">
                <iframe src="https://vk.com/video_ext.php?oid={vid['oid']}&id={vid['id']}" allowfullscreen></iframe>
            </div>
        </div>
    </div>"""

    html_content += """<div class="section-header">📸 Фотоархив</div>"""

    for photo in photos:
        caption = format_date(photo)
        thumb = photo.replace('.jpg', '_thumb.jpg') # Путь к превью
        
        html_content += f"""
    <div class="post-card">
        <div class="post-content">
            <img src="{PHOTO_DIR}/{photo}" loading="lazy" alt="Фото">
        </div>
        <div class="post-footer">{caption}</div>
    </div>"""

    html_content += """
</div>

<script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
<script>
    const players = Array.from(document.querySelectorAll('.js-player')).map(p => new Plyr(p));
</script>
</body>
</html>
"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Обновлено! Подписи добавлены, лента готова.")

if __name__ == "__main__":
    build()