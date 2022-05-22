import streamlit as st
from PIL import Image

def app():

    st.title('Acknowledgements')

    st.write("Huge thank you to Yassine, Yannis, Cristophe, Julio, Marie, \
        and all the other Le Wagon staff for being so patient and generous \
        with their time and knowledge.")

    st.write("We also utilised the resources below when working on our project:")
    st.write("[Generating modern art using GAN](https://towardsdatascience.com/generating-modern-arts-using-generative-adversarial-network-gan-on-spell-39f67f83c7b4)")
    st.write("[Creating Romantic period art with Tensorflow DCGAN](https://www.kaggle.com/amyjang/creating-romantic-period-art-w-tensorflow-dcgan)")
    st.write("[Content-based image retrieval using autoencoders](https://github.com/ArunadeviRamesh/Content-Based-Image-Retrieval-using-Autoencoders-Unsupervised-deep-learning-algorithms)")
    st.write("[WikiArt Kaggle dataset](https://www.kaggle.com/antoinegruson/-wikiart-all-images-120k-link)")
