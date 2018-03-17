# coding=utf-8
import requests
import time
from pprint import pprint
import json
import codecs

# channel = ['100', '1192652582', '179223212', '1525483516','1105405272']
# start_recoid = ['14291986937536083316', '10292047363311365517', '8587147962016366464',
#                 '6987906878966145471','14764850434414846457']
channel = ['472933935']
start_recoid = ['3299662652828336702']


def request_url(channel_id, recoid):
    lesson_url_template = "http://zzd.sm.cn/iflow/api/v1/channel/{}?uc_param_str=dnnivebichfrmintcpgieiwidsudpf" \
                          "&zzd_from=webapp&app=webapp&is_h5=1&client_os=webapp&sn=968251737726511769&method=his" \
                          "&ftime=1521185570000&count=20&summary=0&bid=999&m_ch=000&recoid={}&_" \
                          "=1521207648621 "
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

    ff = codecs.open('E:\OneDrive - smail.nju.edu.cn\learning\云计算比赛/uc_title.txt', 'a', 'utf-8')
    repeat = 0
    for i, ch in enumerate(channel):
        recoid = start_recoid[i]
        s = build_session()
        while True:
            start_url = request_url(ch, recoid)
            resp = s.get(start_url)

            # print(resp.status_code)
            if resp.status_code >= 400:
                print("可能被禁啦")
                break

            resp_content = json.loads(resp.content.decode("utf-8"))

            # pprint(resp_content)
            if not resp_content['data']['articles']:
                print('结束啦')
                pprint(resp_content)
                break
            for _, aritcle in resp_content['data']['articles'].items():
                # pprint(aritcle)

                recoid = aritcle['recoid']
                title = aritcle['title']
                if title not in title_list:
                    title_list.append(title)
                    repeat = 0
                else:
                    repeat += 1
            if repeat > 5000:
                print('repeat')
                repeat = 0
                break
            if len(title_list) > 300000:
                ff.write('\n'.join(title_list))
                ff.write('\n')
                title_list = []
                break
    ff.write('\n'.join(title_list))


if __name__ == '__main__':
    crawl()
