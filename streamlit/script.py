# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sentence_transformers import SentenceTransformer
import support_function as sf
import json

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def local_js(file_name):
    with open(file_name) as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def return_button_html(name):
    button_html =  f"""
                <button class = 'button-{name}'>{name}</button>
                """
    return button_html

def display_text(switch_toggle):
    if switch_toggle == 0:
        return "Sentence Transformer is chosen"
    elif switch_toggle == 1:
        return "TF-IDF is chosen"
    elif switch_toggle == 2:
        return "Word2Vec is chosen"

def execute_return_df(df, switch_toggle, search_query):
    new_df = get_return_df(df = df, switch_toggle= switch_toggle, search_query= search_query)
    st.write(display_text(switch_toggle=switch_toggle))
    # Display the table
    st.table(new_df)

def get_return_df(df, switch_toggle, search_query):

    query_embeddings = sf.determine_model(switch_toggle= switch_toggle, query = search_query)
    # query_embeddings = sf.encode_query(search_query)

    ranked_text = sf.return_ranked_text(query_embeddings, switch_toggle)

    new_df = sf.get_title_from_top10(ranked_text,df)

    return new_df


def main():
    df = sf.get_df()

    # App title
    st.title('Information Retreival in Scholarly Papers')
    st.caption("Authors: Thang Truong, Zachary Soo, Rory James, Nicola Rowe")

    st.markdown('[Github Link](https://github.com/ZacharySoo01/I320D_TextMining-NLP_FinalProject)')
    local_css("style.css")
    local_js("script.js")

    p = """This project is about using word embedding to make academic paper searches in Computational Linguistics more relevant. 
            By learning the semantic meaning of words in sentences, word embedding allows for results that are semantically matched to the search queries. 
            So, you can expect more accurate and on-point results when searching for papers in this field. 
          

    """
    st.markdown(p, unsafe_allow_html=False)

    # Display numbered steps as a list
    st.markdown("""
    The process of searching for query is simple. 
    <ol>
    <li>Type in the query</li>
    <li>Choose the word embedding</li>
    <li>There is no step 3</li>
    </ol>
    """, unsafe_allow_html=True)

    st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)
    
    st.write("**Step 1: Search query**")
    search_query = st.text_input("Enter your search query:", "")


    st.write("**Step 2: Choose Word Embedding**")
    # Define the columns layout
    col1, col2, col3 = st.columns(3)
    switch_toggle = 0
    # Render buttons within columns
    with col1:
        st_button = st.button("ST")
       
    with col2:
        tf = st.button("TF-IDF")
      
    with col3:
        w2 = st.button("W2VEC")
        # st.markdown(return_button_html("ST"), unsafe_allow_html=True)

    if st_button and search_query:
        switch_toggle = 0 
        execute_return_df(df = df, switch_toggle= switch_toggle, search_query=search_query)

        
    if tf and search_query: 
        switch_toggle = 1
        execute_return_df(df = df, switch_toggle= switch_toggle, search_query=search_query)


    if w2 and search_query:
        switch_toggle = 2
        execute_return_df(df = df, switch_toggle= switch_toggle, search_query=search_query)






if __name__ == "__main__":
    main()
