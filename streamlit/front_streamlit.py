import streamlit as st
import requests
import json


def main():
    st.image("streamlit/img/logo.png", width=600)

    ####### ---- IMAGE UPLOADER ---- ######
    st.subheader("1. Je télécharge une photo")
    st.markdown('  ')

    # Add try except to prevent error when file is not uploaded
    try:
        uploaded_file = st.file_uploader("Choisissez un fichier", type=['png', 'jpg'])
        st.image(uploaded_file)
    except:
        pass

    ####### ---- INFORMATIONS ABOUT PAINTING ---- ######
    st.subheader("2. Les informations sur l'oeuvre :art:")
    st.markdown('  ')

    st.write("- **Courant artistique** :")
    st.write("- **Description du courant** :")
    st.write("- **Période historique** :")
    st.write("- **Artistes influents** :")

    ####### ---- RECOMMANDATION SYSTEM ---- ######
    st.subheader("3. On vous recommande :heavy_check_mark:")
    st.markdown('  ')

    ####### ---- REVIEW ---- ######
    st.subheader("4. Donner mon avis sur l'appli :star:")

    opinion = st.selectbox("Votre choix", ["Oui", "Non"])
    if opinion == "Oui":
        task = st.selectbox("Possédez-vous un compte ?", ["J'ai un compte", "Je n'ai pas de compte"])

        if task == "J'ai un compte":
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type='password')

            # Check if user exist in database
            if st.button("Se connecter"):
                # requête à modifier pour soumettre le nom et le mot de passe
                r = requests.get(f'http://127.0.0.1:8000/user/{username}')

                if r.status_code == 403:
                    st.write("Nom d'utilisateur non reconnu")
                else:
                    st.success("Bonjour {}".format(username))
                    placeholder = st.empty()
                    placeholder.text_area("Saisissez votre commentaire :")

                    if st.button("Envoyer"):
                        # ajouter le code pour l'insertion du commentaire dans la base et si ok :
                        r = requests.post('http://127.0.0.1:8000/comments/')
                        st.write(r.status_code)
                        st.success("Votre commentaire a bien été enregistré")

                        placeholder.empty()  # pour réinitialiser le champ commentaire

        if task == "Je n'ai pas de compte":
            create = st.selectbox(" Voulez-vous créer un compte ? ", ["Oui", "Non"])

            if create == "Oui":
                new_user = st.text_input("Nom d'utilisateur")
                new_password = st.text_input("Mot de passe", type='password')

                if st.button("S'inscrire"):
                    # /!\ Make json.dumps everytime otherwise you couldn't submit information to database
                    requests.post('http://127.0.0.1:8000/user/',
                                  data=json.dumps({"username": new_user, "password": new_password}))

                    st.success(
                        "Votre compte a correctement été créé. Veuillez vous connecter pour laisser votre commentaire")


if __name__ == '__main__':
    main()
