import pygame
import numpy as np
import os
from os import path
#font doesn't have to be in event loop 

# 게임 윈도우 크기
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900

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

sun_img = pygame.image.load(path.join(current_path, "real_sun.png"))
sun_img = pygame.transform.scale(sun_img, (180, 180))
venus_img = pygame.image.load(path.join(current_path, "venus.png"))
venus_img = pygame.transform.scale(venus_img, (50, 50))
ear_img = pygame.image.load(path.join(current_path, "Earth.png"))
ear_img = pygame.transform.scale(ear_img, (75, 75))
moon_img = pygame.image.load(path.join(current_path, "moon.png"))
moon_img = pygame.transform.scale(moon_img, (35, 35))
sat_img = pygame.image.load(path.join(current_path, "saturn.png"))
sat_img = pygame.transform.scale(sat_img, (150, 150))
titan_img = pygame.image.load(path.join(current_path, "titan.png"))
titan_img = pygame.transform.scale(titan_img, (36, 36))
starship = pygame.image.load(path.join(current_path, "enterprise.png"))
#enterprise = pygame.transform.scale(titan_img, (30, 15))


def cos(degree):
    radian = degree * np.pi/180
    c = np.cos(radian)
    return c
def sin(degree):
    radian = degree * np.pi/180
    c = np.sin(radian)
    return c

class nPoly:
    def __init__(self, n, color, coord, radius):
        gonN = [] #YOU CAN MAKE MORE 6GONS 7GONS ETC
        for i in range(n):
            deg = i * 360 / n
            radian = deg * np.pi/180 # HOW to convert degree to corresponding radian
            c = np.cos(radian)
            s = np.sin(radian)
            x = radius * c
            y = radius * s
            gonN.append([x,y])
        gonN = np.array(gonN)

        self.radius = radius
        self.vertexList = gonN
        self.color = np.array(color)
        self.degree = 0
        self.ddegree = np.random.randint(2,8)
        self.gonT = gonN.copy()
        self.gonCopy = gonN.copy()
        self.loc = np.array(coord)
        self.dcol = np.random.randint(1,9)
    
    def rotate(self):
        radian = np.deg2rad(self.degree)
        c = np.cos(radian)
        s = np.sin(radian)
        R = np.array([[c, -s], [s, c]])

        tempGon = self.vertexList.copy()
        ppT = R @ tempGon.T
        pp = ppT.T
        self.gonT = pp
        self.degree += self.ddegree

    def translate(self):
        vector = self.loc #make sure that vector is a np array
        tempGon = self.gonT.copy()
        for i in range(tempGon.shape[0]): # move by translation vector
            self.gonCopy[i] = tempGon[i] + vector

    def drawStar(self):
        n = self.gonCopy.shape[0]
        for i in range(n):
            for k in range(n):
                if k == i or k == (i-1)%n or k == (i+1)%n:
                    continue
                pygame.draw.line(screen, self.color, self.gonCopy[i], self.gonCopy[k], 1)
        return


class Player():
    def __init__(self):
        self.image = pygame.transform.scale(starship, (80, 38))
        self.rect = self.image.get_rect()
        self.x = WINDOW_WIDTH / 10
        self.y = WINDOW_HEIGHT /2
        self.speedx = 1
        self.speedy = -1
        self.update_time = pygame.time.get_ticks()
        self.game_start = pygame.time.get_ticks()
        self.boundaryFlag = True

    def update(self):
        if pygame.time.get_ticks() - self.update_time > 2000:
            self.speedx = np.random.randint(-7,8)
            self.speedy = np.random.randint(-7,8)
            self.update_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.game_start > 15000:
            self.boundaryFlag = False

        if self.boundaryFlag == True:
            if self.x < 0 or self.x + 80 > WINDOW_WIDTH:
                self.speedx *=-1
            if self.y < 0 or self.y + 38 > WINDOW_HEIGHT:
                self.speedy *=-1

        self.x += self.speedx
        self.y += self.speedy

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

pygame.init()

pygame.display.set_caption("Solar System")

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

