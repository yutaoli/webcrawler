import os
import sys
import pathlib
import pdfkit
import re
import wc_network
import pyquery
import shutil

def webpage2html(pagenumber, pageurl,htmlname):
    html = wc_network.get_one_page(pageurl)
    if html == None :
        return -1
    
    doc = pyquery.PyQuery(html)

    title = doc('body > div.main.tie > div > div.tieL > div.tieTitle > h1').text()
    title_with_pagenumber = title + str(pagenumber)

    info = str(doc('div.louItme'))# 变成字符串

    out_html="<!DOCTYPE html> \
    <!-- saved from url=(0042)https://tuoshuidu.com/article/65994/1.html --> \
    <html lang=\"en\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"> \
    <head></head> \
    <body><h1>" + title_with_pagenumber + "</h1>" + \
    info + "</body> \
    </html>"
    
    print("out_html=",out_html)

    #将拼接好的html写入文件
    with open(htmlname, 'w', encoding='utf-8') as f:
        f.write(out_html)


def htmls2pdf(dirpath, pdfname):

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }

    #合并到临时文件
    allfilemerge = 'all.html'

    filedir = os.path.join(os.path.abspath('.'), dirpath)

    #文件按创建时间排序
    files = sorted(pathlib.Path(filedir).iterdir(), key=os.path.getctime)

    #print("files=",files)
    #sys.exit()

    desc_file = os.path.join(os.path.abspath('.'), allfilemerge)
    
    for i in files:
        # 遍历单个文件，读取行数
        #print(i)

        res = re.match(".*html$", str(i))
        print("res=",res)

        if res == None:
            continue

        cc = os.path.join(os.path.abspath('.'), dirpath, i)

        #print("test")
        print(cc)

        with open(cc, 'r', encoding='utf-8') as f:
            with open(desc_file, 'a+', encoding='utf-8') as new:
                new.write(f.read())

    #最后调用的是wkhtmltopdf，需要安装wkhtmltopdf软件，否则会报错OSError: No wkhtmltopdf executable found: "b''"
    config = pdfkit.configuration(wkhtmltopdf=r"D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    try:
        pdf = pdfkit.from_file(desc_file, pdfname, options=options,configuration=config)
    except:
        print("except occur!!!")

    if(os.path.exists(desc_file)):
        os.remove(desc_file)
        print("delfile:",desc_file)
    else:
        print("not exist:",desc_file)


#创建目录
dirname = "htmls"
if not os.path.exists(dirname):
    os.makedirs(dirname)

#下载html文件
# 那些事情：革命年代其实很精彩
#total_page = 105
#prefix_url = "https://tuoshuidu.com/article/65994/"


total_page = 54
prefix_url = "https://tuoshuidu.com/article/89130/"
for num in range(1, total_page + 1):
    #https://tuoshuidu.com/article/65994/1.html
    
    htmlname = str(num)+".html"
    url= prefix_url + htmlname
    htmlabspath = os.path.join(os.path.abspath('.'), dirname, htmlname)

    print("htmlname=",htmlname)
    print("url=",url)
    print("htmlabspath=",htmlabspath)

    webpage2html(num, url,htmlabspath)

#多个html文件转换成一个pdf
htmls2pdf(dirname, "out.pdf")

#处理完后的工作
shutil.rmtree(dirname)