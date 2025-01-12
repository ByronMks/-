# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:01:14 2025

@author: mak14
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import json

# Boolean Αναζήτηση
def boolean_search(query, inverted_index, documents):
    
    terms = query.split()
    result_set = set(range(len(documents)))  # Ξεκινάμε με όλα τα έγγραφα
    operation = "OR"  # Default operator
    current_set = set()

    for term in terms:
        if term.upper() in ["AND", "OR", "NOT"]:
            operation = term.upper()
        else:
            matching_docs = set(inverted_index.get(term, []))
            if operation == "AND":
                current_set = current_set & matching_docs if current_set else matching_docs
            elif operation == "OR":
                current_set = current_set | matching_docs
            elif operation == "NOT":
                current_set = current_set - matching_docs
    return current_set

# TF-IDF Κατάταξη (Vector Space Model)
def tfidf_ranking(query, documents):
    
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, doc_vectors).flatten()
    return sorted(enumerate(scores, start=0), key=lambda x: x[1], reverse=True)

# BM25 Κατάταξη
def bm25_ranking(query, documents):
    
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    query_tokens = query.split()
    scores = bm25.get_scores(query_tokens)
    return sorted(enumerate(scores, start=0), key=lambda x: x[1], reverse=True)

# Διεπαφή αναζήτησης με επιλογή τεχνικής
def search_engine(query, algorithm="Boolean", articles_path="wikipedia_articles.json", index_path="inverted_index.json"):
   
    # Φόρτωση άρθρων
    with open(articles_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    documents = [article["content"] for article in articles]
    titles = [article["title"] for article in articles]

    # Φόρτωση ανεστραμμένου ευρετηρίου
    with open(index_path, "r", encoding="utf-8") as f:
        inverted_index = json.load(f)

    if algorithm == "Boolean":
        boolean_results = boolean_search(query, inverted_index, documents)
        if boolean_results:
            print("\nResults of Boolean Search:")
            for doc_id in boolean_results:
                print(f"- {titles[doc_id]}")
        else:
            print("No relatable files found.")

    elif algorithm == "TF-IDF":
        ranked_results = tfidf_ranking(query, documents)
        print("\nSearch Results (TF-IDF):")
        for doc_id, score in ranked_results[:10]:  # Top 10 αποτελέσματα
            if score > 0:
                print(f"- {titles[doc_id]} (Score: {score:.4f})")

    elif algorithm == "BM25":
        ranked_results = bm25_ranking(query, documents)
        print("\nSearch Results (BM25):")
        for doc_id, score in ranked_results[:10]:  # Top 10 αποτελέσματα
            if score > 0:
                print(f"- {titles[doc_id]} (Score: {score:.4f})")

    else:
        print("Unkown algorithm.")

# Εκτέλεση μηχανής αναζήτησης
if __name__ == "__main__":
    while True:
        print("\nWelcome to the Search Engine.")
        print("1. Boolean Search")
        print("2. Rank Results (TF-IDF)")
        print("3. Rank Results (BM25)")
        print("4. Exit")
        choice = input("Choose your operation: ")

        if choice == "1":
            query = input("Insert the Boolean Query: ")
            search_engine(query, algorithm="Boolean")
        elif choice == "2":
            query = input("Insert your Query: ")
            search_engine(query, algorithm="TF-IDF")
        elif choice == "3":
            query = input("Insert your Query: ")
            search_engine(query, algorithm="BM25")
        elif choice == "4":
            print("Exiting the Search Engine.")
            break
        else:
            print("Not valid option. Please try again.")
