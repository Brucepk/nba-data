from pyquery import PyQuery as pq
import requests
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import time

"""
本文原创：pk哥，公众号：Python知识圈（id：PythonCircle），如需转载，请关注公众号，联系pk哥授权。
「Python知识圈」公众号定时分享大量有趣有料的 Python 爬虫和实战项目，值得你的关注，关注后回复1024有惊喜哦！
"""

def parse_html(url):
    # 用的免费代理 ip，如果被封的，在http://www.xicidaili.com/换一个
    proxy_addr = {'http': '121.69.37.6:9797'}
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    reponse = requests.get(url, headers=headers, proxies=proxy_addr)
    if reponse.status_code == 200:
        html = reponse.text
        return html


def get_info(html):                 # 爬取球员比赛数据信息
    doc = pq(html)
    data_items = doc.find("#div_per_game #per_game tbody tr").items()
    season_list, minutes_list, trb_list, ast_list, stl_list, blk_list, \
    tov_list, pts_list = [], [], [], [], [], [], [], []
    for itme in data_items:
        season = itme.find("th[data-stat='season'] a").text()           # 赛季
        minutes_played_per_game = itme.find("td[data-stat='mp_per_g']").text()    # 上场时间
        trb_per_g = itme.find("td[data-stat='trb_per_g']").text()    # 篮板数
        ast_per_g = itme.find("td[data-stat='ast_per_g']").text()    # 助攻
        stl_per_g = itme.find("td[data-stat='stl_per_g']").text()    # 抢断
        blk_per_g = itme.find("td[data-stat='blk_per_g']").text()    # 盖帽
        tov_per_g = itme.find("td[data-stat='tov_per_g']").text()    # 失误
        pts_per_g = itme.find("td[data-stat='pts_per_g']").text()    # 赛季平均得分
        season_list.append(season)
        minutes_list.append(minutes_played_per_game)
        trb_list.append(trb_per_g)
        ast_list.append(ast_per_g)
        stl_list.append(stl_per_g)
        blk_list.append(blk_per_g)
        tov_list.append(tov_per_g)
        pts_list.append(pts_per_g)
    return season_list, minutes_list, trb_list, ast_list, stl_list, blk_list, tov_list, pts_list


"""
本文原创：pk哥，公众号：Python知识圈（id：PythonCircle），如需转载，请关注公众号，联系pk哥授权。
「Python知识圈」公众号定时分享大量有趣有料的 Python 爬虫和实战项目，值得你的关注，关注后回复1024有惊喜哦！
"""


def draw(html):
    season_list, minutes_list, trb_list, ast_list, stl_list, blk_list, tov_list, pts_list = get_info(html)
    # 指定默认字体
    plt.rcParams['font.family'] = 'Arial Unicode MS'
    num = len(season_list)
    ind = np.arange(0, num*4, 4)  # the x locations for the groups
    width = 0.6  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind + width, tuple(list(map(float, minutes_list))), width, color='SkyBlue', align='center', label='上场时间')
    rects2 = ax.bar(ind + 2 * width, tuple(list(map(float, trb_list))), width, color='red', align='center', label='篮板数')
    rects3 = ax.bar(ind + 3 * width, tuple(list(map(float, ast_list))), width, color='Cyan', align='center', label='助攻')
    rects4 = ax.bar(ind + 4 * width, tuple(list(map(float, stl_list))), width, color='Magenta', align='center', label='抢断')
    rects5 = ax.bar(ind + 5 * width, tuple(list(map(float, blk_list))), width, color='Purple', align='center', label='盖帽')
    rects6 = ax.bar(ind + 6 * width, tuple(list(map(float, tov_list))), width, color='Green', align='center', label='失误')
    rects7 = ax.bar(ind + 7 * width, tuple(list(map(float, pts_list))), width, color='Yellow', align='center', label='平均得分')
    title = url.split('/')[-1].split('.')[0].strip('01')[0:-2]
    plt.title('%s赛季数据统计 @Python知识圈 制作' % title, fontsize=20)
    plt.xticks(ind, tuple(season_list), size='small', rotation=30)   # x 轴字体和倾斜角度
    ax.legend(loc='upper left')
    plt.show()      # 显示图片
    fig.savefig(r'D:\图片\%s.png' % title)   # 保存图片到本地


if __name__ == '__main__':
    # 伦纳德  杜兰特  欧文 詹姆斯 肯巴沃克 汤普森 克里斯·保罗 哈登 斯蒂芬·库里 西蒙斯 利拉德 托拜亚斯-哈里斯 米德尔顿 波尔津吉斯 拉塞尔·威斯布鲁克 扬尼斯·安特托昆博  乔尔·恩比德
    urls = [
            'https://www.basketball-reference.com/players/l/leonaka01.html',
            'https://www.basketball-reference.com/players/d/duranke01.html',
            'https://www.basketball-reference.com/players/i/irvinky01.html',
            'https://www.basketball-reference.com/players/j/jamesle01.html',
            'https://www.basketball-reference.com/players/w/walkeke02.html',
            'https://www.basketball-reference.com/players/t/thompkl01.html',
            'https://www.basketball-reference.com/players/p/paulch01.html',
            'https://www.basketball-reference.com/players/h/hardeja01.html',
            'https://www.basketball-reference.com/players/c/curryst01.html',
            'https://www.basketball-reference.com/players/s/simmobe01.html',
            'https://www.basketball-reference.com/players/l/lillada01.html',
            'https://www.basketball-reference.com/players/h/harrito02.html',
            'https://www.basketball-reference.com/players/m/middlkh01.html',
            'https://www.basketball-reference.com/players/p/porzikr01.html',
            'https://www.basketball-reference.com/players/w/westbru01.html',
            'https://www.basketball-reference.com/players/a/antetgi01.html',
            'https://www.basketball-reference.com/players/e/embiijo01.html'
    ]
    for url in urls:
        html = parse_html(url)
        draw(html)
        time.sleep(5)

        """
        查看更多有趣的项目请关注公众号「Python知识圈」
        """