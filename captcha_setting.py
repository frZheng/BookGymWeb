# -*- coding: UTF-8 -*-
import os
# 验证码中的字符
# string.digits + string.ascii_uppercase
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
ALL_CHAR_SET = NUMBER + ALPHABET + alphabet

# message = ""
# for i in alphabet:
#     message += str("'"+ i.lower()+"', ")
# print(message)
# ALL_CHAR_SET = alphabet
ALL_CHAR_SET_LEN = len(ALL_CHAR_SET)
MAX_CAPTCHA = 4

# 图像大小

IMAGE_HEIGHT = 50
IMAGE_WIDTH = 130
path_name = 'mydataset1'

# IMAGE_HEIGHT = 60
# IMAGE_WIDTH = 160
# path_name = 'dataset'
TRAIN_DATASET_PATH = path_name + os.path.sep + 'train'
# TRAIN_DATASET_PATH="../val_dataset"
TEST_DATASET_PATH = path_name + os.path.sep + 'test'
PREDICT_DATASET_PATH = path_name + os.path.sep + 'predict'
