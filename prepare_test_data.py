import os
import shutil
import random
from common_lib import *

TRAIN_DIR = 'train_images'
TEST_DIR = 'test_images'

KITAKATA = 'kitakata'
SANO = 'sano'

ORI_KITAKATA_DIR = os.path.join('img', KITAKATA)
ORI_SANO_DIR = os.path.join('img', SANO)


def move_image_data(source_dir, target_dir, number):
    source_files = os.listdir(source_dir)
    random.shuffle(source_files)
    for f in source_files[:number]:
        source = os.path.join(source_dir, f)
        target = os.path.join(target_dir, f)
        shutil.move(source, target)


def main():

    make_dir(TRAIN_DIR)
    make_dir(TEST_DIR)

    train_kitakata_dir = os.path.join(TRAIN_DIR, KITAKATA)
    train_sano_dir = os.path.join(TRAIN_DIR, SANO)
    test_kitakata_dir = os.path.join(TEST_DIR, KITAKATA)
    test_sano_dir = os.path.join(TEST_DIR, SANO)

    make_dir(train_kitakata_dir)
    make_dir(train_sano_dir)
    make_dir(test_kitakata_dir)
    make_dir(test_sano_dir)

    move_image_data(ORI_KITAKATA_DIR, train_kitakata_dir, 500)
    move_image_data(ORI_SANO_DIR, train_sano_dir, 500)
    move_image_data(ORI_KITAKATA_DIR, test_kitakata_dir, 50)
    move_image_data(ORI_SANO_DIR, test_sano_dir, 50)


if __name__ == '__main__':
    main()