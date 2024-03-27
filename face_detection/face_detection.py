import numpy as np
import mtcnn
from PIL import Image, ImageDraw
import argparse
from io import BytesIO
import os


class Preprocessing:

    def detect_faces(self, image_path):
        """
        Detect faces in an image using MTCNN.

        Args:
            image_path (str): Path to the image file.

        Returns:
            image: An Image object.
            faces: A list of dictionaries containing details of the detected faces.
        """
        face_detector = mtcnn.MTCNN()
        image = Image.open(BytesIO(image_path))
        image = image.convert("RGB")
        faces = face_detector.detect_faces(np.array(image))
        print("Image type", type(image))
        return image, faces

    @staticmethod
    def draw_faces(image, faces, image_path, conf_score=0.9, show_image=False, save_cropped=False, save_uncropped=False, save_image_path=None):
        """
        Draw bounding boxes and keypoints on the detected faces. Optionally, show the image, save the image with drawn faces,
        and save the cropped faces.

        Args:
            image: An Image object.
            faces: A list of dictionaries containing details of the detected faces.
            image_path (str): Path to the image file.
            conf_score (float): Confidence score threshold for face detection.
            show_image (bool): Flag to control the display of the image with drawn faces.
            save_cropped (bool): Flag to control the saving of the cropped faces.
            save_uncropped (bool): Flag to control the saving of the image with drawn faces.
            save_image_path (str): Path to save the image with drawn faces.
        """
        draw = ImageDraw.Draw(image)

        for i, face in enumerate(faces):
            box = face["box"]
            conf = round(face["confidence"], 2)
            if conf >= conf_score:
                # Save individual faces cropped image here before face detection box is drawn on the image
                if save_cropped:
                    cropped_face = image.crop(
                        (box[0], box[1], box[0] + box[2], box[1] + box[3]))
                    _, tail = os.path.split(image_path)
                    if save_image_path is None:
                        cropped_face.save(fp=f'fd_cropped_{i}_{tail}')
                    else:
                        cropped_face.save(fp=os.path.join(
                            save_image_path, f'fd_cropped_{i}_{tail}'))

                keypoints = face["keypoints"]
                draw.rectangle(
                    [(box[0], box[1]), (box[0] + box[2], box[1] + box[3])], outline="green"
                )
                draw.text((box[0], box[1] - 10),
                          "Confidence Score: " + str(conf), fill="red")
                for keypoint in keypoints.values():
                    draw.ellipse(
                        (keypoint[0] - 2, keypoint[1] - 2,
                         keypoint[0] + 2, keypoint[1] + 2),
                        fill="red",
                    )

        if show_image:
            image.show()

        # only makes sense to save one uncropped image with all the faces drawn on the image
        if save_uncropped:
            _, tail = os.path.split(image_path)
            if save_image_path is None:
                image.save(fp=f'fd_uncropped_{tail}')
            else:
                image.save(fp=os.path.join(
                    save_image_path, f'fd_uncropped_{tail}'))

        return image

    def face_detection(self, image_path):
        """
        Main function to detect and draw faces on an image.

        Args:
            image_path (str): Path to the image file.
        """
        image, faces = self.detect_faces(image_path)
        return self.draw_faces(image, faces, image_path)
