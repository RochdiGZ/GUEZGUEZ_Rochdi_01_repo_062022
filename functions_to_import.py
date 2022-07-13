import requests
from bs4 import BeautifulSoup

website_url = "http://books.toscrape.com/"


def get_html_code_from(page_url: str) -> BeautifulSoup:
    response = requests.get(page_url)
    return BeautifulSoup(response.content, 'html.parser')


def get_categories_urls(home_url: str) -> list:
    categories_urls = []
    home_soup = get_html_code_from(home_url)
    # Ne pas parser la balise <li> d'indice 0
    all_li = home_soup.find('ul', class_="nav nav-list").find_all('li')[1:]
    for li in all_li:
        categories_urls.append(home_url + li.find("a")["href"])
    return categories_urls


def get_pages_number_from(category_url: str) -> int:
    category_soup = get_html_code_from(category_url)
    # Extraire le nombre de livres par catégorie
    tag_form = category_soup.find("form", class_="form-horizontal")
    books_number = int(tag_form.find("strong").get_text())
    # Déterminer le nombre de pages web correspondant à une catégorie
    if books_number <= 20:
        pages_number = 1
    else:
        if books_number // 20 == 0:
            pages_number = books_number // 20
        else:
            pages_number = books_number // 20 + 1
    return pages_number


def get_pages_urls_of_category(category_url: str) -> list:
    pages_number = get_pages_number_from(category_url)
    category_pages_urls = [category_url]
    if pages_number > 1:
        for number in range(2, pages_number+1):
            next_page_url = category_url.replace("index", f"page-{number}")
            category_pages_urls.append(next_page_url)
    return category_pages_urls