clock = pygame.time.Clock()

print(clock)
pygame.mixer.music.load(path.join(current_path, 'cinematic-inspiring-dreams.wav'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

sun_r = 50
d_venus = sun_r + 70
d_earth = 2.85*(d_venus-sun_r) + sun_r
d_saturn = 7.5*(d_venus-sun_r) + sun_r
d_moon = d_earth / 4
d_titan = d_moon * 1.4

deg_venus = -30
deg_earth = 90
deg_moon = 0
deg_saturn = 30
deg_titan = 75

CEN = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

starList = []
for i in range(201):
    n = np.random.randint(5,9)
    rscale = np.random.randint(0,256)
    random_grey = (rscale,rscale,rscale)
    rcoord = [np.random.randint(0,WINDOW_WIDTH), np.random.randint(0,WINDOW_HEIGHT)]
    rradius = np.random.randint(1,12)
    star = nPoly(n, random_grey, rcoord, rradius)
    starList.append(star)

enterprise = Player()
# 게임 종료 전까지 반복
done = False
# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

#-----draw stars------
    for i in range(len(starList)):
        if starList[i].color[0] + starList[i].dcol >= 255 or starList[i].color[0] + starList[i].dcol <= 0:
            starList[i].dcol *= -1
        change = starList[i].dcol
        starList[i].color += [change,change,change]
        #print(starList[i].color)

    for i in range(len(starList)):
        starList[i].translate()
        starList[i].drawStar()

#-----draw enterprise ------
    enterprise.update()
    screen.blit(enterprise.image,[enterprise.x,enterprise.y])

    print(pygame.time.get_ticks() - enterprise.game_start)


#----setup planet
    earth_orbit = 0.75
    deg_earth += earth_orbit
    deg_moon += earth_orbit/(27.3/365.2)
    deg_venus += earth_orbit/(224.7/365.2)
    deg_saturn += earth_orbit/(10747/365.2)
    deg_titan += earth_orbit/(15.9/365.2)

    core = np.array([CEN[0],CEN[1], 1])
    saturn_cor = np.array([CEN[0],CEN[1], 1])
    sun = np.array([0, 0, 1])

    H_ven = Tmat(CEN[0], CEN[1]) @ Rmat(deg_venus) @ Tmat(0, -d_venus)
    H_ear = Tmat(CEN[0], CEN[1]) @ Rmat(deg_earth) @ Tmat(0, -d_earth) 
    H_moon = H_ear @ Rmat(deg_moon) @ Tmat(0, -d_moon)
    H_sat = Tmat(CEN[0], CEN[1]+180) @ Rmat(deg_saturn) @ Tmat(0, -d_saturn)
    H_titan = H_sat @ Rmat(deg_titan) @ Tmat(0, -d_titan) 

    Venus = H_ven@sun
    Earth = H_ear@sun
    Moon = H_moon@sun
    Saturn = H_sat@sun
    Titan = H_titan@sun
    Saturn[1] *= 0.75 #so y axis gets squished
    Titan[1] *= 0.75

#------draw------
    sun_rect = sun_img.get_rect()
    sun_rect.center = core[:2]
    screen.blit(sun_img, sun_rect)

    ven_rect = venus_img.get_rect()
    ven_rect.center = Venus[:2]
    screen.blit(venus_img, ven_rect)

    ven_rect = venus_img.get_rect()
    ven_rect.center = Venus[:2]
    screen.blit(venus_img, ven_rect)

    ear_rect = ear_img.get_rect()
    ear_rect.center = Earth[:2]
    screen.blit(ear_img, ear_rect)

    moon_rect = moon_img.get_rect()
    moon_rect.center = Moon[:2]
    screen.blit(moon_img, moon_rect)

    titan_rect = titan_img.get_rect()
    titan_rect.center = Titan[:2]
    screen.blit(titan_img, titan_rect)

    sat_rect = sat_img.get_rect()
    sat_rect.center = Saturn[:2]
    screen.blit(sat_img, sat_rect)

    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()