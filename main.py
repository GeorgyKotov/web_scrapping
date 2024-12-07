from pprint import pprint
import requests
import bs4

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

if __name__ == '__main__':
    response = requests.get('https://habr.com/ru/articles/')
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles_list = soup.select_one('div.tm-articles-list')
    articles = articles_list.select('div.tm-article-snippet')
    parsed_data = []
    for article in articles:
        link = 'https://habr.com' + article.select_one('a.tm-article-datetime-published_link')['href']
        article_response = requests.get(link)
        article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
        header = article_soup.select_one('h1').text
        text_body = article_soup.select_one('div.tm-article-body').text
        for keyword in KEYWORDS:
            if keyword in header.lower() or keyword in text_body.lower():
                time = article_soup.select_one('time')['datetime']
                parsed_data.append({
                    'Дата': time,
                    'Заголовок': header,
                    'Ссылка': link
                })
                break
    pprint(parsed_data)