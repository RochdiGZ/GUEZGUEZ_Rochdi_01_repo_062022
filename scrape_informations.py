import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
site_url = "http://books.toscrape.com/"
# Définir une liste contenant les clés des données pour un livre
keys = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
        "number_available", "product_description", "category", "review_rating", "image_url"]


def get_html_code_from(page_url: str) -> BeautifulSoup:
    response = requests.get(page_url)
    return BeautifulSoup(response.content, 'html.parser')


def scrape_all_tags_li_soup(home_url: str) -> list:
    home_soup = get_html_code_from(home_url)
    # Ne pas parser la balise <li> d'indice 0
    all_li = home_soup.find('ul', class_="nav nav-list").find_all('li')[1:]
    return all_li


def get_categories_urls(home_url: str) -> list:
    categories_urls = []
    all_li = scrape_all_tags_li_soup(home_url)
    for li in all_li:
        categories_urls.append(home_url + li.find("a")["href"])
    return categories_urls


def get_categories_names(home_url: str) -> list:
    categories_names = []
    all_li = scrape_all_tags_li_soup(home_url)
    for li in all_li:
        categories_names.append(li.get_text().strip())
    return categories_names


def get_books_urls_of_page(page_url: str) -> list:
    books_page_urls = []
    books_page_soup = get_html_code_from(page_url)
    titles = books_page_soup.find_all("h3")
    for title in titles:
        book_url = title.find("a")["href"].replace("../../..", site_url + 'catalogue')
        books_page_urls.append(book_url)
    return books_page_urls


def get_all_books_urls(category_url: str) -> list:
    all_books_urls = []
    pages_urls = get_pages_urls_of_category(category_url)
    for page_url in pages_urls:
        all_books_urls.append(get_books_urls_of_page(page_url))
    return all_books_urls


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


def new_file_csv(file_name: str, fieldnames: list):
    folder = Path("data/csv_files/")
    folder.mkdir(parents=True, exist_ok=True)
    with open('data/csv_files/' + file_name + '.csv', 'w', encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file, lineterminator="\n", delimiter=",")
        # Charger la première ligne du fichier csv contenant les clés des données
        writer.writerow(fieldnames)


def scrape_book_data(book_url: str) -> dict:
    book_soup = get_html_code_from(book_url)
    # Extraire le lien, la catégorie et le titre d'un livre
    ul_soup = book_soup.find('ul', class_="breadcrumb")
    book_category = ul_soup.find_all('li')[2].get_text().strip()
    # book_title = ul_soup.find_all('li')[3].get_text().strip()
    # Extraire le lien de l'image d'un livre
    img_soup = book_soup.find(id="product_gallery").find("img")
    book_image_url = img_soup["src"].replace("../../", site_url)
    book_title = img_soup["alt"]
    # Déterminer le code, le prix ht, le prix ttc et la disponibilité d'un livre
    table_soup = book_soup.find('table')
    book_code = table_soup.find_all("td")[0].get_text()
    book_price_excluding_tax = table_soup.find_all("td")[2].get_text()
    book_price_including_tax = table_soup.find_all("td")[3].get_text()
    book_availability = table_soup.find_all("td")[5].get_text()
    # Déterminer la description d'un livre
    soup_div = book_soup.find(id="product_description")
    if soup_div:
        book_description = soup_div.find_next_sibling("p").get_text()
    else:
        book_description = "..."
    # Déterminer la note en étoiles d'un livre
    div_soup = book_soup.find("div", class_="col-sm-6 product_main")
    book_review_rating = div_soup.find_all("p")[2].get('class')[1] + " star(s)"
    # Sauvegarder les informations d'un livre dans un dictionnaire
    book_info = [book_url, book_code, book_title, book_price_including_tax, book_price_excluding_tax,
                 book_availability, book_description, book_category, book_review_rating, book_image_url]
    book_informations = {keys[0]: book_info[0], keys[1]: book_info[1],
                         keys[2]: book_info[2], keys[3]: book_info[3],
                         keys[4]: book_info[4], keys[5]: book_info[5],
                         keys[6]: book_info[6], keys[7]: book_info[7],
                         keys[8]: book_info[8], keys[9]: book_info[9]}
    return book_informations


def save_book_data(file_name: str, book_data: dict):
    relative_path = 'data/csv_files/'
    folder = Path(relative_path)
    folder.mkdir(parents=True, exist_ok=True)
    with open(relative_path + file_name + '.csv', 'a', newline='', encoding='UTF-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys, lineterminator="\n", delimiter=",")
        writer.writerow(book_data)


def scrape_category_name(page_url: str) -> str:
    category_soup = get_html_code_from(page_url)
    category_name = category_soup.find('ul', class_="breadcrumb").find_all('li')[2].get_text().strip()
    return category_name


def save_books_informations(category_url: str):
    file_name = scrape_category_name(category_url)
    # Créer un fichier csv portant le nom de la catégorie
    new_file_csv(file_name, keys)
    # Définir les url(s) de page(s) d'une catégorie
    pages_urls = get_pages_urls_of_category(category_url)
    for page_url in pages_urls:
        books_urls = get_books_urls_of_page(page_url)
        for book_url in books_urls:
            book_data = scrape_book_data(book_url)
            save_book_data(file_name, book_data)


def scrape_books_informations_from(home_url: str):
    print("Exécution en cours pour extraire les informations de tous les livres pour chaque catégorie ...")
    categories = get_categories_urls(home_url)
    for category in categories:
        save_books_informations(category)
