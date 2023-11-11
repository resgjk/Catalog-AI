from io import BytesIO

from PIL import Image


def image_to_byte_array(path_to_img):
    image = Image.open(path_to_img)
    imgByteArr = BytesIO()
    image.save(imgByteArr, format="png")
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
