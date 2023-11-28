#https://v2.vost.pw/

import requests
import re
from bs4 import BeautifulSoup
import os

def download_and_rename_video(url, save_folder, new_filename):
    try:
        # Проверяем, существует ли файл с новым именем в указанной папке
        save_path = os.path.join(save_folder, new_filename)
        if os.path.exists(save_path):
            print(f"Файл {new_filename} уже существует. Пропускаем скачивание.")
            return True  # Возвращаем True, чтобы показать, что файл уже существует

        # Отправляем GET-запрос на страницу с видео
        response = requests.get(url, stream=True)

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Проверяем, существует ли указанная папка, иначе создаем ее
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            # Сохраняем видео в файл
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"Видео успешно скачано и сохранено в {save_path}")
            return True  # Возвращаем True, чтобы показать, что файл успешно скачан
        else:
            print(f"Ошибка при получении видео. Код ответа: {response.status_code}")
            return False  # Возвращаем False, чтобы показать, что произошла ошибка при скачивании
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False  # Возвращаем False, чтобы показать, что произошла ошибка при скачивании


url = input("url:")
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Ищем название аниме на странице
    anime_title = soup.find('div', class_='shortstoryHead').find('h1').get_text(strip=True)
    anime_folder = "".join(char for char in anime_title if char.isalnum() or char in (' ', '_'))

    # Извлекаем JavaScript-код из HTML-страницы
    js_code = re.search(r"var data = ({.*?});", response.text, re.DOTALL)
    if js_code:
        data = js_code.group(1)
        # Преобразуем строку в словарь
        data_dict = eval(data)
        total_episodes = len(data_dict)
        downloaded_episodes = 0

        # Теперь у вас есть доступ к названиям серий и их айди
        for episode, episode_id in data_dict.items():
            print(f"Серия {episode}: {episode_id}")
            # Пример использования
            video_url = f"https://hd.trn.su/720/{episode_id}.mp4"
            new_filename = f"{episode}.mp4"

            if download_and_rename_video(video_url, anime_folder, new_filename):
                downloaded_episodes += 1

        print(f"\nИнформация о скачанных сериях:")
        print(f"Всего серий: {total_episodes}")
        print(f"Скачано серий: {downloaded_episodes}")
        # Добавленная строка для ожидания ввода перед закрытием консоли
        input("Press Enter to exit")
    else:
        print("Не удалось найти JavaScript-объект data на странице.")
else:
    print(f"Ошибка при получении страницы: {response.status_code}")
