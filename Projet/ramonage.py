import streamlit as st
import pandas as pd
import os

# Nom du fichier CSV pour stocker les données
FILENAME = "ramonages.csv"

# Fonction pour charger les données existantes ou créer un fichier vide
def load_data():
    if os.path.exists(FILENAME):
        return pd.read_csv(FILENAME)
    else:
        return pd.DataFrame(columns=["Nom Client", "Numéro de tel", "Adresse", 
                                     "Élément de chauffe", "Difficulté du ramonage", 
                                     "Difficulté d'accès", "Commentaire"])

# Fonction pour sauvegarder les données dans le fichier CSV
def save_data(df):
    df.to_csv(FILENAME, index=False)

# Charger les données existantes
data = load_data()

# Titre de l'application
st.title("Enregistrement des Ramonages")

# Formulaire de saisie des caractéristiques
st.header("Ajouter un nouveau ramonage")

with st.form("form_ramonage"):
    nom_client = st.text_input("Nom du client")
    numero_tel = st.text_input("Numéro de téléphone")
    adresse = st.text_area("Adresse")
    element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"])
    difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"])
    difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"])
    commentaire = st.text_area("Commentaire")
    
    # Bouton pour soumettre le formulaire
    submitted = st.form_submit_button("Enregistrer")

# Si le formulaire est soumis, ajouter une nouvelle ligne dans le DataFrame
if submitted:
    if nom_client and numero_tel and adresse:
        new_row = {
            "Nom Client": nom_client,
            "Numéro de tel": numero_tel,
            "Adresse": adresse,
            "Élément de chauffe": element_chauffe,
            "Difficulté du ramonage": difficulte_ramonage,
            "Difficulté d'accès": difficulte_acces,
            "Commentaire": commentaire
        }
        data = pd.concat([data, new_row], ignore_index=True)
        save_data(data)
        st.success("Nouveau ramonage enregistré avec succès !")
    else:
        st.error("Veuillez remplir tous les champs obligatoires (nom, numéro, adresse).")

# Afficher les données existantes
st.header("Liste des Ramonages")
if not data.empty:
    st.dataframe(data)
else:
    st.write("Aucun ramonage enregistré pour le moment.")
