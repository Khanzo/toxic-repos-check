# -*- coding: utf-8 -*-
import os
import requests

def recursive_word_search(root_dir, word_list, extensions=None):
    """
    Рекурсивный поиск слов в файлах.

    :param root_dir: Путь к корневой директории
    :param word_list: Список слов для поиска
    :param extensions: Список расширений файлов для поиска (например, ['.txt', '.py'])
    """
    # По умолчанию ищем в текстовых файлах
    if extensions is None:
        extensions = ['.py', '.ts', '.json', '.html', '.css', '.js', '.scss']

    # Приводим слова к нижнему регистру для регистронезависимого поиска
    word_list_lower = [word.lower() for word in word_list]
    result_find = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in extensions:
                continue

            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        line_lower = line.lower()
                        # Проверяем, есть ли хотя бы одно слово из списка в строке
                        for word in word_list_lower:
                            if word in line_lower:
                                result_find.append(f"Найдено в: {file_path} (строка {line_number}): {line.strip()}")
                                break  # Чтобы не дублировать, если найдено несколько слов
            except (UnicodeDecodeError, PermissionError, FileNotFoundError):
                # Пропускаем бинарные или недоступные файлы
                pass
    with open('resultFind.log', 'w') as f:
        for item in result_find:
            f.write(str(item) + '\n')

url = "https://raw.githubusercontent.com/toxic-repos/toxic-repos/refs/heads/main/IoC.Txt"
script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    response = requests.get(url)
    response.raise_for_status()
    word_list = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
    recursive_word_search(script_dir, word_list)
    print('ok')

except requests.exceptions.RequestException as e:
    print(f"Ошибка при скачивании: {e}")