import torch
from utils.helpers import *
import warnings
from PIL import Image
from torchvision import transforms

def image_transform(imagepath):
    test_transforms = transforms.Compose([transforms.Resize(255),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])
    image = Image.open(imagepath)
    imagetensor = test_transforms(image)
    return imagetensor


def predict(imagepath, verbose=False):
    if not verbose:
        warnings.filterwarnings('ignore')
    model_path = './models/catvdog.pth'
    model = load_model(model_path)
    model.eval()
    if verbose:
        print("Model Loaded..")
    image = image_transform(imagepath)
    image1 = image[None,:,:,:]
    ps=torch.exp(model(image1))
    topconf, topclass = ps.topk(1, dim=1)
    if topclass.item() == 1:
        return {'class':'dog','confidence':topconf.item()}
    else:
        return {'class':'cat','confidence':topconf.item()}

#print(predict('data/dog1.jpeg'))
#print(predict('data/cat1.jpeg'))
#print(predict('data/dog2.jpeg'))
#print(predict('data/cat2.jpeg'))