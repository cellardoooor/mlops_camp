"""
Скрипт для автоматической загрузки данных Green Taxi Trip Records.
Проверяет наличие файлов и скачивает только отсутствующие.
"""
import os
import urllib.request


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
MONTHS = ["2023-01", "2023-02", "2023-03"]


def download_file(url: str, dest_path: str, month: str) -> bool:
    """Скачать файл по URL и сохранить в dest_path."""
    filename = f"green_tripdata_{month}.parquet"
    full_url = f"{url}/{filename}"
    
    print(f"Скачивание данных за {month}...")
    print(f"URL: {full_url}")
    
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            print(f"\r  Прогресс: {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB)", end="")
        
        urllib.request.urlretrieve(full_url, dest_path, report_progress)
        print(f"\n  ✓ Файл загружен: {dest_path}")
        return True
        
    except Exception as e:
        print(f"\n  ✗ Ошибка при загрузке: {e}")
        return False


def check_file_exists(data_dir: str, month: str) -> bool:
    """Проверить наличие файла данных."""
    filename = f"green_tripdata_{month}.parquet"
    filepath = os.path.join(data_dir, filename)
    exists = os.path.exists(filepath)
    
    if exists:
        size = os.path.getsize(filepath)
        print(f"  ✓ Файл найден: {filename} ({size/1024/1024:.1f}MB)")
    else:
        print(f"  ✗ Файл отсутствует: {filename}")
    
    return exists


def download_all_data(data_dir: str) -> bool:
    """Скачать все необходимые файлы данных."""
    print("=" * 60)
    print("ПРОВЕРКА И ЗАГРУЗКА ДАННЫХ GREEN TAXI")
    print("=" * 60)
    
    os.makedirs(data_dir, exist_ok=True)
    
    all_exist = True
    for month in MONTHS:
        if not check_file_exists(data_dir, month):
            all_exist = False
    
    if all_exist:
        print("\n✓ Все файлы данных уже присутствуют!")
        return True
    
    print("\n" + "-" * 60)
    print("Начинаем загрузку отсутствующих файлов...")
    print("-" * 60)
    
    success_count = 0
    for month in MONTHS:
        filename = f"green_tripdata_{month}.parquet"
        dest_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(dest_path):
            if download_file(BASE_URL, dest_path, month):
                success_count += 1
        else:
            success_count += 1
    
    print("\n" + "=" * 60)
    if success_count == len(MONTHS):
        print(f"✓ Загрузка завершена! {success_count}/{len(MONTHS)} файлов готовы.")
        return True
    else:
        print(f"✗ Загрузка завершена с ошибками: {success_count}/{len(MONTHS)} файлов.")
        return False


if __name__ == "__main__":
    import sys
    
    default_data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data"
    )
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        data_dir = default_data_dir
    
    print(f"Директория для данных: {data_dir}\n")
    
    success = download_all_data(data_dir)
    sys.exit(0 if success else 1)
