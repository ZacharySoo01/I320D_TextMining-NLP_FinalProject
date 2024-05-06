

import numpy as np 
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import json 
import gensim.downloader as api



def get_embedding_data(switch_toggle):
    if switch_toggle == 0:
        # ST
        # Open the JSON file
        with open("embedding.json", "r") as json_file:
            # Read the contents of the file
            embedding_data = json.load(json_file)
        return embedding_data
    elif switch_toggle == 1:
        # TF-IDF
        embedding_data = joblib.load("embedding_tfidf.json")
        return embedding_data
    else:
        # word 2 vec
        embedding_data = joblib.load("embedding_word2vec.json")
        return embedding_data



def determine_model(switch_toggle, query):
    if switch_toggle == 0:
        return encode_query_st(query)
    elif switch_toggle == 1:
        return encode_query_tfidf(query)
    elif switch_toggle == 2:
        return encode_query_word2vec(query)

    return encode_query_st(query)

def w2v_average_word_embeddings(sentence):
    w2v_model = api.load("word2vec-google-news-300")
    words = sentence.split()
    word_vectors = [w2v_model[word] for word in words if word in w2v_model]
    if not word_vectors:
        return np.zeros(w2v_model.vector_size)
    return np.mean(word_vectors, axis=0)

def encode_query_st(query):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    return model.encode(query)

def encode_query_tfidf(query):
    # Load the vectorizer from the file
    loaded_vectorizer = joblib.load('vectorizer.pkl')
    return loaded_vectorizer.transform([query]).toarray()

def encode_query_word2vec(query):
    return w2v_average_word_embeddings(query)

def get_df():
    df = pd.read_csv("https://raw.githubusercontent.com/ZacharySoo01/I320D_TextMining-NLP_FinalProject/main/arxiv_results.csv", names = ["id", "title", "summary"])
    df = df.drop(df.columns[0], axis=1)
    df = df.drop(0, axis=0)
    return df

def cosine_distance_based_similarity (vector1, vector2):
    # dot_product = np.dot(vector1, vector2)
    dot_product = np.dot(vector1, vector2.T)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

        # Check for divide by zero or NaN values
    if norm_vector1 == 0 or norm_vector2 == 0 or np.isnan(dot_product) or np.isnan(norm_vector1) or np.isnan(norm_vector2):
        return 0

    return dot_product / (norm_vector1 * norm_vector2)

def return_ranked_text(query, switch_toggle):

    vector_list = get_embedding_data(switch_toggle=switch_toggle)

    similarity_scores = {}
    for i, title_vector in enumerate(vector_list):
        sim = cosine_distance_based_similarity(title_vector, query)
        similarity_scores[i] = sim

    # Assuming similarity_scores is a dictionary of {text: similarity_score}
    ranked_texts = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

   # Rank texts based on the similarity score in ascending order. Print the top 10 most similar texts.
    if switch_toggle == 1:
        for i, n in enumerate(ranked_texts[:10]):
            # Convert the tuple to a list
            ranked_text_list = list(ranked_texts[i])
            # Modify the desired item
            ranked_text_list[1] = ranked_text_list[1][0]
            # Convert the list back to a tuple
            ranked_texts[i] = ranked_text_list

    return ranked_texts[:10]

def get_title_from_top10(ranked_text, df):
    new_df = {"Title": [], "Score": []}  # Initialize empty lists
    
    for index, score in ranked_text:
        new_df["Title"].append(df.iloc[index]["title"])  # Use square brackets for indexing
        new_df["Score"].append(score)
    
    return new_df



