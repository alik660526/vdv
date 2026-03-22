import os
import re

PHOTO_DIR = 'photos'
VIDEO_FILE = 'video_links.txt'
OUTPUT_FILE = 'index.html'
LOGO_PATH = 'images/logo.jpg'
THUMBS_DIR = 'v-thumbs'

def format_date(filename):
    # Ищем дату в формате @16-10-2022_20-27-34
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
                    raw_name = parts[0]
                    url = parts[1]
                    match = re.search(r'video(\d+)_(\d+)', url)
                    if match:
                        thumb_name = f"{raw_name}.mp4_thumb.jpg"
                        thumb_path = os.path.join(THUMBS_DIR, thumb_name)
                        videos.append({
                            'title': raw_name.replace('_', ' '), 
                            'oid': match.group(1), 
                            'id': match.group(2),
                            'thumb': thumb_path if os.path.exists(thumb_path) else None
                        })
    return videos

def get_photos_data():
    if not os.path.exists(PHOTO_DIR): return []
    # Собираем список словарей с именем файла и форматированной датой
    photos = []
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith('.webp') and '_thumb' not in f]
    # Сортируем по дате изменения файла (самые свежие сверху)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(PHOTO_DIR, x)), reverse=True)
    
    for f in files:
        photos.append({
            'file': f,
            'date': format_date(f)
        })
    return photos

def build():
    v_data = get_video_data()
    p_data = get_photos_data()

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ВПК Юный Десантник</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 50px; color: #1c1e21; }}
        header {{ background: white; padding: 25px 15px; text-align: center; border-bottom: 1px solid #ddd; position: relative; }}
        .logo {{ max-width: 160px; height: auto; margin-bottom: 12px; display: block; margin-left: auto; margin-right: auto; }}
        h1 {{ font-size: 22px; margin: 0; color: #003366; }}
        
        .container {{ max-width: 600px; margin: auto; padding: 10px; }}
        .post-card {{ background: white; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; }}
        .post-header {{ padding: 15px; font-weight: bold; border-bottom: 1px solid #eee; background: #fafafa; font-size: 14px; }}
        
        .video-box {{ position: relative; padding-bottom: 56.25%; height: 0; background: #003366; cursor: pointer; }}
        .video-box img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }}
        .play-btn {{
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 70px; height: 50px; background: rgba(255,0,0,0.9); border-radius: 10px; 
            display: flex; align-items: center; justify-content: center; z-index: 5;
        }}
        .play-btn::after {{ content: ''; border-style: solid; border-width: 10px 0 10px 18px; border-color: transparent transparent transparent white; margin-left: 4px; }}
        
        iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; z-index: 10; }}
        .post-content img {{ width: 100%; display: block; background: #eee; min-height: 250px; }}
        
        .section-title {{ font-size: 18px; color: #003366; text-transform: uppercase; margin: 35px 0 15px; font-weight: bold; border-left: 6px solid #003366; padding-left: 12px; }}
        #loader {{ text-align: center; padding: 30px; color: #65676b; font-style: italic; }}
    </style>
</head>
<body>

<header>
    <img src="{LOGO_PATH}" alt="Логотип" class="logo">
    <h1>ВПК «Юный Десантник»</h1>
</header>

<div class="container">
    <div class="section-title">🎬 Видеоархив</div>
    <div id="videoList">
    """

    for v in v_data:
        img_tag = f'<img src="{v["thumb"]}" loading="lazy">' if v['thumb'] else ''
        html_content += f"""
        <div class="post-card v-item" data-oid="{v['oid']}" data-id="{v['id']}">
            <div class="post-header">{v['title']}</div>
            <div class="video-box" onclick="runVideo(this)">
                {img_tag}
                <div class="play-btn"></div>
            </div>
        </div>"""

    html_content += f"""
    </div>
    <div class="section-title">📸 Фотоархив</div>
    <div id="photoList"></div>
    <div id="loader">Листайте вниз для загрузки фото...</div>
</div>

<script>
    const photoData = {p_data}; // Теперь здесь и файл, и дата
    const pDir = "{PHOTO_DIR}";
    let pIdx = 0;

    function runVideo(div) {{
        document.querySelectorAll('.v-item').forEach(item => {{
            const box = item.querySelector('.video-box');
            if (box !== div && box.querySelector('iframe')) {{
                const thumb = box.dataset.oldImg || '';
                box.innerHTML = (thumb ? `<img src="${{thumb}}">` : '') + '<div class="play-btn"></div>';
            }}
        }});
        const parent = div.closest('.v-item');
        const img = div.querySelector('img');
        if(img) div.dataset.oldImg = img.src;
        div.innerHTML = `<iframe src="https://vk.com/video_ext.php?oid=${{parent.dataset.oid}}&id=${{parent.dataset.id}}&autoplay=1" allow="autoplay" allowfullscreen></iframe>`;
    }}

    function loadP() {{
        const list = document.getElementById('photoList');
        const limit = pIdx + 20;
        for(; pIdx < limit && pIdx < photoData.length; pIdx++) {{
            const item = photoData[pIdx];
            const card = document.createElement('div');
            card.className = 'post-card';
            card.innerHTML = `
                <div class="post-header">${{item.date}}</div>
                <div class="post-content"><img src="${{pDir}}/${{item.file}}" loading="lazy"></div>
            `;
            list.appendChild(card);
        }}
        if(pIdx >= photoData.length) {{
            document.getElementById('loader').innerText = "— Конец архива —";
        }}
    }}

    window.onscroll = () => {{ if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1200) loadP(); }};
    loadP();
</script>
</body>
</html>
"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Исправлено! Даты под фото вернулись.")

if __name__ == "__main__":
    build()