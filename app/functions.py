import streamlit as st
from PIL import Image
import requests
import json

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


def get_prediction(path):
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


def upload_image():
    try:
        uploaded_file = st.file_uploader("Choisissez un fichier", type=['png', 'jpg', 'jpeg'])
        st.image(uploaded_file, width=600)
        img = Image.open(uploaded_file)
        path = 'app/img/uploaded_image.png'
        img.save(path)
    except:
        pass


def get_painting_information(path):
    try:
        pred_current = get_prediction(path)
        st.write("- **Courant artistique** :", pred_current)
        st.write("- **Description du courant** :")
        st.write("- **Période historique** :")
        st.write("- **Artistes influents** :")
    except:
        pass


def login_to_account():
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')

    # Check if user exist in database
    if st.checkbox("Se connecter"):
        # requête à modifier pour soumettre le nom et le mot de passe
        r = requests.get(f'http://127.0.0.1:8000/user/?username={username}&password={password}')

        if r.status_code == 403:
            st.warning("Nom d'utilisateur ou mot de passe non reconnu")
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


def create_account():
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


def read_comments():
    r = requests.get(f'http://127.0.0.1:8000/comments')
    data = r.json()
    for dat in data:
        st.sidebar.write(dat['creation_date'])
        st.sidebar.write(dat['content'])
        st.sidebar.markdown('____')