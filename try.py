# -*- coding: UTF-8 -*-
# 中文注释

import wordcloud
import jieba as jb
import threading as td
import numpy as np
from PIL import Image as ig
# 导入库

#载入背景图片
China=np.array(ig.open(r'map\China.png'))
guangxi = np.array(ig.open(r'map\guangxi.png'))
star = np.array(ig.open(r'map\star.png'))
cloud = np.array(ig.open(r'map\cloud.png'))
princess = np.array(ig.open(r'map\princess.png'))

#背景图片选择模块
def backimage():
    a = int(input('请选择背景轮廓(默认为China)\nChina=1\nguangxi=2\nstar=3\ncloud=4\nprincess=5\n'))
    mask = China
    if a == 1:
        mask = China
    elif a == 2:
        mask = guangxi
    elif a == 3:
        mask = star
    elif a == 4:
        mask = cloud
    elif a == 5:
        mask = princess
    return mask
mask=backimage()


wc = wordcloud.WordCloud(
    background_color='White',
    mask=mask,
    repeat=True,
    font_path='fonts/msyh.ttf',
    height=600,
    width=800,
    colormap='Reds')
text1 = (
    '富强 民主 文明 和谐 自由 平等 公正 法治 爱国 敬业 诚信 友善')
text2 = '五年来，我们坚持加强党的全面领导和党中央集中统一领导，全力推进全面建成小康社会进程，完整、准确、全面贯彻新发展理念，着力推动高质量发展，主动构建新发展格局，蹄疾步稳推进改革，扎实推进全过程人民民主，全面推进依法治国，积极发展社会主义先进文化，突出保障和改善民生，集中力量实施脱贫攻坚战，大力推进生态文明建设，坚决维护国家安全，防范化解重大风险，保持社会大局稳定，大力度推进国防和军队现代化建设，全方位开展中国特色大国外交，全面推进党的建设新的伟大工程。我们隆重庆祝中国共产党成立一百周年、中华人民共和国成立七十周年，制定第三个历史决议，在全党开展党史学习教育，建成中国共产党历史展览馆，号召全党学习和践行伟大建党精神，在新的征程上更加坚定、更加自觉地牢记初心使命、开创美好未来。特别是面对突如其来的新冠肺炎疫情，我们坚持人民至上、生命至上，坚持外防输入、内防反弹，坚持动态清零不动摇，开展抗击疫情人民战争、总体战、阻击战，最大限度保护了人民生命安全和身体健康，统筹疫情防控和经济社会发展取得重大积极成果。面对香港局势动荡变化，我们依照宪法和基本法有效实施对特别行政区的全面管治权，制定实施香港特别行政区维护国家安全法，落实“爱国者治港”原则，香港局势实现由乱到治的重大转折，深入推进粤港澳大湾区建设，支持香港、澳门发展经济、改善民生、保持稳定。面对“台独”势力分裂活动和外部势力干涉台湾事务的严重挑衅，我们坚决开展反分裂、反干涉重大斗争，展示了我们维护国家主权和领土完整、反对“台独”的坚强决心和强大能力，进一步掌握了实现祖国完全统一的战略主动，进一步巩固了国际社会坚持一个中国的格局。面对国际局势急剧变化，特别是面对外部讹诈、遏制、封锁、极限施压，我们坚持国家利益为重、国内政治优先，保持战略定力，发扬斗争精神，展示不畏强权的坚定意志，在斗争中维护国家尊严和核心利益，牢牢掌握了我国发展和安全主动权。五年来，我们党团结带领人民，攻克了许多长期没有解决的难题，办成了许多事关长远的大事要事，推动党和国家事业取得举世瞩目的重大成就。'


result = ' '.join(jb.lcut(text2))

wc.generate(result)

save =int(input('是否保存？(1/0)\n'))
if save == 1:
    name = str(input('请输入文件名\n'))
    wc.to_file(name+'.png')







