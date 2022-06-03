from mediapipe.python.solutions.face_mesh_connections import FACEMESH_CONTOURS
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_FACE_OVAL
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_IRISES
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LEFT_EYE
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LEFT_EYEBROW
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LEFT_IRIS
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_LIPS
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_RIGHT_EYE
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_RIGHT_EYEBROW
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_RIGHT_IRIS
from mediapipe.python.solutions.face_mesh_connections import FACEMESH_TESSELATION
import numpy as np


def unpack_mediapipe_set(edge_set): 
    vertex_set = set()
    for i in edge_set: 
        vertex_set.add(i[0])
        vertex_set.add(i[1])
    return vertex_set

def left_eye_eyebrow_landmark_indices(sorted=True): 
    left_eye = unpack_mediapipe_set(FACEMESH_LEFT_EYE) \
        .union(unpack_mediapipe_set(FACEMESH_LEFT_IRIS)) \
        .union(unpack_mediapipe_set(FACEMESH_LEFT_EYEBROW))
    if sorted: 
        left_eye.sort()
    left_eye = np.array(left_eye, dtype=np.int32)
    return left_eye

def right_eye_eyebrow_landmark_indices(sorted=True): 
    right_eye = unpack_mediapipe_set(FACEMESH_RIGHT_EYE) \
        .union(unpack_mediapipe_set(FACEMESH_RIGHT_IRIS)) \
        .union(unpack_mediapipe_set(FACEMESH_RIGHT_EYEBROW))
    if sorted: 
        right_eye.sort()
    right_eye = np.array(right_eye, dtype=np.int32)
    return right_eye

def left_eye_landmark_indices(sorted=True): 
    left_eye = unpack_mediapipe_set(FACEMESH_LEFT_EYE)
    if sorted: 
        left_eye.sort()
    left_eye = np.array(left_eye, dtype=np.int32)
    return left_eye

def right_eye_landmark_indices(sorted=True): 
    right_eye = unpack_mediapipe_set(FACEMESH_RIGHT_EYE)
    if sorted:
        right_eye.sort()
    right_eye = np.array(right_eye, dtype=np.int32)
    return right_eye

def mouth_landmark_indices(sorted=True): 
    mouth = unpack_mediapipe_set(FACEMESH_LIPS) 
    if sorted: 
        mouth.sort()
    mouth = np.array(mouth, dtype=np.int32)
    return mouth

def face_oval_landmark_indices(sorted=True): 
    face_oval = unpack_mediapipe_set(FACEMESH_FACE_OVAL)
    if sorted: 
        face_oval.sort()
    face_oval = np.array(face_oval, dtype=np.int32)
    return face_oval

def face_oval_landmark_indices(sorted=True): 
    face_oval = unpack_mediapipe_set(FACEMESH_FACE_OVAL)
    if sorted: 
        face_oval.sort()
    face_oval = np.array(face_oval, dtype=np.int32)
    return face_oval

def all_face_landmark_indices(sorted=True): 
    face_all = unpack_mediapipe_set(FACEMESH_TESSELATION)
    if sorted: 
        face_all.sort()
    face_all = np.array(face_all, dtype=np.int32)
    return face_all


