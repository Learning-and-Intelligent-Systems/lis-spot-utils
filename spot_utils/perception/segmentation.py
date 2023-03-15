from spot_utils.structures.image import RGBImage

def scene_segment_image(rgbd:RGBImage) -> RGBImage:
    from spot_utils.third_party.semseg.interface import get_semantic_labels
    return get_semantic_labels(rgbd.rgb)