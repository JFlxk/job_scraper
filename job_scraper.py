#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'lxk'
__mtime__ = '2022/3/18'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃   ☃   ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━━━━┓
              ┃ 神兽保佑   ┣┓
              ┃ 永无BUG！ ┏┛
              ┗┓┓┏━┳┓┏━━━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
# 爬取新发地菜价
from bs4 import BeautifulSoup
import requests
import csv
import time
import pandas as pd
from datetime import date, timedelta


def post_server_wechat(title, desp):
    """

    :param title: 标题
    :param desp: 内容主体
    :return:
    """
    requests.post("http://sc.ftqq.com/xxxx.send", data={'text': title, 'desp': desp})


def is_exist(df, title, publish_time):
    """
    判断是否已经爬取
    :param df:
    :param title: 标体
    :param publish_time: 发布时间
    :return:
    """
    a = df.query('标题 == "{}" and 发布时间 == "{}"'.format(title, publish_time))
    return a.empty


def get_gdrsj_info(df):
    # 广东人社局招聘
    url = "http://hrss.gd.gov.cn/zwgk/sydwzp/index.html"
    resp = requests.get(url)
    resp.encoding = "utf-8"
    # print(resp.text)
    # 1.把页面数据用BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # html.parser：指定HTML解析器

    # 2.从bs对象中查找数据
    tag_a_L = page.select('.list li')
    for i in tag_a_L:
        if is_exist(df, i.a['title'], i.span.text.replace("-", "/")):
            csvwriter.writerow(
                ['广东人社局', i.a['title'], i.a['href'], i.span.text.replace("-", "/"),
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['广东人社局', i.a['title'], i.a['href'], i.span.text.replace("-", "/"),
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def get_qgsydw_info(df):
    # 全国事业单位招聘网
    url_prefix = 'https://www.qgsydw.com'
    url = "https://www.qgsydw.com/dwsp/Search/GetPagerData?dq=&pageIndex=1&channelIds=50,51&timeSolt=30&keyword=%E5%B9%BF%E5%B7%9E"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    }
    res = requests.get(url=url, headers=headers)
    data = res.json()
    job_list = data['data']['pager']['data']
    for job_info in job_list:
        if is_exist(df, job_info['title'], job_info['addDate'].split(' ')[0]):
            csvwriter.writerow(
                ['全国事业单位招聘网', job_info['title'], url_prefix + job_info['linkUrl'], job_info['addDate'].split(' ')[0],
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['全国事业单位招聘网', job_info['title'], url_prefix + job_info['linkUrl'], job_info['addDate'].split(' ')[0],
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def get_zsdx_info(df):
    # 中山大学
    url = "https://uems.sysu.edu.cn/hrrecruit/project/zsdx/defalt/recruitFirstpage.jsp?FM_SYS_ID=hrs"
    resp = requests.get(url)
    resp.encoding = "utf-8"
    # print(resp.text)
    # 1.把页面数据用BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # html.parser：指定HTML解析器

    # 2.从bs对象中查找数据
    tag_a_L = page.select('#list-right li')
    for i in tag_a_L:
        if is_exist(df, i.a.text.replace('    ', ''), i.em.text.replace("-", "/").replace('    ', '')):
            csvwriter.writerow(
                ['中山大学', i.a.text.replace('    ', ''), '', i.em.text.replace("-", "/").replace('    ', ''),
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['中山大学', i.a.text.replace('    ', ''), '', i.em.text.replace("-", "/").replace('    ', ''),
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def get_hnnydx_info(df):
    # 华农人才招聘
    url_prefix = 'https://hr.scau.edu.cn'
    url = "https://hr.scau.edu.cn/6122/list.htm"
    resp = requests.get(url)
    resp.encoding = "utf-8"
    # print(resp.text)
    # 1.把页面数据用BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # html.parser：指定HTML解析器

    # 2.从bs对象中查找数据
    tag_a_L = page.select('.content.contentl p')
    for i in tag_a_L:
        title = i.a.a['title']
        next_url = url_prefix + i.a['href']
        p_time = i.a.span.text.replace("-", "/")
        if is_exist(df, title, p_time):
            csvwriter.writerow(
                ['华农', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['华农', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def get_gzykdx_info(df):
    # 广州医科大学
    # url_prefix = 'https://hr.scau.edu.cn'
    url = "https://zpxt.gzhmu.edu.cn/gzykdx/recruit/a.epx?action=index&entityId=HR_RECRUIT_RESUME"
    resp = requests.get(url)
    resp.encoding = "utf-8"
    # print(resp.text)
    # 1.把页面数据用BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # html.parser：指定HTML解析器

    # 2.从bs对象中查找数据
    tag_a_L = page.select('tr[style="font-size:12px;cursor:pointer"]')
    for i in tag_a_L:
        title = i.td.text.replace(' ', '')
        next_url = ''
        p_time = i.select_one("td:last-of-type").text.replace("-", "/").replace(' ', '')
        if is_exist(df, title, p_time):
            csvwriter.writerow(
                ['广医', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['广医', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def get_gzzyydx_info(df):
    # 广州中医药大学
    url_prefix = 'https://www.gzucm.edu.cn'
    url = "https://www.gzucm.edu.cn/zpxx/gkzp.htm"
    resp = requests.get(url,verify=False)
    resp.encoding = "utf-8"
    # 1.把页面数据用BeautifulSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # html.parser：指定HTML解析器

    # 2.从bs对象中查找数据
    tag_a_L = page.select('.content_list ul li')
    for i in tag_a_L:
        title = i.a['title']
        next_url = url_prefix + i.a['href'].replace("..", "")
        p_time = i.span.text.replace("年", "/").replace("月", "/").replace("日", "").replace(' ', '')
        if is_exist(df, title, p_time):
            csvwriter.writerow(
                ['广州中医药大学', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])
            print(
                ['广州中医药大学', title, next_url, p_time,
                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                 ''])


def summary_to_wechat(df):
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y/%m/%d")
    df_data = df.query('发布时间 == "{}"'.format(yesterday))
    resp_text = ''
    for row in df_data.iterrows():
        resp_text += '{}:{}\r\n'.format(str(row[1][1]), str(row[1][2]))
    resp_title = '{}共发布了{}条招聘信息'.format(yesterday, str(len(df_data)))
    print(resp_title)
    print(resp_text)
    # post_server_wechat(resp_title, resp_text)


# 定时执行爬取任务
while True:
    # 打开csv文件并写入
    f = open("job.csv", mode="a+", newline='', encoding="UTF-8")
    df = pd.read_csv("job.csv")
    csvwriter = csv.writer(f)

    # # 广东人社局招聘
    # get_gdrsj_info(df)
    #
    # # 全国事业单位招聘网
    # get_qgsydw_info(df)

    # # 中大人才招聘
    # get_zsdx_info(df)

    # # 华农人才招聘
    # get_hnnydx_info(df)

    # # 广州医科大学
    # get_gzykdx_info(df)

    # # 广州中医药大学
    # get_gzzyydx_info(df)

    f.close()
    df = pd.read_csv("job.csv")
    # 汇总统计发至微信
    summary_to_wechat(df)
    f.close()
    time.sleep(86400)
