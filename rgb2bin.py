# -*-coding:utf-8-*-
from PIL import Image
import sys
import os
# import pytesseract
import  numpy as np
from selenium import webdriver
# import  cv2

# 图像为白色则返回
def check_img(img_name,threshold=0.9):
    img = Image.open(img_name)
    if np.mean(img)>threshold:
        return True
    else:
        return False


def Identification_verification_code(img_name_rgb,img_file_path):
    # 使用路径导入图片
    # print(img_name_rgb)
    img = Image.open(img_name_rgb)
    # 转化到灰度图
    imgry = img.convert('L')
    # 保存图像
    # imgry.save(img_name_rgb.split(".")[-2]+ "-gray."+img_name_rgb.split(".")[-1])


    # 二值化，采用阈值分割法，threshold为分割点
    threshold = 10
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # imgry.save(img_name_rgb.split(".")[-2] + "-gray." + img_name_rgb.split(".")[-1])
    # out.save(img_name_rgb.split(".")[-2] + "-b." + img_name_rgb.split(".")[-1])
    img_save_path = os.path.join(img_file_path, img_name_rgb.split("\\")[-1])
    # print(img_save_path)
    out.save(img_save_path)
    return out

    # print(img_name_rgb)
    # imgry = cv2.imread(img_name_rgb, 0)
    # imgry = cv2.GaussianBlur(imgry, (7, 7), 0.05)  # 平滑去燥
    # cv2.imwrite(img_name_rgb.split(".")[-2]+ "-gray."+img_name_rgb.split(".")[-1] , imgry)
    # ret1, out = cv2.threshold(imgry, 0, 255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 设阈值二值化
    # print("threshold; ",ret1)
    #
    # img_save_path = os.path.join(img_file_path, img_name_rgb.split("\\")[-1])
    # cv2.imwrite(img_save_path, out)
    # return out

def remove_bg(rgb_img_name,img_file_path):
    print(rgb_img_name)
    img = Image.open(rgb_img_name)
    ref_color = img.getpixel((0,0))
    print(ref_color)
    print(type(ref_color))
    print(img.width,img.height)
    img_width = img.width
    img_height = img.height
    desImg = Image.new(img.mode,(img_width,img_height))
    for x in range(img_width):
        for y in range(img_height):
            cur_color = img.getpixel((x,y))
            #color = np.ones(3,dtype=np.int32)*255
            color = np.zeros(3, dtype=np.int32)
            for i in range(3):
                if abs(cur_color[i]-ref_color[i]) < 3:
                    pass
                else:
                    color[i] = cur_color[i]
            put_color = tuple(color)
            desImg.putpixel((x, y), put_color)

    img_save_path = os.path.join(img_file_path, rgb_img_name.split("\\")[-1])
    # print("img_save_path:",img_save_path)
    desImg.save(img_save_path)


# desImg.show()
# exit()
if __name__ == '__main__':
    bin_file_path ="bin-img1"
    bg_file_path ="bg-img1"
    rgb_file_path ="img1"
    img_file_names_list = sorted(os.listdir(rgb_file_path))
    print(img_file_names_list)

    for img_file_name in img_file_names_list:
        img_file_path = os.path.join(rgb_file_path, img_file_name)
        remove_bg(img_file_path,bg_file_path)
        bg_img_file_path = os.path.join(bg_file_path, img_file_name)
        out = Identification_verification_code(bg_img_file_path,bin_file_path)
    exit()
    #识别
    # text = pytesseract.image_to_string(out)
    # #识别对吗
    # text = text.strip()
    # text = text.upper();
    # print (text)
    # text = pytesseract.image_to_string(out, lang="eng")
    # print(text)