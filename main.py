

from apscheduler.schedulers.blocking import BlockingScheduler

import os
from book_func import muti_book
from book_func import book
from book_func import *
if __name__ == '__main__':
    print("\n\nfile name:", (os.getcwd()), "\n\n")
    scheduler = BlockingScheduler()
    # 只约一个场地
    scheduler.add_job(func=book, args=(eighteen_to_nineteen, 0, 1),
                      trigger='cron', day_of_week=1 - 1, hour=7, minute=59)  # 周1约周3
    scheduler.add_job(func=book, args=(nineteen_to_twenty, 0, 1),
                      trigger='cron', day_of_week=1 - 1, hour=7, minute=59)  # 周1约周3

    scheduler.add_job(func=book, args=(twenty_one_to_twenty_two, 0, 1),
                      trigger='cron', day_of_week=1 - 1, hour=7, minute=59)  # 周1约周3

    # scheduler.add_job(func=muti_book, args=([eighteen_to_nineteen, nineteen_to_twenty],),
    #                   trigger='cron', day_of_week=1 - 1, hour=7, minute=59)  # 周1约周3

    # scheduler.add_job(func=muti_book, args=([eighteen_to_nineteen, nineteen_to_twenty],),
    #                   trigger='cron', day_of_week=2 - 1, hour=7, minute=59)  # 周2约周4

    # scheduler.add_job(func=book, args=(twenty_one_to_twenty_two, 0, 1),
    #                   trigger='cron', day_of_week=2 - 1, hour=7, minute=59)  # 周2约周4
    scheduler.add_job(func=book, args=(eighteen_to_nineteen, 0, 1),
                      trigger='cron', day_of_week=2 - 1, hour=7, minute=59)  # 周2约周4
    scheduler.add_job(func=book, args=(nineteen_to_twenty, 0, 1),
                      trigger='cron', day_of_week=2 - 1, hour=7, minute=59)  # 周2约周4

    # scheduler.add_job(func=muti_book, args=([eighteen_to_nineteen, nineteen_to_twenty],),
    #                   trigger='cron', day_of_week=3 - 1, hour=7, minute=59)  # 周3约周5

    scheduler.add_job(func=book, args=(eighteen_to_nineteen, 0, 1),
                      trigger='cron', day_of_week=3 - 1, hour=7, minute=59)  # 周3约周5
    scheduler.add_job(func=book, args=(nineteen_to_twenty, 0, 1),
                      trigger='cron', day_of_week=3 - 1, hour=7, minute=59)  # 周3约周5


    scheduler.add_job(func=muti_book, args=([fifteen_to_sixteen, sixteen_to_seventeen, seventeen_to_eighteen],),
                      trigger='cron', day_of_week=5 - 1, hour=7, minute=59)  # 周5约周7

    # 只约一个场地
    # scheduler.add_job(func=book, args=(eighteen_to_nineteen,0,1),
    #                   trigger='cron', day_of_week=6 - 1, hour=7, minute=59)  # 周6约周1
    # scheduler.add_job(func=book, args=(nineteen_to_twenty,0,1),
    #                   trigger='cron', day_of_week=6 - 1, hour=7, minute=59)  # 周6约周1
    # scheduler.add_job(func=book, args=(twenty_one_to_twenty_two,0,1),
    #                   trigger='cron', day_of_week=6 - 1, hour=7, minute=59)  # 周6约周1

    # 只约一个场地
    scheduler.add_job(func=book, args=(eighteen_to_nineteen,0,1,),
                      trigger='cron', day_of_week=7 - 1, hour=7, minute=59)  # 周日约周2
    scheduler.add_job(func=book, args=(nineteen_to_twenty,0,1,),
                      trigger='cron', day_of_week=7 - 1, hour=7, minute=59)  # 周日约周2
    # scheduler.add_job(func=book, args=(twenty_one_to_twenty_two, 0, 1),
    #                   trigger='cron', day_of_week=7 - 1, hour=7, minute=59)  # 周7约周2


    scheduler.start()

