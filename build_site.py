import os
from urllib.parse import quote

# Настройки
LINKS_FILE = 'video_links.txt'
HTML_OUTPUT = 'Index.html'
PREVIEW_DIR = 'TO_VK'
PHOTOS_DIR = 'photos'

def build():
    video_html = ""
    
    # Поиск превью для видео
    available_previews = {}
    if os.path.exists(PREVIEW_DIR):
        for f in os.listdir(PREVIEW_DIR):
            available_previews[f.lower()] = f

    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    title, link = line.strip().split('|')
                    found_file = None
                    # Пробуем найти превью по названию
                    possible = [f"{title}.mp4_thumb.jpg".lower(), f"{title}.jpg".lower()]
                    for p_name in possible:
                        if p_name in available_previews:
                            found_file = available_previews[p_name]
                            break
                    
                    img_path = quote(f"{PREVIEW_DIR}/{found_file}") if found_file else "https://via.placeholder.com/280x160"

                    video_html += f'''
                    <div style="display:inline-block; width:280px; margin:10px; border:1px solid #ccc; background:#fff; border-radius:10px; overflow:hidden;">
                        <a href="{link}" target="_blank" style="text-decoration:none; color:#000;">
                            <img src="{img_path}" style="width:100%; height:160px; object-fit:cover;">
                            <div style="padding:10px; font-weight:bold; font-size:13px;">{title}</div>
                        </a>
                    </div>'''

    # Исправленная Фотогалерея
    photo_html = ""
    if os.path.exists(PHOTOS_DIR):
        # Берем только файлы .jpg, которые НЕ являются миниатюрами (_thumb)
        all_files = os.listdir(PHOTOS_DIR)
        photos = [f for f in all_files if f.lower().endswith('.jpg') and '_thumb' not in f.lower()]
        
        for p in sorted(photos):
            encoded_path = quote(f"{PHOTOS_DIR}/{p}")
            photo_html += f'''
            <a href="{encoded_path}" target="_blank">
                <img src="{encoded_path}" style="width:200px; height:150px; object-fit:cover; margin:5px; border-radius:5px; border:1px solid #ddd;">
            </a>'''

    # Сборка страницы
    full_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>ВПК Юный десантник - Архив</title>
    <style>
        body {{ background:#f4f4f4; font-family: sans-serif; text-align:center; padding:20px; }}
        .container {{ max-width:1200px; margin:0 auto; background:#fff; padding:20px; border-radius:10px; }}
        .gallery {{ display:flex; flex-wrap:wrap; justify-content:center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Видеоархив</h1>
        <div class="gallery">{video_html}</div>
        <h1 style="margin-top:40px;">Фотогалерея</h1>
        <div class="gallery">{photo_html}</div>
    </div>
</body>
</html>'''

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Готово! Index.html обновлен.")

if __name__ == "__main__":
    build()