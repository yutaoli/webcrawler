import pyquery
import time
import csv
import wc_network


def writeappendcsv(filename, rows):
    with open(filename, 'w', encoding='utf_8_sig', newline='') as csvfile:
        fieldnames = ['jigoumingcheng', 'title', 'price', 'renshu']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def get_products(products, html):
    doc = pyquery.PyQuery(html)
    course_list = doc('div.market-bd ul li.course-card-item--v3').items()

    #file = open("E:/demo_title.txt", "w", encoding="utf8")

    for course in course_list:
        product = {
            'jigoumingcheng': course.find('div.item-line a.line-cell').text(),
            'title': course.find('h4.item-tt a').text(),
            'price': course.find('div.item-line span.item-price').text(),
            'renshu': course.find('div.item-line span.item-user').text()
        }
        products.append(product)


products = []
for i in range(1, 35):
    url = "https://ke.qq.com/course/list?price_min=1&page="+str(i)
    html = wc_network.get_one_page(url)
    print(url)
    print("\n")
    time.sleep(1)
    get_products(products, html)

writeappendcsv("E:/tengxunketang.csv", products)