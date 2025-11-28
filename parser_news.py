import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

url = "https://web.archive.org/web/20230903112115/https://iz.ru/news"

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 404:
        print("Ошибка: Страница не найдена (404)")
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке страницы: {e}")

else:
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    result = {}
    
    cards = soup.find_all("div", class_="node__cart__item show_views_and_comments")
    
    if len(cards) == 0:
        print("На странице не найдено новостей")
    else:
        for card in cards:
            
            section_tag = card.find("a")
            if section_tag:
                section = section_tag.text.strip()
            else:
                section = "Без раздела"
            
            title_tag = card.find("div", class_="node__cart__item__inside__info__title small-title-style1")
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = None
            
            link_tag = card.find("a", class_="node__cart__item__inside")
            if link_tag:
                raw_link = link_tag.get("href")
            else:
                raw_link = None
            
            if title and raw_link:
                if raw_link.startswith("/"):
                    link = urljoin("https://iz.ru", raw_link)
                else:
                    link = raw_link
                
                if section not in result:
                    result[section] = []
                
                result[section].append({
                    "title": title, 
                    "link": link
                })
        
        if len(result) == 0:
            print("Не удалось извлечь данные из новостей")
        else:
            for section, articles in result.items():
                print(f"'{section}': [")
                for article in articles:
                    print(f"    {{'title': '{article['title']}',")
                    print(f"     'link': '{article['link']}'}},")
                print("]")