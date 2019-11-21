from bs4 import BeautifulSoup

#传入类型url,原网址url ，
# 解析出所有单个图集名字和url,返回单个图集名字和url组成的dic
def GetSetUrlsFromTypeUrl(session,type_url,source_url):
    #

    imgset_urls_dic = {}
    # 初始化图集信息的dic

    type_response = session.get(type_url)
    # 进入类型网页
    type_html = type_response.text
    # 得到类型的网页html

    type_soup = BeautifulSoup(type_html, 'lxml')
    # 用Beautifulsoup解析
    imgset_url_tag_list = type_soup.find('ul', {'class': 'textList'}).find_all('a')
    # 得到图集的url-list

    # 从中选择textLIst为url-list所在，其中a tag 装了href

    for a_tag in imgset_url_tag_list:
        imgset_name=a_tag.get_text()[5:]
        #从atag解析出去了日期的名字部分
        imgset_url = source_url + a_tag['href']
        #得到url
        imgset_urls_dic[imgset_name]=imgset_url
        #放入图集信息dic
        #key： imgsetname  value url

    return imgset_urls_dic


#传入一个图集的url，解析出所有单个图片的url,返回由他们组成的list
def GetImgUrlsFromSetUrl(session,imgset_url):
    #参数：已有session, 图集的url：img_set_url,图集的名称: imgset_name
    #返回 img_urls list
    img_urls=[]
    #初始化图片的url的list
    imgset_response = session.get(imgset_url)
    # 得到一个图片集的response
    imgset_html = imgset_response.text
    # 得到图片集的html
    imgset_soup = BeautifulSoup(imgset_html, 'lxml')
    # 用BeautifulSoup处理图片集html
    img_tags = imgset_soup.find_all('img')
    #得到所有的Img tags
    # 一个图片在一个img tag里的src

    #创建图片的url list
    for img_tag in img_tags:
        img_url = img_tag['src']
        # 得到单个图片url
        img_urls.append(img_url)
        #将这个图片的url加入list

    # imgset_name = imgset_url.split('/')[-1]
    # #暂时的图集名字

    return img_urls



