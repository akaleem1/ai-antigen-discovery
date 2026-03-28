import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import re

st.set_page_config(page_title="AI Antigen Discovery Tool", layout="wide")

# ---------------------------------------------------------
# TITLE + INTRO
# ---------------------------------------------------------
st.title("AI Antigen Discovery Tool")
st.write("Interactive dashboard for ranking viral proteins by predicted antigen potential using ESM-2 embeddings and a Random Forest model.")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Settings")
virus = st.sidebar.selectbox("Select Dataset", ["SARS-CoV-2", "Murine CoV", "Human Proteins", "All Proteins"])
search_query = st.sidebar.text_input("Search protein name")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
df = pd.read_csv("C:/Users/asmak/Documents/ai-anitgen-discovery/data/processed/protein_embeddings.csv")

# ---------------------------------------------------------
# GLYCOSYLATION MOTIFS
# ---------------------------------------------------------
def count_glyco(seq):
    return len(re.findall(r'N[^P][ST]', seq))

df["glyco_count"] = df["sequence"].apply(count_glyco)

# ---------------------------------------------------------
# EMBEDDING PARSER (ROBUST)
# ---------------------------------------------------------
def parse_embedding(x):
    x = x.replace("\n", " ").replace("[", "").replace("]", "")
    return np.fromstring(x, sep=" ")

df["embedding_vector"] = df["embedding_vector"].apply(parse_embedding)

# ---------------------------------------------------------
# BUILD FEATURE MATRIX
# ---------------------------------------------------------
X = np.vstack(df["embedding_vector"].values)
extra = df[["length", "glyco_count"]].values
X_full = np.hstack([X, extra])

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------
model = joblib.load("C:/Users/asmak/Documents/ai-anitgen-discovery/models/antigen_model.pkl")

# Predict
df["antigen_probability"] = model.predict_proba(X_full)[:, 1]

# ---------------------------------------------------------
# FILTERING
# ---------------------------------------------------------
if virus == "SARS-CoV-2":
    filtered = df[df["protein_name"].str.contains("SARS", case=False)]
elif virus == "Murine CoV":
    filtered = df[df["protein_name"].str.contains("CVMAS", case=False)]
elif virus == "Human Proteins":
    filtered = df[df["protein_name"].str.contains("HUMAN", case=False)]
else:
    filtered = df

if search_query:
    filtered = filtered[filtered["protein_name"].str.contains(search_query, case=False)]

# ---------------------------------------------------------
# TOP ANTIGEN TABLE
# ---------------------------------------------------------
st.subheader("Top Antigen Candidates")

top = filtered.sort_values("antigen_probability", ascending=False)[
    ["protein_name", "antigen_probability"]
].head(20)

if top.empty:
    st.warning("No proteins found for this filter.")
else:
    styled = top.style.background_gradient(
        subset=["antigen_probability"],
        cmap="YlOrRd"
    )
    st.dataframe(styled, use_container_width=True)

# ---------------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------------
st.download_button(
    label="Download Results as CSV",
    data=filtered.to_csv(index=False),
    file_name="antigen_predictions.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# PROTEIN DETAILS PANEL
# ---------------------------------------------------------
st.subheader("Protein Details")

if filtered.empty:
    st.info("No proteins available for details.")
else:
    protein_selected = st.selectbox(
        "Select a protein to view details:",
        filtered["protein_name"].tolist()
    )

    row = filtered[filtered["protein_name"] == protein_selected].iloc[0]

    st.markdown(f"""
    ### {row['protein_name']}
    - **Length:** {row['length']}
    - **Glycosylation motifs:** {row['glyco_count']}
    - **Antigen probability:** {row['antigen_probability']:.3f}
    """)

    st.markdown("**Sequence:**")
    st.code(row["sequence"])
