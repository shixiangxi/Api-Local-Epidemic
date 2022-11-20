import requests
import re
from datetime import date
import pygame
import sys
import time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500,250))
icon = pygame.image.load('./img/image1.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("疫情数据v1.0  by:dwylyz")

if __name__ == '__main__':
    while True:
        ans=0
        bg_color=(255,255,255)
        screen.fill(bg_color)

        text = pygame.font.SysFont('Microsoft YaHei UI',25,bold=True)#文字字体
        title1 = pygame.font.SysFont('Microsoft YaHei UI',45,bold=True)#标题字体
        number = pygame.font.SysFont('Microsoft YaHei UI',70,bold=True)#数字字体

        today=date.today()
        data= '20'+today.__format__('%y'+"-"+'%m'+"-"+'%d')#get今日日期
        city_id ="370100"#各省市/区地区区号，详见city文件
        limit="1"#该页面显示几日信息
        url = f'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?adCode={city_id}&limit={limit}'
        #tx的结果更新不及时，可能会导致错误
        #下面提供了两个baidu的接口
        #place=山东-济南 #严格按照省-市的格式，不然百度不认
        #https://voice.baidu.com/newpneumonia/getv2?from=mola-virus&stage=publish&target=trendCity&area={place}&callback=&qq-pf-to=pcqq.c2c
        #place2=山东济南新型肺炎最新动态 #后面的"新型肺炎最新动态"不要删
        #https://opendata.baidu.com/data/inner?resource_id=5653&query={place2}&dsp=iphone&tn=wisexmlnew&alr=1&is_opendata=1&cb=&qq-pf-to=pcqq.c2c
        #baidu的第二个需要转码
        #并且更改下面findall的关键字
        
        headers = {'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'}
        response = requests.get(url, headers)#拉取页面文件
        #获取列表
        confirm_add_list = re.findall('"confirm_add":"(.*?)"', response.text)  
        yes_wzz_add_list = re.findall('"yes_wzz_add":(.*?),', response.text)

        title = title1.render(data, True, (0, 0, 0))#标题
        screen.blit(title, (115, 0))

        x1=100
        x2=200
        da=43

        text1 = text.render("新增确诊:", True, (0, 0, 0))#文字1
        screen.blit(text1, (10, x1))
        #获取列表最后一个数据
        number1 = number.render(confirm_add_list[-1], True, (255, 1, 1))#数字1
        screen.blit(number1, (115, x1-da))       
        
        text2 = text.render("新增无症状:", True, (0, 0, 0))#文字2
        screen.blit(text2, (10, x2))
        #获取列表最后一个数据
        number2 = number.render(yes_wzz_add_list[-1], True, (255, 1, 1))#数字2
        screen.blit(number2, (140, x2-da))

        while True:     
            tic = time.perf_counter()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
            toc = time.perf_counter()
            ans=round(ans+toc-tic,2) #计时3h更新一次数据
            if ans>=10800:
                break
        
    