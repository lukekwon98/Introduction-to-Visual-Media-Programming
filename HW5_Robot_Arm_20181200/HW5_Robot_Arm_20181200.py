import pygame
import numpy as np
import os
#font doesn't have to be in event loop 

# 게임 윈도우 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

# 색 정의
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

current_path = os.path.dirname(__file__)

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

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

bot_sound = pygame.mixer.Sound(os.path.join(current_path, 'robot.wav'))
bot_sound.set_volume(1)


ground = np.array([[1200,750], [1200,700], [0,700], [0,750]])
grass = np.array([[1200,700], [1200,675], [0,675], [0,700]])

PIVOT = [32.5,32.5]

# poly : 4x3 matrix
#poly = np.array([[0,0,1], [100, 0,1], [100, 50,1], [0,50,1]])
poly = np.array([[0,0,1], [200, 0,1], [200, 65,1], [0,65,1]])
trace = np.array([[0,0,1], [200-PIVOT[0], 0,1], [200-PIVOT[0], 65,1], [0,65,1]])
claw = np.array([[10,PIVOT[0]-7.5,1], [60,PIVOT[0]-7.5,1], [60, PIVOT[1]-35,1], [120, PIVOT[1]-35,1], [120,PIVOT[1]-25,1], [72.5, PIVOT[1]-25, 1], [72.5, PIVOT[1]+25,1], [120, PIVOT[1]+25,1], [120, PIVOT[1]+35,1], [60, PIVOT[1]+35,1], [60, PIVOT[0]+7.5,1], [10, PIVOT[0]+7.5,1]])
claw_trace =  np.array([[0,0,1], [200-PIVOT[0]/2, 0,1], [200-PIVOT[0]/2, 65,1], [0,65,1]])
PIVOT = [poly[2][1]/2,poly[2][1]/2]
poly = poly.T # 3x4 matrix
trace = trace.T
claw = claw.T
claw_trace = claw_trace.T
centerOfRotation = np.array([PIVOT[0],PIVOT[1],1])
degree = 0
degree2 = 0
degree3 = 0
degree4 = 0

bot_base = np.array([[0,75,1], [0,0,1],[100,0,1],[100,75,1]])
bot_base = bot_base.T
bot_base_move = Tmat(450, 600) @ bot_base
bot_base_draw = bot_base_move[0:2, :].T

# 게임 종료 전까지 반복
done = False
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    ddeg = 0
    ddeg2 = 0
    ddeg3 = 0
    ddeg4 = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_a]:
        ddeg2 = -1.8
        bot_sound.play()
    if keystate[pygame.K_d]:
        ddeg2 = 1.8
        bot_sound.play()
    if keystate[pygame.K_w]:
        ddeg = -1.6
        bot_sound.play()
    if keystate[pygame.K_s]:
        ddeg = 1.6
        bot_sound.play()
    if keystate[pygame.K_UP]:
        ddeg3 = -1.4
        bot_sound.play()
    if keystate[pygame.K_DOWN]:
        ddeg3 = 1.4
        bot_sound.play()
    if keystate[pygame.K_LEFT]:
        ddeg4 = -1.2
        bot_sound.play()
    if keystate[pygame.K_RIGHT]:
        ddeg4 = 1.2
        bot_sound.play()

    # 윈도우 화면 채우기
    screen.fill(SKY_BLUE)

    # 다각형 그리기
    # We transposed poly, so poly: 3xN, and there are 1 rows
    #pygame.draw.polygon(screen, GREEN, poly[:2].T, 4) # poly[:2] = take away the 1 rows
    
    degree += ddeg
    degree2 += ddeg2
    degree3 += ddeg3
    degree4 += ddeg4


    H = Tmat(470,590)  @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree) @ Tmat(-PIVOT[0],-PIVOT[1])
    p1 = H @ poly
    t1 = H @ trace
    q1 = p1[0:2, :].T
    l1 = t1[0:2, :].T
    corp = H @ centerOfRotation

    H2 = Tmat((l1[1][0]+l1[2][0])/2-PIVOT[0],(l1[1][1]+l1[2][1])/2-PIVOT[1]) @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree2) @ Tmat(-PIVOT[0],-PIVOT[1])
    p2 = H2 @ poly
    t2 = H2 @ trace
    q2 = p2[0:2, :].T
    l2 = t2[0:2, :].T
    corp2 = H2 @ centerOfRotation

    H3 = Tmat((l2[1][0]+l2[2][0])/2-PIVOT[0],(l2[1][1]+l2[2][1])/2-PIVOT[1]) @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree3) @ Tmat(-PIVOT[0],-PIVOT[1])
    p3 = H3 @ poly
    t3 = H3 @ claw_trace
    q3 = p3[0:2, :].T
    l3 = t3[0:2, :].T
    corp3 = H3 @ centerOfRotation

    H4 = Tmat((l3[1][0]+l3[2][0])/2-PIVOT[0],(l3[1][1]+l3[2][1])/2-PIVOT[1]) @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree4) @ Tmat(-PIVOT[0],-PIVOT[1])
    p4 = H4 @ claw
    q4 = p4[0:2, :].T
    corp4 = H4 @ centerOfRotation

    pygame.draw.polygon(screen,BROWN, ground)
    pygame.draw.polygon(screen,GRASS, grass)
    pygame.draw.polygon(screen, NAVY, bot_base_draw)
    pygame.draw.polygon(screen,RED,q1)
    pygame.draw.polygon(screen,GREEN,q2)
    pygame.draw.circle(screen, BLACK, corp[:2], 3)
    pygame.draw.circle(screen, BLACK, corp2[:2], 3)
    pygame.draw.polygon(screen,BLUE,q3)
    pygame.draw.circle(screen, BLACK, corp3[:2], 3)
    pygame.draw.polygon(screen,D_GREEN,q4)
    pygame.draw.circle(screen, BLACK, corp4[:2], 3)

    


    pygame.display.flip()
    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()