import jieba.analyse
import jieba
import pandas as pd
import numpy as np
import math
content = '''原标题：日媒：樱花主力中场清武弘嗣训练中受伤，或将缺战恒大\n虎扑2月18日讯 
据日本媒体《每日新闻》报道，日本大阪樱花队主力中场清武弘嗣在今天的训练中右脚受伤，他有可能缺席21号和广州恒大淘宝队的比赛。\n
日媒报道称，日本大阪樱花队主力中场清武弘嗣在今天的训练中右脚受伤并被送到了医院。虽然大阪樱花官方并未公布伤情报告，但是据球队相关官员介绍称，“感觉他不是很快就能回到赛场”，他有可能缺席21
号与恒大的亚冠联赛小组赛第二轮，甚至可能缺席25号的J联赛第一轮比赛。\n现年28岁的清武弘嗣曾在德甲和西甲踢球，上赛季加盟大阪樱花效力，不过因伤只代表大阪樱花出场26次，打入6球，贡献4
助攻。在不久前的日本超级杯中，他还打入一球，帮助球队夺冠。\n[来源:每日新闻]\n@hupu.com | 更多体育新闻请访问虎扑新闻 '''
tags = jieba.analyse.extract_tags(content, topK=5)
seg_ls = jieba.cut(content)
print(",".join(tags))
print("/ ".join(seg_ls))
