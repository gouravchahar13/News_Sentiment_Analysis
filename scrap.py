import requests
import json
from bs4 import BeautifulSoup

def get_top_articles(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for article in soup.select('a[href*="/articleshow/"]')[:10]:
            title = article.get_text(strip=True)
            link = article['href']
            if not link.startswith("http"):
                link = "https://timesofindia.indiatimes.com" + link
            articles.append({"title": title, "link": link})
        
        return articles
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def extract_article_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1')
        article_title = title.get_text(strip=True) if title else "No title found"
        
        # Find the div with data-article="1"
        article_body = soup.find('div', {'data-articlebody': "1"})
        
        if article_body:
            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('div') if len(p.get_text(strip=True)) > 20]
            content = "\n".join(paragraphs)
        else:
            content = "No content found"
        
        return {"title": article_title, "content": content, "link": url}
    except requests.exceptions.RequestException as e:
        return {"title": "Error", "content": f"Error fetching content: {e}", "link": url}

if __name__ == "__main__":
    url = "https://timesofindia.indiatimes.com/topic/Google"
    print(f"Extracting top 10 articles from: {url}\n")
    articles = get_top_articles(url)
    
    if "error" in articles:
        print("Error:", articles["error"])
    else:
        all_articles = []
        
        for idx, article in enumerate(articles, start=1):
            print(f"Extracting content for article {idx}: {article['title']}\n   Link: {article['link']}\n")
            article_data = extract_article_content(article['link'])
            print(f"Heading: {article_data['title']}\n   Link: {article_data['link']}\n")
            print(f"Content:\n{article_data['content']}\n")
            all_articles.append(article_data)
        
        with open("articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        
        print("All articles saved to articles.json")