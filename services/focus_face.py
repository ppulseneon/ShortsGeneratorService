from ultralytics import YOLO
import cv2
import os
from scipy.ndimage import gaussian_filter1d

def focus_face(video_path):
    model = YOLO("yolov8n.pt")  # load model
    model.to('cuda')
    cap = cv2.VideoCapture(video_path)

    ret = True
    frame_count = 0
    save_dir = "/frames_video/"
    os.makedirs(save_dir, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'H264')

    def smooth_gaussian(x, sigma):
        return gaussian_filter1d(x, sigma)

    centers = []
    import math
    while ret:
        ret, frame = cap.read()
        frame_count += 1

        if ret:
            results = model.track(frame, persist=True, device='0', batch=0)
            for i, det in enumerate(results[0].boxes.xyxy):
                if i != 0:
                    continue

                x1, y1, x2, y2 = map(int, det[:4])
                y1 = 0
                y2 = len(frame)
                x_size = math.ceil(y2 * 9 / 16)
                size = x2 - x1
                centers.append(round(abs(x2 + x1) / 2))
                x1 = x1 - math.floor((x_size - (size)) / 2)
                x2 = x2 + math.ceil((x_size - (size)) / 2)
                crop = frame[y1:y2, x1:x2]

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    print(centers)
    smoothed_list = smooth_gaussian(centers, 2)
    for i in range(len(smoothed_list)):
        smoothed_list[i] = round(smoothed_list[i])
    print(smoothed_list)
    ret = True
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while ret:
        ret, frame = cap.read()
        frame_count += 1

        if ret:
            y1 = 0
            y2 = len(frame)

            size = math.ceil(y2 * 9 / 16)
            x1 = smoothed_list[frame_count - 1] - math.ceil(size / 2)
            x2 = smoothed_list[frame_count - 1] + math.floor(size / 2)

            crop = frame[y1:y2, x1:x2]

            cv2.imwrite(save_dir + 't_' + str(frame_count) + '.jpg', crop)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    cap.release()
