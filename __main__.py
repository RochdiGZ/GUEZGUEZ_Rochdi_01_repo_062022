from scrape_images import scrape_books_images_from
from scrape_informations import scrape_books_informations_from

web_site_url = "http://books.toscrape.com/"

menu = f"""------------------------------------------------------------------------------------------------------------
Bienvenue dans notre application qui nous permet via le lien {web_site_url} de :
1. Extraire les informations de tous les livres pour chaque catégorie et les transformer en un fichier CSV
2. Télécharger et enregistrer toutes les images de livres pour chaque catégorie sous forme des fichiers JPG
------------------------------------------------------------------------------------------------------------"""

if __name__ == '__main__':

    print(menu)

    scrape_books_informations_from(web_site_url)
    scrape_books_images_from(web_site_url)
