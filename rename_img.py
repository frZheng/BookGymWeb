import json
import os


import tqdm
from predict import Predict
from captcha_predict_fun import pred_func
import torch
from captcha_cnn_model import CNN
import time
if __name__ == '__main__':


    with open("config.json", 'r') as f:
        config = json.load(f)
        f.close()

    tf_model = Predict(config)

    tf_cnn = CNN()
    tf_cnn.eval()
    model_name = 'model_20210827.pkl'
    tf_cnn.load_state_dict(torch.load(model_name, map_location='cpu'))

    file_path = "../save-bin-img1-lable"
    file_list = sorted(os.listdir(file_path))

    for i in tqdm.trange(len(file_list)):
    # for i in range(len(file_list)):
        name = file_list[i]
        abs_file_name = os.path.join(file_path,name)
        # label = name.split("_")[0]
        image = open(abs_file_name, 'rb').read()
        tf_pred = tf_model.pred_from_bytes(image)
        torch_pred = pred_func(tf_cnn,abs_file_name)
        print("tf res: ",tf_pred," torch res: ",torch_pred)

        if tf_pred == torch_pred:
            from shutil import copyfile
            source = abs_file_name

            copyfile(source, os.path.join("../save-bin-img-lable", tf_pred + "_" + name.split("_")[-1]))
            # copyfile(source, os.path.join("../save-bin-img-lable",name.split("_")[-1]))
            os.remove(source)
