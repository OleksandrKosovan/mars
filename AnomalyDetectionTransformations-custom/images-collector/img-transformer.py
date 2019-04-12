from PIL import Image, ContainerIO
import pvl

import matplotlib.pyplot as plt

import os

def imshow(img, title='', w=8, h=8):
    """Simple plotter"""
    plt.figure(figsize=(w, h))
    plt.title(title)
    plt.imshow(img)
    # plt.savefig('test.png')
    # plt.show()


def extract_img(image_file: str):
    """Extracts and returns embedded image from PDS3 IMG files as PIL Image"""

    # Parsing label
    label = pvl.load(image_file)  # load label from .IMG file
    image_data = label['IMAGE']  # getting image object info

    h_img, w_img = image_data[0][-1], image_data[1][-1]  # real image sizes
    pref, suff = image_data[6][-1], image_data[7][-1]  # buffer pixels margins
    w_total = w_img + pref + suff  # width with margins

    offset = label['^IMAGE'].value  # pointer where image is located
    size = label['^GAP_TABLE'].value - label['^IMAGE'].value  # image size (in bytes)

    # Now getting back to file
    with open(image_file, "rb") as f:
        container = ContainerIO.ContainerIO(f, offset - 1, size)
        data = container.read()  # reading image bytes
        img = Image.frombytes('L', (w_total, h_img), data, "raw")  # decoding
        img = img.crop((pref, 0, w_img + pref, h_img))  # cropping margins

    return img


list_of_files = os.listdir("images")
path = 'images/'

i = 1
for img_name in list_of_files:
    img = extract_img(path+img_name)
    size = img.size
    img.thumbnail(size=size)

    img.save('images-reformat/mars'+str(i)+'.png', "JPEG")
    i += 1
    print(img_name)

# raw_file = "ESP_011261_1960_BG12_0.IMG"
# img = extract_img(path+raw_file)

# imshow(img.crop((0, 0, 512, 512)), title='Test Crop')

# print(img.size)
# print(format(img))

# size = img.size
# img.thumbnail(size=size)

# print(format(img))

# img.save('example.png', "JPEG")


