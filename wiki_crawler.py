# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:51:31 2025

@author: mak14
"""

import requests
from bs4 import BeautifulSoup
import json

# Βασικές ρυθμίσεις
BASE_URL = "https://en.wikipedia.org/wiki/"
TOPICS = ["Information_retrieval", "Natural_language_processing", "Artificial_intelligence","Data_mining", "Machine_learning", "Deep_learning", "Computer_vision", "Neural_network", "Big_data", "Data_science"]

# Συνάρτηση για τη συλλογή περιεχομένου
def scrape_wikipedia_articles(topics):
    articles = []
    
    for topic in topics:
        url = BASE_URL + topic
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Τίτλος άρθρου
            title = soup.find('h1').text
            
            # Περιεχόμενο άρθρου (μόνο από την κύρια παράγραφο)
            paragraphs = soup.find_all('p')
            content = ' '.join([para.text for para in paragraphs if para.text.strip()])
            
            articles.append({
                "title": title,
                "url": url,
                "content": content
            })
        else:
            print(f"Failed to fetch {url}")
    
    return articles

# Εκτέλεση
articles = scrape_wikipedia_articles(TOPICS)

# Αποθήκευση σε JSON
with open("wikipedia_articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Αποθηκεύτηκαν {len(articles)} άρθρα στο 'wikipedia_articles.json'.")