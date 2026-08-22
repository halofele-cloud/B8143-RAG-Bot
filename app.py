import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="B8143 RAG Bot", layout="wide")
st.title("B8143 Product Review RAG Bot")
st.caption("halofele-cloud | RAG-based Review Intelligence")

DATA_PATH = os.path.join("data", "reviews.csv")

def load_data():
    os.makedirs("data", exist_ok=True)
    # Always recreate with English data to fix old cache
    data = {
        "product": ["Running Shoes", "Backpack", "Powerbank", "Running Shoes", "Backpack"],
        "review": ["Size too small, disappointed", "Stitching came off after 2 weeks", "Long lasting battery, great", "Hard sole hurts feet", "Large capacity, strong material, love it"],
        "rating": [2, 2, 5, 2, 5]
    }
    df = pd.DataFrame(data)
    df.to_csv(DATA_PATH, index=False)
    return df

df = load_data()

st.sidebar.metric("Total Reviews", len(df))
st.sidebar.subheader("Average Rating by Product")
st.sidebar.write(df.groupby("product")["rating"].mean().round(2))

def simple_rag(q, data):
    q_low = q.lower()
    if "shoe" in q_low or "running" in q_low:
        return data[data["product"] == "Running Shoes"]
    if "backpack" in q_low or "bag" in q_low:
        return data[data["product"] == "Backpack"]
    if "powerbank" in q_low or "power" in q_low:
        return data[data["product"] == "Powerbank"]
    return data

query = st.text_input("Ask a question:", "What are complaints about Running Shoes?")

if query:
    res = simple_rag(query, df)
    st.success(f"Found {len(res)} reviews for '{query}'")
    st.dataframe(res, use_container_width=True)
    if not res.empty:
        st.metric("Average Rating", f"{res['rating'].mean():.1f} / 5")
        st.info(f"**RAG Insight:** Customers reported: {', '.join(res['review'].tolist())}")
