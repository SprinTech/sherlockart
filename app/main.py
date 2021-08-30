import streamlit as st
from functions import upload_image, get_painting_information, login_to_account, create_account, read_comments

st.image("app/img/logo.png", width=600)

# 1 - IMAGE UPLOADER
st.subheader("1. Je télécharge une photo")
st.markdown('  ')

upload_image()
validate = st.button("Valider")

# 2 - PAINTING INFORMATION
st.subheader("2. Les informations sur l'oeuvre :art:")
st.markdown('  ')

if validate:
    get_painting_information('app/img/uploaded_image.png')


# 3 - RECOMMANDATION
st.subheader("3. On vous recommande :heavy_check_mark:")
st.markdown('  ')

# 4 - REVIEW
st.subheader("4. Donner mon avis sur l'appli :star:")
st.markdown('  ')

opinion = st.selectbox("Votre choix", ["Oui", "Non"])
if opinion == "Oui":
    has_account = st.selectbox("Possédez-vous un compte ?", ["J'ai un compte", "Je n'ai pas de compte"])

    if has_account == "J'ai un compte":
        login_to_account()
    else:
        create_account()

# 5 - LIVRE D'OR
st.sidebar.subheader("LIVRE D'OR")
st.sidebar.markdown(' ')

read_comments()
