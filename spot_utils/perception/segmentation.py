"""Some functions for segmenting images and pointclouds using neural
networks."""

from spot_utils.structures.image import RGBImage
from spot_utils.third_party.semseg.interface import get_semantic_labels


def scene_segment_image(rgbd: RGBImage) -> RGBImage:
    """Segment an image using the MIT Semseg scene segmentation model."""

    return get_semantic_labels(rgbd.rgb)