class MediaPipeFaceOccluder(object):

    def __init__(self) -> None:
        self.left_eye = left_eye_eyebrow_landmark_indices()
        self.right_eye = right_eye_eyebrow_landmark_indices()
        self.mouth = mouth_landmark_indices()
        self.face_oval = face_oval_landmark_indices()
        self.face_all = all_face_landmark_indices()

    def bounding_box(self, landmarks, region): 
        landmarks = landmarks[:, :2]
        if region == "all":
            left = np.min(landmarks[:, 0])
            right = np.max(landmarks[:, 0])
            top = np.min(landmarks[:, 1])
            bottom = np.max(landmarks[:, 1])
        elif region == "left_eye": 
            left = np.min(landmarks[self.left_eye, 0])
            right = np.max(landmarks[self.left_eye, 0])
            top = np.min(landmarks[self.left_eye, 1])
            bottom = np.max(landmarks[self.left_eye, 1])
        elif region == "right_eye": 
            left = np.min(landmarks[self.right_eye, 0])
            right = np.max(landmarks[self.right_eye, 0])
            top = np.min(landmarks[self.right_eye, 1])
            bottom = np.max(landmarks[self.right_eye, 1])
        elif region == "mouth": 
            left = np.min(landmarks[self.mouth, 0])
            right = np.max(landmarks[self.mouth, 0])
            top = np.min(landmarks[self.mouth, 1])
            bottom = np.max(landmarks[self.mouth, 1])
        else: 
            raise ValueError(f"Invalid region {region}")

        width = right - left
        height = bottom - top
        center_x = left + width / 2
        center_y = top + height / 2
        
        center = np.stack([center_x, center_y], axis=1).round().astype(np.int32)
        size = np.stack([width, height], axis=1).round().astype(np.int32)

        bb = np.array([left, right, top, bottom], dtype = np.int32)
        sizes = np.concatenate([center, size])
        return bb, sizes
    
    def bounding_box_batch(self, landmarks, region): 
        assert landmarks.ndim == 3
        landmarks = landmarks[:, :, :2]
        if region == "all":
            left = np.min(landmarks[:,:, 0], axis=1)
            right = np.max(landmarks[:,:, 0], axis=1)
            top = np.min(landmarks[:,:, 1], axis=1)
            bottom = np.max(landmarks[:,:, 1], axis=1)
        elif region == "left_eye": 
            left = np.min(landmarks[:,self.left_eye, 0], axis=1)
            right = np.max(landmarks[:,self.left_eye, 0], axis=1)
            top = np.min(landmarks[:,self.left_eye, 1], axis=1)
            bottom = np.max(landmarks[:,self.left_eye, 1], axis=1)
        elif region == "right_eye": 
            left = np.min(landmarks[:,self.right_eye, 0], axis=1)
            right = np.max(landmarks[:,self.right_eye, 0], axis=1)
            top = np.min(landmarks[:,self.right_eye, 1], axis=1)
            bottom = np.max(landmarks[:,self.right_eye, 1], axis=1)
        elif region == "mouth": 
            left = np.min(landmarks[:,self.mouth, 0], axis=1)
            right = np.max(landmarks[:,self.mouth, 0], axis=1)
            top = np.min(landmarks[:,self.mouth, 1], axis=1)
            bottom = np.max(landmarks[:,self.mouth, 1], axis=1)
        else: 
            raise ValueError(f"Invalid region {region}")
        
        width = right - left
        height = bottom - top
        centers_x = left + width / 2
        centers_y = top + height / 2
        bb = np.stack([left, right, top, bottom], axis=1).round().astype(np.int32)
        sizes = np.stack([centers_x, centers_y, width, height], axis=1).round().astype(np.int32)
        return bb, sizes

    def occlude(self, image, region, landmarks=None, bounding_box=None):
        assert landmarks is not None and bounding_box is not None, "Specify either landmarks or bounding_box"
        if landmarks is not None: 
            bounding_box = self.bounding_box(landmarks, region) 
        
        image[bounding_box[2]:bounding_box[3], bounding_box[0]:bounding_box[1], ...] = 0 
        return image

    def occlude_batch(self, image, region, landmarks=None, bounding_box_batch=None
            , start_frame=None, end_frame=None, validity=None): 
        assert not(landmarks is not None and bounding_box_batch is not None), "Specify either landmarks or bounding_box"
        start_frame = start_frame or 0
        end_frame = end_frame or image.shape[0]
        assert end_frame <= image.shape[0]
        if landmarks is not None:
            bounding_box_batch, sizes_batch = self.bounding_box_batch(landmarks, region) 
        for i in range(start_frame, end_frame): 
            if validity is not None and not validity[i]: # if the bounding box is not valid, occlude nothing
                continue
            image[i, bounding_box_batch[i, 2]:bounding_box_batch[i, 3], bounding_box_batch[i, 0]:bounding_box_batch[i, 1], ...] = 0
        
        # # do the above without a for loop 
        # image[:, bounding_box_batch[:, 2]:bounding_box_batch[:, 3], bounding_box_batch[:, 0]:bounding_box_batch[:, 1], ...] = 0
        return image


def sizes_to_bb(sizes): 
    left = sizes[0] - sizes[2]
    right = sizes[0] + sizes[2]
    top = sizes[1] - sizes[3]
    bottom = sizes[1] + sizes[3]
    return np.array([left, right, top, bottom], dtype=np.int32)    


def sizes_to_bb_batch(sizes):
    left = sizes[:, 0] - sizes[:, 2]
    right = sizes[:, 0] + sizes[:, 2]
    top = sizes[:, 1] - sizes[:, 3]
    bottom = sizes[:, 1] + sizes[:, 3]
    return np.stack([left, right, top, bottom], axis=1)