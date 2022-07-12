from extract_images import save_books_images
from extract_informations import save_books_informations
from modules_to_import import get_categories_urls, website_url

menu = f"""------------------------------------------------------------------------------------------------------------
Bienvenue dans notre application qui nous permet via le lien {website_url} de :
1. Extraire les informations de tous les livres pour chaque catégorie et les transformer en un fichier CSV
2. Télécharger et enregistrer toutes les images de livres pour chaque catégorie sous forme des fichiers JPG
------------------------------------------------------------------------------------------------------------"""
print(menu)
print("1. Exécution en cours pour extraire les informations de tous les livres pour chaque catégorie ...")
categories = get_categories_urls(website_url)
for category in categories:
    save_books_informations(category)
print("2. Exécution en cours pour télécharger et enregistrer toutes les images de livres ...")
for category in categories:
    save_books_images(category)
