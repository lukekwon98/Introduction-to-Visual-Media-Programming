import pygame
import numpy as np
import os
from os import path
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
base = pygame.image.load(path.join(current_path, "metal_body2.png"))
base = pygame.transform.scale(base, (100, 90))
body1 = pygame.image.load(path.join(current_path, "metal_body2.png"))
body1 = pygame.transform.scale(body1, (200, 65))
body1_rect = body1.get_rect()
body2 = pygame.image.load(path.join(current_path, "metal_body2.png"))
body2 = pygame.transform.scale(body2, (200, 65))
body2_rect = body2.get_rect()
body3 = pygame.image.load(path.join(current_path, "metal_body2.png"))
body3 = pygame.transform.scale(body3, (200, 65))
body3_rect = body3.get_rect()
claw_img = pygame.image.load(path.join(current_path, "claw.png"))
claw_img = pygame.transform.scale(claw_img, (120, 120))
claw_img = pygame.transform.flip(claw_img, True, False)
claw_img_rect = claw_img.get_rect()

sun = pygame.image.load(path.join(current_path, "sun.png"))
sun = pygame.transform.scale(sun, (150, 150))
tree = pygame.image.load(path.join(current_path, "tree.png"))
tree = pygame.transform.scale(tree, (450, 680))
tree2 = pygame.image.load(path.join(current_path, "tree.png"))
tree2 = pygame.transform.scale(tree2, (350, 580))
cloud1 = pygame.image.load(path.join(current_path, "cloud.png"))
cloud1 = pygame.transform.scale(cloud1, (300, 180))
cloud2 = pygame.image.load(path.join(current_path, "cloud.png"))
cloud2 = pygame.transform.scale(cloud2, (200, 120))
cloud3 = pygame.image.load(path.join(current_path, "cloud.png"))
cloud3 = pygame.transform.scale(cloud3, (370, 180))

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


