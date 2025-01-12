# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:47:30 2025

@author: mak14
"""


import json
import re

# Προεπεξεργασία ερωτήματος
def preprocess_query(query):

    query_tokens = re.findall(r'\w+', query.lower())
    return query_tokens

# Αξιολόγηση ερωτήματος
def evaluate_query(query, inverted_index):
    
    tokens = preprocess_query(query)
    result_set = set()
    current_operator = "OR"  # Default operator

    for token in tokens:
        if token in {"and", "or", "not"}:
            current_operator = token.upper()
        else:
            token_docs = set(inverted_index.get(token, []))
            if current_operator == "OR":
                result_set |= token_docs
            elif current_operator == "AND":
                result_set &= token_docs
            elif current_operator == "NOT":
                result_set -= token_docs

    return result_set

# Διεπαφή χρήστη
def search_engine_cli(inverted_index_path, articles_path):
    # Φόρτωση δεδομένων
    with open(inverted_index_path, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)

    with open(articles_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print("Welcome to the Search Engine")
    print("Insert your query or type 'exit' for termination:")

    while True:
        query = input("\nQuery: ")
        if query.lower() == "exit":
            print("Thanks for using the Search Enigne! Terminating...")
            break

        matching_docs = evaluate_query(query, inverted_index)

        if matching_docs:
            print("\nThe suitable files are:")
            for doc_id in matching_docs:
                doc_content = articles[doc_id - 1]["content"]
                print(f"\n[File {doc_id}]")
                print(doc_content[:200] + "...")  # Εμφανίζει τα πρώτα 200 χαρακτήρες
        else:
            print("\nNo relatable files found. Please try again:")

# Κύρια εκτέλεση
if __name__ == "__main__":
    # Αρχεία JSON που δημιουργήθηκαν στα προηγούμενα βήματα
    inverted_index_path = "inverted_index.json"       # Το ανεστραμμένο ευρετήριο
    articles_path = "wikipedia_articles.json"         # Τα άρθρα της Wikipedia

    # Εκτέλεση της διεπαφής
    search_engine_cli(inverted_index_path, articles_path)
