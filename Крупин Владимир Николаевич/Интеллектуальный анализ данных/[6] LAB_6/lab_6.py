# КРУПИН В. Н. (ИС-29) LAB_6

import os
import pandas as pd
import numpy as np
import pathlib
import tensorflow as tf
from tensorflow import keras

data_dir = pathlib.Path("Data\movies_posters")
genres = pd.read_csv("Data\movies_dataset.csv")

img_height = 281
img_width = 190
batch_size = 32

def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*/*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=True)
    return list_ds, image_count

def get_id(file_path):
    parts = tf.strings.split(file_path, sep=os.path.sep)
    img_id = tf.strings.split(parts[-1], ".")[-2]
    return img_id

def decode_img(img, img_height=img_height, img_width=img_width):
    img = tf.io.decode_jpeg(img, channels=3)
    return tf.image.resize(img, [img_height, img_width])

def get_label(id):
    return genres.loc[genres['id'] == id, 'genres_list'].iloc[0]

def processing_path(file_path):
    id = get_id(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, id

list_ds, image_count = load_imgs()
val_size = image_count // 5
train_ds = list_ds.skip(val_size)
val_ds = list_ds.take(val_size)
train_ds = train_ds.map(processing_path, num_parallel_calls=tf.data.AUTOTUNE)
val_ds = val_ds.map(processing_path, num_parallel_calls=tf.data.AUTOTUNE)

for img, id in train_ds.take(3):
    print(f"Name film: {genres.loc[genres['id'] == id, 'title'].iloc[0]}")
    print(f"image shape: {img.numpy().shape}")
    print(f"Labels: {get_label(id)}")
