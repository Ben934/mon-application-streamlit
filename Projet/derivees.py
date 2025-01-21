import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, solve,latex, Eq, parse_expr
from sympy.parsing.sympy_parser import parse_expr

# Configuration de l'application
st.title("Calculateur de dérivée et tracé graphique avec racines")
st.write(
    "Entrez une fonction mathématique pour obtenir sa dérivée symbolique, ses graphiques, "
    "et les antécédents où f(x) = 0."
)

# Définir la variable symbolique
x = symbols('x')

# Entrée de l'utilisateur pour la fonction
fonction = st.text_input(
    "Entrez une fonction en fonction de x (ex: x**2, sin(x), exp(x)):",
    value="x**2 - 4"
)

# Calcul de la dérivée et du tracé
if fonction:
    try:
        # Remplacer 'e^x' par 'exp(x)' si l'utilisateur entre 'e^x'
        fonction = fonction.replace("e^", "exp(")  # Remplacer exponentielle
        expression = parse_expr(fonction, evaluate=False)
        
        # Calcul de la dérivée première
        derivee = diff(expression, x)
        
        # Résoudre f(x) = 0 pour trouver les racines
        racines = solve(Eq(expression, 0), x)
        
        # Fonction lambda pour évaluer la fonction et sa dérivée
        f = lambda t: float(expression.subs(x, t))
        f_prime = lambda t: float(derivee.subs(x, t))
        
        # Plage des valeurs de x pour tracer les courbes
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.array([f(val) for val in x_vals])
        y_prime_vals = np.array([f_prime(val) for val in x_vals])
        
        # Tracé graphique avec Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tracer la fonction f(x) et f'(x)
        ax.plot(x_vals, y_vals, label=r'$f(x)$', color='blue')
        ax.plot(x_vals, y_prime_vals, label=r"$f'(x)$", color='red', linestyle='--')
        
        # Tracer les racines (antécédents de f(x) = 0)
        for racine in racines:
            if racine.is_real:
                ax.plot(float(racine), 0, 'go', label=f"Racine x = {racine}")
        
        ax.set_title(f"Graphes de la fonction et de sa dérivée", fontsize=16)
        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("y", fontsize=12)
        ax.axhline(0, color='black',linewidth=1)
        ax.axvline(0, color='black',linewidth=1)
        ax.legend()
        ax.grid(True)

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
        
        # Affichage des résultats
        st.write("### Résultat :")
        st.write(f"**Fonction entrée :** {fonction}")
        st.latex(f"f(x) = {latex(expression)}")
        st.write("**Dérivée :**")
        st.latex(f"f'(x) = {latex(derivee)}")
        racines_str = ', '.join([f'{racine}' for racine in racines if racine.is_real])
        st.write(f"**Antécédents de f(x) = 0 :** {{{racines_str}}}")

    
    except Exception as e:
        st.error(f"Erreur lors de l'interprétation de la fonction : {e}")
