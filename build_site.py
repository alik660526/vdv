import os

# Пути к вашим папкам
BASE_DIR = r'C:\Users\pro91\OneDrive\Документы\GitHub\vpk'
LINKS_FILE = os.path.join(BASE_DIR, 'video_links.txt')
HTML_OUTPUT = os.path.join(BASE_DIR, 'Index.html')
PREVIEW_DIR = 'TO_VK'
PHOTOS_DIR = 'photos'

def build():
    # 1. СОБИРАЕМ ВИДЕО
    video_html = ""
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Получаем список всех файлов в папке TO_VK для поиска
        all_previews = os.listdir(os.path.join(BASE_DIR, PREVIEW_DIR)) if os.path.exists(os.path.join(BASE_DIR, PREVIEW_DIR)) else []

        for line in lines:
            if '|' in line:
                title, link = line.strip().split('|')
                
                # Ищем подходящую картинку в TO_VK
                img_path = "images/default_video.jpg" # Заглушка
                for p in all_previews:
                    if title.lower() in p.lower() or p.lower() in title.lower():
                        img_path = f"{PREVIEW_DIR}/{p}"
                        break
                
                video_html += f'''
                <div style="display:inline-block; width:250px; margin:10px; border:1px solid #ccc; border-radius:8px; overflow:hidden; vertical-align:top; background:white;">
                    <a href="{link}" target="_blank" style="text-decoration:none; color:black;">
                        <img src="{img_path}" style="width:100%; height:140px; object-fit:cover;" onerror="this.src='https://via.placeholder.com/250x140?text=Video'">
                        <p style="padding:5px; font-size:12px; height:30px; overflow:hidden;">{title}</p>
                    </a>
                </div>'''

    # 2. СОБИРАЕМ ФОТОГРАФИИ (из папки photos)
    photo_html = ""
    if os.path.exists(os.path.join(BASE_DIR, PHOTOS_DIR)):
        all_photos = [f for f in os.listdir(os.path.join(BASE_DIR, PHOTOS_DIR)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for photo in all_photos:
            photo_html += f'<img src="{PHOTOS_DIR}/{photo}" style="width:200px; margin:5px; border-radius:5px; border:1px solid #ddd;">'

    # 3. ИТОГОВЫЙ HTML
    full_html = f'''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Архив ВПК "Юный десантник"</title>
        <style>
            body {{ font-family: Arial; background: #f0f0f0; padding: 20px; text-align: center; }}
            .section {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h2 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>ВПК "Юный десантник" - Полный Архив</h1>
        
        <div class="section">
            <h2>Видео из ВК (38 шт.)</h2>
            <div>{video_html}</div>
        </div>

        <div class="section">
            <h2>Фотогалерея</h2>
            <div>{photo_html}</div>
        </div>
    </body>
    </html>
    '''

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Готово! Проверьте Index.html. Видео: {len(lines)}, Фото: {len(all_photos if 'all_photos' in locals() else [])}")

if __name__ == "__main__":
    build()