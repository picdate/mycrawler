import requests
import re
from sqlconnector import MysqlConnector
from bean import Game
from bs4 import BeautifulSoup
import time

def getDownloadUrl(str):
    pattern=re.compile('(https:\/\/pan\.baidu\.com\/s\/)[\w]+(\?)(pwd=)[\w]{4}')
    search_res=pattern.search(str)
    return search_res

def getfourURL(str):
    pattern=re.compile('(https:\/\/fourpetal\.com\/)[\d]+(.html)')
    search_res=pattern.search(str)
    return search_res


index=6
while index<=10:
    myproxies={'http':requests.get(url="http://localhost:5555/random").content.decode()}
    print("开始爬取第"+index.__str__()+"页内容")
    x520_url="https://xxxxx520.com/switchyouxi/page/"+index.__str__()
    pro_headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
    html= requests.get(url=x520_url,headers=pro_headers,proxies=myproxies)
    soup=BeautifulSoup(html.text,"lxml")
    res=soup.select("div .placeholder")

    for item in res:
        tag_a=item.find("a")
        href=tag_a.attrs['href']
        inner_html=requests.get(url=href,headers=pro_headers,proxies=myproxies)
        inner_page=BeautifulSoup(inner_html.text,"lxml")
        """获取头部"""
        header=inner_page.find_all("header",class_="entry-header")[0]
        """获取描述体"""
        descript_body=inner_page.find_all("div",class_="entry-wrapper")[0]
        """获取名称，平台,语言属性"""
        game_name=header.contents[3].text
        categroy=header.contents[1].contents[3]
        platform="无"
        language="无"
        flag=0;
        for i in categroy.contents:
            if i!="\n" and i!="":
                if flag==0:
                    platform=i.text.strip()
                    flag=1
                    continue
                if flag==1:
                    language=i.text.strip()
                    break

                

        """获取描述"""
        descript=descript_body.contents[3].text

        """获取下载连接属性"""
        pattern = re.compile('/[0-9]+')
        number=pattern.search(href)
        r_number=number.group()[1:]
        download_pag_url="https://xxxxx520.com/go/?post_id="+r_number
        """可能是script结构，也有可能直接是百度链接"""
        download_pag_script=requests.get(download_pag_url,headers=pro_headers,proxies=myproxies).content.decode()
        
        search_res=getDownloadUrl(download_pag_script)
        if(search_res!=None):
            download=search_res.group()
        else :
            search_res=getfourURL(download_pag_script)
            """没有链接"""
            if(search_res==None):
                continue
            download_url=search_res.group()
            """script结构处理"""
            download_html=requests.get(download_url,headers=pro_headers,proxies=myproxies)
            download_pag_soup=BeautifulSoup(download_html.text,"lxml")
            download=download_pag_soup.find("div",class_="entry-content u-text-format u-clearfix").text
        
        

        temp_game=Game(name=game_name,language=language,description=descript,download=download,platefrom=platform)
        insert_sql="INSERT INTO game  (game.`name`,game.`language`,description,download,plateform) SELECT  '"+game_name+"','"+language+"','"+descript+"','"+download+"','"+platform+"' FROM DUAL   WHERE NOT EXISTS (SELECT * FROM game WHERE game.`name`='"+game_name+"') "
        connector=MysqlConnector()
        connector.insert(sql=insert_sql)
        print(game_name+"---------插入成功")
    print("第"+index.__str__()+"页内容爬取结束")
    index=index+1

