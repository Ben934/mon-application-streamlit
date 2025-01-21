import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid  # Import de uuid pour générer des identifiants uniques

# Chargement et sauvegarde des données
def load_data():
    if os.path.exists("clients.csv"):
        return pd.read_csv("clients.csv")
    else:
        # Ajouter la colonne "id_intervention" si elle n'existe pas déjà
        return pd.DataFrame(columns=[
            "id_intervention", "Nom Client", "Numéro de tel", "Adresse", "Ville", "Code Postal",
            "Date d'intervention", "Élément de chauffe",
            "Difficulté du ramonage", "Difficulté d'accès", "Commentaire", "Prix de l'intervention"
        ])

def save_data(data):
    data.to_csv("clients.csv", index=False)

# Fonction pour générer un id unique pour chaque client
def generate_id():
    return str(uuid.uuid4())

# Chargement des données
data = load_data()

# Titre de l'application
st.title("Gestion des Ramonages")

# Menu principal
menu = st.sidebar.radio("Menu", ["Ajouter un client", "Clients", "Modifier un client", "Statistiques"])

if menu == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")

    # Formulaire d'ajout
    nom_client = st.text_input("Nom Client", key="nouveau_nom")
    numero_tel = st.text_input("Numéro de tel", key="nouveau_tel")
    adresse = st.text_input("Adresse", key="nouvelle_adresse")
    ville = st.text_input("Ville", key="nouvelle_ville")
    code_postal = st.text_input("Code Postal", key="nouveau_code_postal")
    date_intervention = st.date_input("Date d'intervention", key="nouvelle_date")
    element_chauffe = st.selectbox("Élément de chauffe", ["Cheminée", "Insert", "Poêle à bois"], key="nouvel_element")
    difficulte_ramonage = st.selectbox("Difficulté du ramonage", ["Facile", "Moyen", "Difficile"], key="nouvelle_difficulte_ramonage")
    difficulte_acces = st.selectbox("Difficulté d'accès", ["Facile", "Moyen", "Difficile"], key="nouvelle_difficulte_acces")
    commentaire = st.text_area("Commentaire", key="nouveau_commentaire")
    prix_intervention = st.number_input("Prix de l'intervention (€)", min_value=0.0, format="%.2f", key="nouveau_prix")

    if st.button("Ajouter client"):
        new_row = {
            "id_intervention": generate_id(),
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
    st.write(data)

elif menu == "Modifier un client":
    st.subheader("Modifier un client existant")

    nom_recherche = st.text_input("Rechercher un client par nom")
    client_data = data[data["Nom Client"] == nom_recherche]

    # Vérifier si la colonne "id_intervention" existe
    if "id_intervention" not in client_data.columns:
        st.error("La colonne 'id_intervention' est manquante dans les données.")
    else:
        if not client_data.empty:
            st.success("Client trouvé ! Modifiez les informations ci-dessous :")
            
            # Formulaire de modification
            id_intervention = client_data.iloc[0]["id_intervention"]  # Conserver l'id pour la modification
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
                data = data[data["id_intervention"] != id_intervention]  # Supprimer par id unique
                save_data(data)
                st.success(f"Client avec ID {id_intervention} supprimé avec succès.")
        else:
            st.warning("Client introuvable.")

elif menu == "Statistiques":
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
    else:
        st.warning("Aucune donnée disponible pour générer des statistiques.")
