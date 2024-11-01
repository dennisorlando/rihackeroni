from urllib.request import urlopen
from PIL import Image
import timm
import torch
import urllib

img = Image.open('img.jpg')

model = timm.create_model('mobilenetv4_conv_small.e1200_r224_in1k', pretrained=True)
model = model.eval()

# get model specific transforms (normalization, resize)
data_config = timm.data.resolve_model_data_config(model)
transforms = timm.data.create_transform(**data_config, is_training=False)

output = model(transforms(img).unsqueeze(0))  # unsqueeze single image into batch of 1

top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1)[0] * 100, k=5)

url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")

# urllib.request.urlretrieve(url, filename) 

with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

print(top5_probabilities[0])
print(top5_class_indices[0])

for i in range(top5_probabilities.size(0)):
    print(categories[top5_class_indices[i]], top5_probabilities[i].item())
