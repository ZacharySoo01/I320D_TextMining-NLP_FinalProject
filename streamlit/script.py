# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import streamlit as st

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



def main():

    # App title
    st.title('Search for NLP Paper')
    st.caption("Authors: Thang Truong, Zachary Soo, Rory James, Nicola Rowe")

    st.markdown('[Github Link](https://github.com/ZacharySoo01/I320D_TextMining-NLP_FinalProject)')
    local_css("style.css")
    local_js("script.js")

    p = "This project is a part of bigger project"
    st.markdown(p, unsafe_allow_html=False)
        
    st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)
    search_query = st.text_input("Enter your search query:", "")

    # Check if the search query is not empty
    if search_query:
        # Generate some random data for demonstration
        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))

        # Display the table
        st.table(df)


if __name__ == "__main__":
    main()
