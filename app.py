@st.cache_data
def load_data():
    # force fresh english data
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)
    os.makedirs("data", exist_ok=True)
    dummy = {"product":["Running Shoes","Backpack","Powerbank","Running Shoes","Backpack"],
             "review":["Size too small, disappointed","Stitching came off after 2 weeks","Long lasting battery, great","Hard sole hurts feet","Large capacity, strong material, love it"],
             "rating":[2,2,5,2,5]}
    pd.DataFrame(dummy).to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)
