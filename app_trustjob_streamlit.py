from pathlib import Path
import re

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "outputs" / "trustjob_pipeline.joblib"
TEXT_FIELDS = [
    "title", "location", "department", "salary_range", "company_profile",
    "description", "requirements", "benefits", "employment_type",
    "required_experience", "required_education", "industry", "function"
]
RISK_TERMS = [
    "upfront fee", "processing fee", "application fee", "pay a fee",
    "wire transfer", "western union", "money order", "bank account",
    "social security number", "passport", "frais de dossier",
    "paiement préalable", "virement bancaire", "coordonnées bancaires"
]

st.set_page_config(page_title="TrustJob AI", page_icon="🛡️", layout="centered")
st.title("TrustJob AI")
st.subheader("Vérification expérimentale d’une offre d’emploi")
st.write(
    "Saisissez les informations visibles dans l’annonce. Le modèle estime si elle "
    "ressemble aux annonces frauduleuses de son jeu d’entraînement."
)
st.info(
    "Cette application fournit une estimation pédagogique. Elle ne prouve pas "
    "juridiquement qu’une annonce ou une entreprise est frauduleuse."
)

@st.cache_resource
def load_model(path):
    return joblib.load(path)

if not MODEL_PATH.exists():
    st.error(
        "Le modèle n’a pas encore été créé. Exécutez le notebook jusqu’à la cellule "
        "de sauvegarde du pipeline complet."
    )
    st.stop()

model = load_model(str(MODEL_PATH))

with st.form("job_posting_form"):
    raw = {
        "title": st.text_input("Titre du poste"),
        "location": st.text_input("Localisation"),
        "department": st.text_input("Département"),
        "salary_range": st.text_input("Salaire indiqué"),
        "company_profile": st.text_area("Profil de l’entreprise"),
        "description": st.text_area("Description de l’offre"),
        "requirements": st.text_area("Exigences et qualifications"),
        "benefits": st.text_area("Avantages proposés"),
        "employment_type": st.text_input("Type d’emploi"),
        "required_experience": st.text_input("Expérience requise"),
        "required_education": st.text_input("Formation requise"),
        "industry": st.text_input("Secteur d’activité"),
        "function": st.text_input("Fonction"),
    }
    telecommuting = st.checkbox("Télétravail proposé")
    has_company_logo = st.checkbox("Logo d’entreprise présent")
    has_questions = st.checkbox("L’annonce pose des questions")
    submitted = st.form_submit_button("Analyser l’offre")

if submitted:
    row = {
        "text": " ".join(str(raw[col] or "") for col in TEXT_FIELDS),
        "telecommuting": int(telecommuting),
        "has_company_logo": int(has_company_logo),
        "has_questions": int(has_questions),
    }
    prediction = int(model.predict(pd.DataFrame([row]))[0])
    if prediction == 1:
        st.error("Résultat : annonce probablement FRAUDULEUSE selon le modèle.")
    else:
        st.success("Résultat : annonce probablement LÉGITIME selon le modèle.")

    full_text = " ".join(str(value or "") for value in raw.values()).lower()
    found_terms = [
        term for term in RISK_TERMS
        if re.search(r"\b" + re.escape(term) + r"\b", full_text)
    ]
    st.markdown("### Indicateurs lexicaux")
    if found_terms:
        st.warning("Termes à vérifier : " + ", ".join(found_terms))
    else:
        st.write("Aucun terme de la liste de repérage n’a été trouvé.")
    st.caption(
        "Ces termes sont des règles descriptives indépendantes du modèle. Ils peuvent "
        "apparaître dans des annonces légitimes et ne constituent pas une preuve."
    )
