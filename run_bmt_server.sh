
PROCESS=`ps -ef | grep bmt_server.py | grep -v grep | awk '{print $2}' | xargs kill -9`
sleep 10
rm nohup.out
# 路径是/tmp/zfrFile/Book_gym_20211020/


nohup /root/anaconda3/bin/python bmt_server.py &

