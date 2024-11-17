import feedparser
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime

def fetch_rss_feed(url):
    """Fetch and filter RSS feed data from Towards Data Science."""
    articles = []
    restricted_phrases = ["Continue reading on Towards Data Science", "source=rss"]
    
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # Limit to latest 20 entries
            if not any(phrase in entry.summary for phrase in restricted_phrases):
                summary_soup = BeautifulSoup(entry.summary, "html.parser")
                clean_summary = summary_soup.get_text(separator=" ", strip=True)
                
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'content': clean_summary
                })
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
    return articles

def fetch_kdnuggets_articles():
    """Fetch articles from KDNuggets."""
    base_url = "https://www.kdnuggets.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a'):
                b_tag = a_tag.find('b')
                if b_tag:
                    title = b_tag.get_text(strip=True)
                    link = a_tag.get('href')
                    if link and not link.startswith('http'):
                        link = base_url + link
                    
                    try:
                        page_response = requests.get(link, headers=headers)
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        post_div = page_soup.find('div', id='post-')
                        content = post_div.get_text(strip=True) if post_div else "Content not found"
                        
                        articles.append({
                            'title': title,
                            'link': link,
                            'content': content
                        })
                    except Exception as e:
                        print(f"Error fetching KDNuggets article at {link}: {e}")
                    time.sleep(1 + random.uniform(0, 1))
    except Exception as e:
        print(f"Error fetching KDNuggets homepage: {e}")
    
    return articles

def fetch_devto_articles():
    """Fetch articles from Dev.to."""
    url = "https://dev.to/t/ai/latest"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        for article in soup.find_all("div", class_="crayons-story"):
            title_tag = article.find("h2", class_="crayons-story__title")
            link_tag = title_tag.find("a") if title_tag else None
            
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = f"https://dev.to{link_tag['href']}"
                
                try:
                    article_response = requests.get(link, headers=headers)
                    article_soup = BeautifulSoup(article_response.content, "html.parser")
                    content_div = article_soup.find("div", class_="crayons-article__body text-styles spec__body")
                    content = content_div.get_text(strip=True) if content_div else "Content not found"
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'content': content
                    })
                except Exception as e:
                    print(f"Error fetching Dev.to article at {link}: {e}")
                
                time.sleep(1 + random.uniform(0, 1))
    except Exception as e:
        print(f"Error fetching Dev.to homepage: {e}")

    return articles

def fetch_nvidia_blog_articles():
    """Fetch articles from NVIDIA blog."""
    url = "https://developer.nvidia.com/blog/recent-posts/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link_tag in soup.find_all('a', class_='carousel-row-slide__link'):
                title_span = link_tag.find('span', class_='visually-hidden')
                if title_span:
                    title = title_span.get_text(strip=True)
                    link = link_tag['href']
                    if not link.startswith('http'):
                        link = 'https://developer.nvidia.com' + link
                    
                    try:
                        post_response = requests.get(link, headers=headers)
                        post_soup = BeautifulSoup(post_response.content, 'html.parser')
                        content_div = post_soup.find('div', class_='entry-content')
                        content = content_div.get_text(separator="\n", strip=True) if content_div else "Content not found"
                        
                        articles.append({
                            'title': title,
                            'link': link,
                            'content': content
                        })
                    except Exception as e:
                        print(f"Error fetching NVIDIA article at {link}: {e}")
                    
                    time.sleep(1 + random.uniform(0, 1))
    except Exception as e:
        print(f"Error fetching NVIDIA homepage: {e}")

    return articles

def save_articles_to_json(data):
    """Save articles to a JSON file with timestamp."""
    current_time = datetime.now().strftime("%d-%m-%y-%H-%M")
    file_name = f"{current_time}.json"
    
    try:
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Articles saved to '{file_name}'.")
        return file_name
    except Exception as e:
        print(f"Error saving articles to JSON: {e}")
        return None

def gather_and_save_articles():
    """Fetch articles from multiple sources and save them to a JSON file."""
    all_articles = {
        "Towards Data Science": fetch_rss_feed("https://towardsdatascience.com/feed"),
        "KDNuggets": fetch_kdnuggets_articles(),
        "Dev.to": fetch_devto_articles(),
        "NVIDIA Blog": fetch_nvidia_blog_articles()
    }
    return save_articles_to_json(all_articles)

if __name__ == "__main__":
    gather_and_save_articles()
