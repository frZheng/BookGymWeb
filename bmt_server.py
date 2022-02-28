
import random
import os,sys
from socket import *
import threading

mongoclient = "mongodb://localhost:27017/"
badminton_db = 'badminton'
user_info_col = "book_user"
badminton_str = 'badminton'

ip_addr = 'www.lrdkzz.com'
# ip_addr = "120.25.179.200"
# ip_addr = '172.20.110.139'

# 用ifconfig 查看的IP
ip_addr_innet = "172.22.59.165"
# ip_addr_innet = "172.20.110.139"

port = 9998
buffer_size = 1024     #1024代表接收字节
back_log = 5           #半连接池最多可以有5个建立好三次握手后的连接等待
succeed_msg = "OK"
failed_msg = "Failed"
cli_send_seq = "\t"
server_send_seq = "\n"
bumen_list = [
    "数字所",
    "脑所",
    "合成所",
    "集成所",
    "医工所",
    "医药所",
    "职能部门",
]
import random
prelist=["130", "131", "132", "133", "134", "135", "136", "137", "138", "139","147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188", "189","172","176","185"]

def createPhone():
    phone_num = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
    return phone_num


def GBK2312(length=2):
    res = ""
    for i in range(length):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)   # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
        val = f'{head:x}{body:x}'
        str = bytes.fromhex(val).decode('gb2312')
        res += str
    return res

surname_list = """赵钱孙李周吴郑王冯陈蒋韩杨朱秦"""
name_str = """子赫,祺祾,朝彦,圣鹏,新哲,鼎明
楠明,裕昊,智棋,皓福,敬坤,渊荣
景尧,敬洪,朝实,善玮,朝棋,朝寒
楷林,景瑞,琪洋,捷杰,寒柏,敬易
涛光,鼎益,朝波,新明,昌震,皓翔
乔豪,敬轩,尚兴,皓清,裕明,杰宇
岩乐,乔宁,乔诚,川善,东辉,皓宁
雄杰,金锋,涛宇,楠峻,靖轩,尚欧
琪哲,皓景,昊辉,雨锋,智凯,捷旭
雨逸,宜磊,川峰,智睿,尚啸,铭晨
莱远,宝峰,涆安,腾波,星儒,玥隆
日麒,震可,远皓,宇正,铭振,蓄景
曜为,昂康,豪嘉,晟良,逸凌,珹耀
轩越,燎段,炎殿,淼瀚,昌烨,黎伟
昱名,彭奎,爵立,嘉珂,行成,曦栋
盛承,华博,达绍,颉钊,睿健,雄璟
灿厚,禧琛,锋宁,栋轩,阔继,宕珸
慨轮,锐天,辰富,可尧,裔圣,裔风
裔璇,裔瑛,政哲,一鸣,伟华,伟哲
炫琰,金鑫,柠浩,嘉熙,贝玺,子默
思远,浩轩,语堂,昕宇,家宇,宇豪
宇鞅,绍衡,鸿儒,鹏威,昊东,子骞
博文,尚卿,尚博,兴江,朗达,瑄家
鹏涛,炎彬,烨华,煜祺,正豪,章昭
鹤轩,伟泽,哲瀚,雨泽,楷瑞,建辉
煜城,昊然,鸿涛,志泽,弘文,黎昕
荣轩,君昊,熠彤,鸿煊,苑杰,贵伦
君煜,宇洋,郎霖,圣烨,瀚天,书孝
云厉,俞宇,柏轩,睿睿,霖泓,贻烁
政鑫,煜倩,皓宸,钰天,昆勤,嘉洋"""
name_lsit = name_str.replace("\n",",").split(",")

def query_badminton_user_info(data_dict):
    import pymongo
    myclient = pymongo.MongoClient(mongoclient)
    mydb = myclient[badminton_db]
    mycol = mydb[user_info_col]
    myquery = {"id": data_dict["id"]}
    mydoc_1 = mycol.find(myquery)
    query_res = {}
    # print("quere result")
    query_res_len = 0
    for y in mydoc_1:
        query_res_len += 1
        # 每一个结果只有一条记录
        query_res = y
        if query_res_len > 1:
            print("query_user_info query error")
    print("query_res")
    if query_res == {}:
        print("query_res empty")
        random_index = random.randint(0, len(surname_list))
        random_index2 = random.randint(0, len(name_lsit))
        # name = surname_list[random_index] + GBK2312()
        name = surname_list[random_index] + name_lsit[random_index2]
        random_index = random.randint(0, len(bumen_list))
        bumen = bumen_list[random_index]
        random_gonghao = str(random.randint(1,200000))
        gonghao = "XJY" + "0" * (6-len(random_gonghao)) + random_gonghao
        lxfs = createPhone()
        insert_dict = {"id": data_dict["id"],"name":name,"bumen":bumen,"gonghao":gonghao,"lxfs":lxfs}
        print("insert_dict",insert_dict)
        mycol.insert_one(insert_dict)


    mydoc_1 = mycol.find(myquery)
    query_res = {}
    # print("quere result")
    query_res_len = 0
    for y in mydoc_1:
        query_res_len += 1
        # 每一个结果只有一条记录
        query_res = y
        if query_res_len > 1:
            print("query_user_info query error")
    del query_res["_id"]
    return query_res

def tcplink(conn, addr):
    print('Accept new connection from %s:%s...' % addr)
    data = conn.recv(1024)
    cli_msg = data.decode('utf-8')

    msg_list = cli_msg.split(cli_send_seq)
    data = eval(msg_list[1])

    if msg_list[0] == badminton_str:# 插入申请记录
        query_dict_list = query_badminton_user_info(data)
    else:
        print("mode error")
        conn.send(failed_msg.encode('utf-8'))  # 第八步：服务端发送data字节格式通过upper()转大写回给客户端
        raise ValueError
    print('客户端发来的消息是', cli_msg)

    if msg_list[0] == badminton_str:# 返回用户信息
        msg = succeed_msg + server_send_seq + str(query_dict_list)
        print("服务器发送的消息是： ", msg)
        conn.send(msg.encode('utf-8'))
    else:
        conn.send(succeed_msg.encode('utf-8'))  # 第八步：服务端发送data字节格式通过upper()转大写回给客户端
    conn.close()
    print('Connection from %s:%s closed.' % addr)

if __name__ == '__main__':

    code_version = 202108131000
    print(os.getcwd())
    print("file name: %s" % (__file__), ", code Version: ", code_version)
    print("line: %s" % (sys._getframe().f_lineno))
    server_ip_port = (ip_addr_innet, port)
    print(server_ip_port)
    tcp_server = socket(AF_INET,
                        SOCK_STREAM)  # 第一步：产生一个对象传俩个参数(socket.AF_INET基于网络通讯,socket.SOCK_STREAM表TCP协议)给tcp_server创建服务器套接字
    tcp_server.bind(server_ip_port)  # 第二步：把IP地址和访问和端口号绑定到套接字
    tcp_server.listen(back_log)  # 第三步：监听链接，listen(5)最多可以有五个建立好三次握手后的backlog(半连接池)等着，后面的需要排队等着

    while True:  # 第四步：服务端做连接循环的接，可以做到接收多个人发的连接
        print('服务端开始运行了')
        conn, addr = tcp_server.accept()  # 第五步：tcp_server.accept()相当于拿到了TCP三次握手的结果是个元祖解压给给conn(三次握手的连接)和addr服务端阻塞
        print('双向链接是', conn)  # 打印conn：
        print('客户端地址', addr)  # 打印addr：
        t = threading.Thread(target=tcplink, args=(conn, addr))
        t.start()
