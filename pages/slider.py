from typing import Counter
import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from .utils import arr2PIL
from .find_k_neighbours import find_k_neighbours
import skimage

# def arr2PIL(arr):
#     arr = (arr+1)/2*255
#     arr = arr.astype('uint8')
#     img = Image.fromarray(arr)
#     return img


def app():
    st.title("Generate art")
    st.write("Click the generate button to create a piece of art using our trained deep learning generator.")
    st.write("Use the slider to view the evolution of the image from random noise to the final artwork.")

    @st.cache(allow_output_mutation=True)
    def load_models(model_list):
        return [tf.keras.models.load_model(model_name) for model_name in model_list]


    def get_noise():
        return np.random.normal(0, 1, (32,100))

    @st.cache(allow_output_mutation=True)
    def get_muatable_list():
        return []

    @st.cache(allow_output_mutation=True)
    def get_muatable_list_result():
        return []

    @st.cache(allow_output_mutation=True)
    def get_muatable_list_images():
        return []

    model_list = ['models/model_epoch_0.h5', 'models/model_epoch_1.h5', 'models/model_epoch_100.h5', 'models/model_epoch_1000.h5', 'models/model_epoch_10000.h5', 'models/model_epoch_12100.h5']

    models = load_models(model_list)

    if 'slider' not in st.session_state:
        st.session_state['slider'] = 0

    button = st.button('GENERATE')

    current_all_images = get_muatable_list()
    result_cache = get_muatable_list_result()

    if button or len(current_all_images) > 0:
        if button:
            st.session_state['slider'] += 1

        if button and len(current_all_images) > 0:
            current_all_images.clear()
            result_cache.remove(result_cache[0])

        if len(current_all_images) == 0:
            noise = get_noise()
            for model in models:
                current_all_images.append(model.predict(noise))



        final_image = current_all_images[-1]
        col1, col2 = st.columns(2)
        col2.write('Final image')
        col2.image(arr2PIL(final_image[0]),use_column_width=True)
        #model_list_len = len(model_list)-1
        #max = [i for i, v in enumerate(model_list)]
        #sliders = st.slider('MODEL SELECTION',0,len(model_list)-1,0,step=1, key=st.session_state['slider'])

        slider_labels = ['Noise', 'Epoch 1', 'Epoch 100', 'Epoch 1000', 'Epoch 10,000', 'Final Epoch']
        slider = st.select_slider('MODEL SELECTION', options=slider_labels, key=st.session_state['slider'])

        cpt = 0

        for i in slider_labels:
            if slider == i:
                break
            cpt += 1

        col1.write(f'{slider}')
        slider_image = current_all_images[cpt]

        col1.image(arr2PIL(slider_image[0]),use_column_width=True)


        with st.container():

            st.title('Find similar images')
            st.write("Encodes generated images into latent space with Abstract Expressionism dataset \
                    and finds 4 closest neighbours in that space.")


            knn_image = (arr2PIL(final_image[0]))
            resized_img = knn_image.resize((128, 128))
            st.image(resized_img)
            st.write("Similar images:")

            # find_k_neighbours
            result_cache = get_muatable_list_result()
            if len(result_cache) == 0:
                result = find_k_neighbours(transform = False, image = resized_img,
                file_location = "data/abstract_ex.csv")
                result_cache.append(result)

            result = result_cache[0]


            col1, col2, col3, col4 = st.columns(4)

            with col1:
                image1 = skimage.io.imread(f"images/abstract_ex/{result[0]['Image_filename']}", as_gray=False)
                st.image(image1)
                st.write(f"{result[0]['Title']}" )
                st.write(f"by {result[0]['Artist']}")

            with col2:
                st.image(f"images/abstract_ex/{result[1]['Image_filename']}")
                st.write(f"{result[1]['Title']}")
                st.write(f"by {result[1]['Artist']}")

            with col3:
                st.image(f"images/abstract_ex/{result[2]['Image_filename']}")
                st.write(f"{result[2]['Title']}")
                st.write(f"by {result[2]['Artist']}")

            with col4:
                st.image(f"images/abstract_ex/{result[3]['Image_filename']}")
                st.write(f"{result[3]['Title']}")
                st.write(f"by {result[3]['Artist']}")


#st.slider('MODEL SELECTION',0,len(model_list)-1,0,step=1, key=st.session_state['slider'])
#models = load_models(list(model_list.values()))
#st.select_slider('MODEL SELECTION', options=slider_labels, value=list(model_list.keys()), key=st.session_state['slider'])
#{'0':'models/model_epoch_0.h5', '1':'models/model_epoch_1.h5', '2':'models/model_epoch_100.h5', '3':'models/model_epoch_1000.h5', '4':'models/model_epoch_10000.h5'}
# if __name__=='__main__':
#     app()
