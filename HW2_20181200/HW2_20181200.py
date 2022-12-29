import pygame
import os
import numpy as np
import math

WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 900
WHITE = (255,255,255)
RED = (255, 0, 0)

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'hng_assets') #specify path to image file

background_image = pygame.image.load(os.path.join(assets_path, 'Chalkboard2.jpg')) #path to image file

words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'
words = words.split()
guessed = []
repeatFlag = False
state = 0
tick = 0

class Hangman:
    def __init__(self,name):
        self.img = pygame.image.load(os.path.join(assets_path, name + '.png')) #join connects two strings
        self.x = WINDOW_WIDTH / 10 + 10
        self.y = WINDOW_HEIGHT / 10 + 100
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self, screen):
        screen.blit(self.img, [self.x, self.y])

def getRandomWord(wordList): # words put in parameter
    # This function returns a random string from the passed list of strings.
    word =  np.random.choice(wordList)
    return word

def win_display():
    screen.blit(background_image, background_image.get_rect())
    text3 = word_font.render("CONGRATS! YOU GET TO LIVE" ,True, WHITE)
    screen.blit(text3, [50, 75])
    text5 = word_font.render("THE SECRET WORD WAS: " + secretWord, True, WHITE)
    screen.blit(text5, [50, 150])
    text4 = word_font.render("TRY AGAIN? (y OR n)", True, WHITE)
    screen.blit(text4, [50, 225])

def lose_display():
    screen.blit(background_image, background_image.get_rect())
    text3 = word_font.render("YOU'RE DEAD!" ,True, WHITE)
    screen.blit(text3, [50, 75])
    text5 = word_font.render("THE SECRET WORD WAS: " + secretWord, True, WHITE)
    screen.blit(text5, [50, 150])
    text4 = word_font.render("TRY AGAIN? (y OR n)", True, WHITE)
    screen.blit(text4, [50, 225])

def update():
    for letter in letters:
        current_found = ''
        current_missed = ''
        for letter in secretWord:
            if letter in guessed:
                current_found += letter + ' '
            else:
                current_found += '_ '
        for letter in guessed:
            if letter not in secretWord:
                current_missed += letter + ' '

        text = word_font.render(current_found, True, WHITE)
        screen.blit(text, [600, 200])
        text2 = word_font.render(current_missed, True, WHITE)
        screen.blit(text2, [70,650])

        if repeatFlag == True:
            text3 = word_font.render("LETTER ALREADY CHOSEN!", True, WHITE)
            screen.blit(text3,[50,790])
        elif won == True:
            if tick != 0:
                yay_sound.play()
                win_display()
        elif won == False and Lost == True:
            fail_sound.play()
            lose_display()
        for letter in letters:
            x,y,lett= letter
            #pygame.draw.circle(screen, WHITE, (x,y), bWIDTH/2, 2)
            text = font.render(lett, True, WHITE)
            screen.blit(text, (x-text.get_width()/1.5,y - text.get_width()/1.5))


pygame.init()

pygame.display.set_caption("Hangman")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('chalkduster', 45, True, False) #Name of Font, Size, bold, italic
word_font = pygame.font.SysFont('chalkduster', 60, True, False)
pygame.mixer.music.load(os.path.join(assets_path, 'elementary_school_playground.wav'))
pygame.mixer.music.play(-1)

chalk_sound = pygame.mixer.Sound(os.path.join(assets_path, 'chalk.wav'))
chalk_sound.set_volume(50)
yay_sound = pygame.mixer.Sound(os.path.join(assets_path, 'Yay.wav'))
yay_sound.set_volume(0.3)
denied_sound = pygame.mixer.Sound(os.path.join(assets_path, 'denied.wav'))
gasp_sound = pygame.mixer.Sound(os.path.join(assets_path, 'gasp.wav'))
fail_sound = pygame.mixer.Sound(os.path.join(assets_path, 'Spongebob_Disappointed.wav'))

hangList = []
for i in range(7):
    hangman = Hangman('stage' + str(i) + '_wr')
    hangList.append(hangman)

secretWord = getRandomWord(words)
done = False
won = True
Lost = False
#buttons
letters = []
bWIDTH = 50
bGAP = 15
startx = round(WINDOW_WIDTH - (bWIDTH + bGAP)*13) - 50 #bWIDTH + bGAP is whole rect area of buttons /2 to place it somewhere in the middle
starty = 400
for i in range(26):
    x = startx + bGAP * 2 + ((bWIDTH + bGAP) * (i%13)) #start pos + 2*GAP to give enough space, + position is shifted as much as index button
    y = starty + ((i//13) * (bGAP + bWIDTH * 2)) #if i gets bigger than 14, y will be increased by a Gap + Width, therefore  writing it on the next line
    letters.append([x,y,chr(97+i)])


while not done:
# 이벤트 반복 구간
    if tick == 0:
        print(secretWord)
    screen.blit(background_image, background_image.get_rect())

    text = font.render("CHOOSE A LETTER, IF YOU DARE", True, WHITE)
    screen.blit(text, [WINDOW_WIDTH/3.8, WINDOW_HEIGHT/12])
    hangList[state].draw(screen)

    update()
    tick +=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            repeatFlag = False
            xCoord, yCoord = pygame.mouse.get_pos()
            for letter in letters:
                x, y, lett= letter
                d = math.sqrt((x-xCoord)**2 + (y-yCoord)**2)
                if won == True or (won == False and Lost == True):
                    if d < bWIDTH/2 :
                        if lett == 'y':
                            chalk_sound.play()
                            guessed = []
                            won = False
                            Lost = False
                            state = 0
                            tick = 0
                            secretWord = getRandomWord(words)
                        elif lett == 'n':
                            chalk_sound.play()
                            done = True
                else:
                    if d < bWIDTH/2 :
                        if lett in guessed:
                            denied_sound.play()
                            repeatFlag = True
                        else:
                            chalk_sound.play()
                            guessed.append(lett)
                            if lett not in secretWord:
                                gasp_sound.play()
                                state += 1

        won = True
        for letter in secretWord:
            if letter not in guessed:
                won = False
                break       

        if state == 6:
            Lost = True

        

        pygame.display.flip()

        clock.tick(60)

pygame.quit()