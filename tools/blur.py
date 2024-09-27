from cv2 import GaussianBlur


def blur_frame(frame):
    return GaussianBlur(frame, (37, 37), 67)