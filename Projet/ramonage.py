import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.write(f"Répertoire courant : {os.getcwd()}")
# Chargement et sauvegarde des données
def load_data():
    if os.path.exists("clients.csv"):
        st.info("Chargement des données depuis 'clients.csv'.")
        return pd.read_csv("clients.csv")
    else:
        st.warning("'clients.csv' introuvable. Création d'un fichier vide.")
        return pd.DataFrame(columns=[
            "Nom Client", "Numéro de tel", "Adresse", "Ville", "Code Postal",
            "Date d'intervention", "Élément de chauffe",
            "Difficulté du ramonage", "Difficulté d'accès", "Commentaire", "Prix de l'intervention"
        ])



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
    # Vérification du numéro de téléphone (doit être composé uniquement de chiffres)
    numero_tel = st.text_input("Numéro de tel", key="nouveau_tel")
    if numero_tel and not numero_tel.isdigit():
        st.error("Le numéro de téléphone doit contenir uniquement des chiffres.")

    # Vérification du code postal (doit être composé de 5 chiffres)
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
    # Affichage des clients avec formatage des champs
    data["Numéro de tel"] = data["Numéro de tel"].astype(str)
    data["Code Postal"] = data["Code Postal"].astype(str)
    data["Numéro de tel"] = data["Numéro de tel"].apply(format_tel)
    data["Code Postal"] = data["Code Postal"].apply(format_code_postal)
    st.write(data)

elif menu == "Modifier un client":

    # Affichage des clients avec formatage des champs
    data["Numéro de tel"] = data["Numéro de tel"].astype(str)
    data["Code Postal"] = data["Code Postal"].astype(str)
    data["Numéro de tel"] = data["Numéro de tel"].apply(format_tel)
    data["Code Postal"] = data["Code Postal"].apply(format_code_postal)
    st.write(data)

    st.subheader("Modifier un client existant")

    # Recherche du client par nom
    nom_recherche = st.text_input("Rechercher un client par nom")
    client_data = data[data["Nom Client"] == nom_recherche]

    if not client_data.empty:
        st.success("Client trouvé ! Modifiez les informations ci-dessous :")
        
        # Affichage des données du client dans un tableau
        st.write("**Données actuelles du client :**")
        client_data["Numéro de tel"] = client_data["Numéro de tel"].apply(format_tel)
        client_data["Code Postal"] = client_data["Code Postal"].apply(format_code_postal)
        st.write(client_data)

        # Formulaire de modification
        nom_client = st.text_input("Nom Client", value=client_data.iloc[0]["Nom Client"])
        
        # Gestion du numéro de téléphone avec vérification de NaN
        numero_tel_val = client_data.iloc[0]["Numéro de tel"]
        if pd.notna(numero_tel_val):
            numero_tel_val = int(numero_tel_val)  # Convertir en int uniquement si non NaN
        numero_tel = st.text_input("Numéro de tel", value=numero_tel_val)

        adresse = st.text_input("Adresse", value=client_data.iloc[0]["Adresse"])
        ville = st.text_input("Ville", value=client_data.iloc[0]["Ville"])
        
        # Gestion du code postal avec vérification de NaN
        code_postal_val = client_data.iloc[0]["Code Postal"]
        if pd.notna(code_postal_val):
            code_postal_val = int(code_postal_val)  # Convertir en int uniquement si non NaN
        code_postal = st.text_input("Code Postal", value=code_postal_val)

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

        # Bouton de modification
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
        
        # Bouton de suppression
        if st.button("Supprimer le client"):
            data = data[data["Nom Client"] != nom_client]
            save_data(data)
            st.success(f"{nom_client} a été supprimé avec succès.")
    else:
        st.warning("Client introuvable.")

elif menu == "Statistiques":

    # Affichage des clients avec formatage des champs
    data["Numéro de tel"] = data["Numéro de tel"].astype(str)
    data["Code Postal"] = data["Code Postal"].astype(str)
    data["Numéro de tel"] = data["Numéro de tel"].apply(format_tel)
    data["Code Postal"] = data["Code Postal"].apply(format_code_postal)
    st.write(data)

    st.subheader("Statistiques sur les clients")
    
    # Graphique du nombre de clients par ville
    st.write("**Répartition des clients par ville :**")
    if not data.empty:
        ville_counts = data["Ville"].value_counts()
        fig, ax = plt.subplots()
        ville_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Nombre de clients par ville")
        ax.set_xlabel("Ville")
        ax.set_ylabel("Nombre de clients")
        st.pyplot(fig)

        # Graphique des revenus par mois
        st.write("**Revenus par mois :**")
        
        # S'assurer que la colonne "Date d'intervention" est bien en format datetime
        data["Date d'intervention"] = pd.to_datetime(data["Date d'intervention"], errors='coerce')
        
        # Extraire l'année et le mois
        data["Mois_Année"] = data["Date d'intervention"].dt.to_period("M")  # Format "YYYY-MM"
        
        # S'assurer que la colonne "Prix de l'intervention" est numérique
        data["Prix de l'intervention"] = pd.to_numeric(data["Prix de l'intervention"], errors='coerce')
        
        # Regrouper par mois et sommer les revenus
        revenus_mensuels = data.groupby("Mois_Année")["Prix de l'intervention"].sum().sort_index()
        
        # Tracer l'histogramme
        fig, ax = plt.subplots(figsize=(10, 6))
        revenus_mensuels.plot(kind="bar", ax=ax, color="lightgreen")
        ax.set_title("Revenus mensuels")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Revenus (€)")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée disponible pour générer des statistiques.")
