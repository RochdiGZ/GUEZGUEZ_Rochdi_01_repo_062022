import re
import requests
from pathlib import Path
from modules_to_import import get_html_code_from, get_pages_urls_of_category, website_url


def save_page_images(page_url: str, relative_path: str):
    page_soup = get_html_code_from(page_url)
    all_tags_img = page_soup.find_all("img", class_="thumbnail")
    for tag_img in all_tags_img:
        image_url = tag_img['src'].replace("../../../../", website_url)
        image_title = tag_img['alt']
        image_name = re.sub(r"[\-!=$é%&.|:(){}[\]?#\"*+/,']*", "", image_title)
        image_format = '.jpg'
        path_length = len(str(Path.cwd())) + len(relative_path) + len(image_format)
        if len(image_name) > 255 - path_length:
            image_name = image_name[:255 - path_length - len(image_format)]
        with open(relative_path + image_name + image_format, 'wb') as jpg_file:
            response = requests.get(image_url)
            jpg_file.write(response.content)


def save_books_images(category_url: str):
    # Extraire le nom de la catégorie de livres
    category_soup = get_html_code_from(category_url)
    category_name = category_soup.find('ul', class_="breadcrumb").find_all('li')[2].get_text().strip()
    # Créer un dossier portant le nom de la catégorie
    relative_path = 'data/images/' + category_name + '/'
    folder = Path(relative_path)
    folder.mkdir(parents=True, exist_ok=True)
    # Extraire le(s) lien(s) de page(s) de livres pour une catégorie
    category_pages_urls = get_pages_urls_of_category(category_url)
    for page_url in category_pages_urls:
        save_page_images(page_url, relative_path)
