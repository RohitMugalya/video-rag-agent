import base64
from io import BytesIO

import cv2
import numpy as np
from PIL import Image

VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv")


def extract_frames(video_path, interval_sec=1.0):
    cap = cv2.VideoCapture(video_path)
    frames, idx = [], 0
    while True:
        cap.set(cv2.CAP_PROP_POS_MSEC, idx * interval_sec * 1000)
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append((idx * interval_sec, Image.fromarray(rgb)))
        idx += 1
    cap.release()
    return frames


def get_raw_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames, fps


def get_frame(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def frame_to_base64(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def frames2tensor(vid_list, fnum=8, target_size=(224, 224)):
    import torch

    step = max(len(vid_list) // fnum, 1)
    vid_list = vid_list[::step][:fnum]
    vid_list = [cv2.resize(x[:, :, ::-1], target_size) for x in vid_list]
    v_mean = np.array([0.485, 0.456, 0.406]).reshape(1, 1, 3)
    v_std = np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3)
    vid_tube = [np.expand_dims((x / 255.0 - v_mean) / v_std, axis=(0, 1)) for x in vid_list]
    vid_tube = np.concatenate(vid_tube, axis=1)
    vid_tube = np.transpose(vid_tube, (0, 1, 4, 2, 3))
    return torch.from_numpy(vid_tube).float()
