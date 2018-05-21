import urllib.request
import os
from urllib.parse import urlparse
from keras.applications.vgg16 import VGG16
from keras.models import Sequential, Model
from keras.layers import Input, Dropout, Flatten, Dense


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_root_dir(root_dir_path, sub_directory):
    make_dir(root_dir_path)
    save_dir_path = root_dir_path + "/" + sub_directory
    make_dir(save_dir_path)
    return save_dir_path


def save_image(url, directory):
    file_path = urlparse(url).path
    file_name = os.path.basename(file_path)
    local_path = os.path.join(directory, file_name)
    urllib.request.urlretrieve(url, local_path)


def create_model(img_rows, img_cols, channel, nb_classes):
    input_tensor = Input(shape=(img_rows, img_cols, channel))
    vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

    top_model = Sequential()
    top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(nb_classes, activation='softmax'))

    model = Model(inputs=vgg16.input, outputs=top_model(vgg16.output))

    return model
