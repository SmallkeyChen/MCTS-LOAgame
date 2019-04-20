import pygame, sys, time  # 声明 导入需要的模块

from pygame.locals import *


pygame.init()  # 初始化pygame

DISPLAYSURF = pygame.display.set_mode((400, 600))  # 设置窗口的大小，单位为像素

pygame.display.set_caption('Clock')  # 设置窗口的标题

# 定义几个颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

DISPLAYSURF.fill(WHITE)  # 设置背景

# 初始化计时器
counts = 0

# 自定义计时事件
COUNT = pygame.USEREVENT + 1

# 每隔1秒发送一次自定义事件
pygame.time.set_timer(COUNT, 1000)


# 抽象出一个方法用来绘制Text在屏幕上
def showText(fontObj, text, x, y):

    textSurfaceObj = fontObj.render(text, True, GREEN, WHITE)  # 配置要显示的文字

    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect

    textRectObj.center = (x, y)  # 设置显示对象的坐标

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)  # 绘制字体


fontbigObj = pygame.font.SysFont("arial", 48)  # 通过字体文件获得字体对象

fontminObj = pygame.font.SysFont("arial", 24)  # 通过字体文件获得字体对象

showText(fontminObj, "Time:", 100, 100)

showText(fontminObj, "Count:", 100, 300)

while True:  # 程序主循环

    now = time.ctime()  # 获得系统当前时间

    clock = now[11:19]  # 格式化形式

    showText(fontbigObj, clock, 200, 150)

    for event in pygame.event.get():  # 获取事件

        if event.type == QUIT:  # 判断事件是否为退出事件

            pygame.quit()  # 退出pygame

            sys.exit()  # 退出系统

        if event.type == COUNT:  # 判断事件是否为计时事件

            counts = counts + 1

            countstext = str(counts)

            showText(fontbigObj, countstext, 200, 350)

    pygame.display.update()  # 绘制屏幕内容
