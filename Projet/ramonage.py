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
        return pd.DataFrame(columns=[
            "Nom Client", "Numéro de tel", "Adresse", "Ville", "Code Postal", 
            "Élément de chauffe", "Difficulté du ramonage", "Difficulté d'accès", "Commentaire"
        ])

# Fonction pour sauvegarder les données dans le fichier CSV
def save_data(df):
    df.to_csv(FILENAME, index=False)

# Charger les données existantes
data = load_data()

# Titre de l'application
st.title("Enregistrement des Ramonages")

# Section : Ajouter un nouveau ramonage
st.header("Ajouter un nouveau ramonage")

with st.form("form_ramonage"):
    nom_client = st.text_input("Nom du client")
    numero_tel = st.text_input("Numéro de téléphone")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.text_input("Code Postal")
    element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"])
    difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"])
    difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"])
    commentaire = st.text_area("Commentaire")
    
    # Bouton pour soumettre le formulaire
    submitted = st.form_submit_button("Enregistrer")

# Si le formulaire est soumis, ajouter une nouvelle ligne dans le DataFrame
if submitted:
    if nom_client and numero_tel and adresse and ville and code_postal:
        # Créer une nouvelle ligne avec les colonnes alignées
        new_row = pd.DataFrame([{
            "Nom Client": nom_client,
            "Numéro de tel": numero_tel,
            "Adresse": adresse,
            "Ville": ville,
            "Code Postal": code_postal,
            "Élément de chauffe": element_chauffe,
            "Difficulté du ramonage": difficulte_ramonage,
            "Difficulté d'accès": difficulte_acces,
            "Commentaire": commentaire
        }], columns=data.columns)
        
        # Concaténer en respectant les colonnes
        data = pd.concat([data, new_row], ignore_index=True)
        save_data(data)
        st.success("Nouveau ramonage enregistré avec succès !")
    else:
        st.error("Veuillez remplir tous les champs obligatoires (nom, numéro, adresse, ville, code postal).")

# Section : Modifier ou supprimer une ligne
st.header("Modifier ou supprimer un ramonage")
if not data.empty:
    with st.form("form_edit"):
        selected_index = st.selectbox("Sélectionnez une ligne à modifier/supprimer", data.index)
        selected_row = data.iloc[selected_index]
        
        nom_client = st.text_input("Nom du client", value=selected_row["Nom Client"])
        numero_tel = st.text_input("Numéro de téléphone", value=selected_row["Numéro de tel"])
        adresse = st.text_input("Adresse", value=selected_row["Adresse"])
        ville = st.text_input("Ville", value=selected_row["Ville"])
        code_postal = st.text_input("Code Postal", value=selected_row["Code Postal"])
        element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"], index=["Cheminée", "Insert", "Poêle à bois"].index(selected_row["Élément de chauffe"]))
        difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"], index=["Facile", "Moyen", "Difficile"].index(selected_row["Difficulté du ramonage"]))
        difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"], index=["Facile", "Moyen", "Difficile"].index(selected_row["Difficulté d'accès"]))
        commentaire = st.text_area("Commentaire", value=selected_row["Commentaire"])
        
        modify = st.form_submit_button("Modifier")
        delete = st.form_submit_button("Supprimer")
    
    if modify:
        # Mise à jour de la ligne sélectionnée
        data.at[selected_index, "Nom Client"] = nom_client
        data.at[selected_index, "Numéro de tel"] = numero_tel
        data.at[selected_index, "Adresse"] = adresse
        data.at[selected_index, "Ville"] = ville
        data.at[selected_index, "Code Postal"] = code_postal
        data.at[selected_index, "Élément de chauffe"] = element_chauffe
        data.at[selected_index, "Difficulté du ramonage"] = difficulte_ramonage
        data.at[selected_index, "Difficulté d'accès"] = difficulte_acces
        data.at[selected_index, "Commentaire"] = commentaire
        save_data(data)
        st.success("Ramonage modifié avec succès !")
    
    if delete:
        # Suppression de la ligne sélectionnée
        data = data.drop(index=selected_index).reset_index(drop=True)
        save_data(data)
        st.success("Ramonage supprimé avec succès !")

# Section : Représentation des clients par ville
st.header("Clients par ville")
if not data.empty:
    city_counts = data["Ville"].value_counts()
    st.bar_chart(city_counts)
else:
    st.write("Aucun ramonage enregistré pour afficher des statistiques.")

# Afficher les données existantes
st.header("Liste des Ramonages")
if not data.empty:
    st.dataframe(data)
else:
    st.write("Aucun ramonage enregistré pour le moment.")
