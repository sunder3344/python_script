'''
Created on 2016年5月17日

@author: sunder3344
'''
#coding=utf-8
import boto3
import time
import os
import re
import json
from datetime import datetime
import urllib.request
import urllib.parse
import http.cookiejar
from boto3.session import Session
from xml.dom.minidom import *
from boto3.dynamodb.conditions import Key, Attr

def init_dynamodb(region='cn-north-1'):
    session = Session(
        aws_access_key_id='***',
        aws_secret_access_key='***',
        region_name=region,
    )
    if session:
        dynamo = session.resource('dynamodb')
        return dynamo

def query():
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = table.query(
            IndexName = 'cellphone-user_uuid-index',
            KeyConditionExpression = Key('cellphone').eq('13916807203')
    )
    print(response)

def user_statistic():
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, origin')
        else:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, origin', ExclusiveStartKey = response['LastEvaluatedKey'])
        for item in response['Items']:
            if 'user_uuid' in item:
                key = 'default'
                if 'origin' in item and item['origin'] != None:
                    key = item['origin']
                if key in data:
                    data[key] = int(data[key]) + 1
                else:
                    data[key] = 1
    print(data)

def statistic():
    count = 0
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    now = int(time.time())
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.scan(Limit = 100, ProjectionExpression = 'vip_begin_time, vip_end_time')
        else:
            response = table.scan(Limit = 100, ProjectionExpression = 'vip_begin_time, vip_end_time', ExclusiveStartKey = response['LastEvaluatedKey'])
        for item in response['Items']:
            if 'vip_begin_time' in item and 'vip_end_time' in item:
                if int(item['vip_begin_time']) <= now and int(item['vip_end_time']) >= now:
                    count = count + 1
    print('count:=%s' % count)    

def download():
    system = os.sys.platform
    def callbackfunc(blocknum, blocksize, totalsize):
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
#         if 'win' in system:
#             os.system('cls')
#         else:
#             os.system('clear')
        print("%.2f%%" % percent)
            
    url = 'http://mirrors.neusoft.edu.cn/eclipse/technology/epp/downloads/release/mars/2/eclipse-java-mars-2-win32-x86_64.zip'
    urllib.request.urlretrieve(url, './eclipse.zip', callbackfunc)
    
#模拟登陆
def fakeLogin():
    name = 's********4'
    pwd = '*******'
    mail = 'sunder3344@163.com'
    url = 'https://mail.163.com/entry/cgi/ntesdoor?df=mail163_letter&from=web&funcid=loginone&iframe=1&language=-1&passtype=1&product=mail163&net=t&style=-1&race=570_558_569_bj&uid=' + mail
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    data = {'savelogin': '1', 'url2': 'http://mail.163.com/errorpage/error163.htm', 'username': name, 'password': pwd}
    post_data = urllib.parse.urlencode(data)
    post_data = post_data.encode('utf-8')
    
    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = http.cookiejar.CookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
    urllib.request.install_opener(opener)
    
#     req = urllib.request.Request(url = url, data = post_data, headers = header, method = 'POST')
#     f = urllib.request.urlopen(req, timeout=120)
#     content = f.read()
#     content = str(content, encoding='utf8').strip()
    f = opener.open(url, data = urllib.parse.urlencode(data).encode())
    content = f.read()
    content = str(content, encoding='utf8').strip()
    
    m = re.match(r"[\w\W]*href = \"([\w\W]*)\";<\/script>", content)
    url = ''
    if m.group(1):
        url = m.group(1)
    if url != '':
        sid_re = re.match(r"[\w\W]*sid=([\w\W]*)=mail163_letter", url)
        sid = sid_re.group(1)
        m = opener.open(url)
        m = str(m.read(), encoding='utf8').strip()
        #获取邮箱联系人列表
        url = 'http://mail.163.com/contacts/call.do?uid='+mail+'&sid='+sid+'&from=webmail&cmd=newapi.getContacts&vcardver=3.0&ctype=all&attachinfos=yellowpage,frequentContacts&freContLim=20'
        contactList = opener.open(url).read()
        contactList = str(contactList, encoding='utf8').strip()
        contactMap = json.loads(contactList)
        print(contactMap)
        
        #获取邮件信息
        url = 'http://mail.163.com/js6/s?sid='+sid+'&func=mbox:listMessages&LeftNavfolder1Click=1&mbox_folder_enter=1'
        param = {"var": "<?xml version=\"1.0\"?><object><int name=\"fid\">1</int><string name=\"order\">date</string><boolean name=\"desc\" \
                >true</boolean><int name=\"limit\">50</int><int name=\"start\">0</int><boolean name=\"skipLockedFolders\">false \
                </boolean><string name=\"topFlag\">top</string><boolean name=\"returnTag\">true</boolean><boolean name=\"returnTotal\" \
                >true</boolean></object>"}
