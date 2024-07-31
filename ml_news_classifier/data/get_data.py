from config import NEWS_DATA_API
import os
import aiohttp

async def download_data(file_path):
    link = NEWS_DATA_API
    if os.path.exists(file_path):
        print(f"Файл уже существует: {file_path}")
        return
    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    if response.status == 200:
                        with open(file_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    print(f"Файл успешно загружен и сохранен по пути: {file_path}")
                                    break
                                f.write(chunk)
                    else:
                        print(
                            f"Ошибка при загрузке. Статус код: {response.status}")
        except Exception as e:
            print("Что-то пошло не так при попытке загрузить файл:", e)
            raise e
