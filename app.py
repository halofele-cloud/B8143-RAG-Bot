import os, streamlit as st, pandas as pd
st.set_page_config(page_title="B8143 RAG Bot", layout="wide")
st.title("B8143 Product Review RAG Bot")
st.caption("halofele-cloud | RAG-based Review Intelligence")

DATA_PATH = os.path.join("data", "reviews.csv")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs("data", exist_ok=True)
        dummy = {"product":["Running Shoes","Backpack","Powerbank","Running Shoes","Backpack"],
                 "review":["Size too small, disappointed","Stitching came off after 2 weeks","Long lasting battery, great","Hard sole hurts feet","Large capacity, strong material, love it"],
                 "rating":[2,2,5,2,5]}
        pd.DataFrame(dummy).to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)

df = load_data()
st.sidebar.metric("Total Reviews", len(df))
st.sidebar.subheader("Average Rating")
st.sidebar.write(df.groupby("product")["rating"].mean().round(2))

def simple_rag(q, data):
    q_low = q.lower()
    for prod in data["product"].unique():
        if prod.lower().split()[0] in q_low or prod.lower() in q_low:
            return data[data["product"].str.lower() == prod.lower()]
    return data

query = st.text_input("Ask a question:", "What are complaints about Running Shoes?")
if query:
    res = simple_rag(query, df)
    st.success(f"Found {len(res)} reviews for '{query}'")
    st.dataframe(res, use_container_width=True)
    if not res.empty:
        st.metric("Average Rating", f"{res['rating'].mean():.1f} / 5")
        st.info(f"**RAG Insight:** Customers reported: {', '.join(res['review'].tolist())}")
