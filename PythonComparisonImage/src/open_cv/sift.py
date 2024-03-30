import cv2 as cv
import numpy as np

def match(image1, image2):
    # Преобразование изображений в оттенки серого
    gray_image1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    gray_image2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)

    # Инициализация детектора SIFT
    sift = cv.SIFT_create()

    # Поиск ключевых точек и их дескрипторов на обоих изображениях
    keypoints1, descriptors1 = sift.detectAndCompute(gray_image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray_image2, None)

    # Инициализация объекта для сопоставления дескрипторов
    matcher = cv.BFMatcher()

    # Сопоставление дескрипторов
    matches = matcher.match(descriptors1, descriptors2)

    # Вычисление дисперсии длин векторов
    variance_length = np.var([np.linalg.norm(desc) for desc in descriptors1])

    # Вычисление корня из дисперсии
    std_dev_length = np.sqrt(variance_length)

    # Подсчет количества совпадающих дескрипторов
    matching_descriptors = [matchItem for matchItem in matches if matchItem.distance < std_dev_length]

    # Вычисление схожести изображений
    similarity = len(matching_descriptors) / max(len(keypoints1), len(keypoints2))

    return similarity



def show_difference(image1_path, image2_path):
    # Загрузка изображений
    image1 = cv.imread(image1_path)
    image2 = cv.imread(image2_path)

    # Преобразование изображений в оттенки серого
    gray_image1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    gray_image2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)

    # Инициализация детектора SIFT
    sift = cv.SIFT_create()

    # Поиск ключевых точек и их дескрипторов на обоих изображениях
    keypoints1, descriptors1 = sift.detectAndCompute(gray_image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray_image2, None)

    # Инициализация объекта для сопоставления дескрипторов
    matcher = cv.BFMatcher()

    # Сопоставление дескрипторов
    matches = matcher.match(descriptors1, descriptors2)

    # Сортировка сопоставлений по расстоянию между дескрипторами
    matches = sorted(matches, key=lambda x: x.distance)

    # Отображение сопоставлений на изображении
    matched_image = cv.drawMatches(image1, keypoints1, image2, keypoints2, matches[:20], None)

    cv.imwrite("resources/output/sift/sift_opencv_difference.jpg", matched_image)

    return "resources/output/sift/sift_opencv_difference.jpg"
