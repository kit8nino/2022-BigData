import pandas as pd
import numpy as np
import pathlib
import tensorflow as tf
import os

data_dir = pathlib.Path("d:/work/2022-bigdata/_lab-6/movies_posters")
img_height = 281
img_width = 190
batch_size = 32
genres = pd.read_csv('d:/work/2022-bigdata/_lab-6/movies_dataset.csv')


def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=False)
    list_ds = list_ds.shuffle(image_count, reshuffle_each_iteration=False)
    return list_ds, image_count


def get_label(file_path, genres=genres):
    parts = tf.strings.split(file_path, os.path.sep)
    img_id = parts.numpy()[-1][:-4]
    return list(genres[genres['id'] == img_id]['genres_list'])


def decode_img(img, img_height=img_height, img_width=img_width):
    img = tf.io.decode_jpeg(img, channels=3)
    return tf.image.resize(img, [img_height, img_width])


def process_path(file_path):
    label = get_label(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label


list_ds, image_count = load_imgs()
val_size = image_count // 5
train_ds = list_ds.skip(val_size)
val_ds = list_ds.take(val_size)

train_ds = train_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
val_ds = val_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)

for image, label in train_ds.take(3):
    print(f'image shape: {image.numpy().shape}')
    print(f'labels: {label}')
