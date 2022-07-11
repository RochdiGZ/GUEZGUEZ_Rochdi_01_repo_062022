import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from scrape_informations import get_pages_urls_of_category, get_categories_names, get_categories_urls


def scrape_books_images_from(home_url: str):
    print("Exécution en cours pour télécharger et enregistrer toutes les images de livres ...")
    folders_names = get_categories_names(home_url)
    categories_urls = get_categories_urls(home_url)
    for i in range(len(categories_urls)):
        folder_name = folders_names[i]
        relative_path = 'data/images/' + folder_name + '/'
        folder = Path(relative_path)
        folder.mkdir(parents=True, exist_ok=True)
        category_pages_urls = get_pages_urls_of_category(categories_urls[i])
        for page_url in category_pages_urls:
            response = requests.get(page_url)
            page_soup = BeautifulSoup(response.content, 'html.parser')
            all_tags_img = page_soup.find_all("img", class_="thumbnail")
            for tag_img in all_tags_img:
                image_url = tag_img['src'].replace("../../../../", home_url)
                image_title = tag_img['alt']
                image_name = re.sub(r"[\-!=$é%&.|:(){}[\]?#\"*+/,']*", "", image_title)
                image_format='.jpg'
                path_length = len(str(Path.cwd())) + len(relative_path) + len(image_format)
                if len(image_name) > 255 - path_length:
                    image_name = image_name[:255 - path_length - len(image_format)]
                    print('image_name:', image_name)
                with open(relative_path + image_name + image_format, 'wb') as jpg_file:
                    response = requests.get(image_url)
                    jpg_file.write(response.content)
