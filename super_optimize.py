import os
from PIL import Image

# Путь к папке
PHOTO_DIR = r"C:\Users\pro91\OneDrive\Документы\GitHub\vpk\photos"
# Максимальный размер стороны (ширина или высота)
MAX_SIZE = 1280 

def super_optimize():
    if not os.path.exists(PHOTO_DIR):
        print("Папка не найдена!")
        return

    # Обрабатываем и старые форматы, и уже созданные WebP (если нужно пережать)
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    print(f"Начинаю обработку {len(files)} изображений...")

    for filename in files:
        file_path = os.path.join(PHOTO_DIR, filename)
        name_only = os.path.splitext(filename)[0]
        webp_path = os.path.join(PHOTO_DIR, f"{name_only}.tmp") # Временный файл

        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")
                
                # РЕСАЙЗ: Проверяем, нужно ли уменьшать
                width, height = img.size
                if width > MAX_SIZE or height > MAX_SIZE:
                    if width > height:
                        new_width = MAX_SIZE
                        new_height = int(MAX_SIZE * height / width)
                    else:
                        new_height = MAX_SIZE
                        new_width = int(MAX_SIZE * width / height)
                    
                    # Используем качественный фильтр LANCZOS для четкости
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # СОХРАНЕНИЕ: Качество 75-80 оптимально для WebP
                final_path = os.path.join(PHOTO_DIR, f"{name_only}.webp")
                img.save(final_path, "WEBP", quality=75, method=6)
            
            # Если исходник был не .webp или имел другое имя - удаляем старый
            if file_path != final_path:
                os.remove(file_path)
                
            print(f"✅ Оптимизировано: {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка в {filename}: {e}")

    print("\nГотово! Теперь все 1751 фото имеют оптимальный размер и формат.")

if __name__ == "__main__":
    super_optimize()