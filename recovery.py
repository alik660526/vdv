import requests
import os

# ВАШ НОВЫЙ ТОКЕН И ЛИЧНЫЙ ID
TOKEN = 'vk1.a.vrPsFztCyZz1F0TwwqVC8ggyd0otEOh9W0T5svU3XT5yEIJd_XyYny_Zbz4-j41rlLM4GhDwG7lRgcgwe7C8w5jQrvD0gzg7qmyWahWashUt1n-dJXahuSF5jtZZlFhMfQBOQgqX0QxR8mh4YBSLO8PSK5wEU7xMul5BWeLL0unbnC0iYvBfGs6p6ms9CV8W-Fq_JwkJpXx2E7w8wM5cNA'
MY_ID = 604021725  # Ваш ID пользователя
TARGET_DIR = r'C:\Users\pro91\Desktop\ARCHIVE_VPC'

def run_recovery():
    print(f"Ищем видео в профиле ID: {MY_ID}...")
    
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    
    url = "https://api.vk.com/method/video.get"
    # Запрашиваем все видео профиля, включая загруженные в альбомы
    params = {
        'owner_id': MY_ID,
        'count': 100,
        'access_token': TOKEN,
        'v': '5.131'
    }

    try:
        response = requests.get(url, params=params).json()
        
        if 'error' in response:
            print(f"ОШИБКА ВК: {response['error']['error_msg']}")
        else:
            videos = response['response']['items']
            if not videos:
                print("Видео не найдено. Проверьте настройки приватности в ВК (должно быть 'Видно всем').")
                return

            file_path = os.path.join(TARGET_DIR, 'video_links.txt')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for v in videos:
                    title = v.get('title', 'video')
                    link = f"https://vk.com/video{v['owner_id']}_{v['id']}"
                    f.write(f"{title}|{link}\n")
            
            print("*" * 40)
            print(f"УСПЕХ! Найдено видео в профиле: {len(videos)}")
            print(f"Файл создан: {file_path}")
            print("*" * 40)
            
    except Exception as e:
        print(f"ОШИБКА: {e}")

    input("\nНажмите Enter, чтобы закрыть окно...")

if __name__ == "__main__":
    run_recovery()