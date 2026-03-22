import os
import re

PHOTO_DIR = 'photos'
VIDEO_FILE = 'video_links.txt'
OUTPUT_FILE = 'index.html'

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
    videos = get_video_data()
    photos = get_photos()

    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ВПК Юный Десантник | Лента</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 50px; color: #1c1e21; }}
        header {{ background: white; padding: 15px; text-align: center; border-bottom: 1px solid #ddd; position: sticky; top:0; z-index:100; }}
        .container {{ max-width: 600px; margin: auto; padding: 10px; }}
        .post-card {{ background: white; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); overflow: hidden; display: none; }}
        .post-header {{ padding: 10px; font-weight: bold; border-bottom: 1px solid #eee; }}
        .post-content img {{ width: 100%; display: block; background: #eee; min-height: 200px; }}
        .post-footer {{ padding: 8px; color: #65676b; font-size: 13px; }}
        .video-container {{ position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000; }}
        .video-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }}
        .section-title {{ font-size: 14px; color: #65676b; text-transform: uppercase; margin: 20px 0 10px; font-weight: bold; }}
        #loader {{ text-align: center; padding: 20px; color: #65676b; font-size: 14px; }}
    </style>
</head>
<body>

<header>
    <h1>ВПК «Юный Десантник»</h1>
</header>

<div class="container" id="mainContainer">
    <div class="section-title">🎬 Видеоархив</div>
    <div id="videoList">
    """

    for v in videos:
        html_content += f"""
        <div class="post-card video-item">
            <div class="post-header">{v['title']}</div>
            <div class="video-container">
                <iframe src="https://vk.com/video_ext.php?oid={v['oid']}&id={v['id']}" allowfullscreen loading="lazy"></iframe>
            </div>
        </div>"""

    html_content += """
    </div>
    <div class="section-title">📸 Фотоархив</div>
    <div id="photoList">
    """

    for photo in photos:
        caption = format_date(photo)
        html_content += f"""
        <div class="post-card photo-item">
            <div class="post-content">
                <img src="{PHOTO_DIR}/{photo}" alt="Фото" loading="lazy">
            </div>
            <div class="post-footer">{caption}</div>
        </div>"""

    html_content += """
    </div>
    <div id="loader">Загрузка новых материалов...</div>
</div>

<script>
    let videosShown = 0;
    let photosShown = 0;
    const videosPerLoad = 3;
    const photosPerLoad = 10;
    let isLoading = false;

    function showNext() {
        if (isLoading) return;
        isLoading = true;

        let hasMore = false;

        // Видео
        const videoCards = document.querySelectorAll('.video-item');
        for (let i = videosShown; i < videosShown + videosPerLoad && i < videoCards.length; i++) {
            videoCards[i].style.display = 'block';
            hasMore = true;
        }
        videosShown += videosPerLoad;

        // Фото
        const photoCards = document.querySelectorAll('.photo-item');
        for (let i = photosShown; i < photosShown + photosPerLoad && i < photoCards.length; i++) {
            photoCards[i].style.display = 'block';
        }
        photosShown += photosPerLoad;

        if (videosShown >= videoCards.length && photosShown >= photoCards.length) {
            document.getElementById('loader').innerHTML = 'Вы просмотрели все материалы';
            window.removeEventListener('scroll', handleScroll);
        } else {
            document.getElementById('loader').style.display = 'block';
        }
        
        isLoading = false;
    }

    function handleScroll() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
            showNext();
        }
    }

    window.addEventListener('scroll', handleScroll);
    showNext(); // Первая порция при загрузке
</script>

</body>
</html>
"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Готово! Бесконечная лента настроена.")

if __name__ == "__main__":
    build()