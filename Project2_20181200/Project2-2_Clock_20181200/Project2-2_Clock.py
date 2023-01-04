import pygame
import numpy as np
import datetime

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
PURPLE = (143, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BROWN = (101,67,33)
GRASS = (0, 154, 23)
SKY_BLUE = (0,204, 255)
D_GREEN = (1,50,32)

C_RADIUS = 300
clock_digits = ['1','2','3','4','5','6','7','8','9','10','11','12']
num_loc = np.array([[0, -C_RADIUS+50, 1]])
num_loc = num_loc.T
hour_needle = np.array([[0, 0, 1], [0,-C_RADIUS*0.5,1]])
hour_needle= hour_needle.T
minute_needle = np.array([[0, 0, 1], [0,-C_RADIUS*0.7,1]])
minute_needle= minute_needle.T
sec_needle = np.array([[0, 0, 1], [0, -C_RADIUS+30, 1]])
sec_needle= sec_needle.T


font_name = pygame.font.match_font('Times New Roman')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s,0], [s, c,0],[0,0,1]])
    return R

def Tmat(a,b):
    H = np.eye(3) #identity, 3x3
    H[0,2] = a
    H[1,2] = b
    return H

def drawDigits():
    for i in range(12):
        num_deg = i*30
        H = Tmat(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) @ Rmat(num_deg)
        num_center = H @ num_loc
        num = num_center[0:2,:].T
        #pygame.draw.circle(screen,WHITE,q4[0],2)
        draw_text(screen, clock_digits[i-1], 30, num[0][0], num[0][1])
        print(num)

pygame.init()

pygame.display.set_caption("Clock")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

done = False

while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    now =datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second
    print(h, m, s)

    sec_deg = s*6
    H_sec = Tmat(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) @ Rmat(sec_deg)
    sec = H_sec @ sec_needle
    second = sec[0:2,:].T

    min_deg= m*6 
    H_min = Tmat(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) @ Rmat(min_deg)
    min = H_min @ minute_needle 
    minute = min[0:2,:].T

    hour_deg = h*30 + m/2 #1 hour = 360/12 degrees + 1:59 -> almost 60 degrees, so 60*x = 30, x = 1/2
    # if m != 60:
    #     hour_deg += m/2
    H_hour = Tmat(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) @ Rmat(hour_deg)
    hou = H_hour @ hour_needle
    hour = hou[0:2,:].T     

    screen.fill(BLACK)
    pygame.draw.circle(screen,WHITE,[WINDOW_WIDTH/2, WINDOW_HEIGHT/2],C_RADIUS,6)
    drawDigits()
    pygame.draw.line(screen, ORANGE, second[0],second[1],2)
    pygame.draw.line(screen, BLUE, minute[0],minute[1],4)
    pygame.draw.line(screen, D_GREEN, hour[0],hour[1],5)

    #------clock middle ------
    pygame.draw.circle(screen,WHITE,[WINDOW_WIDTH/2, WINDOW_HEIGHT/2],7)
    pygame.draw.circle(screen,RED,[WINDOW_WIDTH/2, WINDOW_HEIGHT/2],5)
    pygame.draw.circle(screen,WHITE,[WINDOW_WIDTH/2, WINDOW_HEIGHT/2],3)

    pygame.display.flip()
    

    # 화면에 텍스트 표시

    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()
