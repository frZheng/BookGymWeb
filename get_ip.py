
# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 2:29 下午
# @Author  : SunRuichuan
# @File    : get_ip.py

import socket



# 根据dns解析，获取网卡ip
def get_inner_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        _ip = s.getsockname()[0]
    finally:
        s.close()
    return _ip


# 解析网页，正则判断，获取用户实际公网ip
def get_outer_ip():
    import requests

    import re

    r = requests.get("http://txt.go.sohu.com/ip/soip")

    ip = re.findall(r'\d+.\d+.\d+.\d+', r.text)

    # print(ip[0])
    return ip[0]

# import socket
#
# # url = 'www.baidu.com'
# url = 'www.lrdkzz.com'
# res = socket.getaddrinfo(url, None)
# print(res)
#
# ip = res[0][4][0]
# print(ip)

if __name__ == '__main__':
    ip1 = get_inner_ip()
    ip2 = get_outer_ip()
    print("inner", ip1)
    print("outer", ip2)
    exit()