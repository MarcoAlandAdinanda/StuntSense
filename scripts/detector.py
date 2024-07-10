import torch
import cv2
from ultralytics import YOLO

# PARAMETERS
CONF = 0.65
IOU = 0.9
MAX_DET = 1
IS_SHOW = False
IS_VERBOSE = False
IS_STREAM = False
IS_SAVE = False

MODEL_PATH = '../models/yolov8n-pose.pt' # PATH SERING TROUBLE, GUNAKAN FULL PATH

class Detector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def predict(self, frame, crop_value, height, width):
        """
            To perform pose estimation and get the keypoints & bbox
        """
        if crop_value != 0:
            mid_x = width / 2
            croped_value_rasio = mid_x * (crop_value / 100) 
            start_x = int(mid_x - croped_value_rasio)
            end_x = int(mid_x + croped_value_rasio)

            croped_frame = frame[:, start_x:end_x]
            results = self.model.track(source=croped_frame, conf=CONF, iou=IOU, max_det=MAX_DET,
                                    show=IS_SHOW, stream=IS_STREAM, save=IS_SAVE)
            keypoints = results[0].keypoints.xy
            keypoints_reshape = keypoints.view(-1, 2).type(torch.long)
            keypoints_reshape[:, 0] = keypoints_reshape[:, 0] + start_x
            
            # bbox format [x1, y1, x2, y2]
            bbox = results[0].boxes.xyxy[0].numpy() # bbox point of cropped image
            # change the x coordinate to full image and convert to integer
            bbox[0] = bbox[0] + start_x
            bbox[2] = bbox[2] + start_x
            bbox = bbox.astype('int')
        else:
            results = self.model.track(source=frame, conf=CONF, iou=IOU, max_det=MAX_DET,
                                    show=IS_SHOW, stream=IS_STREAM, save=IS_SAVE)
            keypoints = results[0].keypoints.xy
            keypoints_reshape = keypoints.view(-1, 2).type(torch.long)
            
            # bbox format [x1, y1, x2, y2]
            bbox = results[0].boxes.xyxy[0].numpy() # bbox point of cropped image
            bbox = bbox.astype('int')
            
        # Visualize    
        for point in keypoints_reshape:
            cv2.circle(frame, point.tolist(), 2, (0, 255,0), -1)
        
        # draw bbox
        cv2.rectangle(frame, (bbox[0:2]), (bbox[2:]), color=(255, 0, 0))
        return keypoints_reshape, bbox