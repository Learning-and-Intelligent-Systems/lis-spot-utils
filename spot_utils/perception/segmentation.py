"""Some functions for segmenting images and pointclouds using neural
networks."""

from spot_utils.structures.image import RGBDImage
from spot_utils.third_party.semseg.interface import get_semantic_labels


def scene_segment_image(rgbd: RGBDImage) -> RGBDImage:
    """Segment an image using the MIT Semseg scene segmentation model."""

    return RGBDImage(
        get_semantic_labels(rgbd.rgb),
        rgbd.depth,
        rgbd.frame,
        rgbd.intrinsics,
        rgbd.depth_scale,
    )
