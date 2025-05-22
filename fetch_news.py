import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from urllib.parse import urljoin, urlparse

# Configuration
DEXERTO_URL = "https://www.dexerto.com/gaming/"
POST_URL = "https://gamemasterx.great-site.net/test_post.php"  # URL de post_news.php
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
MAX_ARTICLES = 3  # Nombre d'articles à récupérer
DELAY = 2  # Délai en secondes entre requêtes pour éviter le bannissement

def clean_text(text):
    """Nettoie le texte des caractères indésirables"""
    if not text:
        return ''
    return text.strip().replace('\n', ' ').replace('\r', '').replace('\t', ' ')

def normalize_url(base_url, link):
    """Transforme un lien relatif en lien absolu"""
    if not link:
        return ''
    return urljoin(base_url, link)

def fetch_and_post():
    try:
        print(f"Récupération des articles depuis {DEXERTO_URL}...")
        response = requests.get(DEXERTO_URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".news-archive__item")[:MAX_ARTICLES]

        if not articles:
            print("Aucun article trouvé - vérifie les sélecteurs CSS.")
            return

        for i, article in enumerate(articles, 1):
            try:
                print(f"\nTraitement de l'article {i}/{len(articles)}...")

                title_tag = article.select_one(".news-archive__title")
                excerpt_tag = article.select_one(".news-archive__excerpt")
                link_tag = article.find("a", href=True)
                image_tag = article.find("img")

                title = clean_text(title_tag.get_text()) if title_tag else ''
                content = clean_text(excerpt_tag.get_text()) if excerpt_tag else ''
                link = normalize_url(DEXERTO_URL, link_tag['href']) if link_tag else ''
                image_url = normalize_url(DEXERTO_URL, image_tag['src']) if image_tag else ''

                if not title or not content:
                    print(f"Article {i} ignoré : titre ou contenu manquant.")
                    continue

                published_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                data = {
                    "title": title,
                    "content": content,
                    "image_url": image_url,
                    "link": link,
                    "published_at": published_at
                }

                print(f"Titre: {title[:50]}...")
                res = requests.post(POST_URL, data=data)
                print(f"Statut HTTP: {res.status_code} - Réponse: {res.text}")

                time.sleep(DELAY)

            except Exception as e:
                print(f"Erreur sur l'article {i}: {e}")
                continue

    except Exception as e:
        print(f"Erreur majeure : {e}")

if __name__ == "__main__":
    print("=== Début du script ===")
    fetch_and_post()
    print("=== Script terminé ===")
