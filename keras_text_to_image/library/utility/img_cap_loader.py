import os
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
import h5py
from os.path import *

def load_normalized_img_and_its_text(img_dir_path, txt_dir_path, img_width, img_height):

    images = dict()
    texts = dict()
    for f in os.listdir(img_dir_path):
        filepath = os.path.join(img_dir_path, f)
        if os.path.isfile(filepath) and f.endswith('.jpg'):
            name = f.replace('.jpg', '')
            images[name] = filepath


    h = h5py.File(join(txt_dir_path), 'r')
    for ds in h.items():
        texts[ds[0].replace('.jpg', '')] = np.array(ds[1])

    #print(texts)
    #
    # for f in os.listdir(txt_dir_path):
    #     filepath = os.path.join(txt_dir_path, f)
    #     if os.path.isfile(filepath) and f.endswith('.txt'):
    #         name = f.replace('.txt', '')
    #         texts[name] = open(filepath, 'rt').read()

    result = []
    for name, img_path in images.items():
        if name in texts:
            text = texts[name]
            image = img_to_array(load_img(img_path, target_size=(img_width, img_height)))
            image = (image.astype(np.float32) / 255) * 2 - 1
            for caption in text:
                result.append([image, caption])

    return np.array(result)
