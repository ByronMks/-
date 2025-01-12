# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 21:31:07 2025

@author: mak14
"""

import json
from collections import defaultdict

# Φόρτωση των καθαρισμένων άρθρων από το προηγούμενο βήμα
with open("processed_wikipedia_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Δημιουργία ανεστραμμένου ευρετηρίου
inverted_index = defaultdict(list)

# Κατασκευή του ανεστραμμένου ευρετηρίου
for doc_id, article in enumerate(articles):
    # Διαχωρισμός των λέξεων από το καθαρισμένο περιεχόμενο
    tokens = article["cleaned_content"].split()
    # Για κάθε μοναδική λέξη στο έγγραφο
    for token in set(tokens):  # Χρησιμοποιούμε set για να μην αποθηκεύσουμε διπλές εμφανίσεις
        inverted_index[token].append(doc_id)

# Αποθήκευση του ανεστραμμένου ευρετηρίου
with open("inverted_index.json", "w", encoding="utf-8") as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=4)

print("Inverted index created and save in 'inverted_index.json'.")
