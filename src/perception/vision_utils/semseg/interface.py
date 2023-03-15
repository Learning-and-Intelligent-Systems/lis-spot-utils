import numpy as np
import torch
import sys
import PIL.Image
import torchvision
from scipy import io
import csv

sys.path.extend(["./"])
from mit_semseg.models import ModelBuilder, SegmentationModule
from mit_semseg.utils import colorEncode

# Network Builders
net_encoder = ModelBuilder.build_encoder(
    arch='resnet50dilated',
    fc_dim=2048,
    weights='semseg/ckpt/ade20k-resnet50dilated-ppm_deepsup/encoder_epoch_20.pth')
net_decoder = ModelBuilder.build_decoder(
    arch='ppm_deepsup',
    fc_dim=2048,
    num_class=150,
    weights='semseg/ckpt/ade20k-resnet50dilated-ppm_deepsup/decoder_epoch_20.pth',
    use_softmax=True)

crit = torch.nn.NLLLoss(ignore_index=-1)
segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)
segmentation_module.eval()
segmentation_module.cuda()



colors = io.loadmat('semseg/data/color150.mat')['colors']
names = {}
with open('semseg/data/object150_info.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        names[int(row[0])] = row[5].split(";")[0]


# Load and normalize one image as a singleton tensor batch
pil_to_tensor = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(
        mean=[0.485, 0.456, 0.406], # These are RGB mean+std values
        std=[0.229, 0.224, 0.225])  # across a large photo dataset.
])



def get_semantic_labels(img_data):
    np_image = np.array(img_data).astype(np.uint8)
    # np_image = numpy.transpose(np_image, (2, 0, 1))
    pil_image = PIL.Image.fromarray(np_image)
    img_data = pil_to_tensor(pil_image)

    singleton_batch = {'img_data': img_data[None].cuda()}
    output_size = img_data.shape[1:]


    # Run the segmentation at the highest resolution.
    with torch.no_grad():
        scores = segmentation_module(singleton_batch, segSize=output_size)
        
    # Get the predicted scores for each pixel
    _, pred = torch.max(scores, dim=1)
    pred = pred.cpu()[0].numpy()

    # colorize prediction
    pred_color = colorEncode(pred, colors).astype(np.uint8)
    return pred_color

