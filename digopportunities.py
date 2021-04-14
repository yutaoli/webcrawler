import jieba
import csv

keywords_frequency={}

#encoding utf-8-sig or gb2312 or gbk
with open('how_1618269673.csv', 'r', encoding='gbk') as csvfile:
    csv_header = csv.reader(csvfile, delimiter=',')
    line = 0
    for row in csv_header:

        if(line == 0):
            line = line + 1
            continue
        
        keyword=row[0]
        #data clean
        if len(keyword) < 2 or len(keyword) > 10:
            continue

        # ref:https://github.com/fxsjy/jieba
        seg_list = jieba.cut(keyword)  # 默认是精确模式
        #print(line, "=", ", ".join(seg_list))

        for keyword_i in seg_list:
            if len(keyword_i) < 2 or len(keyword_i) > 10 or '怎么' in keyword_i :
                continue
            
            if keyword_i not in keywords_frequency:
                keywords_frequency[keyword_i] = 1
            else:
                keywords_frequency[keyword_i] = keywords_frequency[keyword_i] + 1

        line = line + 1


#topN 
top_num = 10
i = 0
res_list = sorted(keywords_frequency.items(), key=lambda x:x[1], reverse=True)
#print(res_list)

for res_list_i in res_list:
    if i >= top_num:
        exit()

    print(res_list_i[0], res_list_i[1])
    i = i + 1