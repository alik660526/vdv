import os
import re

PHOTO_DIR = 'photos'
VIDEO_FILE = 'video_links.txt'
OUTPUT_FILE = 'index.html'
LOGO_PATH = 'images/logo.jpg' 

def format_date(filename):
    match = re.search(r'@(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{2})', filename)
    if match:
        date_str, time_str = match.groups()
        return f"📅 {date_str} в {time_str.replace('-', ':')}"
    return "Архив ВПК"

def get_video_data():
    videos = []
    if os.path.exists(VIDEO_FILE):
        with open(VIDEO_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    url = parts[1]
                    match = re.search(r'video(\d+)_(\d+)', url)
                    if match:
                        videos.append({
                            'title': parts[0].replace('_', ' '), 
                            'oid': match.group(1), 
                            'id': match.group(2)
                        })
    return videos

def get_photos():
    if not os.path.exists(PHOTO_DIR): return []
    photos = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith('.webp') and '_thumb' not in f]
    photos.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTO_DIR, x)), reverse=True)
    return photos

def build():
    v_data = get_video_data()
    p_data = get_photos()

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ВПК Юный Десантник</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 50px; color: #1c1e21; }}
        header {{ background: white; padding: 20px 15px; text-align: center; border-bottom: 1px solid #ddd; position: sticky; top:0; z-index:100; }}
        .logo {{ max-width: 180px; height: auto; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto; }}
        .container {{ max-width: 600px; margin: auto; padding: 10px; }}
        .post-card {{ background: white; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); overflow: hidden; }}
        .post-header {{ padding: 12px; font-weight: bold; border-bottom: 1px solid #eee; }}
        .post-content img {{ width: 100%; display: block; background: #ddd; min-height: 250px; }}
        .video-container {{ position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000; }}
        .video-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}
        .section-title {{ font-size: 16px; color: #0056b3; text-transform: uppercase; margin: 30px 0 15px; font-weight: bold; border-left: 5px solid #0056b3; padding-left: 10px; }}
        #loader {{ text-align: center; padding: 40px; color: #65676b; font-style: italic; }}
    </style>
</head>
<body>

<header>
    <img src="{LOGO_PATH}" alt="Логотип" class="logo">
    <h1>ВПК «Юный Десантник»</h1>
</header>

<div class="container">
    <div class="section-title">🎬 Видеоархив (Всего: {len(v_data)})</div>
    <div id="videoList">
    """

    # Видео выводим ВСЕ СРАЗУ
    for v in v_data:
        html_content += f"""
        <div class="post-card">
            <div class="post-header">{v['title']}</div>
            <div class="video-container">
                <iframe src="https://vk.com/video_ext.php?oid={v['oid']}&id={v['id']}" allowfullscreen loading="lazy"></iframe>
            </div>
        </div>"""

    html_content += f"""
    </div>
    
    <div class="section-title">📸 Фотоархив</div>
    <div id="photoList"></div>
    
    <div id="loader">Листайте вниз для загрузки фото...</div>
</div>

<script>
    const allPhotos = {p_data};
    const photoDir = "{PHOTO_DIR}";
    let currentP = 0;
    const pStep = 20;

    function loadPhotos() {{
        const pList = document.getElementById('photoList');
        for(let i=0; i<pStep && currentP < allPhotos.length; i++) {{
            const p = allPhotos[currentP++];
            const div = document.createElement('div');
            div.className = 'post-card';
            div.innerHTML = `<div class="post-content"><img src="${{photoDir}}/${{p}}" loading="lazy"></div>`;
            pList.appendChild(div);
        }}
        if(currentP >= allPhotos.length) {{
            document.getElementById('loader').innerHTML = "— Все фото загружены —";
            window.removeEventListener('scroll', handleScroll);
        }}
    }}

    function handleScroll() {{
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1500) {{
            loadPhotos();
        }}
    }}

    window.addEventListener('scroll', handleScroll);
    loadPhotos(); // Первая пачка фото
</script>
</body>
</html>
"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Сайт пересобран. Видео — все сразу, фото — лентой.")

if __name__ == "__main__":
    build()