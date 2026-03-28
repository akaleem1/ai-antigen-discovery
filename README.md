# AI Antigen Discovery Pipeline
*A machine learning workflow for prioritizing vaccine antigen candidates using protein language models and biological features.*

Built as a self-directed project to explore how modern AI methods can support early-stage vaccine antigen discovery and hypothesis generation in translational vaccinology.

---

## Overview

This project explores how **protein language models and machine learning** can support early-stage vaccine antigen discovery.

Using **ESM-2 protein embeddings**, biological annotations, and a Random Forest classifier, the pipeline ranks pathogen proteins by predicted antigen potential.

An interactive **Streamlit dashboard** enables exploration of:

- antigen probability scores
- protein sequences
- glycosylation motifs
- biological metadata

The goal is to demonstrate how **AI-driven analysis can help generate hypotheses for vaccine target selection**, a key step in translational vaccine research.

---

## Dataset

Protein sequences were collected from publicly available biological databases such as:

- UniProt
- NCBI Virus

The current prototype dataset includes:

- SARS-CoV-2 proteins
- related coronavirus proteins
- control human proteins

These sequences were processed into **ESM-2 embeddings** to capture evolutionary and biochemical information useful for downstream modeling.

---

## Key Features

### 1. Protein Embeddings (ESM-2)

Protein sequences are encoded using **ESM-2**, a transformer-based protein language model.

Benefits:

- captures evolutionary relationships
- encodes biochemical patterns
- enables machine learning on protein sequence representations

These embeddings serve as the primary feature space for downstream modeling.

---

### 2. Biological Feature Engineering

In addition to embeddings, biologically meaningful features are incorporated:

- **Glycosylation motif detection** (`N-X-[S/T]`)
- **Protein sequence length**

Planned additions include:

- structural accessibility (AlphaFold-based)
- epitope density
- evolutionary conservation across strains

---

### 3. Machine Learning Model

A **Random Forest classifier** predicts antigen probability for each protein.

The feature matrix combines:
X = [ESM embedding + protein length + glycosylation count]

The model outputs a probability score between **0 and 1** representing predicted antigen potential.

Future modeling experiments may compare:

- XGBoost
- logistic regression
- neural network classifiers

---

### 4. Interactive Streamlit Dashboard

The Streamlit application allows users to explore model predictions interactively.

Features include:

- filtering by virus
- protein name search
- ranked antigen candidate list
- protein sequence inspection
- motif visualization
- export of ranked results

This demonstrates how AI predictions can be translated into **usable tools for scientists**.

---

## Example Output

| Protein Name | Antigen Probability |
|--------------|---------------------|
| Spike (S)    | 0.91 |
| Envelope (E) | 0.77 |
| ORF7a        | 0.42 |

These scores help prioritize proteins for further biological investigation.

---

## Project Structure
ai-antigen-discovery/
│
├── data/
│ └── processed/
│ └── protein_embeddings.csv
│
├── models/
│ └── antigen_model.pkl
│
├── notebooks/
│ ├── 01_preprocessing.ipynb
│ ├── 02_embedding_generation.ipynb
│ ├── 03_model_training.ipynb
│ └── 04_visualization.ipynb
│
├── visualization/
│ └── streamlit_app.py
│
└── README.md


---

## Modeling Assumptions

For the prototype model:

- proteins known to function as **surface or structural viral proteins** were treated as positive antigen examples
- **non-structural proteins** were treated as negative examples

This simplified labeling strategy enables initial model exploration while demonstrating the potential of AI methods for antigen prioritization.

---

## Translational Application

This pipeline illustrates how AI methods can support vaccine R&D by:

- rapidly screening pathogen proteomes
- identifying potentially immunogenic proteins
- prioritizing candidate antigens
- generating hypotheses for experimental validation
- integrating multimodal biological data

Such workflows mirror how **modern biopharma teams apply machine learning to accelerate antigen discovery**.

---

## Future Enhancements

### Structural Biology

- integrate AlphaFold protein structures
- compute solvent accessibility
- add surface exposure scores

### Immunology

- predict B-cell epitopes
- incorporate epitope density
- evaluate antigen conservation across strains

### Literature Mining

- apply **SciBERT** to extract antigen evidence from PubMed
- compute a literature support score

### Modeling

- compare Random Forest with XGBoost and neural networks
- apply **SHAP** for model interpretability

---

## Example Visualization
<img width="1303" height="836" alt="dashboard" src="https://github.com/user-attachments/assets/a1ea5e1c-0db2-4eb1-befd-bc8819842c3f" />


---

## Running the Dashboard

Install dependencies:

```bash
pip install -r requirements.txt

Run the Streamlit application:
streamlit run visualization/streamlit_app.py

Motivation

This project was developed to explore how AI methods can complement experimental vaccinology.

By combining machine learning, biological features, and interactive tools, the workflow demonstrates how computational approaches can help guide vaccine target discovery and translational research.
