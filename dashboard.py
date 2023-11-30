import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
import streamlit as st

all_df = pd.read_csv('all_data.csv')


st.write(
    """
    # My First App
    Hello world
"""
)