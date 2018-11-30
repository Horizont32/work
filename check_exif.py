import PIL.Image
img = PIL.Image.open('img.jpg')
exif_data = img._getexif()