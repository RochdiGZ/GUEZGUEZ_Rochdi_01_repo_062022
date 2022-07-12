from scrape_images import scrape_books_images_from
from scrape_informations import get_categories_urls, save_books_informations

web_site_url = "http://books.toscrape.com/"
menu = f"""------------------------------------------------------------------------------------------------------------
Bienvenue dans notre application qui nous permet via le lien {web_site_url} de :
1. Extraire les informations de tous les livres pour chaque catégorie et les transformer en un fichier CSV
2. Télécharger et enregistrer toutes les images de livres pour chaque catégorie sous forme des fichiers JPG
------------------------------------------------------------------------------------------------------------"""
print(menu)
print("1. Exécution en cours pour extraire les informations de tous les livres pour chaque catégorie ...")
categories = get_categories_urls(web_site_url)
for category in categories:
    save_books_informations(category)
print("2. Exécution en cours pour télécharger et enregistrer toutes les images de livres ...")
for category in categories:
    save_books_images(category, web_site_url)
