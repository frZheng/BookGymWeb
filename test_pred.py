
import datetime

from rgb2bin import remove_bg
from rgb2bin import Identification_verification_code
from rgb2bin import check_img
from predict import  pre_img_to_lable
from captcha_predict_fun import torch_pred_func

from selenium import webdriver  # 用于打开网站
import requests as req
from bs4 import BeautifulSoup

import time
from apscheduler.schedulers.blocking import BlockingScheduler
import threading


def book_result(result_list,filename):
    book_success = 0
    code_error = 2
    other_err = 1
    with open(filename, "a", encoding='utf-8') as file:  # ”w"代表着每次运行都覆盖内容
        for txt in result_list:
            file.write(txt)
            if "如需要取消预约请联系健身房管理员" in txt:
                print("预约成功")
                return book_success
            elif "验证码错误" in txt:
                print("验证码错误")
                # 应该再次预约此时间段
                return code_error
            else:
                # 预约其他时间段
                pass
            file.write("\n")
    return other_err

def book_time(driver,book_time,book_xiangmu):
    # 场地没预约则重来
    while 1:
        the_day_after_tomorrow = str(datetime.date.today() + datetime.timedelta(days=2))
        xiangmu_list = ["羽毛球(1号场)", "羽毛球(2号场)"]

        # http://zky.elstp.cn:8801/make-is-lit/?type=羽毛球(1号场)&date=2021-03-23&time=21:00-22:00
        html = "http://zky.elstp.cn:8801/make-is-lit/?type={}&date={}&time={}".format(
            xiangmu_list[book_xiangmu], the_day_after_tomorrow, book_time)
        print(html)
        driver.get(html)

        # 保证验证码是四位的，这个还需要加一个一定要验证码是正确的
        while 1:
            result = driver.find_elements_by_tag_name("src")
            # print(result)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            img_link = soup.select('.container')[0].select('img ')[0]['src']
            print(img_link)
            img_req = req.get(img_link)

            tmp_img_file_name = "tmp2{}_{}.png".format(book_time.replace(":", ""),book_xiangmu)
            with open(tmp_img_file_name, 'wb') as f:
                for chunk in img_req.iter_content(chunk_size=128):
                    f.write(chunk)

            remove_bg(tmp_img_file_name, "")
            Identification_verification_code(tmp_img_file_name, "")
            if check_img(tmp_img_file_name): # 图像为白色
                driver.execute_script("return get_code_img()")
                continue
            img_lable1 = torch_pred_func(tmp_img_file_name)
            img_lable = pre_img_to_lable(tmp_img_file_name)

            print("tf res: ",img_lable," torch res: ",img_lable1)
            normal_lable_len = 4
            # 这里还要再增加判断的条件，保证一次就完事
            if len(img_lable) == normal_lable_len and img_lable1==img_lable:
                break
            else:
                driver.execute_script("return get_code_img()")
                time.sleep(0.2)

        driver.find_element_by_name("name").send_keys("郑富荣".encode('utf-8').decode('utf-8'))  # 输入 姓名
        driver.find_element_by_name("bumen").send_keys("数字所".encode('utf-8').decode('utf-8'))  # 输入 部门
        driver.find_element_by_name("gonghao").send_keys("XYJ107963")  # 输入 工号
        driver.find_element_by_name("lxfs").send_keys("15217975717")  # 输入 联系方式

        # driver.find_element_by_name("name").send_keys("吴伟伟".encode('utf-8').decode('utf-8'))  # 输入 姓名
        # driver.find_element_by_name("bumen").send_keys("集成所".encode('utf-8').decode('utf-8'))  # 输入 部门
        # driver.find_element_by_name("gonghao").send_keys("XJY004442")  # 输入 工号
        # driver.find_element_by_name("lxfs").send_keys("18589049825")  # 输入 联系方式

        # driver.find_element_by_name("name").send_keys("杨猛".encode('utf-8').decode('utf-8'))  # 输入 姓名
        # driver.find_element_by_name("bumen").send_keys("集成所".encode('utf-8').decode('utf-8'))  # 输入 部门
        # driver.find_element_by_name("gonghao").send_keys("XJY107778")  # 输入 工号
        # driver.find_element_by_name("lxfs").send_keys("17843124470")  # 输入 联系方式

        # driver.find_element_by_name("name").send_keys("尉增杰".encode('utf-8').decode('utf-8'))  # 输入 姓名
        # driver.find_element_by_name("bumen").send_keys("数字所".encode('utf-8').decode('utf-8'))  # 输入 部门
        # driver.find_element_by_name("gonghao").send_keys("XYJ107470")  # 输入 工号
        # driver.find_element_by_name("lxfs").send_keys("13121133933")  # 输入 联系方式




        # driver.execute_script(add_time)
        # driver.execute_script("return elstp_date()")
        #
        # s1 = Select(driver.find_element_by_name('xiangmu'))  # 实例化Select
        #
        # s1.select_by_value(xiangmu_list[book_xiangmu])

        # s1 = Select(driver.find_element_by_id('time_s'))  # 实例化Select
        # s1.select_by_value(book_time)

        driver.find_element_by_name("code").send_keys(img_lable)  # 输入 验证码

        time.sleep(10)
        continue

        #等待到了八点点击
        while True:
            now_time = datetime.datetime.now()
            cur_time = now_time.hour * 60 + now_time.minute
            if cur_time>=8*60:
                time.sleep(0.01)#休眠10MS，防止时间对不上
                driver.find_element_by_class_name("btn-primary").click()  # 提交审核
                break
            else:
                time.sleep(0.1)


        ferdigtxt = []
        allelements = driver.find_elements_by_xpath("/html/body")
        for i in allelements:

            if i.text in ferdigtxt:
                pass
        else:
            ferdigtxt.append(i.text)

        print("ferdigtxt", ferdigtxt)

        result_num = book_result(ferdigtxt, "logs/" + the_day_after_tomorrow + "-" + str(book_time).replace(":", "") + "-{}.txt".format(book_xiangmu))

        code_error = 2
        if result_num == code_error:  # 再次预约此时间段
            pass
        else :  # 预约成功或者失败都要退出
            return result_num


