import streamlit as stream
from dotenv import load_dotenv
import os
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI 

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


# Configuration de la page Streamlit avec un titre
stream.set_page_config(page_title="WizWheel : Your Personal Car Assistant", layout="wide")
stream.header("")

# Code HTML avec JavaScript pour la mise en page
javascript_code = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("container");
    const logo = document.getElementById("logo");
    const title = document.getElementById("title");

    // Fonction pour ajuster la mise en page en fonction de la taille de l'écran
    function adjustLayout() {
        if (window.innerWidth <= 600) {
            container.style.flexDirection = 'column';
            title.style.marginLeft = '0';
            title.style.marginTop = '10px';
        } else {
            container.style.flexDirection = 'row';
            title.style.marginLeft = '20px';
            title.style.marginTop = '0';
        }
    }

    // Appel de la fonction d'ajustement de mise en page lors du chargement de la page et lors du redimensionnement de la fenêtre
    adjustLayout();
    window.addEventListener('resize', adjustLayout);
});
</script>
"""

html_code = """
<div id="container" style="display: flex; align-items: center;">
    <img id="logo" src="https://cdn.discordapp.com/attachments/772845550532820992/1224095545002295488/Red_and_Blue_Illustrative_Car_Engineering_Logo__1_-removebg-preview.png?ex=661c3ed0&is=6609c9d0&hm=adbdd00332e435d3fc0295fe5a184e1712a9c2b8b6e8062b592bee844b9dfcc2&" width="100">
    <h1 id="title" style="margin-left: 20px; color: white;">WizWheel : Your Personal Car Assistant</h1>
</div>
"""

stream.write(javascript_code, unsafe_allow_html=True)
stream.markdown(html_code, unsafe_allow_html=True)

# Récupération de la clé API à partir de la variable d'environnement
api_key = os.getenv("API_KEY")

# Vérification si la clé API est bien définie 
if not api_key:
    print("OPENAI_API_KEY is not set")
    exit(1)

print("OPEN_AI_API_KEY is set")

# L'utilisateur peut uploader un ou plusieurs fichiers CSV
multiple_input_csv_file = stream.file_uploader("Upload a CSV file", type="csv", accept_multiple_files=True)

# Si l'utilisateur a uploadé un fichier CSV
if multiple_input_csv_file:
    # Créer un agent pour intéragir avec les fichiers CSV
    agent = create_csv_agent(OpenAI(temperature=0), multiple_input_csv_file, verbose=True)
    # Demander à l'utilisateur de poser une question sur les CSV 
    user_question = stream.text_input("Ask a question about your CSV: ")

    #Si l'utilisateur a posé une question 
    if user_question:
        # Afficher un spinner pendant que l'agent traite la question 
        with stream.spinner(text="In progress..."):
            # Afficher la réponse de l'agent à la question de l'utilisateur 
            stream.write(agent.run(user_question))

