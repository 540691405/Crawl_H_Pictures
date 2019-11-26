import os
import requests
import multiprocessing as mp
import aiohttp
import asyncio
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
        return ''
    return Type_url


#从一个已经选择的分类下载,用requests
def DownLoadFromType(type_url:str,type_string:str):
    #参数为 类型的url  类型的string

    #若此分类不存在，创建此分类文件夹
    type_path='%s/%s' %(save_path,type_string)
    if(not os.path.exists(type_path)):
        os.makedirs(type_path)

    session = requests.session()
    #requests 会话
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

    # #进程池
    # with mp.Pool(processes=4) as pool:
    #
    #     print("多进程地下载图集")
    #     for imgset_name, imgset_url in imgset_urls_dic.items():
    #     # 得到图集名字,url对
    #         pool.apply_async(
    #         ioUtil.DownloadImgSet,
    #         args=(session, imgset_url, type_path, imgset_name,)
    #         )
    #     # 下载图集
    #     pool.close()
    #     pool.join()
    #     #等待所用进程完成

    return True

#从一个已经选择的分类下载,用aiohttp
async def DownLoadFromType_async(loop,type_url:str,type_string:str):
    #参数为 loop asyncio的envnt_loop 下载方法:way  类型的url  类型的string

    #若此分类不存在，创建此分类文件夹
    type_path='%s/%s' %(save_path,type_string)
    if(not os.path.exists(type_path)):
        os.makedirs(type_path)

    async with aiohttp.ClientSession() as session:
    # 创建 aiohttp 的 clien session

        #先分析分类网页
        # finished= await asyncio.wait([AnalysisHtml.GetSetUrlsFromTypeUrl_async(session,type_url,source_url)])
        # # 异步执行tasks
        # imgset_urls_dic = [r.result() for r in finished][0]
        imgset_urls_dic = await AnalysisHtml.GetSetUrlsFromTypeUrl_async(session, type_url, source_url)


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

            await ioUtil.DownloadImgSet_async(session,loop,imgset_url, type_path, imgset_name)
            # 下载图集
            ####################################
            i = i + 1
            if (i > tempcount):
                return True
            # 计数器，测试用
            #######################################


    # #进程池
    # with mp.Pool(processes=4) as pool:
    #
    #     print("多进程地下载图集")
    #     for imgset_name, imgset_url in imgset_urls_dic.items():
    #     # 得到图集名字,url对
    #         pool.apply_async(
    #         ioUtil.DownloadImgSet,
    #         args=(session, imgset_url, type_path, imgset_name,)
    #         )
    #     # 下载图集
    #     pool.close()
    #     pool.join()
    #     #等待所用进程完成


    return True





if __name__ == '__main__':

    flag=True
    #是否退出
    while(flag):
        print('''
选择下载方式：
    0:多进程
    1:异步
    ''')
        way=input()
        #way为下载方式
        if(way=='0' or way=='1'):
            flag=False
        else:
            print("请输入数字选择")

    flag=True
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
            Type_url=selectd_photo_type(type_string=type_string)
            #选择类型
            print('正在从[' + type_string + ']下载中!')

            if(way=='0'):
                #0：用多进程
                DownLoadFromType(Type_url, type_string)
                # 从正确的分类下载

            elif(way=='1'):
                #1:用异步
                loop = asyncio.get_event_loop()
                loop.run_until_complete(DownLoadFromType_async(loop,Type_url,type_string))
                loop.close()


