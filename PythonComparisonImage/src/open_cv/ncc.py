import cv2 as cv
import numpy as np


def match(image, template):
    return np.mean(cv.matchTemplate(image, template, cv.TM_CCORR_NORMED))


def match_matrix(image, template):
    return cv.matchTemplate(image, template, cv.TM_CCORR_NORMED)


def show_difference(image_path, template_path):
    image = cv.imread(image_path)
    template = cv.imread(template_path)

    corr_map = match_matrix(image, template)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(corr_map)

    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    cv.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

    cv.imwrite("resources/output/ncc/ncc_opencv_difference.jpg", image)

    return "resources/output/ncc/ncc_opencv_difference.jpg"
