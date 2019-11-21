import os
import re
import requests
from bs4 import BeautifulSoup

# 原网站url:
source_url = 'http://mmee94.com'
# 分类的url
#亚洲色图
Asian='亚洲色图'
Asian_url='http://mmee94.com/rjpu_7.html'
#欧美色图
Ou_Mei='欧美色图'
Ou_Mei_url='http://mmee94.com/rjpu_8.html'
#美腿丝袜
Leg='美腿丝袜'
Leg_url='http://mmee94.com/rjpu_9.html'
# 清纯
Qing_Chun='清纯'
Qing_Chun_url = 'http://mmee94.com/rjpu_10.html'
#卡通动漫
Cartoon='卡通动漫'
Cartoon_url='http://mmee94.com/rjpu_12.html'


save_path='D:/爬取的图片'

# 选择图片分类调用方法
def selectd_photo_type(type_string):
    print('正在从[' + type_string + ']下载中!')
    session = requests.session()
    # 构建request会话

    # 选择不同分类进入不同分类url
    if (type_string == Asian):
        Type_url = Asian_url
        #亚洲色图
    elif (type_string == Ou_Mei):
        Type_url = Ou_Mei_url
        #欧美
    elif (type_string == Leg):
        Type_url = Leg_url
        # 若选择美腿丝袜，则选择那个url
    elif (type_string == Qing_Chun):
        Type_url = Qing_Chun_url
        #清纯
    elif (type_string == Cartoon):
        Type_url = Cartoon_url
        #动漫

    else:
        print("无此分类")
        return

    DownLoad_From_Type(session,Type_url,type_string)
    #从正确的分类下载


def DownLoad_From_Type(session,Type_url,type_string):
    #参数为 会话session  类型的url  类型的string

    #若此分类不存在，创建此分类文件夹
    type_path='%s/%s' %(save_path,type_string)
    if(not os.path.exists(type_path)):
        os.makedirs(type_path)

    base_response = session.get(Type_url)
    # 进入类型网页
    base_html = base_response.text
    # 得到类型的网页html

    base_soup = BeautifulSoup(base_html, 'lxml')
    # 用Beautifulsoup解析
    url_list_tag = base_soup.find('ul', {'class': 'textList'}).find_all('a')
    # 得到图集的url-list
    # 从中选择textLIst为url-list所在，其中a tag 装了href
    download_from_url_list_tag(session, url_list_tag,type_path)


def download_from_url_list_tag(session,url_list_tag,type_path):
    #参数为 会话session  类型的url_list_tang   类型的文件夹
    #从装了url list的tag下载


    # tempcount = 1
    # i = 0

    for a_tag in url_list_tag:
        imgset_url = source_url + a_tag['href']
        # 图集的url
        imgset_response = session.get(imgset_url)
        # 得到一个图片集的response
        imgset_html = imgset_response.text
        # 得到图片集的html
        imgset_soup = BeautifulSoup(imgset_html, 'lxml')
        # 用BeautifulSoup处理图片集html
        imgs_url = imgset_soup.find_all('img')
        # 图片都在此html的img tag里的src

        imgset_name = imgset_url.split('/')[-1]
        # 得到图集名字

        imgset_path='%s/%s/' % (type_path,imgset_name)
        #图集存放位置的path

        if(not os.path.exists(imgset_path)):
            #若此图集没有，就下载

            os.makedirs('%s/%s/' % (type_path, imgset_name), exist_ok=True)
            # 创建图集路径
            print('downloading from %s' % imgset_name)
            # 接着对图集url下载图片:
            for img_tag in imgs_url:
                img_url = img_tag['src']
                # 得到单个图片url

                img_name = img_url.split('/')[-1]
                # 创建图片名

                img_response = session.get(img_url, stream=True)
                # 得到图片
                with open('%s/%s/%s' % (type_path, imgset_name, img_name), 'wb') as f:
                    for chunk in img_response.iter_content(chunk_size=128):
                        f.write(chunk)
                        # 写入图片
            print('Successfully Saved  Img Set! : %s' % imgset_name)


            # i = i + 1
            # if (i > tempcount):
            #     return

        else:
            print('此图集已经存在')



if __name__ == '__main__':
    flag=True
    #是否退出
    while(flag):
        print('''
请输入选择的类型:
    亚洲色图
    欧美色图
    美腿丝袜
    清纯
    卡通动漫
    
    退出
    ''')
        #选择类型的输出

        type_string = input()
        #输入分类
        print('已选择:' + type_string)
        if(type_string == '退出'):
            flag=False
        else:
            selectd_photo_type(type_string=type_string)

