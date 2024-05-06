
from sentence_transformers import SentenceTransformer
import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
import nltk
import time
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('words')

# get a set of stopwords from NLTK
stops = set(stopwords.words('english'))
# get a set of words from the english dictionary
en_dict = set(words.words())


# Get the current time before the operation
start_time = time.time()

def pre_process_text(text):
  # 1) Lowercasing
  text = text.lower()

  processed_text = []

  # 2) Tokenize the text
  txt = word_tokenize(text)

  # 3) Lemmatize the text
  wnl = WordNetLemmatizer()
  lemmatized_words = [wnl.lemmatize(token) for token in txt]

  # 4) Filter out non-words and stopwords
  filtered_text = [token for token in lemmatized_words if token not in stops and token in en_dict]

  processed_text = " ".join (filtered_text)
  return processed_text

model = SentenceTransformer('bert-base-nli-mean-tokens')

df = pd.read_csv("../arxiv_results.csv", names = ["id", "title", "summary"])
df = df.drop(df.columns[0], axis=1)
df = df.drop(0, axis=0)

text_list = [pre_process_text(title+summary) for title, summary in zip(df["title"], df["summary"])]

with open("preprocess.json", "w") as json_pre_process:
   json.dump(text_list, json_pre_process)

# Get the current time after the operation
end_time = time.time()

print("Prepocessed done", {end_time - start_time})


start_time = time.time()

embedding = model.encode(text_list)

end_time = time.time()
print("Embedding Done: ", end_time - start_time)

start_time = time.time()
# # Convert embedding to embedding list 
embedding_list = embedding.tolist()

# # Put into dictionary with key is the df["title"] and value is embedding 
embeddings_dict = {}
for i, emb in enumerate(embedding_list):
    embeddings_dict[df.iloc[i]["title"]] = emb

# # Export to JSON 
with open("embedding.json", "w") as json_file:
   json.dump(embedding_list, json_file)

with open("embedding_dict.json", "w") as json_file:
   json.dump(embeddings_dict, json_file)

# Get the current time after the operation
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print("Elapsed time End:", elapsed_time, "seconds")