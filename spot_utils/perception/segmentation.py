from spot_utils.structures.image import RGBImage

<<<<<<< HEAD
def scene_segment_image(rgbd:RGBImage) -> RGBImage:
    from spot_utils.third_party.semseg.interface import get_semantic_labels
=======

def scene_segment_image(rgbd:RGBImage) -> RGBImage:
    from spot_utils.perception.vision_utils.semseg.interface import \
        get_semantic_labels
>>>>>>> fn issues
    return get_semantic_labels(rgbd.rgb)