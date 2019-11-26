import os
import AnalysisHtml
import multiprocessing as mp
import aiohttp
import asyncio
import requests




#说不定可以用异步
#下载一个图片的方法
def DownloadImg(session:requests.sessions.Session,img_url:str,path:str,img_name:str):
    #在此处理响应。
    img_response = session.get(img_url, stream=True)
    #用已有session，得到图片，stream
    with open('%s/%s' % (path, img_name), 'wb') as f:
        for chunk in img_response.iter_content(chunk_size=128):
            f.write(chunk)
            # 写入图片
    return True

#多进程下载一个图集的方法
#传入session ,图集url ， 图集类型的下载位置，图集名字
def DownloadImgSet(session:requests.sessions.Session,imgset_url:str,type_path:str,imgset_name:str):
    #传入图集的url ，下载里面所有图片
    #参数： session 会话 , imgset_url 图集的url,
    # type_path 图集的类型的下载位置，imgset_name 图集的名字

    imgset_path = '%s/%s/' %(type_path, imgset_name)
    # 图集存放位置的path

    #若此图集没有,就下载
    if (not os.path.exists(imgset_path)):

        os.makedirs(imgset_path, exist_ok=True)
        # 创建图集存放图片的路径
        print('Downloading from %s' % imgset_name)

        # 先对图集的url分析,得到由单个图片的url组成的list
        img_urls = AnalysisHtml.GetImgUrlsFromSetUrl(session, imgset_url)

        # # 图片的url list下载图片,下载到当前图集里:
        # for img_url in img_urls:
        #     img_name = img_url.split('/')[-1]
        #     # 创建图片名
        #     DownloadImg(session, img_url, imgset_path, img_name)
        #     # 下载到当前图集里:

        # 进程池
        with mp.Pool() as pool:

            print("MultiProcessing Downloading Img!")
            for img_url in img_urls:
                #得到图集名字,url对
                img_name = img_url.split('/')[-1]
                #创建图片名
                pool.apply_async(
                    DownloadImg,
                    args=(session, img_url, imgset_path,img_name,)
                )
            # 下载图集
            pool.close()
            pool.join()
            # 等待所用进程完成

        print('Successfully Saved  Img Set: %s !!' % imgset_name)

        return True

    #图集有了,就：
    else:
        print("图集[%s]已存在" %imgset_name)
        return False


#异步下载一张图片的方法
async def DownloadImg_async(session:aiohttp.client.ClientSession,img_url:str,path:str,img_name:str):
    async with session.get(img_url) as img_response:
        #aiohttp下打开网页
        await img_response.content.read(10)
        #aiohttp 的流读取
        with open('%s/%s' % (path, img_name),'wb') as f:
            #写入图片
            while True:
                chunk = await img_response.content.read(chunk_size=128)
                #对aiohttp的流文件下载
                if not chunk:
                    break
                f.write(chunk)

async def DownloadImgSet_async(session:aiohttp.client.ClientSession,loop,imgset_url:str,type_path:str,imgset_name:str):
    #传入图集的url ，下载里面所有图片
    #参数： session 会话 , loop  asyncio envent loop
    # imgset_url 图集的url,
    # type_path 图集的类型的下载位置，imgset_name 图集的名字

    imgset_path = '%s/%s/' %(type_path, imgset_name)
    # 图集存放位置的path

    #若此图集没有,就下载
    if (not os.path.exists(imgset_path)):

        os.makedirs(imgset_path, exist_ok=True)
        # 创建图集存放图片的路径
        print('Async Downloading from %s' % imgset_name)

        # 先对图集的url分析,得到由单个图片的url组成的list
        img_urls = await AnalysisHtml.GetImgUrlsFromSetUrl_async(session, imgset_url)
        # 图片的url list下载图片,下载到当前图集里:

        tasks=[loop.create_task(DownloadImg_async(session, img_url, imgset_path, img_url.split('/')[-1])) for img_url in img_urls]
        # 创建异步任务list ，异步第分配给任务进程
        await asyncio.wait(tasks)

        print('Successfully Saved  Img Set: %s !!' % imgset_name)

        return True



async def main(loop):

    async with aiohttp.ClientSession() as session:
    # 创建 aiohttp 的 clien session
        loop.run_until_complete(asyncio.wait(DownloadImgSet(session, imgset_url, type_path, imgset_name)))

    await session.close()


if __name__ == '__main__':
    type_path = 'D:/爬取的图片/欧美色图'
    imgset_url = 'http://mmee94.com/fdft_826216.html'
    imgset_name = '不绝美不收藏，御姐的笑容让人陶醉 [20P]'


    loop=asyncio.get_event_loop()
    loop.run_until_complete(DownloadImgSet_async(session,loop,imgset_url, type_path, imgset_name))
    loop.close()
    # session=requests.session()
    # DownloadImgSet(session,'http://mmee94.com/fdft_826216.html','D:/爬取的图片/欧美色图','不绝美不收藏，御姐的笑容让人陶醉 [20P]')
