import streamlit as st


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
                if username != 'ffffff' or password != "ffffff":  # à remplacer par les code et user récupérés de la base
                    st.write(" - User inconnu - ")
                else:
                    st.success("Bonjour {}".format(username))
                    placeholder = st.empty()
                    placeholder.text_area("Saisissez votre commentaire :")

                    if st.button("Envoyer"):
                        # ajouter le code pour l'insertion du commentaire dans la base et si ok :
                        st.success("Votre commentaire a bien été enregistré")

                        placeholder.empty()  # pour réinitialiser le champ commentaire

        if task == "Je n'ai pas de compte":
            create = st.selectbox(" Voulez-vous créer un compte ? ", ["Oui", "Non"])
            if create == "Oui":
                new_user = st.text_input("Nom d'utilisateur")
                new_password = st.text_input("Mot de passe", type='password')
                if st.button("S'inscrire"):
                    # ajouter le code pour l'insertion en base et si code retour ok alors :
                    st.success(
                        "Votre compte a correctement été créé. Veuillez vous connecter pour laisser votre commentaire")


if __name__ == '__main__':
    main()
