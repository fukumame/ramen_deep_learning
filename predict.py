import os
import sys
from keras.applications.vgg16 import VGG16
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing import image
import numpy as np
from common_lib import *


def main():

    if len(sys.argv) != 2:
        print("usage: python predict.py [filename]")
        sys.exit(1)

    filename = sys.argv[1]
    print('input:', filename)

    result_dir = 'results'
    weight_file_path = 'finetuning.h5'

    classes = ['kitakata', 'sano']
    nb_classes = len(classes)
    img_rows, img_cols = 150, 150
    channels = 3

    model = create_model(img_cols, img_rows, channels, nb_classes)
    model.load_weights(os.path.join(result_dir, weight_file_path))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    img = image.load_img(filename, target_size=(img_rows, img_cols))

    # この時点では x.shapeは (150, 150, 3)
    x = image.img_to_array(img)

    # x.shapeは (1, 150, 150, 3) となり、4次元となる。 1つめの要素は画像数を表す。
    x = np.expand_dims(x, axis=0)

    x = x / 255.0

    pred = model.predict(x)[0]
    top = 2
    top_indices = pred.argsort()[-top:][::-1]
    result = [(classes[i], pred[i]) for i in top_indices]
    for x in result:
        print(x)


if __name__ == '__main__':
    main()
