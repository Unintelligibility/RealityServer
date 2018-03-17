# coding=utf-8
import requests
import time
from pprint import pprint
import json
import codecs

channel = ['0']
start_recoid = range(0, 300)


def request_url(channel_id, recoid):
    lesson_url_template = "http://toutiao.jxnews.com.cn/m/ajaxlist.php?from=dj08&cate={}&pagesize=20&page={}&lasttime" \
                          "=1521156979&timestamp=1521270436392 "
    return lesson_url_template.format(channel_id, recoid)


def build_session():
    s = requests.Session()
    return s


def crawl():
    title_list = []
    fr = codecs.open('E:\OneDrive - smail.nju.edu.cn\learning\云计算比赛/uc_title.txt', 'r', 'utf-8')
    for line in fr:
        tt = line.strip()
        if tt not in title_list:
            title_list.append(tt)
    fr.close()

    ff = codecs.open('E:\OneDrive - smail.nju.edu.cn\learning\云计算比赛/uc_title.txt', 'w', 'utf-8')
    repeat = 0
    for ch in channel:
        s = build_session()
        for recoid in start_recoid:
            start_url = request_url(ch, recoid)
            resp = s.get(start_url)

            # print(resp.status_code)
            if resp.status_code >= 400:
                print("可能被禁啦")
                break

            resp_content = json.loads(resp.content.decode("utf-8"))

            # pprint(resp_content)
            if not resp_content:
                print('结束啦')
                pprint(resp_content)
                break
            for aritcle in resp_content:
                # pprint(aritcle)

                title = aritcle['title']
                print(title)
                if title not in title_list:
                    title_list.append(title)
                    repeat = 0
                else:
                    repeat += 1
            if repeat > 200:
                print('repeat')
                repeat = 0
                break
            if len(title_list) > 30000:
                ff.write('\n'.join(title_list))
                ff.write('\n')
                title_list = []
                break

    ff.write('\n'.join(title_list))


if __name__ == '__main__':
    crawl()
