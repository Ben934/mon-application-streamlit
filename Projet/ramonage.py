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
            "Date d'intervention", "Élément de chauffe", "Difficulté du ramonage", 
            "Difficulté d'accès", "Commentaire"
        ])

# Fonction pour enregistrer les données
def save_data(data):
    data.to_csv(FILENAME, index=False)

# Charger les données
data = load_data()

# Interface Streamlit
st.title("Gestion des Ramonages")

# Choix entre ajouter un nouveau client ou modifier un client existant
action = st.radio("Action :", ["Nouveau client", "Modifier client"])

if action == "Nouveau client":
    st.header("Ajouter un nouveau client")
    
    # Champs de saisie
    nom_client = st.text_input("Nom Client")
    numero_tel = st.text_input("Numéro de téléphone")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.text_input("Code Postal")
    date_intervention = st.date_input("Date d'intervention")
    element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"])
    difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"])
    difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"])
    commentaire = st.text_area("Commentaire")

    # Bouton pour ajouter un nouveau client
    if st.button("Enregistrer"):
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
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        save_data(data)
        st.success("Client ajouté avec succès !")
        st.experimental_rerun()

elif action == "Modifier client":
    st.header("Modifier un client existant")
    
    # Recherche du client par nom
    client_nom = st.text_input("Rechercher par Nom Client")
    client_data = data[data["Nom Client"] == client_nom]
    
    if not client_data.empty:
        st.write("Client trouvé. Modifiez les informations ci-dessous :")
        
        # Charger les données existantes
        numero_tel = st.text_input("Numéro de téléphone", client_data.iloc[0]["Numéro de tel"])
        adresse = st.text_input("Adresse", client_data.iloc[0]["Adresse"])
        ville = st.text_input("Ville", client_data.iloc[0]["Ville"])
        code_postal = st.text_input("Code Postal", client_data.iloc[0]["Code Postal"])
        date_intervention = st.date_input("Date d'intervention", pd.to_datetime(client_data.iloc[0]["Date d'intervention"]))
        element_chauffe = st.selectbox(
            "Élément de chauffe", 
            ["Cheminée", "Insert", "Poêle à bois"], 
            index=["Cheminée", "Insert", "Poêle à bois"].index(client_data.iloc[0]["Élément de chauffe"])
        )
        difficulte_ramonage = st.selectbox(
            "Difficulté du ramonage", 
            ["Facile", "Moyen", "Difficile"], 
            index=["Facile", "Moyen", "Difficile"].index(client_data.iloc[0]["Difficulté du ramonage"])
        )
        difficulte_acces = st.selectbox(
            "Difficulté d'accès", 
            ["Facile", "Moyen", "Difficile"], 
            index=["Facile", "Moyen", "Difficile"].index(client_data.iloc[0]["Difficulté d'accès"])
        )
        commentaire = st.text_area("Commentaire", client_data.iloc[0]["Commentaire"])

        # Bouton pour enregistrer les modifications
        if st.button("Modifier"):
            index = client_data.index[0]
            data.loc[index, "Numéro de tel"] = numero_tel
            data.loc[index, "Adresse"] = adresse
            data.loc[index, "Ville"] = ville
            data.loc[index, "Code Postal"] = code_postal
            data.loc[index, "Date d'intervention"] = str(date_intervention)
            data.loc[index, "Élément de chauffe"] = element_chauffe
            data.loc[index, "Difficulté du ramonage"] = difficulte_ramonage
            data.loc[index, "Difficulté d'accès"] = difficulte_acces
            data.loc[index, "Commentaire"] = commentaire
            
            save_data(data)
            st.success("Client modifié avec succès !")
            st.experimental_rerun()
    elif client_nom:
        st.warning("Aucun client trouvé avec ce nom.")

# Afficher les données des clients par ville
st.header("Clients par Ville")
ville_selection = st.selectbox("Sélectionnez une ville :", data["Ville"].unique())
clients_ville = data[data["Ville"] == ville_selection]
st.write(clients_ville)
