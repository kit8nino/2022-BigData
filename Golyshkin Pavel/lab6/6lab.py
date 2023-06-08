import pandas as pd
import numpy as np
import pathlib
import tensorflow as tf
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
from keras.models import Sequential

img_height = 56
img_width = 38
batch_size = 4
data_dir = pathlib.Path("movies_posters")
genres = pd.read_csv('movies_dataset.csv')
genres_set = set(genres['genres_list'])
genres_dict = dict(zip(genres_set, range(len(genres_set))))

def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=False)
    list_ds = list_ds.shuffle(image_count, reshuffle_each_iteration=False)
    return list_ds, image_count

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode="int"
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode="int"
)

model = Sequential([
    Conv2D(filters=50, kernel_size=(4, 4), padding='same', activation='relu', strides=(2, 2), input_shape=(img_height, img_width, 3)),
    BatchNormalization(),
    MaxPooling2D(pool_size=2, strides=None, padding='valid', data_format='channels_last'),
    Dropout(0.25),

    Conv2D(filters=10, kernel_size=(4, 4), padding='same', activation='relu', strides=(2, 2)),
    BatchNormalization(),
    MaxPooling2D(pool_size=(1, 1), strides=(1, 1), padding='valid', data_format='channels_last'),
    Dropout(0.25),

    Conv2D(filters=10, kernel_size=(4, 4), padding='same', activation='relu', strides=(2, 2)),
    BatchNormalization(),
    MaxPooling2D(pool_size=2, strides=None, padding='valid', data_format='channels_last'),

    Flatten(),
    Dropout(0.5),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(20, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

checkpoint_path = 'checkpoint_{epoch}.ckpt'
early_stopping = EarlyStopping(monitor='val_loss', patience=2)

cp_callback = ModelCheckpoint(
    filepath=checkpoint_path,
    save_weights_only=True,
    save_freq='epoch'
)

model.summary()

input("Press ENTER to continue")

model.fit(
    train_ds,
    validation_data=val_ds,
    validation_freq=1,
    epochs=9,
    callbacks=[cp_callback, early_stopping],
    use_multiprocessing=True
)

test_loss, test_accuracy = model.evaluate(val_ds)
print('Test accuracy:', test_accuracy)