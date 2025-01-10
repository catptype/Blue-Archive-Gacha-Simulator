import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from typing import Tuple, Union

class Converter:
    
    ### Bytes Converter
    @staticmethod
    def byte_to_base64(byte_data: bytes) -> str:
        if byte_data is None:
            return None
        try:
            # Convert bytes to base64 string
            return base64.b64encode(byte_data).decode('utf-8')
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid byte data provided: {e}")
    
    @staticmethod
    def byte_to_pil(byte_data: bytes) -> Image.Image:
        if byte_data is None:
            return None
        base64_data = Converter.byte_to_base64(byte_data)
        pil_image = Converter.base64_to_pil(base64_data)
        return pil_image
    
    @staticmethod
    def byte_to_cv2(byte_data: bytes) -> np.ndarray:
        if byte_data is None:
            return None
        base64_data = Converter.byte_to_base64(byte_data)
        pil_image = Converter.base64_to_pil(base64_data)
        cv2_image = Converter.pil_to_cv2(pil_image)
        return cv2_image

    ### Base64 Converter
    @staticmethod
    def base64_to_byte(base64_string: str) -> bytes:
        if base64_string is None:
            return None
        if not isinstance(base64_string, str):
            raise ValueError("Input must be a valid base64 string")
        try:
            # Decode base64 string to bytes
            return base64.b64decode(base64_string)
        except (base64.binascii.Error, ValueError) as e:
            raise ValueError(f"Invalid base64 string: {e}")
        
    @staticmethod
    def base64_to_pil(base64_string: str) -> Image.Image:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        
        # Convert the binary data to an image
        image = Image.open(BytesIO(image_data))

        return image
    
    @staticmethod
    def base64_to_cv2(base64_string: str) -> np.ndarray:
        pil_image = Converter.base64_to_pil(base64_string)
        cv2_image = Converter.pil_to_cv2(pil_image)
        return cv2_image
    
    ### Image Converter
    @staticmethod
    def cv2_to_pil(numpy_array: np.ndarray) -> Image.Image:
        if not isinstance(numpy_array, np.ndarray):
            raise TypeError("Input must be a NumPy array")
        
        try:
            return Image.fromarray(numpy_array)
        except Exception as e:
            raise ValueError(f"Failed to convert from cv2 to PIL: {e}")
    
    @staticmethod
    def cv2_to_base64(numpy_array: np.ndarray) -> str:
        # Encode the image to a memory buffer as JPEG
        _, buffer = cv2.imencode('.jpg', numpy_array)

        # Convert to base64
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return image_base64

    @staticmethod
    def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
        if not isinstance(pil_image, Image.Image):
            raise TypeError("Input must be a PIL Image")
        try:
            return np.array(pil_image)
        except Exception as e:
            raise ValueError(f"Failed to convert from PIL to cv2: {e}")
    
    @staticmethod
    def pil_to_base64(pil_image: Image.Image) -> str:
        cv_image = Converter.pil_to_cv2(pil_image)
        return Converter.cv2_to_base64(cv_image)

    ### YOLO bbox converter
    @staticmethod
    def xywh2xyxy(bbox:Union[Tuple[int,int,int,int], Tuple[float,float,float,float]]):
        # Calculate top-left (x1, y1) and bottom-right (x2, y2) coordinates
        center_x, center_y, width, height = bbox
        x1 = center_x - (width / 2.0)
        y1 = center_y - (height / 2.0)
        x2 = center_x + (width / 2.0)
        y2 = center_y + (height / 2.0)
        
        return x1, y1, x2, y2

    @staticmethod
    def xyxy2xywh(bbox: Union[Tuple[int, int, int, int], Tuple[float, float, float, float]]):
        # Extract top-left (x1, y1) and bottom-right (x2, y2) coordinates
        x1, y1, x2, y2 = bbox
        
        # Calculate the center (cx, cy), width, and height
        center_x = (x1 + x2) / 2.0
        center_y = (y1 + y2) / 2.0
        width = x2 - x1
        height = y2 - y1
        
        return center_x, center_y, width, height
    
    @staticmethod
    def xyxy_norm2scalar(
        bbox:Tuple[float,float,float,float],
        image_width:int, 
        image_height:int
    ) -> Tuple[float,float,float,float]:
        x1, y1, x2, y2 = bbox

        x1 *= image_width
        x2 *= image_width
        y1 *= image_height
        y2 *= image_height

        return x1, y1, x2, y2
    
    @staticmethod
    def keypoint_norm2scalar(
        keypoint:Union[Tuple[float,float,int], Tuple[float,float]],
        image_width:int, 
        image_height:int
    ) -> Tuple[float, float]:
        if not len(keypoint) in [2,3]:
            raise ValueError(
            f"Invalid keypoint format: {keypoint}. Expected a tuple of length 2 or 3, "
            f"either [x, y] or [x, y, flag]. Received length {len(keypoint)}."
        )
        
        x = keypoint[0] * image_width
        y = keypoint[1] * image_height
        return x, y