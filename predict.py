import json
import os

import tensorflow as tf

from core.model import CNN
from core.utils import vec2text

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '-1'


class Predict:
    # 传入图片预测结果
    def __init__(self,config):
        self._config = config
        self.model_save_dir = self._config['model_save_dir'] + '/model_weight'
        self.model = CNN(self._config['max_length'], len(self._config['char_set']))
        try:
            # tf.print("尝试加载模型文件..")
            self.model.load_weights(self.model_save_dir)
            tf.print("加载模型成功")
        except:
            tf.print("未读取到模型文件..")

    def pred_from_path(self, path):
        # 以路径形式传入图片识别
        image = tf.io.read_file(path)
        image = self.preprocess_img(image)
        pred = self.model(image)
        label = vec2text(pred)
        return label

    def pred_from_bytes(self, image):
        # 以二进制流形式传入图片识别
        image = tf.convert_to_tensor(image)
        image = self.preprocess_img(image)
        pred = self.model(image)
        label = vec2text(pred)
        return label

    def preprocess_img(self, image):
        image = tf.image.decode_png(image, channels=3)
        image = tf.image.resize(image, [self._config['image_height'], self._config['image_width']])
        image = 2 * tf.cast(image, dtype=tf.float32) / 255. - 1
        if len(image.shape) > 2:
            r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
            image = 0.2989 * r + 0.5870 * g + 0.1140 * b
        image = tf.expand_dims(image, axis=0)
        image = tf.expand_dims(image, axis=3)
        return image


def pre_img_to_lable(img_file):
    with open("config.json", 'r') as f:
        config = json.load(f)
        f.close()
    image = open(img_file, 'rb').read()
    label = Predict(config).pred_from_bytes(image)
    return label

if __name__ == '__main__':
    # 加载配置文件
    with open("config.json", 'r') as f:
        config = json.load(f)
        f.close()


    # 以二进制流形式传入图片预测
    image = open("feci.png", 'rb').read()
    label = Predict(config).pred_from_bytes(image)
    print("预测结果为：", label)