def book(index_booktime=0):
    # 提早了1分钟，则先休眠50秒？
    now_time = datetime.datetime.now()
    cur_time = now_time.hour * 60 + now_time.minute
    if cur_time < 8 * 60:
        print("I am Sleeping")
        time.sleep(40)


    cal_start_time = time.time()

    # # 将下面的路径替换为你电脑内chromedriver所在的路径
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 MicroMessenger/5.0.1"')
    driver = webdriver.Chrome("chrom/chromedriver",
                              chrome_options=options)


    time_s_list = ["9:00-10:00",
                   "10:00-11:00",
                   "11:00-12:00",
                   "14:00-15:00",
                   "15:00-16:00",
                   "16:00-17:00",
                   "17:00-18:00",
                   "18:00-19:00",
                   "19:00-20:00",
                   "20:00-21:00",
                   "21:00-22:00"]


    book_success = 0



    badminton_court_1 = 0  # 场地1
    badminton_court_2 = 1  # 场地2

    result_num = book_time(driver,time_s_list[index_booktime],badminton_court_1) #预定1号场地八点到九点的
    if(result_num==book_success):#成功
        print("预约1号场地 {} 成功".format(time_s_list[index_booktime]))
    else:
        print("预约1号场地 {} 失败".format(time_s_list[index_booktime]))
        result_num = book_time(driver, time_s_list[index_booktime], badminton_court_2)#预定2号场地八点到九点的
        if (result_num == book_success):  # 成功
            print("预约2号场地 {} 成功".format(time_s_list[index_booktime]))
        else:
            print("预约2号场地 {} 失败,这一天没预定".format(time_s_list[index_booktime]))



    cal_end_time = time.time()
    print("cal time:", cal_end_time - cal_start_time)
    driver.close()
    return result_num



