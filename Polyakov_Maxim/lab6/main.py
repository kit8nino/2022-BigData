import pathlib
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

IMG_HEIGHT = 56
IMG_WEIGHT = 38
BATCH_SIZE = 32
DATA_DIR = pathlib.Path("../../_lab-6/movies_posters")
TEST_PATH = pathlib.Path("Test")
SAVE_PATH = pathlib.Path("saved_model.h5")


def normalize_img(image, label):
    return tf.cast(image, tf.float32) / 255., label


def load_model():
    _model = keras.models.load_model(str(SAVE_PATH))
    return _model


def create_model():
    if SAVE_PATH.is_file():
        return load_model()

    ds_train = keras.preprocessing.image_dataset_from_directory(
        DATA_DIR,
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        image_size=(IMG_HEIGHT, IMG_WEIGHT),
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="training"
    )

    ds_validation = keras.preprocessing.image_dataset_from_directory(
        DATA_DIR,
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        image_size=(IMG_HEIGHT, IMG_WEIGHT),
        shuffle=True,
        seed=123,
        validation_split=0.1,
        subset="validation"
    )

    print(ds_train.class_names)

    ds_train = ds_train.map(normalize_img)
    ds_validation = ds_validation.map(normalize_img)

    _model = keras.Sequential([
        keras.layers.Normalization(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 3)),
        keras.layers.Conv2D(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 3),
                            filters=128, kernel_size=(5, 3),
                            padding='same', activation='sigmoid'),
        keras.layers.MaxPool2D(pool_size=3, strides=None,
                               padding='valid', data_format='channels_last'),
        keras.layers.Conv2D(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 3),
                            filters=64, kernel_size=(5, 3),
                            padding='same', activation='sigmoid'),
        keras.layers.MaxPool2D(pool_size=3, strides=None,
                               padding='valid', data_format='channels_last'),
        keras.layers.Flatten(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 1)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(20, activation="softmax"),
    ])

    _model.compile(
        optimizer=keras.optimizers.Adam(),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"])

    _model.summary()

    _model.fit(
        ds_train,
        validation_data=ds_validation,
        epochs=5,
        batch_size=BATCH_SIZE
    )
    _model.save(str(SAVE_PATH))
    return _model


def test_model(_model):
    for item_path in os.listdir(str(TEST_PATH)):
        if item_path.endswith(".jpg"):
            item_path = os.path.join(str(TEST_PATH / item_path))
            img = tf.io.read_file(item_path)
            img = tf.image.decode_jpeg(img)
            reshaped_img = tf.image.resize(img, (IMG_HEIGHT, IMG_WEIGHT))
            reshaped_img = tf.reshape(reshaped_img, (IMG_HEIGHT, IMG_WEIGHT, 3))
            img_arr = keras.utils.img_to_array(reshaped_img)
            img_arr = tf.expand_dims(img_arr, 0)

            predictions = _model.predict(img_arr)
            score = tf.nn.softmax(predictions[0])
            item_name = item_path.split(os.path.sep)[-1]
            print("Score for {}: {}, {}%".format(
                item_name,
                np.argmax(score),
                np.max(score) * 100)
            )


if __name__ == "__main__":
    model = create_model()
    test_model(model)
