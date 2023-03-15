from structures.image import RGBImage

def scene_segment_image(rgbd:RGBImage) -> RGBImage:
    from src.perception.semseg.interface import get_semantic_labels
    return get_semantic_labels(rgbd.rgb)