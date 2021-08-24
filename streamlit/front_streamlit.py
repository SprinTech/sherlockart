import streamlit as st
#import streamlit.components.v1 as components
import sys
sys.path.insert(0, "/home/apprenant/PycharmProjects/sherlock-art")

def main():

    st.image("/home/apprenant/PycharmProjects/pythonProject/sherlock-art/streamlit/Sherlockart.png", width=600)
    st.subheader("1. Je télécharge une photo: ")
    st._transparent_write('  ')
    # chargement de l'image. try/except pour éviter d'avoir un message d'erreur si l'utilisateur supprime l'image
    try:
        uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])
        st.image(uploaded_file)
    except:
        pass
    st.subheader("2. lire les informations de l'oeuvre: ")
    # ici ajouter le code pour le ML
    st.write("les infos retournés par le ML") # à suprimmer sur les versions +
    #st.subheader("3. on vous recommande : )
    # ici ajouter le code recommandation

    st.subheader("3. Donner mon avis sur l'appli: ")
    #
    opinion = st.selectbox(" ", ["Oui", "Non"])
    if opinion =="Oui":
        task = st.selectbox(" ", ["J'ai un compte", "Je n'ai pas de compte"])

        if task == "J'ai un compte":
            username = st.text_input("User Name")
            password = st.text_input("Password", type='password')
        #ici code pour voir ci user exist dans base et récupérer le mot de passe
            if st.checkbox("login"):
                if username !='ffffff' or password != "ffffff": # àremplacer par les code et user récupérés de la base
                    st.write(" - User inconnu - ")
                else:
                    st.success("Bonjour {}".format(username))
                    placeholder = st.empty()
                    placeholder.text_area("Saisissez votre commentaire :")
                    if st.checkbox("send your comment"):
        # ajouter le code pour l'insertion du commentaire dans la base et si ok :
                        st.success("Votre commentaire a bien été enregistré")

                        placeholder.empty()  # pour réinitialiser le champ commentaire

        if task == "Je n'ai pas de compte":
            create = st.selectbox(" Voulez-vous créer un compte? ", ["oui", "non"])
            if create == "oui":
                new_user = st.text_input("User Name")
                new_password = st.text_input("Password", type = 'password')
                if st.checkbox("signUp"):
    #

    # ajouter le code pour l'insertion en base et si code retour ok alors :
                    st.success("Votre compte a correctement été créé. Veuillez vous connecter pour laisser votre commentaire")



if __name__== '__main__':
    main()