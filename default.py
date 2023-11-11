from io import BytesIO

from PIL import Image


def image_to_byte_array():
    image = Image.open("default.png")
    imgByteArr = BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return str(imgByteArr)
