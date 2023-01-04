import pygame
import numpy as np
import os
from os import path
#font doesn't have to be in event loop 

# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

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


background = pygame.image.load(path.join(current_path, "dan-blackburn.jpg"))
background = pygame.transform.scale(background, (800, 1000))
background_rect = background.get_rect()

sun = pygame.image.load(path.join(current_path, "sun.png"))
sun = pygame.transform.scale(sun, (150, 150))

pygame.mixer.music.load(path.join(current_path, 'windy_countryside.wav'))
pygame.mixer.music.set_volume(5)
pygame.mixer.music.play(loops=-1)
mill_sound = pygame.mixer.Sound(os.path.join(current_path, 'creak.wav'))
mill_sound.set_volume(1)



class Windmill:
    def __init__(self, coord, location):
        WING1 = np.array(coord)
        self.WING_LEN= WING1[2][0]
        self.WING1 = WING1.T
        self.CENTER = location #(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.degree = 90
        self.ddeg = 0

        self.H1 = Tmat(self.CENTER[0],self.CENTER[1]) @ Rmat(self.degree)@ Tmat(-self.WING_LEN, 0)
        self.temp_w1 = self.H1 @ self.WING1
        self.draw_w1 = self.temp_w1[0:2, :].T

        self.H2 = self.H1 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w2 = self.H2 @ self.WING1
        self.draw_w2 = self.temp_w2[0:2, :].T

        self.H3 = self.H2 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w3 = self.H3 @ self.WING1
        self.draw_w3 = self.temp_w3[0:2, :].T

        self.H4 = self.H3 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w4 = self.H4 @ self.WING1
        self.draw_w4 = self.temp_w4[0:2, :].T

        self.body = np.array([[self.CENTER[0]-self.WING_LEN/3,self.CENTER[1]-self.WING_LEN/6], [self.CENTER[0],self.CENTER[1]-self.WING_LEN/5], [self.CENTER[0]+self.WING_LEN/3,self.CENTER[1]-self.WING_LEN/6],[self.CENTER[0]+self.WING_LEN*4/5,self.CENTER[1]+self.WING_LEN*2],[self.CENTER[0]-self.WING_LEN*4/5,self.CENTER[1]+self.WING_LEN*2]])

    def update(self):

        self.degree =self.degree + self.ddeg

        self.H1 = Tmat(self.CENTER[0],self.CENTER[1]) @ Rmat(self.degree)@ Tmat(-self.WING_LEN, 0)
        self.temp_w1 = self.H1 @ self.WING1
        self.draw_w1 = self.temp_w1[0:2, :].T

        self.H2 = self.H1 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w2 = self.H2 @ self.WING1
        self.draw_w2 = self.temp_w2[0:2, :].T

        self.H3 = self.H2 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w3 = self.H3 @ self.WING1
        self.draw_w3 = self.temp_w3[0:2, :].T

        self.H4 = self.H3 @ Tmat(self.WING_LEN, 0) @ Rmat(90) @Tmat(-self.WING_LEN, 0)
        self.temp_w4 = self.H4 @ self.WING1
        self.draw_w4 = self.temp_w4[0:2, :].T

    def draw(self, bodyCol, wing1, wing2):
        pygame.draw.polygon(screen,bodyCol,self.body)
        pygame.draw.polygon(screen,wing1, self.draw_w1)
        pygame.draw.polygon(screen,wing2, self.draw_w2)
        pygame.draw.polygon(screen,wing1, self.draw_w3)
        pygame.draw.polygon(screen,wing2, self.draw_w4)

windmill1 = Windmill([[0,-50,1], [0,50,1], [150,0,1]], (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
windmill2 = Windmill([[0,-10,1], [0,10,1], [35,0,1]], (WINDOW_WIDTH*9/10, WINDOW_HEIGHT*6/10))
windmill2.ddeg = 1
windmill3 = Windmill([[0,-10,1], [0,10,1], [25,0,1]], (WINDOW_WIDTH*1/10, WINDOW_HEIGHT*5.5/10))
windmill3.ddeg = 0.75
windmill4 = Windmill([[0,-10,1], [0,10,1], [12,0,1]], (WINDOW_WIDTH*8/10, WINDOW_HEIGHT*4.8/10))
windmill4.ddeg = 0.5


# 게임 종료 전까지 반복
done = False
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #ddeg = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        windmill1.ddeg += -1
    if keystate[pygame.K_RIGHT]:
        windmill1.ddeg += 1
    if keystate[pygame.K_SPACE]:
        windmill1.ddeg = 0       

    # 윈도우 화면 채우기
    screen.fill(SKY_BLUE)

    if windmill1.ddeg != 0:
        mill_sound.play()
    

    screen.blit(background,background_rect)

    #print(windmill1.degree)

    windmill1.update()
    windmill2.update()
    windmill3.update()
    windmill4.update()

    windmill1.draw(WHITE,BLACK,BLUE)
    windmill2.draw(NAVY, WHITE, RED)
    windmill3.draw(D_GREEN, YELLOW, BLUE)
    windmill4.draw(ORANGE, YELLOW, YELLOW)


    screen.blit(sun, [WINDOW_WIDTH-175, 20])
    


    pygame.display.flip()
    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()