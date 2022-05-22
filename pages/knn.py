import streamlit as st
from pages.find_k_neighbours import find_k_neighbours
import skimage
from PIL import Image

def app():
    st.title('Find similar images')
    st.write('Encodes images into latent space and finds 4 closest neighbours in that space \
        from our dataset of 3,600 Abstract Expressionist artworks')

    st.set_option('deprecation.showfileUploaderEncoding', False)

    uploaded_file = st.file_uploader("Choose an image")

    if uploaded_file is not None:
        st.write("Your image:")
        with Image.open(uploaded_file) as img:
            resized_img = img.resize((128, 128))
        st.image(resized_img)
        st.write("Similar images:")

        # find_k_neighbours
        result = find_k_neighbours(image = resized_img, file_location = "data/abstract_ex.csv")

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
