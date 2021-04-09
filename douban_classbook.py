from lxml import etree
import pyquery
import re
import wc_network
import time
import csv

#推荐队列去重，id是title
uniq_recommand_books={}

def writeappendcsv(filename, rows):
    with open(filename, 'w', encoding='utf_8_sig', newline='') as csvfile:
        '''
 'title':title,
        'author':author,
        'publish_press':publish_press,
        'yizhe':yizhe,
        'publish_time':publish_time,
        'pages':pages,
        'price':price,
        'series':series,
        'series_url':series_url,
        'ISBN':ISBN,
        'score':score,
        'pingjiarenshu':pingjiarenshu,
        'url':url,
        '''
        fieldnames = ['title', 'author', 'publish_press', 'yizhe','publish_time','pages',
        'price','series','series_url','ISBN','score','pingjiarenshu','url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

def get_one_page_and_html_parse_with_xml(pageurl, recommand_books, recommand_pageurls):
    html = wc_network.get_one_page(pageurl)
    doc = etree.HTML(html)

    title = doc.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    try:
        score = doc.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    except:
        score = '-1'
    if score=='  ' :
        score = '-1'

    try:
        pingjiarenshu = doc.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()')[0]
    except:
        pingjiarenshu = '0'

    #更多的数据，因为有的有译者，有的没有译者，导致写死的xpath方法定位错误，这里只选择几个肯定有的并且很重要的字段进行爬取
    book = {
        'title':title,
        'score':score,
        'pingjiarenshu':pingjiarenshu,
        'url':pageurl,
    }
    recommand_books.append(book)
    print(book)

    doc_recommand = pyquery.PyQuery(html)
    down_recommand_books = doc_recommand(
        '#db-rec-section div.content dl').items()

    #file = open("E:/demo_title.txt", "w", encoding="utf8")

    for single_recommand_book in down_recommand_books:
        recommand_book = {
            'title': single_recommand_book.find('dd a').text(),
            'url': single_recommand_book.find('dd a').attr['href'],
        }
        if recommand_book['title'] != '':
            # print(recommand_book)
            recommand_pageurls.append(recommand_book['url'])

#下载成功返回0，否则返回1
def get_one_page_and_html_parse_with_pyquery(pageurl, recommand_books, recommand_pageurls):
    html = wc_network.get_one_page(pageurl)
    doc = pyquery.PyQuery(html)

    # 返回字段定义
    title=''
    author = ''
    publish_press=''
    yizhe='' #译者
    publish_time=''
    pages = ''
    price = ''
    series = '' #丛书
    series_url = '' #丛书链接
    ISBN = ''
    score = '' #评分
    pingjiarenshu = '' #评价人数
    url = ''

    #title = doc('head > title').text().replace(' (豆瓣)','')
    title = doc('head > title').text()
    title = re.sub('\(豆瓣\)','',title)

    info = str(doc('#info'))# 变成字符串
    book_info_items = info.replace('\n','').split('<br/>')
    print('book_info_items=',book_info_items,'\n')

    for book_info_item  in book_info_items:
        book_info_item = book_info_item.strip() #去掉多余的空格

        if '作者' in book_info_item:
            authors = re.findall('<a .*?>(.*)</a>', book_info_item)

            i = 0
            for a_author in authors:
                if i != 0:
                    author = author + ','
                
                a_author = re.sub('<a .*?>','',a_author)
                a_author = re.sub('</a>','',a_author)
                author = author + a_author.strip()
                i = i + 1
        elif '出版社' in book_info_item:
            publish_press = re.sub('<span class.*?>(.*?)</span>','',book_info_item)
        elif '译者' in book_info_item:
            i = 0
            pattern = re.compile('<a class.*?>(.*?)</a>')
            search_group = re.findall(pattern, book_info_item) #需要遍历
            for search_group_i in search_group:
                if i != 0:
                    yizhe = yizhe+','
                yizhe_i = re.sub('<a class.*?>','',search_group_i)
                yizhe_i = re.sub('</a>','',yizhe_i)
                yizhe = yizhe + yizhe_i
                i = i + 1             

        elif '出版年' in book_info_item:
            publish_time = re.sub('<span class.*?>(.*?)</span>','',book_info_item)
        elif '页数' in book_info_item:
            pages = re.sub('<span class.*?>(.*?)</span>','',book_info_item)
        elif '定价' in book_info_item:
            price = re.sub('<span class.*?>(.*?)</span>','',book_info_item)
        elif '丛书' in book_info_item:
            match_gorup = re.search('<a href=\".*?\">(.*?)</a>',book_info_item)
            #print('丛书=',book_info_item,'match_group=',match_gorup)
            if match_gorup :
                series = match_gorup.group()
                #print('series=',series)
                series = re.sub('<a href=\".*?\">','', series)
                series = re.sub('</a>','', series)

                match_url_group = re.search('<a href=\".*?\">',book_info_item)
                if match_url_group :
                    series_url = match_url_group.group()
                    series_url = re.sub('<a href=\"','', series_url)
                    series_url = re.sub('\">','', series_url)
        elif 'ISBN' in book_info_item:
            ISBN = re.sub('<span class.*?>(.*?)</span>','',book_info_item)

    score = doc('#interest_sectl > div > div.rating_self.clearfix > strong').text()
    pingjiarenshu = doc('#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span').text()
    url = pageurl

    book={
        'title':title,
        'author':author,
        'publish_press':publish_press,
        'yizhe':yizhe,
        'publish_time':publish_time,
        'pages':pages,
        'price':price,
        'series':series,
        'series_url':series_url,
        'ISBN':ISBN,
        'score':score,
        'pingjiarenshu':pingjiarenshu,
        'url':url,
    }
    print(book)

    recommand_books.append(book)

    doc_recommand = pyquery.PyQuery(html)
    down_recommand_books = doc_recommand(
        '#db-rec-section div.content dl').items()

    #file = open("E:/demo_title.txt", "w", encoding="utf8")

    for single_recommand_book in down_recommand_books:
        recommand_book = {
            'title': single_recommand_book.find('dd a').text(),
            'url': single_recommand_book.find('dd a').attr['href'],
        }
        
        if recommand_book['title'] == '':
            continue

        # uniq_recommand_books去重，提高效率，这里有误杀的可能，部分好书，被过滤了，也只是少了几本同名书，但能保证筛选出来的书都不重复
        if recommand_book['title'] in uniq_recommand_books.keys():
            #print('already in uniq_recommand_books,title=', recommand_book['title'])
            continue

        uniq_recommand_books[recommand_book['title']]=1
        
        recommand_pageurls.append(recommand_book['url'])
    return 0

def get_recommand_books(recommand_books, start_pageurl, book_num):
    recommand_pageurls = []
    recommand_pageurls.append(start_pageurl)
    recommand_pageurl_index = 0
    get_book_num = 0
    while get_book_num < book_num and recommand_pageurl_index < len(recommand_pageurls):
        time.sleep(1)

        pageurl = recommand_pageurls[recommand_pageurl_index]
        print("yutaoli debug:recommand_pageurl_index=",
              recommand_pageurl_index, ",pageurl=", pageurl)

        page_recommand_books = []
        page_recommand_pageurls = []
        res = get_one_page_and_html_parse_with_pyquery(pageurl, page_recommand_books,
                   page_recommand_pageurls)  # parse
        if res == 0:
            recommand_books.extend(page_recommand_books)
            recommand_pageurls.extend(page_recommand_pageurls)
            get_book_num = get_book_num + 1
        
        recommand_pageurl_index = recommand_pageurl_index+1

###main###
recommand_books = []
start_pageurl = 'https://book.douban.com/subject/34845099/'
get_recommand_books(recommand_books, start_pageurl, 1000)

# display
#print(recommand_books)
writeappendcsv('./douban_classbook.csv', recommand_books)
