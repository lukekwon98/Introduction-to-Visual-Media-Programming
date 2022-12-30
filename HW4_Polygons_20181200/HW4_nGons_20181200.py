import pygame
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 950

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
rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, NAVY, PURPLE, BLACK]


pygame.init()
pygame.display.set_caption("Polygons & Stars")
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

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
        self.color = color
        self.degree = 0
        self.ddegree = np.random.randint(2,8)
        self.gonT = gonN.copy()
        self.gonCopy = gonN.copy()
        self.loc = np.array(coord)
    
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
                pygame.draw.line(screen, self.color, self.gonCopy[i], self.gonCopy[k], 5)
        return



def main():
    starList = []
    polyList = []
    count = 0
    for i in range(5, 13):
        radius = np.random.randint(75,111)
        if i <= 8:
            starList.append(nPoly(i, rainbow[i-5], [200 + (i-5)*270, 15+ 125], radius))
            polyList.append(nPoly(i, rainbow[i-5], [200 + (i-5)*270, 15+ 345], radius))
            polyList[count].ddegree = starList[count].ddegree
            count += 1
        else:
            starList.append(nPoly(i, rainbow[i-5], [200 + (i-9)*270, 15+ 565], radius))
            polyList.append(nPoly(i, rainbow[i-5], [200 + (i-9)*270, 15+ 785], radius))
            polyList[count].ddegree = starList[count].ddegree
            count += 1

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        screen.fill(WHITE)

        for i in range(len(starList)):
            starList[i].rotate()
            starList[i].translate()
            starList[i].drawStar()

        for i in range(len(polyList)):
            polyList[i].rotate()
            polyList[i].translate()
            pygame.draw.polygon(screen, polyList[i].color, polyList[i].gonCopy, 4)


        
        pygame.display.flip()

        clock.tick(60)

    # 게임 종료
    pygame.quit()

    return 0

if __name__ == "__main__":
    main()