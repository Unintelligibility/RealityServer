import jieba.analyse
import jieba
import pandas as pd
import numpy as np
import math
content = '''从网吧到网咖, 中国网吧经历了什么?'''
seg_ls = jieba.cut(content)
print("/ ".join(seg_ls))
