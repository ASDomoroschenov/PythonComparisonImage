import cv2 as cv
from skimage.metrics import structural_similarity as ssim


def match(image, template):
    ssim_channels = [ssim(image[:, :, i], template[:, :, i]) for i in range(3)]
    ssim_mean = sum(ssim_channels) / len(ssim_channels)
    return ssim_mean


def show_difference(image_path, template_path, threshold=0.9):
    image = cv.imread(image_path)
    template = cv.imread(template_path)

    channels1 = cv.split(image)
    channels2 = cv.split(template)

    highlighted_channels = []

    for channel1, channel2 in zip(channels1, channels2):
        channel1 = cv.normalize(channel1.astype('float'), None, 0.0, 1.0, cv.NORM_MINMAX)
        channel2 = cv.normalize(channel2.astype('float'), None, 0.0, 1.0, cv.NORM_MINMAX)

        ssim_map = ssim(channel1, channel2, full=True, data_range=1.0)[1]

        highlighted_channel = channel1.copy()

        for row in range(ssim_map.shape[0]):
            for col in range(ssim_map.shape[1]):
                if ssim_map[row, col] < threshold:
                    highlighted_channel[row, col] = 1.0

        highlighted_channels.append(highlighted_channel)

    highlighted_diffs = cv.merge(highlighted_channels)

    cv.imwrite("resources/output/ssim/ssim_opencv_difference.jpg", highlighted_diffs * 255)

    return "resources/output/ssim/ssim_opencv_difference.jpg"

