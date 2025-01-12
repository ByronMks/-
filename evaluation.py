# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:33:20 2025

@author: mak14
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from sklearn.metrics import precision_score, recall_score, f1_score
import json
import numpy as np

# TF-IDF Κατάταξη
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

# Boolean Αναζήτηση
def boolean_search(query, inverted_index):
    terms = query.lower().split()
    matching_docs = set(inverted_index.get(terms[0], []))
    for term in terms[1:]:
        if term in inverted_index:
            matching_docs = matching_docs.intersection(inverted_index[term])
    return sorted(matching_docs)

# Φόρτωση Inverted Index
def load_inverted_index(path="inverted_index.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Αξιολόγηση
test_queries = [
    {"query": "machine learning", "relevant_docs": {0, 2}},
    {"query": "data science", "relevant_docs": {1, 3}},
    {"query": "natural language processing", "relevant_docs": {4}},
    {"query": "artificial intelligence", "relevant_docs": {0, 4, 5}},
    {"query": "deep learning", "relevant_docs": {2, 5}},
]

def evaluate_search_engine(algorithm, articles_path="wikipedia_articles.json", inverted_index_path="inverted_index.json"):
    with open(articles_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    documents = [article["content"] for article in articles]
    all_precisions = []
    all_recalls = []
    all_f1_scores = []
    average_precisions = []

    if algorithm == "Boolean":
        inverted_index = load_inverted_index(inverted_index_path)

    for test in test_queries:
        query = test["query"]
        relevant_docs = test["relevant_docs"]

        if algorithm == "Boolean":
            retrieved_docs = boolean_search(query, inverted_index)
        elif algorithm == "TF-IDF":
            ranked_results = tfidf_ranking(query, documents)
            retrieved_docs = [doc_id for doc_id, score in ranked_results if score > 0]
        elif algorithm == "BM25":
            ranked_results = bm25_ranking(query, documents)
            retrieved_docs = [doc_id for doc_id, score in ranked_results if score > 0]
        else:
            raise ValueError("Unknown algorithm!")

        y_true = [1 if i in relevant_docs else 0 for i in range(len(documents))]
        y_pred = [1 if i in retrieved_docs else 0 for i in range(len(documents))]

        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1_scores.append(f1)

        ap = 0
        hits = 0
        for rank, doc_id in enumerate(retrieved_docs, start=1):
            if doc_id in relevant_docs:
                hits += 1
                ap += hits / rank
        average_precisions.append(ap / len(relevant_docs) if relevant_docs else 0)

    mean_precision = np.mean(all_precisions)
    mean_recall = np.mean(all_recalls)
    mean_f1 = np.mean(all_f1_scores)
    mean_ap = np.mean(average_precisions)

    print(f"\nEvaluation of Search Engine (Algorithm: {algorithm}):")
    print(f"- Average Precision: {mean_precision:.4f}")
    print(f"- Average Recall: {mean_recall:.4f}")
    print(f"- Average F1-score: {mean_f1:.4f}")
    print(f"- Mean Average Precision (MAP): {mean_ap:.4f}")

# Εκτέλεση Αξιολόγησης
print("Start of Evaluation...\n")
evaluate_search_engine("TF-IDF")
evaluate_search_engine("BM25")
evaluate_search_engine("Boolean")
