import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt

st.write(
    """
    # SUBMISSION DICODING
    """
)

st.subheader('Penjualan Per-Bulan')

all_df = pd.read_csv('all_data.csv')

all_df['order_purchase_timestamp']=pd.to_datetime(all_df['order_purchase_timestamp'])

all_df.reset_index(inplace=True)

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price" : "sum"
    })

    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id" : "order_count",
        "total_price" : "revenue"
    }, inplace=True)

    return daily_orders_df


def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

daily_orders_df = create_daily_orders_df(all_df)
sum_order_items_df = create_sum_order_items_df(all_df)

fig, ax = plt.subplots(figsize=(16,8))

ax.plot(
    daily_orders_df['order_purchase_timestamp'],
    daily_orders_df['order_count'],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="price", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="price", y="product_category_name_english", data=sum_order_items_df.sort_values(by="price", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