def book2(index_booktime=0,badminton_court=0):
    # 提早了1分钟，则先休眠50秒？
    now_time = datetime.datetime.now()
    cur_time = now_time.hour * 60 + now_time.minute
    if cur_time < 8 * 60:
        print("I am Sleeping")
        time.sleep(40)


    cal_start_time = time.time()

    # # 将下面的路径替换为你电脑内chromedriver所在的路径
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 MicroMessenger/5.0.1"')
    driver = webdriver.Chrome("chrom/chromedriver",
                              chrome_options=options)


    time_s_list = ["9:00-10:00",
                   "10:00-11:00",
                   "11:00-12:00",
                   "14:00-15:00",
                   "15:00-16:00",
                   "16:00-17:00",
                   "17:00-18:00",
                   "18:00-19:00",
                   "19:00-20:00",
                   "20:00-21:00",
                   "21:00-22:00"]


    book_success = 0



    # badminton_court_1 = 0  # 场地1
    # badminton_court_2 = 1  # 场地2

    result_num = book_time(driver,time_s_list[index_booktime],badminton_court) #预定1号场地八点到九点的
    if(result_num==book_success):#成功
        print("预约{}号场地 {} 成功".format(badminton_court + 1, time_s_list[index_booktime]))
    else:
        print("预约{}号场地 {} 失败".format(badminton_court + 1, time_s_list[index_booktime]))




    cal_end_time = time.time()
    print("cal time:", cal_end_time - cal_start_time)
    driver.close()
    return result_num

def muti_book():

    nine_to_ten = 0                # "9:00-10:00",
    ten_to_eleven = 1              # "10:00-11:00",
    eleven_to_twelve = 2           # "11:00-12:00",
    fourteen_to_fifteen = 3        # "14:00-15:00",
    fifteen_to_sixteen = 4         # "15:00-16:00",
    sixteen_to_seventeen = 5       # "16:00-17:00",
    seventeen_to_eighteen = 6      # "17:00-18:00",
    eighteen_to_nineteen = 7      # "18:00-19:00",
    nineteen_to_twenty = 8        # "19:00-20:00",
    twenty_to_twenty_one = 9      # "20:00-21:00",
    twenty_one_to_twenty_two = 10 # "21:00-22:00"

    book_time_list = [fifteen_to_sixteen,sixteen_to_seventeen,seventeen_to_eighteen]
    thread_list = []
    for book_time in book_time_list:
        t = threading.Thread(target=book2, args=(book_time,0))
        t.start()
        t = threading.Thread(target=book2, args=(book_time, 1))
        t.start()
        # thread_list.append(t)


    # t1 = threading.Thread(target=book, args=(fifteen_to_sixteen,))
    # t2 = threading.Thread(target=book, args=(sixteen_to_seventeen,))
    # t3 = threading.Thread(target=book, args=(seventeen_to_eighteen,))

    # t1.start()
    # # t1.join()
    # t2.start()
    # # t2.join()
# muti_book()
# exit()
book()
exit()
if __name__ == '__main__':

    scheduler = BlockingScheduler()
    # scheduler.add_job(func=muti_book, trigger='cron',day_of_week=1-1, hour=8,minute=0) # 周一
    # scheduler.add_job(func=muti_book, trigger='cron', day_of_week=2 - 1, hour=8, minute=0)  # 周二
    # scheduler.add_job(func=muti_book, trigger='cron', day_of_week=3-1, hour=8, minute=0) # 周三约周五
    # scheduler.add_job(func=muti_book, trigger='cron', day_of_week=4 - 1, hour=7, minute=59)  # 周四约周六
    scheduler.add_job(func=muti_book, trigger='cron', day_of_week=5 - 1, hour=7, minute=59)  # 周五约周日
    # scheduler.add_job(func=muti_book, trigger='cron', day_of_week=6 - 1, hour=7, minute=59)  # 周6约周1
    scheduler.start()

