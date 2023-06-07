import pathlib
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

IMG_HEIGHT = 56
IMG_WEIGHT = 38
BATCH_SIZE = 32
DATA_DIR = pathlib.Path("../../_lab-6/movies_posters")
TEST_PATH = pathlib.Path("test_images")
SAVE_PATH = pathlib.Path("model_dump.h5")

LOAD_MODEL = True

CLASS_NAMES = [
    "Action", "Comedy", "Documentary",
    "Drama", "Family", "Horror",
    "Mystery", "Romance", "Science Fiction",
    "Thriller"
]


def normalize_img(image, label):
    return tf.cast(image, tf.float32) / 255., label


def create_model():
    if LOAD_MODEL and SAVE_PATH.is_file():
        return keras.models.load_model(str(SAVE_PATH))

    ds_train = keras.preprocessing.image_dataset_from_directory(
        DATA_DIR,
        labels="inferred",
        label_mode="int",
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        image_size=(IMG_HEIGHT, IMG_WEIGHT),
        shuffle=True,
        seed=123,
        validation_split=0.2,
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
        validation_split=0.2,
        subset="validation"
    )

    print(ds_train.class_names)

    ds_train = ds_train.map(normalize_img)
    ds_validation = ds_validation.map(normalize_img)

    model = keras.Sequential([
        keras.layers.Normalization(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 3)),
        keras.layers.Flatten(input_shape=(IMG_HEIGHT, IMG_WEIGHT, 3)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(10, activation="softmax"),
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"])

    model.summary()

    model.fit(
        ds_train,
        validation_data=ds_validation,
        epochs=100,
        batch_size=BATCH_SIZE,
    )
    model.save(str(SAVE_PATH))
    return model


def test_model(_model):
    for item_path in os.listdir(str(TEST_PATH)):
        if not item_path.endswith(".jpg") and not item_path.endswith(".jpeg"):
            continue

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
        print(f"score {item_name} {CLASS_NAMES[np.argmax(score)]} {np.max(score) * 100}")


if __name__ == "__main__":
    _model = create_model()
    test_model(_model)
