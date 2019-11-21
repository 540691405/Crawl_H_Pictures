import os
import requests
import multiprocessing as mp
#上面为别人包
#此为我的包
import ioUtil
import AnalysisHtml





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

    DownLoadFromType(session,Type_url,type_string)
    #从正确的分类下载

#从一个已经选择的分类下载
def DownLoadFromType(session,type_url,type_string):
    #参数为 会话session  类型的url  类型的string

    # pool=mp.Pool()
    # 加入多进程下载


    #若此分类不存在，创建此分类文件夹
    type_path='%s/%s' %(save_path,type_string)
    if(not os.path.exists(type_path)):
        os.makedirs(type_path)

    #先分析分类网页
    imgset_urls_dic=AnalysisHtml.GetSetUrlsFromTypeUrl(session,type_url,source_url)
    # 得到图集的url-dic


    #####################################
    tempcount = 1
    i = 0
    #计数器，控制图集数，测试用
    ######################################


    #对所有图集的url信息dic
    for imgset_name,imgset_url in imgset_urls_dic.items():
        #key： imgsetname  value url
        # 得到图集名字,url对

        ioUtil.DownloadImgSet(session, imgset_url, type_path, imgset_name)
        # 下载图集

        ####################################
        i = i + 1
        if (i > tempcount):
            return True
        # 计数器，测试用
        #######################################


    return True




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

