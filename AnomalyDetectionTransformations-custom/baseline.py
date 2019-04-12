from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input

import numpy as np

_image_h = 224
_image_w = 224

img = 'images-collector/example.png'


def extract_resnet(img_path):
    model = ResNet50(weights='imagenet')

    img = image.load_img(img_path, target_size=(_image_h, _image_w))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features_array = model.predict(x)
    return features_array


example = extract_resnet(img)
print(type(example))




