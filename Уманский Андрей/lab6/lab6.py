import os
import pandas as pd
import pathlib
import tensorflow as tf

df = pd.read_csv(r'movies_dataset.csv')


data_dir = pathlib.Path("E:\\2022-BigData\\_lab-6\\movies_posters")
img_height = 56
img_width = 38
batch_size = 32
genres_set = set(df['genres_list'])
genres_dict = dict(zip(genres_set, range(len(genres_set))))


def load_imgs(data_dir=data_dir):
    image_count = len(list(data_dir.glob('*/*.jpg')))
    list_ds = tf.data.Dataset.list_files(str(data_dir/'*'), shuffle=True)
    list_ds = list_ds.shuffle(image_count, reshuffle_each_iteration=False)
    return list_ds, image_count


def get_id(file_path):
    parts = tf.strings.split(file_path, sep=os.path.sep)
    img_id = tf.strings.split(parts[-1], ".")[-2]
    return img_id


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
    print(f"image shape: {img.numpy().shape}")
    print(f"Labels: {get_label(id)}")

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical')

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='categorical')

model = tf.keras.models.Sequential([
    tf.keras.layers.Normalization(input_shape=(img_height, img_width, 3),
                                  mean=510, variance=255),
    tf.keras.layers.Conv2D(filters=512, kernel_size=(4, 4),
                           padding='same', activation='relu',
                           strides=(2, 2)),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=None,
                              padding='valid',
                              data_format='channels_last'),
    tf.keras.layers.Conv2D(filters=256, kernel_size=(4, 4),
                           padding='same', activation='relu',
                           strides=(2, 2)),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=None,
                              padding='valid',
                              data_format='channels_last'),
    tf.keras.layers.Conv2D(filters=256, kernel_size=(3, 3),
                           padding='same', activation='relu',
                           strides=(1, 1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Dense(64, activation='sigmoid'),
    tf.keras.layers.Dense(32, activation='sigmoid'),
    tf.keras.layers.Dense(20, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=[tf.keras.metrics.CategoricalAccuracy()],
              jit_compile=True)

epoch = 0
PATH = f'checkpoint_{epoch}.ckpt'

cp_callback = tf.keras.callbacks.ModelCheckpoint(
                             filepath=PATH,
                             save_weights_only=True,  # If False, full model
                             save_freq='epoch')

model.summary()
hist = model.fit(train_ds,
                 validation_data=val_ds,
                 validation_freq=[2, 5, 9],
                 epochs=3,
                 callbacks=[cp_callback])

model.save('posters_training.h5')