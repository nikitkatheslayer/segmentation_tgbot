from pixellib.instance import instance_segmentation
from config import model_path
import os

class SegmentImage:

    def object_detection_on_an_image(self, image_path):
        segment_image = instance_segmentation()
        segment_image.load_model(model_path)

        save_path = os.path.splitext(image_path)[0] + '_detected_faces.jpg'

        result = segment_image.segmentImage(
            image_path=image_path,
            segment_target_classes=segment_image.select_target_classes(person=True),
            show_bboxes=True,
            output_image_name=save_path
        )
