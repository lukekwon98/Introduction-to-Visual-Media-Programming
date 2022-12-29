import pygame
import random
import math
from math import pi
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
T_BLUE = (0,59,111)
GREEN = (0, 255, 0)
PINK = (255,192,203)
DARK_RED = (139,0,0)
BLACK = (0,0,0)
SKY_BLUE = (0,204,255)

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Ball")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()


# You can also use random.randrange(200,500)
class Ball:
    def __init__(self,):
        self.x = np.random.randint(200,900)
        self.y = np.random.randint(200,500)
        self.radius = np.random.randint(45,80)
        self.mass = (self.radius)**2*pi
        self.dx = np.random.randint(-12,13)
        self.dy = np.random.randint(-12,13)
        self.color = (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))
    
    def update(self,):
        self.x+=self.dx
        self.y+=self.dy

        if self.x + self.radius > WINDOW_WIDTH or self.x - self.radius < 0:
            self.dx *= -1
        if self.y + self.radius > WINDOW_HEIGHT or self.y - self.radius < 0: 
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius, 0)


def collide(ball, ball2):
    if ((ball.x - ball2.x)**2 + (ball.y - ball2.y)**2)**(1/2)<(ball.radius+ball2.radius):
        m1 = ball.mass
        m2 = ball2.mass
        v1 = np.array([ball.dx, ball.dy])
        v2 = np.array([ball2.dx, ball2.dy])
        x1 = np.array([ball.x, ball.y])
        x2 = np.array([ball2.x, ball2.y])
        dist = math.sqrt(np.dot(x2-x1, x2-x1))

        normUnit = (x2-x1)/dist
        tanUnit = np.array([(-1)*normUnit[1],normUnit[0]])
        v1Norm = np.dot(normUnit, v1)
        v1Tan = np.dot(tanUnit, v1)
        v2Norm = np.dot(normUnit, v2)
        v2Tan = np.dot(tanUnit, v2)

        v1Norm_Next = (v1Norm*(m1-m2) + 2*m2*v2Norm) / (m1 + m2)
        v2Norm_Next = (v2Norm*(m2-m1) + 2*m1*v1Norm) / (m1 + m2)

        v1Norm_Next_vec = v1Norm_Next*normUnit
        v2Norm_Next_vec = v2Norm_Next*normUnit
        v1Tan_Next_vec = v1Tan*tanUnit
        v2Tan_Next_vec = v2Tan*tanUnit


        v1Next = v1Norm_Next_vec + v1Tan_Next_vec
        v2Next = v2Norm_Next_vec + v2Tan_Next_vec

        ball.dx = v1Next[0]
        ball.dy = v1Next[1]
        ball2.dx = v2Next[0]
        ball2.dy = v2Next[1]

def collide2(ball, ball2):
    if ((ball.x - ball2.x)**2 + (ball.y - ball2.y)**2)**(1/2)<(ball.radius+ball2.radius):
        m1 = ball.mass
        m2 = ball2.mass
        v1 = np.array([ball.dx, ball.dy])
        v2 = np.array([ball2.dx, ball2.dy])
        x1 = np.array([ball.x, ball.y])
        x2 = np.array([ball2.x, ball2.y])
        dist1 = np.dot(x1-x2, x1-x2)
        dist2 = np.dot(x2-x1, x2-x1)
        
        v1Next = v1 - (2*m2/(m1+m2))*np.dot(v1-v2, x1-x2)/dist1*(x1-x2)
        v2Next = v2 - (2*m1/(m1+m2))*np.dot(v2-v1, x2-x1)/dist2*(x2-x1)
        ball.dx = v1Next[0]
        ball.dy = v1Next[1]
        ball2.dx = v2Next[0]
        ball2.dy = v2Next[1]

# 게임 종료 전까지 반복
done = False

listOfBalls = []
for i in range(2):
    ball = Ball()
    if i == 1:
        while(((listOfBalls[0].x - ball.x)**2 + (listOfBalls[0].y - ball.y)**2)**(1/2)<(listOfBalls[0].radius+ball.radius)):
            ball.x = np.random.randint(100,800)
            ball.y = np.random.randint(100,600)
    listOfBalls.append(ball)

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 게임 로직 구간
    # 속도에 따라 원형 위치 변경 #state up date/logic update/parameter update

    for i in range(2):
        ball = listOfBalls[i]
        ball.update()

    collide2(listOfBalls[0], listOfBalls[1])
    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 화면 그리기 구간
    # 공 그리기

    for i in range(2):
        ball = listOfBalls[i]
        ball.draw(screen)

    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60) # 60 frames per sec
                   # ball dx = 4 
                   # ball velocity = 4 pixels per frame, so 240 frames per second

# 게임 종료
pygame.quit()