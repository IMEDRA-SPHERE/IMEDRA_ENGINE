from flask import Flask, render_template, request, jsonify
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

app = Flask(__name__)

def get_page_info(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get title
        title = soup.title.string if soup.title else urlparse(url).netloc
        
        # Get description/summary
        description = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        else:
            # If no meta description, get first paragraph or first 200 characters of text
            first_p = soup.find('p')
            if first_p:
                description = first_p.get_text()[:200]
            else:
                description = soup.get_text()[:200]
        
        return {
            'title': title.strip() if title else url,
            'summary': description.strip(),
            'url': url
        }
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return {
            'title': urlparse(url).netloc,
            'summary': "Unable to fetch page content",
            'url': url
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search_results():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'results': []})
    
    # Add cybersecurity context to the search query
    search_query = f"{query} cybersecurity"
    results = []
    
    try:
        # Get search results
        search_results = search(search_query, num_results=10)
        
        # Process each URL
        for url in search_results:
            # Add a small delay to avoid overwhelming servers
            time.sleep(0.2)
            page_info = get_page_info(url)
            
            # Calculate a simple relevance score based on query terms
            score = 1.0
            query_terms = query.lower().split()
            content = (page_info['title'] + ' ' + page_info['summary']).lower()
            
            for term in query_terms:
                if term in content:
                    score += 0.2
            
            page_info['score'] = round(score, 2)
            results.append(page_info)
        
        # Sort results by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({'results': results})
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
