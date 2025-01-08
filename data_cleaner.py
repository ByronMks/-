# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 17:35:59 2025

@author: mak14
"""

import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import download

# Κατεβάζουμε τους απαραίτητους πόρους από το NLTK
download('punkt')  # Για tokenization
download('stopwords')  # Για stop-word removal
download('wordnet')  # Για lemmatization
download('omw-1.4')  # Βοηθητικά δεδομένα για lemmatizer

# Αρχικοποιήσεις
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Διαβάζουμε το dataset
with open("wikipedia_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Συνάρτηση για προεπεξεργασία
def preprocess_text(text):
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Αφαίρεση ειδικών χαρακτήρων (κρατάμε μόνο γράμματα και κενά)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Stop-word removal
    tokens = [word for word in tokens if word not in stop_words]
    
    # 5. Lemmatization
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Επιστροφή των καθαρισμένων tokens ως ενιαίο κείμενο
    return ' '.join(lemmatized_tokens)

# Επεξεργασία των άρθρων
processed_articles = []
for article in articles:
    cleaned_content = preprocess_text(article["content"])
    processed_articles.append({
        "title": article["title"],
        "url": article["url"],
        "cleaned_content": cleaned_content
    })

# Αποθήκευση του "καθαρισμένου" dataset
with open("processed_wikipedia_articles.json", "w", encoding="utf-8") as f:
    json.dump(processed_articles, f, ensure_ascii=False, indent=4)

print(f"Preprocessing completed! Cleaned data saved in 'processed_wikipedia_articles.json'.")
