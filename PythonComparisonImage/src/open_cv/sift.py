import cv2 as cv


def match(image_path, pattern_path):
    # Загрузка изображений
    image1 = cv.imread(image_path)
    image2 = cv.imread(pattern_path)

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

    # Вычисление схожести изображений
    similarity = len(matches) / max(len(keypoints1), len(keypoints2))

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