def rot_center(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image,new_rect

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

bot_sound = pygame.mixer.Sound(os.path.join(current_path, 'robot.wav'))
bot_sound.set_volume(0.4)


ground = np.array([[1200,750], [1200,700], [0,700], [0,750]])
grass = np.array([[1200,700], [1200,675], [0,675], [0,700]])

poly = np.array([[0,0,1], [200, 0,1], [200, 65,1], [0,65,1]])
PIVOT = [poly[2][1]/2,poly[2][1]/2]
trace = np.array([[0,0,1], [200-PIVOT[0], 0,1], [200-PIVOT[0], 65,1], [0,65,1]])
claw = np.array([[10,PIVOT[0]-7.5,1], [60,PIVOT[0]-7.5,1], [60, PIVOT[1]-35,1], [120, PIVOT[1]-35,1], [120,PIVOT[1]-25,1], [72.5, PIVOT[1]-25, 1], [72.5, PIVOT[1]+25,1], [120, PIVOT[1]+25,1], [120, PIVOT[1]+35,1], [60, PIVOT[1]+35,1], [60, PIVOT[0]+7.5,1], [10, PIVOT[0]+7.5,1]])
claw_trace =  np.array([[0,0,1], [200-PIVOT[0]/2, 0,1], [200-PIVOT[0]/2, 65,1], [0,65,1]])
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

font = pygame.font.SysFont('chalkduster', 40, True, False)

# 게임 종료 전까지 반복
done = False
autoFlag = False
start = True
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    if start == True:
        screen.fill(SKY_BLUE)
        text1 = font.render('PRESS ARROWS, WASD TO MOVE', True, WHITE)
        text2 = font.render('PRESS SPACE FOR', True, WHITE)
        text2_1 = font.render('AUTO DANCING MODE', True, WHITE)
        text3 = font.render('PRESS ANY KEY TO START', True, WHITE)
        screen.blit(text1, [WINDOW_WIDTH/2-400, WINDOW_HEIGHT/2-250])
        screen.blit(text2, [WINDOW_WIDTH/2-260, WINDOW_HEIGHT/2-75])
        screen.blit(text2_1, [WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2-25])
        screen.blit(text3, [WINDOW_WIDTH/2-350, WINDOW_HEIGHT/2+150])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                start = False

    else: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        ddeg = 0
        ddeg2 = 0
        ddeg3 = 0
        ddeg4 = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            autoFlag = not autoFlag
        if autoFlag == True:
            ddeg2 = 1.3
            ddeg = -1.2
            ddeg4 = -1.1
            ddeg3 = 1
            bot_sound.play()
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
        
        degree += ddeg
        degree2 += ddeg2
        degree3 += ddeg3
        degree4 += ddeg4

        H = Tmat(470,590) @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree) @ Tmat(-PIVOT[0],-PIVOT[1])
        p1 = H @ poly
        t1 = H @ trace
        #body1_rect = H @ body1_rect
        q1 = p1[0:2, :].T
        l1 = t1[0:2, :].T
        print(q1)
        cent = [(q1[0][0] + q1[2][0])/2, (q1[0][1]+q1[2][1])/2, 1]
        print(cent)
        body1_rect.center = cent[:2]
        body1n, body1n_rect = rot_center(body1, body1_rect, -degree)
        #body1n_rect = body1n.get_rect()

        corp = H @ centerOfRotation

        H2 = Tmat((l1[1][0]+l1[2][0])/2-PIVOT[0],(l1[1][1]+l1[2][1])/2-PIVOT[1]) @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree2) @ Tmat(-PIVOT[0],-PIVOT[1])
        p2 = H2 @ poly
        t2 = H2 @ trace
        q2 = p2[0:2, :].T
        l2 = t2[0:2, :].T
        cent2 = [(q2[0][0] + q2[2][0])/2, (q2[0][1]+q2[2][1])/2]
        body2_rect.center = cent2
        body2n, body2n_rect = rot_center(body2, body2_rect, -degree2)
        corp2 = H2 @ centerOfRotation

        H3 = Tmat((l2[1][0]+l2[2][0])/2-PIVOT[0],(l2[1][1]+l2[2][1])/2-PIVOT[1])  @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree3) @ Tmat(-PIVOT[0],-PIVOT[1])
        p3 = H3 @ poly
        t3 = H3 @ claw_trace
        q3 = p3[0:2, :].T
        l3 = t3[0:2, :].T
        body3_rect.center = [(q3[0][0] + q3[2][0])/2, (q3[0][1]+q3[2][1])/2]
        body3n, body3n_rect = rot_center(body3, body3_rect, -degree3)
        corp3 = H3 @ centerOfRotation

        H4 = Tmat((l3[1][0]+l3[2][0])/2-PIVOT[0],(l3[1][1]+l3[2][1])/2-PIVOT[1])  @ Tmat(PIVOT[0],PIVOT[1]) @ Rmat(degree4) @ Tmat(-PIVOT[0],-PIVOT[1])
        p4 = H4 @ claw
        q4 = p4[0:2, :].T
        #claw_img_rect.center = [(q4[0][0] + q4[3][0])/2, (q4[3][1]+q4[8][1])/2]
        claw_img_rect.center = [(q4[0][0] + q4[10][0])/2, (q4[0][1]+q4[10][1])/2]
        claw1n, claw1n_rect = rot_center(claw_img, claw_img_rect, -degree4)
        corp4 = H4 @ centerOfRotation


        screen.blit(sun, [WINDOW_WIDTH-175, 20])
        screen.blit(cloud3, [WINDOW_WIDTH/15-20, 20])
        screen.blit(tree, [WINDOW_WIDTH/15-80, 20])
        screen.blit(tree2, [WINDOW_WIDTH-300, 120])
        screen.blit(cloud1, [WINDOW_WIDTH/2-80, 20])
        screen.blit(cloud2, [WINDOW_WIDTH/15-80, 20])
        pygame.draw.polygon(screen,BROWN, ground)
        pygame.draw.polygon(screen,GRASS, grass)
        screen.blit(base,[WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2+222])
        screen.blit(body1n,body1n_rect)
        screen.blit(body2n,body2n_rect)
        pygame.draw.circle(screen, BLACK, corp[:2], 3)
        pygame.draw.circle(screen, BLACK, corp2[:2], 3)
        screen.blit(body3n,body3n_rect)
        pygame.draw.circle(screen, BLACK, corp3[:2], 3)
        #pygame.draw.polygon(screen,D_GREEN,q4)
        screen.blit(claw1n,claw1n_rect)
        pygame.draw.circle(screen, BLACK, corp4[:2], 3)




    pygame.display.flip()
    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()