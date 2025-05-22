import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Configuration
DEXERTO_URL = "https://www.dexerto.com/gaming/"
POST_URL = "https://gamemasterx.great-site.net/post_news.php"  # Votre URL corrigée
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
MAX_ARTICLES = 3  # Nombre d'articles à récupérer
DELAY = 2  # Délai en secondes entre les requêtes pour éviter le bannissement

def clean_text(text):
    """Nettoie le texte des caractères indésirables"""
    return text.strip().replace('\n', ' ').replace('\r', '')

def fetch_and_post():
    try:
        # 1. Récupération des articles
        print(f"Récupération des articles depuis {DEXERTO_URL}...")
        response = requests.get(DEXERTO_URL, headers=HEADERS)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".news-archive__item")[:MAX_ARTICLES]
        
        if not articles:
            print("Aucun article trouvé - vérifiez les sélecteurs CSS")
            return

        # 2. Traitement des articles
        for i, article in enumerate(articles, 1):
            try:
                print(f"\nTraitement de l'article {i}/{len(articles)}...")
                
                # Extraction des données
                title = clean_text(article.select_one(".news-archive__title").get_text())
                link = article.find("a")["href"]
                image = article.find("img")["src"]
                content = clean_text(article.select_one(".news-archive__excerpt").get_text())
                published_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Construction des données à envoyer
                data = {
                    "title": title,
                    "content": content,
                    "image_url": image,
                    "link": link,
                    "published_at": published_at
                }
                
                print(f"Titre: {title[:50]}...")  # Affiche les 50 premiers caractères
                
                # 3. Envoi des données
                res = requests.post(POST_URL, data=data)
                print(f"Statut HTTP: {res.status_code} - Réponse: {res.text}")
                
                time.sleep(DELAY)  # Respectueux du serveur cible
                
            except Exception as e:
                print(f"Erreur sur l'article {i}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Erreur majeure: {str(e)}")

if __name__ == "__main__":
    print("=== Début du script ===")
    fetch_and_post()
    print("=== Script terminé ===")
