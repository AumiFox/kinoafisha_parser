import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd


def parse_user_ratings_fast(user_id):
    """
    Быстрый парсинг оценок пользователя (только 1 страница)
    """
    scraper = cloudscraper.create_scraper()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    url = f"https://www.kinoafisha.info/user/{user_id}/votes/"
    print(f"Загрузка страницы...")

    response = scraper.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все блоки с оценками
    rating_items = soup.find_all('div', class_='profileRatingsList_item')

    if not rating_items:
        print("Оценки не найдены!")
        return []

    data = []
    for item in rating_items:
        title_tag = item.find('a', class_='profileRatingsList_title')
        rating_tag = item.find('span', class_='mark_num')

        if title_tag and rating_tag:
            data.append({
                'название_фильма': title_tag.text.strip(),
                'оценка_пользователя': rating_tag.text.strip()
            })

    return data


# --- ЗАПУСК ---
if __name__ == "__main__":
    user_id = 14287287  # Пользователь Comon

    print(f"Парсинг оценок пользователя ID: {user_id}")
    data = parse_user_ratings_fast(user_id)

    if data:
        df = pd.DataFrame(data)
        filename = f'user_{user_id}_ratings.xlsx'
        df.to_excel(filename, index=False)

        print(f"\n Парсинг Завершён!")
        print(f" Собрано оценок: {len(data)}")
        print(f" Файл сохранен: {filename}")

        # Показываем первые 10
        print(f"\nПервые 10 оценок пользователя:")
        for i, row in df.head(10).iterrows():
            print(f"  {i + 1}. {row['название_фильма'][:50]} - {row['оценка_пользователя']}/10")
    else:
        print(" Данные не найдены!")