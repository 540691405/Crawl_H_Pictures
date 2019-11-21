import os
import AnalysisHtml

#说不定可以用异步
#下载一个图片的方法
def DownloadImg(session,img_url,path,img_name):
    # 从一个图片的url下载一张图片，传入session，图片的url ，存入path,图片名
    img_response = session.get(img_url, stream=True)
    #用已有session，得到图片，stream
    with open('%s/%s' % (path, img_name), 'wb') as f:
        for chunk in img_response.iter_content(chunk_size=128):
            f.write(chunk)
            # 写入图片

    return True



#下载一个图集的方法
#传入session ,图集url ， 图集类型的下载位置，图集名字
def DownloadImgSet(session,imgset_url,type_path,imgset_name):
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

        # 图片的url list下载图片,下载到当前图集里:
        for img_url in img_urls:
            img_name = img_url.split('/')[-1]
            # 创建图片名
            DownloadImg(session, img_url, imgset_path, img_name)
            # 下载到当前图集里:
        print('Successfully Saved  Img Set: %s !!' % imgset_name)

        return True


    #图集有了,就：
    else:
        print("图集[%s]已存在" %imgset_name)
        return False
