import numpy as np
import cv2 as cv

WINDOW_SIZE = 4


def match(image, template):
    sumSSIM = 0
    numWindows = 0

    for row in range(image.shape[0] - WINDOW_SIZE):
        for col in range(image.shape[1] - WINDOW_SIZE):
            subImg1 = image[row:row + WINDOW_SIZE, col:col + WINDOW_SIZE]
            subImg2 = template[row:row + WINDOW_SIZE, col:col + WINDOW_SIZE]

            ssim = calculate_SSIM(subImg1, subImg2)

            sumSSIM += ssim
            numWindows += 1

    return sumSSIM / numWindows


def match_matrix(image, template, threshold=0.9):
    width, height = image.shape[1], image.shape[0]

    ssimMap = np.zeros((height, width), dtype=np.float32)

    for row in range(height - WINDOW_SIZE):
        for col in range(width - WINDOW_SIZE):
            subImg1 = image[row:row + WINDOW_SIZE, col:col + WINDOW_SIZE]
            subImg2 = template[row:row + WINDOW_SIZE, col:col + WINDOW_SIZE]

            ssim = calculate_SSIM(subImg1, subImg2)
            ssimMap[row + WINDOW_SIZE // 2, col + WINDOW_SIZE // 2] = ssim

    resultImg = np.copy(image)

    for row in range(height - WINDOW_SIZE):
        for col in range(width - WINDOW_SIZE):
            ssim = ssimMap[row + WINDOW_SIZE // 2, col + WINDOW_SIZE // 2]
            if ssim < threshold:
                resultImg[row + WINDOW_SIZE // 2, col + WINDOW_SIZE // 2] = 255

    return resultImg


def show_difference(image_path, template_path):
    image = cv.imread(image_path)
    template = cv.imread(template_path)
    cv.imwrite("resources/output/ssim/ssim_mine_difference.jpg", match_matrix(image, template))


def calculate_SSIM(image, template):
    ssim = 0

    for c in range(image.shape[2]):
        img1Pixels = image[:, :, c].astype(np.float64)
        img2Pixels = template[:, :, c].astype(np.float64)

        ssimChannel = get_SSIM_Channel(img1Pixels, img2Pixels)

        ssim += ssimChannel

    return ssim / image.shape[2]


def get_SSIM_Channel(img1Pixels, img2Pixels):
    img1Mean = np.mean(img1Pixels)
    img2Mean = np.mean(img2Pixels)

    img1Variance = np.var(img1Pixels)
    img2Variance = np.var(img2Pixels)

    covariance = np.mean((img1Pixels - img1Mean) * (img2Pixels - img2Mean))

    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    return ((2 * img1Mean * img2Mean + c1) * (2 * covariance + c2)) / \
        ((img1Mean ** 2 + img2Mean ** 2 + c1) * (img1Variance + img2Variance + c2))
