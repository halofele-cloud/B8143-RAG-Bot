import os, streamlit as st, pandas as pd
st.set_page_config(page_title="B8143 RAG Bot")
st.title("B8143 Review Bot - halofele-cloud")
DATA_PATH = os.path.join("data", "reviews.csv")
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs("data", exist_ok=True)
        dummy = {"product":["Sepatu Running","Tas Ransel","Powerbank","Sepatu Running","Tas Ransel"],"review":["Ukuran kekecilan, kecewa","Jahitan lepas 2 minggu","Daya tahan lama mantap","Sol keras kaki sakit","Muatan banyak bahan kuat suka"],"rating":[2,2,5,2,5]}
        pd.DataFrame(dummy).to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)
df = load_data()
st.sidebar.metric("Total Reviews", len(df))
st.sidebar.dataframe(df.groupby("product")["rating"].mean().round(2))
def simple_rag(q, data):
    q=q.lower()
    return data[data.apply(lambda r: any(w in r["review"].lower() for w in q.split()) or q in r["product"].lower(), axis=1)]
query = st.text_input("Tanya:", "Sepatu Running keluhannya apa?")
if query:
    res = simple_rag(query, df)
    st.write(res)
