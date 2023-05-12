from PIL import Image
import os, sys
import pandas as pd


path = "movies_posters/"
dirs = os.listdir(path)
resize_ratio = .2  # where 0.5 is half size, 2 is double size
df = pd.read_csv('movies_dataset.csv')


def resize_aspect_fit():
    dirs = os.listdir(path)
    for item in dirs:
        if item == '.jpg':
            continue
        if os.path.isfile(path+item):
            image = Image.open(path+item)
            file_path, extension = os.path.splitext(path+item)

            new_image_height = int(image.size[0] / (1/resize_ratio))
            new_image_length = int(image.size[1] / (1/resize_ratio))

            image = image.resize((new_image_height, new_image_length),
                                 Image.ANTIALIAS)

            folder, img_id = file_path.split('/')
            genre = df.loc[df['id'] == img_id, 'genres_list'].apply(eval)
            try:
                genre = genre.tolist()[0][0]
            except:
                genre = 'Mystery'
            new_folder = folder + '/' + genre
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
            image.save(folder + '/' + genre + '/' + img_id +
                       extension, 'JPEG', quality=90)


resize_aspect_fit()
