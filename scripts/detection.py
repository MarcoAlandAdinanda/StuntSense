import cv2
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class Detection():
    def __init__(self,
                 mode = False, 
                 complexity = 1, 
                 smooth = True, 
                 segmentation = False,
                 smoothSegmentation = True, 
                 detectCon = 0.5, 
                 trackCon = 0.5):
        self.static_image_mode = mode
        self.model_complexity = complexity
        self.smooth_landmarks = smooth
        self.enable_segmentation = segmentation
        self.smooth_segmentation = smoothSegmentation
        self.min_detection_confidence = detectCon
        self.min_tracking_confidence = trackCon

        self.mpPose = mp.solutions.mediapipe.solutions.pose
        self.mpDraw = mp.solutions.mediapipe.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.static_image_mode, 
                                     self.model_complexity, 
                                     self.smooth_landmarks, 
                                     self.enable_segmentation, 
                                     self.smooth_segmentation, 
                                     self.min_detection_confidence, 
                                     self.min_tracking_confidence)

    def draw_pose(self, img, draw = True):
        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(rgb)
        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.result.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    
    def get_pose_coords(self, img, draw = True):
        lm_list = []
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = img.shape
                # print(id,lm)
                px, py = int(lm.x * w), int(lm.y * h)
                lm_list.append([id,px,py])
                
                if draw:
                    cv2.circle(img,(px,py),3,(255,0,0),cv2.FILLED)
        return lm_list
    
    def head_detection(self, img, draw = True):
        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        face_mesh_results = face_mesh_images.process(rgb[:,:,::-1])

        if face_mesh_results.multi_face_landmarks:
            for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                pt1 = face_landmarks.landmark[10]
                return pt1
        else:
            return 0