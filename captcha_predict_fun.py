# -*- coding: UTF-8 -*-
import numpy as np
import torch
from torch.autograd import Variable
import captcha_setting

from captcha_cnn_model import CNN

import os
from torch.utils.data import DataLoader,Dataset
import torchvision.transforms as transforms
from PIL import Image


class pred_dataset(Dataset):

    def __init__(self, file_name, transform=None):
        self.file_name = file_name
        self.transform = transform
        pass

    def __len__(self):
        return 1 #只有一个文件
        # pass

    def __getitem__(self, idx):
        image_root = self.file_name
        image = Image.open(image_root)
        if self.transform is not None:
            image = self.transform(image)
        return image

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])

# model_name = 'model.pkl'
model_name = 'model_20210827.pkl'
def pred_func(model,file_name):

    # print("load cnn net.")
    predict_dataloader = DataLoader(pred_dataset(file_name, transform=transform), batch_size=1, shuffle=False)

    for i, images in enumerate(predict_dataloader):
        image = images
        vimage = Variable(image)
        predict_label = model(vimage)
        pred_str = ""
        for j in range(captcha_setting.MAX_CAPTCHA):
            pred_str += captcha_setting.ALL_CHAR_SET[np.argmax(predict_label[0,(captcha_setting.ALL_CHAR_SET_LEN*j):(captcha_setting.ALL_CHAR_SET_LEN*(j+1))].data.numpy())]
        return pred_str

def torch_pred_func(file_name):
    cnn = CNN()
    cnn.eval()
    cnn.load_state_dict(torch.load(model_name, map_location='cpu'))
    return pred_func(cnn,file_name)

if __name__ == '__main__':
    file_name = "mydataset1/predict/czpf_1629602012.png"
    label = torch_pred_func(file_name)
    print(label)



