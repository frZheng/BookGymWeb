
import datetime
import os
from rgb2bin import remove_bg
from rgb2bin import Identification_verification_code
from rgb2bin import check_img
from predict import  pre_img_to_lable
from captcha_predict_fun import torch_pred_func

from selenium import webdriver  # 用于打开网站
import requests as req
from bs4 import BeautifulSoup

import time
from multiprocessing import Process




nine_to_ten = 0  # "9:00-10:00",
ten_to_eleven = 1  # "10:00-11:00",
eleven_to_twelve = 2  # "11:00-12:00",
fourteen_to_fifteen = 3  # "14:00-15:00",
fifteen_to_sixteen = 4  # "15:00-16:00",
sixteen_to_seventeen = 5  # "16:00-17:00",
seventeen_to_eighteen = 6  # "17:00-18:00",
eighteen_to_nineteen = 7  # "18:00-19:00",
nineteen_to_twenty = 8  # "19:00-20:00",
twenty_to_twenty_one = 9  # "20:00-21:00",
twenty_one_to_twenty_two = 10  # "21:00-22:00"


def log_string(log, string):
    message = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"  "+string
    log.write(message+ '\n')
    log.flush()
    print(message)

def create_path(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def book_result(result_list,filename):
    book_success = 0
    code_error = 2
    other_err = 1

    with open(filename, "a", encoding='utf-8') as file:  # ”w"代表着每次运行都覆盖内容
        file.write("\n\n")
        for txt in result_list:
            file.write(txt)
            if "如需要取消预约请联系健身房管理员" in txt:
                print("预约成功")
                return book_success
            elif "验证码错误" in txt:
                print("验证码错误")
                # 应该再次预约此时间段
                return code_error
            elif "系统维护时间" in txt:
                return code_error
            else:
                # 预约其他时间段
                pass
            file.write("\n")
    return other_err

from bmt_server import ip_addr
from bmt_server import port
from bmt_server import badminton_str
from bmt_server import cli_send_seq
from bmt_server import buffer_size
from bmt_server import server_send_seq
from bmt_server import succeed_msg

from socket import *

def get_today_bmt_msg(id):
    max_try = 5
    for i in range(max_try):
        try:
            print("get_today_apply try time " + str(i))
            server_ip_port=(ip_addr,port)
            tcp_client=socket(AF_INET,SOCK_STREAM)   #第一步：客户端产生一个对象传俩个参数(socket.AF_INET基于网络通讯,socket.SOCK_STREAM表TCP协议)给tcp_client创建客户端套接字
            tcp_client.connect(server_ip_port)              #第二步：客户端连接服务器端的IP和端口
            break
        except:
            pass


    msg = badminton_str + cli_send_seq + str({"id":id})

    for i in range(max_try):
        tcp_client.send(msg.encode('utf-8')) #第六步：客户端把用户输入的消息进行二进制编码给服务端的msg(socket发消息会从用户态内存send给内核态内存，发到内核态的内存由操作系统接收，操作系统操作网卡发送出去)
        print('客户端已经发送消息')
        data = tcp_client.recv(buffer_size)    #第七步：客户端接收服务端字节格式
        rec_msg = data.decode('utf-8')
        print('收到服务端发来的消息',rec_msg)  #通过解码看服务端发送的消息
        rec_msg_list = rec_msg.split(server_send_seq)

        # print(rec_msg_list)
        if rec_msg_list[0] == succeed_msg:
            res = eval(rec_msg_list[1])
            tcp_client.close()  # 第八步：关闭客户端套接字
            return res
        else:
            print("today_trade error")
            continue
    tcp_client.close()                       #第八步：关闭客户端套接字
    return {}

def book_time(driver,book_time,book_xiangmu,file_path = "00_zfr/"):
    while True:
        # 报了异常则重来
        try:
            res,user_dict = book_time_o(driver, book_time, book_xiangmu,file_path)
            return res,user_dict
        except:
            print("try error")
            pass

def book_time_o(driver,book_time,book_xiangmu,file_path = "00_zfr/"):
    tmp_path = file_path + "tmp/"
    create_path(tmp_path)
    log_file_name = tmp_path + "log{}_{}.txt".format(book_time.replace(":", ""), book_xiangmu)
    log = open(log_file_name, 'a')  # append the log
    # 场地没预约则重来
    while 1:
        the_day_after_tomorrow = str(datetime.date.today() + datetime.timedelta(days=2))
        xiangmu_list = ["羽毛球(1号场)", "羽毛球(2号场)"]


        log_string(log,"网页开始加载")
        start_time = time.time()
        # http://zky.elstp.cn:8801/make-is-lit/?type=羽毛球(1号场)&date=2021-03-23&time=21:00-22:00
        html = "http://zky.elstp.cn:8801/make-is-lit/?type={}&date={}&time={}".format(
            xiangmu_list[book_xiangmu], the_day_after_tomorrow, book_time)
        log_string(log,html)
        driver.get(html)
        log_string(log,"网页加载完成 time= " + str(time.time() - start_time))

        start_time = time.time()
        # 保证验证码是四位的，这个还需要加一个一定要验证码是正确的
        while 1:
            # result = driver.find_elements_by_tag_name("src")
            # print(result)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            img_link = soup.select('.container')[0].select('img ')[0]['src']
            log_string(log,img_link)
            img_req = req.get(img_link)



            tmp_img_file_name = tmp_path + "tmp2{}_{}.png".format(book_time.replace(":", ""),book_xiangmu)
            with open(tmp_img_file_name, 'wb') as f:
                for chunk in img_req.iter_content(chunk_size=128):
                    f.write(chunk)

            # muggle_ocr无法识别带干扰的图片
            # import muggle_ocr
            # sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
            #
            # # n = "image.png"
            # with open(tmp_img_file_name, "rb") as f:
            #     b = f.read()
            # img_lable2 = sdk.predict(image_bytes=b)
            # print("muggle_ocr res: ",img_lable2)
            # if len(img_lable2) != 4:
            #     print("length error")

            remove_bg(tmp_img_file_name, "")
            Identification_verification_code(tmp_img_file_name, "")
            if check_img(tmp_img_file_name): # 图像为白色
                driver.execute_script("return get_code_img()")
                log_string(log, "图片为白色")
                continue
            img_lable1 = torch_pred_func(tmp_img_file_name)
            img_lable = pre_img_to_lable(tmp_img_file_name)



            log_string(log,"tf res: " +  img_lable+", torch res: " + img_lable1)
            normal_lable_len = 4
            # 这里还要再增加判断的条件，保证一次就完事
            if len(img_lable) == normal_lable_len and img_lable1==img_lable:
                break
            else:
                driver.execute_script("return get_code_img()")
                log_string(log, "重新获取验证码")
                time.sleep(0.1)
        log_string(log,"验证码加载完成 time= " + str(time.time() - start_time))

        with open(file_path+"user.txt", 'r', encoding='utf-8') as fin:
            # 读取所有行
            for line in fin.readlines():
                if line[-1] == "\n":
                    line = line[:-1]
        line_split = line.split(",")
        name = line_split[0]
        bumen = line_split[1]
        gonghao = line_split[2]
        lxfs = line_split[3]

        # today = str(time.strftime("%Y-%m-%d", time.localtime()))
        # msg = lxfs+"_" + today + book_time.replace(":", "") + str(book_xiangmu)
        # abs_file_name = tmp_path + msg+".txt"
        #
        #
        # if os.path.isfile(abs_file_name):
        #     log_string(log, "abs_file_name exist")
        #     try:
        #
        #         with open(abs_file_name, 'r', encoding='utf-8') as fin:
        #             # 读取所有行
        #             for line in fin.readlines():
        #                 if line[-1] == "\n":
        #                     line = line[:-1]
        #         user_dict = eval(line)
        #     except:
        #         log_string(log, "error")
        #         user_dict = get_today_bmt_msg(msg)
        #         with open(abs_file_name, 'w', encoding='utf-8') as fout:
        #             fout.write(str(user_dict))
        #             fout.flush()
        #
        # else:
        #     log_string(log, "abs_file_name not exist")
        #     user_dict = get_today_bmt_msg(msg)
        #
        #     with open(abs_file_name, 'w', encoding='utf-8') as fout:
        #         fout.write(str(user_dict))
        #         fout.flush()
        #         # fout.close()
        # if user_dict is None or user_dict=={}:
        #     log_string(log, "user_dict empty")
        #     user_dict = {'id': '18772101209_2021-12-122000-21000', 'name': '韦全生', 'bumen': '数字所', 'gonghao': 'XJY167761', 'lxfs': '15506789184'}
        #
        # log_string(log, str(user_dict))
        # name = user_dict["name"]
        # bumen = user_dict["bumen"]
        # gonghao = user_dict["gonghao"]
        # lxfs = user_dict["lxfs"]

        user_dict = {'id': '18772101209_2021-12-122000-21000', 'name': name, 'bumen':bumen, 'gonghao': gonghao,
                     'lxfs': lxfs}
        driver.find_element_by_name("name").send_keys(name.encode('utf-8').decode('utf-8'))  # 输入 姓名
        driver.find_element_by_name("bumen").send_keys(bumen.encode('utf-8').decode('utf-8'))  # 输入 部门
        driver.find_element_by_name("gonghao").send_keys(gonghao)  # 输入 工号
        driver.find_element_by_name("lxfs").send_keys(lxfs)  # 输入 联系方式

        driver.find_element_by_name("code").send_keys(img_lable)  # 输入 验证码



        # time.sleep(100)
        #等待到了八点点击
        while True:
            now_time = datetime.datetime.now()
            cur_time = now_time.hour * 3600 + now_time.minute * 60 + now_time.second + now_time.microsecond/1000000 # microsecond是微妙,转换为秒
            log_string(log,str(now_time))
            # 等待时间
            # 6500-M2,这个时间估计每台电脑都不一样?
            if cur_time >= 8*3600 + 0.9:
                # time.sleep(0.2)#休眠200MS，防止时间对不上
                driver.find_element_by_class_name("btn-primary").click()  # 提交审核
                now_time = datetime.datetime.now()
                log_string(log, "click" + str(now_time))
                break
            else:
                time.sleep(0.1)
                log_string(log,"waiting...")

        create_path(file_path + "logs/")


        ferdigtxt = []
        allelements = driver.find_elements_by_xpath("/html/body")
        for i in allelements:

            if i.text in ferdigtxt:
                pass
            else:
                ferdigtxt.append(i.text)

        print("ferdigtxt", ferdigtxt)

        result_num = book_result(ferdigtxt, file_path + "logs/" + the_day_after_tomorrow + "-" + str(book_time).replace(":", "") + "-{}.txt".format(book_xiangmu))

        code_error = 2
        if result_num == code_error:  # 再次预约此时间段
            log_string(log, "code_error")
            pass
        else:  # 预约成功或者失败都要退出
            log_string(log, "finish " + str(result_num))

            # time.sleep(100)
            # # 2. 写入文件
            # res_path = file_path + "logs/" + the_day_after_tomorrow + "-" + str(book_time).replace(":", "") \
            #            + "-{}".format(book_xiangmu)

            # # time.sleep(1000)
            # # 1. 执行 Chome 开发工具命令，得到mhtml内容
            # res = driver.execute_cdp_cmd('Page.captureSnapshot', {})
            #
            #
            # with open(res_path + ".mhtml", 'w', newline='') as f:  # 根据5楼的评论，添加newline=''
            #     f.write(res['data'])
            # driver.get_screenshot_as_file(res_path + ".png")
            # driver.get_screenshot_as_base64(res_path)
            # user_dict = {}
            return result_num,user_dict





def book(index_booktime=0,badminton_court=0,sigle_book=0,first_book_stadium=0,file_path = "00_zfr/"):
    # 提早了1分钟，则先休眠50秒？
    now_time = datetime.datetime.now()
    cur_time = now_time.hour * 60 * 60 + now_time.minute*60 + now_time.second

    # eight_time = 15 * 3600 + 34*60
    eight_time = 8 * 3600
    if cur_time < eight_time:
        #休眠时间到7：59：40，留下20秒来做开启服务
        sleep_time = eight_time-cur_time-20
        print("I am Sleeping",sleep_time)
        if sleep_time>0:
            time.sleep(sleep_time)
        print(str(datetime.datetime.now()))
    # exit()

    cal_start_time = time.time()

    # # 将下面的路径替换为你电脑内chromedriver所在的路径
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument(
        'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329 MicroMessenger/5.0.1"')
    # driver = webdriver.Chrome("chrom/chromedriver",
    #                           chrome_options=options)
    chromedriver_path = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver"
    # driver = webdriver.Chrome(chromedriver_path)
    driver = webdriver.Chrome(chromedriver_path, options=options)

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

    import get_ip
    inner_ip = get_ip.get_inner_ip()
    print(inner_ip)
    send = 0
    ip_6500 = "172.20.110.188"
    if inner_ip == ip_6500:#6500ip
        send = 1

    import send_email
    if sigle_book:
        if first_book_stadium:
            badminton_court_1 = 1  # 场地1
            badminton_court_2 = 0  # 场地2
        else:
            badminton_court_1 = 0  # 场地1
            badminton_court_2 = 1  # 场地2
        result_num, user_dict = book_time(driver, time_s_list[index_booktime], badminton_court_1,file_path)  # 预定1号场地八点到九点的
        if (result_num == book_success):  # 成功
            if first_book_stadium:
                msg = "预约2号场地 {} 成功".format(time_s_list[index_booktime])
            else:
                msg = "预约1号场地 {} 成功".format(time_s_list[index_booktime])
            msg += "\n" + "姓名:" + user_dict["name"] + str(inner_ip)
            print(msg)
            if send:
                send_email.send_mail_fun(file_path[:-1], msg,None,user_email=[])
        else:
            print("预约1号场地 {} 失败".format(time_s_list[index_booktime]))
            result_num, user_dict = book_time(driver, time_s_list[index_booktime], badminton_court_2,file_path)  # 预定2号场地八点到九点的
            if (result_num == book_success):  # 成功
                if first_book_stadium:
                    msg = "预约1号场地 {} 成功".format(time_s_list[index_booktime])
                else:
                    msg = "预约2号场地 {} 成功".format(time_s_list[index_booktime])
                msg += "\n" + "姓名:" + user_dict["name"] + str(inner_ip)
                print(msg)
                if send:
                    send_email.send_mail_fun(file_path[:-1], msg, None, user_email=[])
            else:
                print("预约2号场地 {} 失败,这一天没预定".format(time_s_list[index_booktime]))
    else:
        result_num, user_dict = book_time(driver,time_s_list[index_booktime],badminton_court,file_path) #预定1号场地八点到九点的
        if(result_num==book_success):#成功
            msg = "预约{}号场地 {} 成功".format(badminton_court + 1, time_s_list[index_booktime])
            msg += "\n" + "姓名:" + user_dict["name"] + str(inner_ip)
            print(msg)
            if send:
                send_email.send_mail_fun(file_path[:-1], msg, None, user_email=[])
        else:
            print("预约{}号场地 {} 失败".format(badminton_court + 1, time_s_list[index_booktime]))




    cal_end_time = time.time()
    print("cal time:", cal_end_time - cal_start_time)
    driver.close()

    print("\n\n", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," file name:", file_path, "\n\n")
    return result_num

def muti_book(book_time_list,file_path = "00_zfr/"):

    # book_time_list = [fifteen_to_sixteen,sixteen_to_seventeen,seventeen_to_eighteen]
    # thread_list = []

    for book_time in book_time_list:
        t = Process(target=book, args=(book_time, 0, 0,0,file_path))
        t.start()
        t = Process(target=book, args=(book_time, 1, 0,0,file_path))
        t.start()
        # t = threading.Thread(target=book, args=(book_time, 0, 0,0,file_path))
        # t.start()
        # t = threading.Thread(target=book, args=(book_time, 1, 0,0,file_path))
        # t.start()
        # thread_list.append(t)



if __name__ == '__main__':

    book()
    # book(nineteen_to_twenty, 1, 1,0,"00_zfr/")
    # exit()
    # muti_book([nine_to_ten,eleven_to_twelve],file_path = "05_xy/")



