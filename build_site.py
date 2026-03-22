import os
import urllib.parse

# --- НАСТРОЙКИ ---
# Теперь строго с маленькой буквы, чтобы Гитхаб не ругался
HTML_OUTPUT = 'index.html'
PHOTO_DIR = 'Фото'        # Ваша папка с фото
VIDEO_FILE = 'video_links.txt' # Файл со ссылками ВК

def generate_site():
    photo_html = ""
    video_html = ""

    # 1. ОБРАБОТКА ФОТОГРАФИЙ
    if os.path.exists(PHOTO_DIR):
        photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        for photo in photos:
            # Кодируем имя файла для ссылок (чтобы пробелы не ломали сайт)
            photo_url = urllib.parse.quote(f"{PHOTO_DIR}/{photo}")
            photo_html += f'''
            <div class="photo-card">
                <a href="{photo_url}" target="_blank">
                    <img src="{photo_url}" loading="lazy" alt="Фото ВПК">
                </a>
            </div>'''
    else:
        photo_html = "<p>Папка с фото не найдена</p>"

    # 2. ОБРАБОТКА ВИДЕО (ИЗ ФАЙЛА)
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    title, link = line.strip().split('|')
                    # Делаем заглушку-превью (синий фон с иконкой видео)
                    video_html += f'''
                    <div class="video-card">
                        <div class="video-thumb-placeholder">🎬</div>
                        <div class="video-info">
                            <div class="video-title">{title}</div>
                            <a class="video-btn" href="{link}" target="_blank">СМОТРЕТЬ В ВК</a>
                        </div>
                    </div>'''
    else:
        video_html = "<p>Файл со ссылками не найден</p>"

    # 3. ПОЛНЫЙ HTML ШАБЛОН (С ШАПКОЙ И ЛОГОТИПОМ)
    full_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ВПК ЮНЫЙ ДЕСАНТНИК - АРХИВ</title>
    <style>
        body {{ background: #0f172a; color: #f1f5f9; font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; text-align: center; }}
        
        /* СТИЛЬ ШАПКИ С ЛОГОТИПОМ */
        .header-block {{ margin-bottom: 40px; padding: 20px; border-bottom: 2px solid #334155; }}
        .header-logo {{ 
            width: 180px; height: 180px; 
            object-fit: cover; 
            border-radius: 50%; 
            border: 4px solid #38bdf8; 
            margin-bottom: 15px; 
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
        }}
        h1 {{ color: #38bdf8; font-size: 2.5em; margin: 10px 0; text-transform: uppercase; letter-spacing: 2px; }}
        h2 {{ color: #94a3b8; margin-top: 40px; border-left: 5px solid #38bdf8; padding-left: 15px; text-align: left; }}

        /* СЕТКА ФОТО */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }}
        .photo-card img {{ width: 100%; height: 180px; object-fit: cover; border-radius: 10px; transition: 0.3s; border: 1px solid #334155; }}
        .photo-card img:hover {{ transform: scale(1.03); border-color: #38bdf8; cursor: pointer; }}

        /* СЕТКА ВИДЕО */
        .video-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .video-card {{ background: #1e293b; border-radius: 12px; overflow: hidden; border: 1px solid #334155; transition: 0.3s; }}
        .video-card:hover {{ border-color: #38bdf8; }}
        .video-thumb-placeholder {{ background: #334155; height: 150px; display: flex; align-items: center; justify-content: center; font-size: 50px; }}
        .video-info {{ padding: 20px; }}
        .video-title {{ font-weight: bold; margin-bottom: 15px; height: 45px; overflow: hidden; color: #f8fafc; }}
        .video-btn {{ 
            display: block; background: #0284c7; color: white; 
            padding: 10px; border-radius: 6px; text-decoration: none; 
            font-weight: bold; transition: 0.2s; 
        }}
        .video-btn:hover {{ background: #0ea5e9; }}
    </style>
</head>
<body>
    <div class="container">
        
        <div class="header-block">
            <img src="images/logo.jpg" class="header-logo" alt="Логотип">
            <h1>ВПК «ЮНЫЙ ДЕСАНТНИК»</h1>
            <p style="color: #94a3b8;">г. Павлово • Военно-патриотический клуб</p>
        </div>

        <h2>🎥 Видеоматериалы</h2>
        <div class="video-grid">{video_html}</div>

        <h2>📸 Фотоархив</h2>
        <div class="grid">{photo_html}</div>

        <footer style="margin-top: 50px; color: #475569; font-size: 0.9em;">
            © {os.path.getmtime(PHOTO_DIR) if os.path.exists(PHOTO_DIR) else '2026'} ВПК Юный Десантник
        </footer>
    </div>
</body>
</html>'''

    # ЗАПИСЬ В ФАЙЛ
    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Сайт успешно собран в файл: {HTML_OUTPUT}")

if __name__ == "__main__":
    generate_site()