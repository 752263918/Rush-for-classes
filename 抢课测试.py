# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 23:42:23 2020

@author: LiSunBowen
"""

import requests
import time

urlh=input('请输入url后回车：')
url=urlh
header={'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Connection': 'keep-alive', 'Content-Length': '659', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Cookie': 'JSESSIONID=EB7FC341DC5217219226FDEE5ED8BD36', 'DNT': '1', 'Host': '218.197.80.13', 'Origin': 'http://218.197.80.13', 'Referer': 'http://218.197.80.13/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=18020115', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56', 'X-Requested-With': 'XMLHttpRequest'}

#header=dict([line.split(": ",1) for line in header[i].split("\n")]) 已弃用
data=[
{'jxb_ids': '75105f21f5f71f114f0e0d582f0b93363f0f6e85928de0f68d701e4f806aa85a2e3fe2c0838b8980461af5907fa5e87b795e22d7f31d80ced5b6fe14befc045dcdcf5752fbb163c91ea4fee4b3d930b889e833036c226e3f43344505e631b9ecdefcddc54c6d5bac5b0b8cca4e372d4c8ee733bb641b5b4c4fccb4659b601ad8', 'kch_id': '7D33DD0A6668723CE0530B50C5DA0DBB', 'kcmc': '(TX3431)当代中国政府与政治(网络通识课) - 2.0 学分', 'rwlx': '2', 'rlkz': '0', 'rlzlkz': '1', 'sxbj': '1', 'xxkbj': '0', 'qz': '0', 'cxbj': '0', 'xkkz_id': 'A83E41F4B6362D30E0530B50C5DA0F14', 'njdm_id': '2018', 'zyh_id': '0307', 'kklxdm': '10', 'xklc': '2', 'xkxnm': '2020', 'xkxqm': '3'},
{'jxb_ids': '37bc628e36f5670d096b76d137588ba836ef1623fd275fae2fd9b07ce33cb9b01d390173d7ee30aa66a0689da389cb8aafd4793c5a5299ac56c273f0c63208a73c982e5e4ef31c3a5cf1804f07a9b9647b3c1a32aed983dc4e24acdb8f989bfc960cda1809cc2afcaf48d79fe5bcbf3247366f84453b4cb4f4e6dde3a13357d8', 'kch_id': '8C3555B8B84533A1E0530B50C5DA571C', 'kcmc': '(TX9845)聆听心声：音乐审美心理分析(网络通识课) - 2.0 学分', 'rwlx': '2', 'rlkz': '0', 'rlzlkz': '1', 'sxbj': '1', 'xxkbj': '0', 'qz': '0', 'cxbj': '0', 'xkkz_id': 'A83E41F4B6362D30E0530B50C5DA0F14', 'njdm_id': '2018', 'zyh_id': '0307', 'kklxdm': '10', 'xklc': '2', 'xkxnm': '2020', 'xkxqm': '3'},
]
#data[i]=dict([line.split(": ",1) for line in data.split("\n")]) 已弃用

t=-1 #初始化t值，t是抢课后服务器返回值，返回-1表示因为满员或其他原因未抢课成功，返回1表示抢课成功
num=0 #计数器，记录重复发送了多少次
e=0 #记录出错次数，在后续代码中，出错14次就会停止执行程序并报错
p=0 #计算抢到的各个课程的学分和，避免超过学分上限，比如只需要3分，避免抢到5分
i=0 #初始化i=0，也可不写，因为在循环中i默认从0开始
p0=int(input('请输入学分上限：'))  #设置学分上限，比如输入4分，就不会抢到5分，但可能抢到3分停止
if isinstance(data,list): #判断data是不是列表，建议使用列表
    while (t==-1) and (p<p0) and (e<14) and (num<10000) :   #默认t=-1时才能进入循环体，现有学分P要小于设定的学分上限，错误次数e小于14次才能继续循环（可以调整），设置了num的上限，重复10000次后停止，避免无限循环，可以手动调整
        for i in range(len(data)):
            try:
                if p+eval(data[i]['kcmc'].split(' ')[2])<=p0:   #获取data中的课程学分，避免抢到的学分超过上限
                    r=requests.post(url,data=data[i],headers=header,timeout=5)   ####发送请求，这是关键步骤####
                    t=eval(eval(r.text)['flag'])   #判断返回值，返回值的参数flag后是1或-1，代表选课成功、不成功
                    num=num+1  #计数器
                    time.sleep(0.3)  #每次提交请求后休息0.3秒（可以调整）
                    if t==-1:  #返回-1抢课失败
                        print('没有抢到{}，重复执行第{}次,现学分{}'.format(data[i]['kcmc'].split(' ')[0],num,p))
                    elif t!=-1: #返回1抢课成功
                        p=p+eval(data[i]['kcmc'].split(' ')[2])  #累加抢到的学分
                        print('>>抢课成功,课程名称:{}，现学分{}'.format(data[i]['kcmc'],p))
                    if p==p0:  #抢满学分时跳出循环，停止程序
                        break
                elif p+eval(data[i]['kcmc'].split(' ')[2])>p0:  #避免超过学分上限，若会超过，跳出循环，停止程序
                    print('-->当前已经抢到最大学分限度，现有学分{}'.format(p))
                    if p0==1:  #学分上限是特殊情况，只需要抢到一分课即可跳出
                        t=1
                    break
            except:  #出现网络问题会提示以下信息
                print('\n***出现网络问题，请登入网站检查是否正常***')
                e=e+1
    else:  #不满足while的条件时显示以下内容
        if p+eval(data[i]['kcmc'].split(' ')[2])>p0:  #继续抢课会超过学分上限提示
            print('==已经抢到最大限度，现有学分{}=='.format(p))
        elif p==p0:  #学分抢满提示
            print('==学分已经满，现学分{}=='.format(p))
        else:  #其他问题提示
            print('出现其他问题')
else: #不是列表提示
    print('data不是列表，检查数据')