#         mailList = urllib.request.urlopen(url, data = urllib.parse.urlencode(param).encode()).read()
        mailList = opener.open(url, data = urllib.parse.urlencode(param).encode()).read()
        mailList = str(mailList, encoding='utf8').strip()
        print(mailList)
    
def feedback():
    import csv
    file = 'feedback.csv'
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('feedback')
    response = {'LastEvaluatedKey': None}
    with open(file, "w", newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        while ('LastEvaluatedKey' in response):
            if response['LastEvaluatedKey'] == None:
                response = table.scan(Limit = 100, ProjectionExpression = 'id, client_version, connect_type, contact, create_time, feedback_content, ip, os, uid, vid, video_type')
            else:
                response = table.scan(Limit = 100, ProjectionExpression = 'id, client_version, connect_type, contact, create_time, feedback_content, ip, os, other_info, uid, vid, video_type', ExclusiveStartKey = response['LastEvaluatedKey'])
            for item in response['Items']:
                if item['create_time'] >= 1470389256:
                    csvwriter.writerow([item['id'], item['client_version'], item['connect_type'], item['contact'], item['create_time'], item['feedback_content'], item['ip'], item['os'], item['uid'], item['vid'], item['video_type']])

def pizzaHut(city):
    url = 'http://www.pizzahut.com.cn/'
    data = {'NSC_CX_QfstjtufodzHspvq':'ffffffff09320b0745525d5f4f58455e445a4a423660', '_u_':'1', 'iplocation':city + '|0|0'}
    cookieStr = urllib.parse.urlencode(data)
#     cookieStr = 'NSC_CX_QfstjtufodzHspvq=ffffffff09320b0745525d5f4f58455e445a4a423660; _u_=1; iplocation=%E4%B8%8A%E6%B5%B7%E5%B8%82%7C0%7C0'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 'Cookie': cookieStr}
    req = urllib.request.Request(url = url, headers = header, method = 'GET')
    f = urllib.request.urlopen(req, timeout = 10)
    content = f.read()
    content = str(content, encoding='utf8').strip()
    print(content)
    
def userOrderList():
    import csv
    file = 'userOrderList.csv'
    dynamo = init_dynamodb()
    table = dynamo.Table('order_info')
    response = {'LastEvaluatedKey': None}
    print(time.time())
    with open(file, 'w', newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv, dialect = ('excel'))
        csvwriter.writerow(['订单id', '订单描述', '创建时间', '是否退款', '支付状态', '支付类型', '产品', '主题', '金额', '用户id', '渠道号', '卡密卡券'])
        while ('LastEvaluatedKey' in response):
            if response['LastEvaluatedKey'] == None:
                response = table.scan(Limit = 100, ProjectionExpression = 'order_id, body, create_time, is_refund, pay_status, pay_type, product_id, subject, total_fee, user_id, channelId, card_no')
            else:
                response = table.scan(Limit = 100, ProjectionExpression = 'order_id, body, create_time, is_refund, pay_status, pay_type, product_id, subject, total_fee, user_id, channelId, card_no', ExclusiveStartKey = response['LastEvaluatedKey'])
            for item in response['Items']:
                create_time = time.localtime(item['create_time'])
                create_time = time.strftime('%Y-%m-%d %H:%M:%S', create_time)
                if item['pay_status'] > 1 and item['pay_type'] in [1,2,3,4,5]:      #只用支付成功的
                    pay_type = ''
                    if item['pay_type'] == 1:
                        pay_type = '支付宝'
                    elif item['pay_type'] == 2:
                        pay_type = '微信'
                    elif item['pay_type'] == 3:
                        pay_type = 'IAP'
                    elif item['pay_type'] == 4:
                        pay_type = '卡密'
                    elif item['pay_type'] == 5:
                        pay_type = '卡券'
                    product = ''
                    if item['product_id'] == 1:
                        product = '1个月'
                    elif item['product_id'] == 2:
                        product = '3个月'
                    elif item['product_id'] == 3:
                        product = '1年'
                    elif item['product_id'] == 4:
                        product = '3天体验包'
                    elif item['product_id'] == 5:
                        product = '半年免费包'
                    elif item['product_id'] == 6:
                        product = '1个月免费包'
                    elif item['product_id'] == 7:
                        product = '1年免费包'
                    channelId = ''
                    card_no = ''
                    if ('channelId' in item.keys()):
                        channelId = item['channelId']
                    if ('card_no' in item.keys()):
                        card_no = item['card_no']
                    csvwriter.writerow([item['order_id'], item['body'], create_time, item['is_refund'], item['pay_status'], pay_type, product, item['subject'], item['total_fee'], item['user_id'], channelId, card_no])
    print("success");
    print(time.time())
    
def user_gender_list():
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    print("start %s" % datetime.now())
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, gender')
        else:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, gender', ExclusiveStartKey = response['LastEvaluatedKey'])
        for item in response['Items']:
            if 'user_uuid' in item:
                key = 'default'
                if 'gender' in item and item['gender'] != None:
                    key = item['gender']
                else:
                    key = 0
                if key in data:
                    data[key] = int(data[key]) + 1
                else:
                    data[key] = 1
    print(data)
    print("end %s" % datetime.now())

def tick():
    print("Tick! the time is: %s" % datetime.now())
    
def startJob():
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', second="*/3", hour='*')
    print("endless loop")
    try:
        scheduler.start()
    except (Exception, KeyboardInterrupt):
        scheduler.shutdown()
        

#上海联通活动数据统计
def sh_unicom():
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, activity_flag')
        else:
            response = table.scan(Limit = 100, ProjectionExpression = 'user_uuid, activity_flag', ExclusiveStartKey = response['LastEvaluatedKey'])
        for item in response['Items']:
            if 'user_uuid' in item:
                key = 'default'
                if 'activity_flag' in item and item['activity_flag'] != None:
                    key = item['activity_flag']
                if key in data:
                    data[key] = int(data[key]) + 1
                else:
                    data[key] = 1
    print(data)
    
#广东移动校园项目统计
def gd_mobile_campus():
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.query(Limit = 100, IndexName = 'origin-index', ProjectionExpression = 'user_uuid, register_time', KeyConditionExpression = Key('origin').eq('GD_CAMPUS'))
        else:
            response = table.query(Limit = 100, IndexName = 'origin-index', ProjectionExpression = 'user_uuid, register_time', KeyConditionExpression = Key('origin').eq('GD_CAMPUS'), ExclusiveStartKey = response['LastEvaluatedKey'])
        for item in response['Items']:
            if 'user_uuid' in item and item['user_uuid'] != None:
                key = time.strftime('%Y-%m-%d', time.localtime(int(item['register_time'])))
                if key in data:
                    data[key] = int(data[key]) + 1
                else:
                    data[key] = 1
    print(data)        

def gd_mobiel_statistic():
    count = 0
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.query(Limit = 2000, IndexName = 'origin-index', ProjectionExpression = 'user_uuid, register_time', KeyConditionExpression = Key('origin').eq('GD_Mobile'))
        else:
            response = table.query(Limit = 2000, IndexName = 'origin-index', ProjectionExpression = 'user_uuid, register_time', KeyConditionExpression = Key('origin').eq('GD_Mobile'), ExclusiveStartKey = response['LastEvaluatedKey'])
        if 'Count' in response and response['Count'] != None:
            count = count + int(response['Count'])
    print(count)
    
#提取9月18、19日两天中，反馈信息为“朱家角”“拾音而上”的手机号
def feedback_search():
    import csv
    file = 'feedback_search.csv'
    data= {}
    dynamo = init_dynamodb()
    table = dynamo.Table('feedback')
    response = {'LastEvaluatedKey': None}
    with open(file, "w", newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        while ('LastEvaluatedKey' in response):
            if response['LastEvaluatedKey'] == None:
                response = table.scan(Limit = 100, ProjectionExpression = 'id, client_version, connect_type, contact, create_time, feedback_content, ip, os, uid, vid, video_type')
            else:
                response = table.scan(Limit = 100, ProjectionExpression = 'id, client_version, connect_type, contact, create_time, feedback_content, ip, os, other_info, uid, vid, video_type', ExclusiveStartKey = response['LastEvaluatedKey'])
            for item in response['Items']:
#                 if item['create_time'] >= 1474128000 and item['create_time'] < 1474300800:
                    res1 = re.findall(u'朱家角', item['feedback_content'])
                    res2 = re.findall(u'拾音而上', item['feedback_content'])
#                     if item['feedback_content'] == "朱家角" or item['feedback_content'] == "拾音而上":
                    if len(res1) != 0 or len(res2) != 0:
                        print(item)
                        csvwriter.writerow([item['id'], item['contact'], item['uid']])
                        
def gd_mobile_order_count():
    count = 0
    dynamo = init_dynamodb()
    table = dynamo.Table('order_info')
    response = {'LastEvaluatedKey': None}
    while ('LastEvaluatedKey' in response):
        if response['LastEvaluatedKey'] == None:
            response = table.query(Limit = 2000, IndexName = 'product_id-pay_status-index', ProjectionExpression = 'order_id', KeyConditionExpression = Key('product_id').eq(10))
        else:
            response = table.query(Limit = 2000, IndexName = 'product_id-pay_status-index', ProjectionExpression = 'order_id', KeyConditionExpression = Key('product_id').eq(10), ExclusiveStartKey = response['LastEvaluatedKey'])
        if 'Count' in response and response['Count'] != None:
            count = count + int(response['Count'])
    print(count)
    
#查询重复用户
def duplicate_user():
    import csv
    count = 0
    file = 'duplicate.csv'
    dynamo = init_dynamodb()
    table = dynamo.Table('t_user')
    response = {'LastEvaluatedKey': None}
    now = int(time.time())
    with open(file, "w", newline="", encoding='utf-8') as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        while ('LastEvaluatedKey' in response):
            if response['LastEvaluatedKey'] == None:
                response = table.scan(Limit = 1000, ProjectionExpression = 'user_uuid, register_time, cellphone')
            else:
                response = table.scan(Limit = 1000, ProjectionExpression = 'user_uuid, register_time, cellphone', ExclusiveStartKey = response['LastEvaluatedKey'])
            for item in response['Items']:
                if 'cellphone' in item:
                    phone = item['cellphone']
                    #根据手机再去查询
                    response2 = table.query(Limit = 100, IndexName = 'cellphone-user_uuid-index', ProjectionExpression = 'user_uuid, register_time, cellphone', KeyConditionExpression = Key('cellphone').eq(phone))
                    if 'Count' in response2:
                        count = int(response2['Count'])
                        if count > 1:
                            print(phone)
                            csvwriter.writerow([phone])
    

if __name__ == '__main__':
#     query()
#     user_statistic()
#     statistic()
#     download()
#     fakeLogin()
#     loginTaoBao()
#     feedback()
#     pizzaHut('上海市')
#     pizzaHut('安阳')
#     userOrderList()
#     user_gender_list()
#     startJob()
#     sh_unicom()
#     gd_mobile_campus()
#     gd_mobiel_statistic()
#     feedback_search()
    duplicate_user()
