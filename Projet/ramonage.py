import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
import io

# URL brute de GitHub
CSV_URL = "https://raw.githubusercontent.com/Ben934/mon-application-streamlit/main/Projet/clients.csv"

def load_data():
    try:
        # Télécharger le fichier CSV depuis l'URL
        response = requests.get(CSV_URL)
        if response.status_code == 200:
            data = pd.read_csv(io.StringIO(response.text))
            st.success("Données chargées depuis GitHub avec succès.")
            return data
        else:
            st.error("Impossible de télécharger les données depuis GitHub.")
            return pd.DataFrame()  # Renvoie un DataFrame vide
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
data = load_data()

def save_data(data):
    data.to_csv("clients.csv", index=False)

# Chargement des données
data = load_data()

# Fonction pour formater le numéro de téléphone
def format_tel(numero_tel):
    if pd.notna(numero_tel):
        numero_tel = str(numero_tel)  # Convertir en chaîne
        if numero_tel.isdigit():
            return f"{numero_tel[:3]} {numero_tel[3:6]} {numero_tel[6:]}"  # Format '123 456 789'
    return numero_tel  # Retourne tel quel si NaN ou invalide

# Fonction pour formater le code postal
def format_code_postal(code_postal):
    if pd.notna(code_postal):
        code_postal = str(code_postal)  # Convertir en chaîne
        if code_postal.isdigit() and len(code_postal) == 5:
            return code_postal
    return code_postal  # Retourne tel quel si NaN ou invalide

# Titre de l'application
st.title("Gestion des Ramonages")

# Menu principal
menu = st.sidebar.radio("Menu", ["Ajouter un client", "Clients", "Modifier un client", "Statistiques"])

if menu == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")

    # Formulaire d'ajout
    nom_client = st.text_input("Nom Client", key="nouveau_nom")
    numero_tel = st.text_input("Numéro de tel", key="nouveau_tel")
    if numero_tel and not numero_tel.isdigit():
        st.error("Le numéro de téléphone doit contenir uniquement des chiffres.")
    code_postal = st.text_input("Code Postal", key="nouveau_code_postal")
    if code_postal and (not code_postal.isdigit() or len(code_postal) != 5):
        st.error("Le code postal doit contenir exactement 5 chiffres.")
    adresse = st.text_input("Adresse", key="nouvelle_adresse")
    ville = st.text_input("Ville", key="nouvelle_ville")
    date_intervention = st.date_input("Date d'intervention", key="nouvelle_date")
    element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"], key="nouvel_element")
    difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"], key="nouvelle_difficulte_ramonage")
    difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"], key="nouvelle_difficulte_acces")
    commentaire = st.text_area("Commentaire", key="nouveau_commentaire")
    prix_intervention = st.number_input("Prix de l'intervention (€)", min_value=0.0, format="%.2f", key="nouveau_prix")

    if st.button("Ajouter client"):
        new_row = {
            "Nom Client": nom_client,
            "Numéro de tel": numero_tel,
            "Adresse": adresse,
            "Ville": ville,
            "Code Postal": code_postal,
            "Date d'intervention": str(date_intervention),
            "Élément de chauffe": element_chauffe,
            "Difficulté du ramonage": difficulte_ramonage,
            "Difficulté d'accès": difficulte_acces,
            "Commentaire": commentaire,
            "Prix de l'intervention": prix_intervention
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        save_data(data)
        st.success("Client ajouté avec succès !")
        st.session_state.clear()

elif menu == "Clients":
    data["Numéro de tel"] = data["Numéro de tel"].astype(str)
    data["Code Postal"] = data["Code Postal"].astype(str)
    data["Numéro de tel"] = data["Numéro de tel"].apply(format_tel)
    data["Code Postal"] = data["Code Postal"].apply(format_code_postal)
    st.write(data)

elif menu == "Modifier un client":
    nom_recherche = st.text_input("Rechercher un client par nom")
    client_data = data[data["Nom Client"] == nom_recherche]

    if not client_data.empty:
        st.success("Client trouvé !")
        st.write(client_data)

        # Formulaire de modification
        nom_client = st.text_input("Nom Client", value=client_data.iloc[0]["Nom Client"])
        numero_tel = st.text_input("Numéro de tel", value=client_data.iloc[0]["Numéro de tel"])
        adresse = st.text_input("Adresse", value=client_data.iloc[0]["Adresse"])
        ville = st.text_input("Ville", value=client_data.iloc[0]["Ville"])
        code_postal = st.text_input("Code Postal", value=client_data.iloc[0]["Code Postal"])
        date_intervention = st.date_input("Date d'intervention", value=pd.to_datetime(client_data.iloc[0]["Date d'intervention"]))
        element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"], 
                                       index=["Cheminée", "Insert", "Poêle à bois"].index(client_data.iloc[0]["Élément de chauffe"]))
        difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"], 
                                           index=["Facile", "Moyen", "Difficile"].index(client_data.iloc[0]["Difficulté du ramonage"]))
        difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"], 
                                        index=["Facile", "Moyen", "Difficile"].index(client_data.iloc[0]["Difficulté d'accès"]))
        commentaire = st.text_area("Commentaire", value=client_data.iloc[0]["Commentaire"])
        prix_intervention = st.number_input("Prix de l'intervention (€)", min_value=0.0, 
                                           value=client_data.iloc[0]["Prix de l'intervention"], format="%.2f")

        if st.button("Modifier client"):
            index = client_data.index[0]
            data.loc[index, "Nom Client"] = nom_client
            data.loc[index, "Numéro de tel"] = numero_tel
            data.loc[index, "Adresse"] = adresse
            data.loc[index, "Ville"] = ville
            data.loc[index, "Code Postal"] = code_postal
            data.loc[index, "Date d'intervention"] = str(date_intervention)
            data.loc[index, "Élément de chauffe"] = element_chauffe
            data.loc[index, "Difficulté du ramonage"] = difficulte_ramonage
            data.loc[index, "Difficulté d'accès"] = difficulte_acces
            data.loc[index, "Commentaire"] = commentaire
            data.loc[index, "Prix de l'intervention"] = prix_intervention
            save_data(data)
            st.success("Client modifié avec succès !")

elif menu == "Statistiques":
    st.subheader("Statistiques sur les clients")
    if not data.empty:
        ville_counts = data["Ville"].value_counts()
        fig, ax = plt.subplots()
        ville_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Nombre de clients par ville")
        st.pyplot(fig)
