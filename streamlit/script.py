# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title('My First Streamlit App')

# Generate some random data
data = np.random.randn(100)

# Plot the data
st.line_chart(data)
