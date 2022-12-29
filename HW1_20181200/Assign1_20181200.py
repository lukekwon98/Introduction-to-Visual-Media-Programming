import pygame
import os
import numpy as np

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets') #specify path to image file

# 게임 윈도우 크기
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Mushrooms and Lumas")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# sound
sound = pygame.mixer.Sound(os.path.join(assets_path, 'boing.wav'))
sound.set_volume(0.03)
pygame.mixer.set_num_channels(101)

# 색 정의
SKY = (209, 237, 242)

class Fren:
    def __init__(self,name,index):
        self.img = pygame.image.load(os.path.join(assets_path, name + '.png')) #join connects two strings
        self.x = np.random.randint(200,900)
        self.y = np.random.randint(200,500)
        self.dx = np.random.randint(-11,12)
        self.idx = index
        while self.dx == 0:
            self.dx = np.random.randint(-11,12)
        self.dy = self.dx
    
    def update(self):
        self.x+=self.dx
        self.y+=self.dy

        if (self.x + self.img.get_width()) > WINDOW_WIDTH or (self.x) < 0:
            pygame.mixer.Channel(self.idx).play(sound)
            self.dx *= -1
        if (self.y + self.img.get_height()) > WINDOW_HEIGHT or (self.y) < 0: 
            pygame.mixer.Channel(self.idx).play(sound)
            self.dy *= -1

    def draw(self, screen):
        screen.blit(self.img, [self.x, self.y])

# 배경 이미지 로드
background_image = pygame.image.load(os.path.join(assets_path, 'Mario_World1.jpeg')) #path to image file

# 이미지 로드
frenList = []
for i in range(101):
    if i < 80:
        index = (i//10)+1
        Shroom = Fren('mushroom'+str(index),i)
        frenList.append(Shroom)
    elif i < 100:
        index = (i//90)+1
        Luma = Fren('luma'+str(index),i)
        frenList.append(Luma)
    else:
        star = Fren('resize_star(me)',i)
        star.dx = 5
        star.dy = 5
        frenList.append(star)

player_image = pygame.image.load(os.path.join(assets_path, 'goldshroom.png')) #keyboard image
player_x = int(WINDOW_WIDTH / 2)
player_y = int((WINDOW_HEIGHT*8.5) / 10)
player_dx = 0
player_dy = 0

# 게임 종료 전까지 반복
done = False

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN: #event = when pressing keys
            if event.key == pygame.K_LEFT:
                    player_dx = -7.3
            elif event.key == pygame.K_RIGHT:
                    player_dx = 7.3
            elif event.key == pygame.K_UP:
                    player_dy = -7.3
            elif event.key == pygame.K_DOWN:
                    player_dy = 7.3
        # 키가 놓일 경우
        elif event.type == pygame.KEYUP: #event = when releasing keys, so it DOESN'T MOVE when KEY isn't pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_dy = 0

    # 게임 로직 구간
    player_x += player_dx
    player_y += player_dy

    # 화면 삭제 구간

    for i in range(101):
        fren = frenList[i]
        fren.update()

    # 윈도우 화면 채우기
    screen.fill(SKY) #clean screen first 

    screen.blit(background_image, background_image.get_rect()) #blit land

    screen.blit(player_image, [player_x, player_y])
    # 화면 그리기 구간
    for i in range(101):
        fren = frenList[i]
        fren.draw(screen)


    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()