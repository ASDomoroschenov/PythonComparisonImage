import cv2 as cv
import numpy as np
from scipy.fft import fft2, ifft2


def match(image, template):
    matCorrelation = match_matrix(image, template)
    return np.mean(matCorrelation)


def match_matrix(image, template):
    imageChannels = cv.split(image)
    templateChannels = cv.split(template)
    result = None

    for imageChannel, templateChannel in zip(imageChannels, templateChannels):
        channelResult = visualize_match_for_channel(imageChannel, templateChannel)
        if result is None:
            result = np.zeros(channelResult.shape, dtype=np.float32)
        result += channelResult

    result = cv.normalize(result, None, 0, 1, norm_type=cv.NORM_MINMAX)

    return result


def show_difference(image_path, template_path):
    image = cv.imread(image_path)
    template = cv.imread(template_path)

    corr_map = match_matrix(image, template)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(corr_map)

    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    cv.rectangle(image, top_left, bottom_right, 255, 2)

    cv.imwrite("resources/output/ncc/ncc_mine_difference.jpg", image)


def visualize_match_for_channel(imageChannel, templateChannel):
    M1, M2 = templateChannel.shape

    extendedPattern = np.zeros_like(imageChannel)
    extendedPattern[:M1, :M2] = templateChannel

    fftImage = fft2(imageChannel)
    fftTemplate = fft2(extendedPattern)

    result = fftImage * np.conj(fftTemplate)

    autoCorrImage = calculate_auto_correlation(fftImage)
    autoCorrTemplate = calculate_auto_correlation(fftTemplate)

    result /= np.sqrt(autoCorrImage) * np.sqrt(autoCorrTemplate)

    result = ifft2(result)
    result = np.real(result)

    return result


def calculate_auto_correlation(fftMatrix):
    autoCorrMatrix = fftMatrix * np.conj(fftMatrix)
    return autoCorrMatrix.real


def normalize_matrix(matrix):
    max_val = np.max(np.abs(matrix))
    if max_val != 0:
        matrix /= max_val
