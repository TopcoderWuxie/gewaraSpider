#coding: utf-8

import pymysql
from Config import conn

def saveMoviesInfo(*args):
    """
    把电影的基本信息保存到数据库
    :param args:
    :return:
    """
    for a in args:
        print a,
    print
    # cur = conn.cursor()
    # try:
    #     cur.execute("call pro_add_gewara_movie('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % args)
    #     conn.commit()
    #     print u"当前信息写入成功！！！"
    # except Exception as e:
    #     print u"写入失败"
    #     conn.rollback()

def saveMoviesComment(*args):
    """
    把每个用户的评论保存到数据库
    :param args:
    :return:
    """

    for a in args:
        print a,
    print a
    # cur = conn.cursor()
    # try:
    #     cur.execute("call pro_add_gewara_comment('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % args)
    #     conn.commit()
    #     print u"当前信息写入成功！！！"
    # except Exception as e:
    #     print u"写入失败"
    #     conn.rollback()