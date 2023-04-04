import os
import pandas as pd
import numpy as np
import pathlib
import tensorflow as tf
from tensorflow import keras

df = pd.read_csv(r'..\2022-BigData\_lab-6\movies_dataset.csv')
                 
#print(df.describe())

data_dir = pathlib.Path("./_lab-6/movies_posters/")
img_height = 281
img_width = 190
batch_size = 32

def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*/*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=True)
    #list_ds = list_ds.shuffle(image_count, reshuffle_each_iteration=False)
    return list_ds, image_count

def get_id(file_path):
    parts = tf.strings.split(file_path, sep=os.path.sep)
    img_id = tf.strings.split(parts[-1], ".")[-2]
    return img_id
    #return list(df[df['id'] == img_id]['genres_list'])

def decode_img(img, img_height=img_height, img_width=img_width):
    img = tf.io.decode_jpeg(img, channels=3)
    return tf.image.resize(img, [img_height, img_width])

def get_label(id):
    return df.loc[df['id'] == id, 'genres_list'].iloc[0]

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
    print(f"Name film: {df.loc[df['id'] == id, 'title'].iloc[0]}")
    print(f"image shape: {img.numpy().shape}") #в img хранятся массивы пикселей
    print(f"Labels: {get_label(id)}")

"""""    
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)
"""""
