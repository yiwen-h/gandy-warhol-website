import numpy as np
from tensorflow.keras.models import load_model
from skimage.transform import resize
import skimage.io
import numpy as np
import pandas as pd
import pickle
import joblib


knnfile = "models/knnmodel.joblib"
knn = joblib.load(knnfile)
vgg = "models/vgg19_autoencoder.h5"
vggmodel = load_model(vgg)
vggmodel.compile()

"""
REQUIRES TO RUN:
- Trained VGG model to embed input files
- Trained KNN model to find neighbours
- all data CSV file
- all 3600 images with correct filenames
"""


class ImageTransformer(object):

    def __init__(self, shape_resize):
        self.shape_resize = shape_resize

    def __call__(self, img):
        img_transformed = resize_img(img, self.shape_resize)
        img_transformed = normalize_img(img_transformed)
        return img_transformed

def normalize_img(img):
    return img / 255.

def read_img(filePath):
    return skimage.io.imread(filePath, as_gray=False)

def resize_img(img, shape_resized):
    img_resized = resize(img, shape_resized,
                         anti_aliasing=True,
                         preserve_range=True)
    assert img_resized.shape == shape_resized
    return img_resized

def get_vgg19_model(vggmodel = "models/vgg19_autoencoder.h5"):
    model = load_model(vggmodel)
    model.compile()
    return model

def get_art_info(file_location = "data/abstract_ex.csv"):
    art_info = pd.read_csv(file_location)
    return art_info

def apply_transformer(imgs, transformer):
    imgs_transform = [transformer(img) for img in imgs]
    return imgs_transform

def get_images_as_array(images, input_shape_model):
    images_as_array = np.array(images).reshape((-1,) + input_shape_model)
    return images_as_array

def get_flattened_array(images_as_array, output_shape_model):
    images_as_flattened_array = images_as_array.reshape((-1, np.prod(output_shape_model)))
    return images_as_flattened_array

def single_image_neighbours_info_as_dict(E_test_flatten, knn, art_info):
    related_images = []
    result = knn.kneighbors(E_test_flatten)
    img_ids = list(result[1][0])
    for i in img_ids:
        image_info = {}
        image_info['Image_filename'] = f"{art_info.iloc[i].ID}.jpeg"
        image_info['Title'] = f"{art_info.iloc[i].Artwork}"
        image_info['Artist'] = f"{art_info.iloc[i].Artist}"
        related_images.append(image_info)
    return related_images


def find_k_neighbours(image = "images/test_images/26601.jpeg", transform = True, vggmodel = vggmodel,
                        knnmodel=knn, file_location = "data/abstract_ex.csv"):
    image = [np.asarray(image)]
    shape_img = (128,128,3)
    output_shape_model = (4, 4, 512)
    # instantiate model
    model = vggmodel
    if transform == True:
        transformer = ImageTransformer(shape_img)
        img_transformed = apply_transformer(image, transformer)
        X_test = get_images_as_array(img_transformed, shape_img)
    elif transform == False:
        X_test = get_images_as_array(image, shape_img)
    # transform into embeddings
    E_test = model.predict(X_test)
    E_test_flatten = get_flattened_array(E_test, output_shape_model)
    # process with knn and get info about neighbours from csv file
    art_info = get_art_info(file_location = file_location)
    result = single_image_neighbours_info_as_dict(E_test_flatten, knnmodel, art_info)
    return result

if __name__ == "__main__":
    print(find_k_neighbours())
