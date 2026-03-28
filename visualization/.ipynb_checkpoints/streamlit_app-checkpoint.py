import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="AI Antigen Discovery Tool", layout="wide")

st.title("AI Antigen Discovery Tool")
st.write("Rank proteins by predicted antigen potential using ESM-2 embeddings and a Random Forest model.")

# Sidebar
st.sidebar.header("Settings")
virus = st.sidebar.selectbox("Select Dataset", ["SARS-CoV-2", "Murine CoV", "Human Proteins", "All Proteins"])

# Load data
df = pd.read_csv("C:/Users/asmak/Documents/ai-anitgen-discovery/data/processed/protein_embeddings.csv")
#df = pd.read_csv("../data/processed/protein_embeddings.csv")

# Load model
model = joblib.load("C:/Users/asmak/Documents/ai-anitgen-discovery/models/antigen_model.pkl")

# Prepare features
df["embedding_vector"] = df["embedding_vector"].apply(
    lambda x: np.array(list(map(float, x.split(","))))
)

X = np.vstack(df["embedding_vector"].values)
extra = df[["length", "glyco_count"]].values
X_full = np.hstack([X, extra])

# Predict
df["antigen_probability"] = model.predict_proba(X_full)[:, 1]

# Filter by virus selection
if virus == "SARS-CoV-2":
    filtered = df[df["protein_name"].str.contains("SARS2")]
elif virus == "Murine CoV":
    filtered = df[df["protein_name"].str.contains("CVMAS")]
elif virus == "Human Proteins":
    filtered = df[df["protein_name"].str.contains("HUMAN")]
else:
    filtered = df

# Display results
st.subheader("Top Antigen Candidates")
top = filtered.sort_values("antigen_probability", ascending=False)[
    ["protein_name", "antigen_probability"]
].head(10)

st.dataframe(top, use_container_width=True)
