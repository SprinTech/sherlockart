import streamlit as st
import requests
import json
from PIL import Image

import numpy as np
from keras import preprocessing, models


def preprocess_image(path):
    """
    Preparing an image to give it to the computer vision model
    """
    test_image = preprocessing.image.load_img(path, target_size=(224, 224))
    test_image = preprocessing.image.img_to_array(test_image)
    test_image /= 255.
    test_image = np.expand_dims(test_image, axis=0)
    return test_image


def get_prediction_from_path(path):
    """
    Given the path of a picture,
    the model (loaded from a .h5 file)
    will return a prediction of its current
    """

    # Load the model with keras
    model = models.load_model('/home/apprenant/PycharmProjects/sherlockart/API_1/models/my_model.h5')

    # We need labels
    labels = {0: 'Abstract Expressionism', 1: 'Baroque', 2: 'Byzantine Art', 3: 'Cubism', 4: 'Early Renaissance',
              5: 'Expressionism', 6: 'High Renaissance', 7: 'Impressionism', 8: 'Mannerism', 9: 'Neoplasticism',
              10: 'Northern Renaissance', 11: 'Pop Art', 12: 'Post-Impressionism', 13: 'Primitivism',
              14: 'Proto Renaissance', 15: 'Realism', 16: 'Romanticism', 17: 'Suprematism', 18: 'Surrealism',
              19: 'Symbolism'}

    # Preprocessing the image
    test_image = preprocess_image(path)

    # Get prediction
    prediction = model.predict(test_image)
    prediction_probability = np.amax(prediction)
    prediction_idx = np.argmax(prediction)

    return labels[prediction_idx].replace('_', ' ')


def main():
    st.image("streamlit/img/logo.png", width=600)

    ####### ---- IMAGE UPLOADER ---- ######
    st.subheader("1. Je télécharge une photo")
    st.markdown('  ')

    # Add try except to prevent error when file is not uploaded
    try:
        uploaded_file = st.file_uploader("Choisissez un fichier", type=['png', 'jpg', 'jpeg'])
        st.image(uploaded_file, width=600)
        img = Image.open(uploaded_file)
        path = 'streamlit/img/uploaded_image.png'
        img.save(path)

    except:
        pass

    ####### ---- INFORMATIONS ABOUT PAINTING ---- ######
    st.subheader("2. Les informations sur l'oeuvre :art:")
    st.markdown('  ')
    pred_current = get_prediction_from_path(path)

    st.write("- **Courant artistique** :", pred_current)
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
            if st.checkbox("Se connecter"):
                # requête à modifier pour soumettre le nom et le mot de passe
                r = requests.get(f'http://127.0.0.1:8000/user/?username={username}&password={password}')

                if r.status_code == 403:
                    st.warning("Nom d'utilisateur non reconnu")
                else:
                    st.success("Bonjour {}".format(username))
                    placeholder = st.empty()
                    review = st.text_area("Saisissez votre commentaire :")

                    if st.checkbox("Envoyer"):
                        # ajouter le code pour l'insertion du commentaire dans la base et si ok :
                        r = requests.post(f'http://127.0.0.1:8000/comments/?username={username}',
                                          data=json.dumps({"content": review}))
                        if r.status_code == 200:
                            st.success("Votre commentaire a bien été enregistré")
                            placeholder.empty()  # pour réinitialiser le champ commentaire

        if task == "Je n'ai pas de compte":
            create = st.selectbox(" Voulez-vous créer un compte ? ", ["Oui", "Non"])

            if create == "Oui":
                new_user = st.text_input("Nom d'utilisateur")
                new_password = st.text_input("Mot de passe", type='password')

                if st.button("S'inscrire"):
                    # /!\ Make json.dumps everytime otherwise you couldn't submit information to database
                    r = requests.post('http://127.0.0.1:8000/user/',
                                      data=json.dumps({"username": new_user, "password": new_password}))
                    if r.status_code == 200:
                        st.success(
                            "Votre compte a correctement été créé. Veuillez vous connecter pour laisser votre "
                            "commentaire")
                    else:
                        st.warning("Erreur. Compte déjà existant !")

    ####### ---- REVIEW ---- ######
    st.subheader("Livre d'or")
    r = requests.get(f'http://127.0.0.1:8000/comments')
    data = r.json()
    for dat in data:
        st.write(dat['creation_date'])
        st.write(dat['content'])
        st.markdown('____')


if __name__ == '__main__':
    main()
