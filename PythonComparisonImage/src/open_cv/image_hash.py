import imagehash
from PIL import Image


def average_hash(path_to_image):
    return imagehash.average_hash(Image.open(path_to_image))


def perceptual_hash(path_to_image):
    return imagehash.phash(Image.open(path_to_image))


def difference_hash(path_to_image):
    return imagehash.dhash(Image.open(path_to_image))


def wavelet_hash(path_to_image):
    return imagehash.whash(Image.open(path_to_image))


def color_hash(path_to_image):
    return imagehash.colorhash(Image.open(path_to_image))


def crop_resistant_hash(path_to_image):
    return imagehash.crop_resistant_hash(Image.open(path_to_image))