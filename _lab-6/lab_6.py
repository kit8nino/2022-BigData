import pandas as pd
import numpy as np
import pathlib
import tensorflow as tf

data_dir = pathlib.Path("./movies_poster/")
img_height = 201
img_width = 180
batch_size = 32


def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*/*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*'), shuffle=False)
    list_ds = list_ds.shuffle(image_count, reshuffle_each_iteration=False)
    return 0

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
