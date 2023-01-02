import pygame
import os
import numpy as np
import random

WIDTH = 1400
HEIGHT = 829
WHITE = (255,255,255)
RED = (237,119,119)
BLUE = (148,192,204)

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'TTT_assets') #specify path to image file

background = pygame.image.load(os.path.join(assets_path, 'chalk_board1.webp')) #path to image file
background_rect = background.get_rect()

def makeMove(board, letter, move):
    board[move] = letter

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if np.random.randint(0, 2) == 0:
        return 'computer'
    else:
        return 'player'

def isWinner(bo):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    winner = False
    le = 'X'
    if (bo[7] == le and bo[8] == le and bo[9] == le) or (bo[4] == le and bo[5] == le and bo[6] == le) or (bo[1] == le and bo[2] == le and bo[3] == le) or (bo[7] == le and bo[4] == le and bo[1] == le) or (bo[8] == le and bo[5] == le and bo[2] == le) or (bo[9] == le and bo[6] == le and bo[3] == le) or (bo[7] == le and bo[5] == le and bo[3] == le) or (bo[9] == le and bo[5] == le and bo[1] == le):   
        winner = 'X'
    le = 'O'
    if (bo[7] == le and bo[8] == le and bo[9] == le) or (bo[4] == le and bo[5] == le and bo[6] == le) or (bo[1] == le and bo[2] == le and bo[3] == le) or (bo[7] == le and bo[4] == le and bo[1] == le) or (bo[8] == le and bo[5] == le and bo[2] == le) or (bo[9] == le and bo[6] == le and bo[3] == le) or (bo[7] == le and bo[5] == le and bo[3] == le) or (bo[9] == le and bo[5] == le and bo[1] == le):   
        winner = 'O'
    if winner == False and True == isBoardFull(theBoard):
        return 'Draw'
    else:
        return winner


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getComputerMove(theBoard, computerLetter, playerLetter):
    bestScore = -1000
    for i in range(1,10):
            if theBoard[i] == ' ': #is spot available
                theBoard[i] = computerLetter
                score = minimax(theBoard, 0, False, computerLetter, playerLetter) #return the score of minimax of the board after one empty part of board is filled with a move
                theBoard[i] = ' '
                if score > bestScore:
                    bestScore = score
                    move = i
    return move

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the list is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
#-----------------------------from tictactoe.py-----------------------------------

def minimax(theBoard, depth, isMaximizing, computerLetter, playerLetter): #depth = minimum moves, isMaximizing = bool, whether we are maximizing
    result = isWinner(theBoard) #first check if someone won, returns 'o', 'x', or 'tie'
    if result != False: #if game ended, so result came out as something
        if result == computerLetter:
            return 10 - depth
        elif result == playerLetter:
            return -10 + depth
        elif result == 'Draw':
            return 0

    if isMaximizing:
        bestScore = -1000
        for i in range(1,10):
                if theBoard[i] == ' ': #check all possible spots
                    theBoard[i] = computerLetter
                    score = minimax(theBoard, depth+1, False, computerLetter, playerLetter) #recursive, next player is 'player', so maximizing is false
                    theBoard[i] = ' '
                    bestScore = max(score, bestScore)
        return bestScore

    else:
        bestScore = 1000
        for i in range(1,10):
                if theBoard[i] == ' ': #check all possible spots
                    theBoard[i] = playerLetter
                    score = minimax(theBoard, depth+1, True, computerLetter, playerLetter) #recursive, next player is computer, so minimizing is true
                    theBoard[i] = ' '
                    bestScore = min(score, bestScore)
        return bestScore

#-----------------------------from the coding train-----------------------------------

def show_start_screen():
    screen.blit(background, background_rect)
    choiceList = [[],pygame.Rect(285, 530, 242, 250),pygame.Rect(555, 525, 267, 255),pygame.Rect(860, 525, 245, 255), pygame.Rect(270, 282, 270, 220), pygame.Rect(560, 282, 270, 215), pygame.Rect(860, 278, 255, 220),pygame.Rect(270, 60, 270, 200),pygame.Rect(555, 60, 285, 200),pygame.Rect(860, 60, 255, 200)]
    draw_text(screen, "TIC", 100, loc_x(choiceList[7]),loc_y(choiceList[7])+75)
    draw_text(screen, "TAC", 100, loc_x(choiceList[8]),loc_y(choiceList[8])+75)
    draw_text(screen, "TOE", 100, loc_x(choiceList[9]),loc_y(choiceList[9])+75)
    draw_text(screen, "CHOOSE", 60, loc_x(choiceList[1])-10, loc_y(choiceList[1])+110)
    draw_text(screen, "YOUR", 60, loc_x(choiceList[2]), loc_y(choiceList[2])+110)
    draw_text(screen, "SYMBOL", 60, loc_x(choiceList[3])+10, loc_y(choiceList[3])+110)
    draw_o(screen, loc_x(choiceList[4]), loc_y(choiceList[4])-10)
    draw_x(screen, loc_x(choiceList[6]), loc_y(choiceList[6])-50)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    xPos, yPos = pygame.mouse.get_pos()
                    if blockList[4].collidepoint(xPos, yPos):
                        print("O")
                        waiting = False
                        return "O"
                    elif blockList[6].collidepoint(xPos, yPos):
                        print("X")
                        waiting = False
                        return "X"

def show_fin_screen(win):
    pygame.time.delay(2600)
    screen.blit(background, background_rect)
    choiceList = [[],pygame.Rect(285, 530, 242, 250),pygame.Rect(555, 525, 267, 255),pygame.Rect(860, 525, 245, 255), pygame.Rect(270, 282, 270, 220), pygame.Rect(560, 282, 270, 215), pygame.Rect(860, 278, 255, 220),pygame.Rect(270, 60, 270, 200),pygame.Rect(555, 60, 285, 200),pygame.Rect(860, 60, 255, 200)]
    if win == "Won":
        draw_text(screen, "YOU", 100, loc_x(choiceList[7]),loc_y(choiceList[7])+75)
        draw_text(screen, "WON", 100, loc_x(choiceList[9]),loc_y(choiceList[9])+75)
        yay_sound.play()
    elif win == "Lost":
        draw_text(screen, "YOU", 100, loc_x(choiceList[7]),loc_y(choiceList[7])+75)
        draw_text(screen, "LOST", 100, loc_x(choiceList[9]),loc_y(choiceList[9])+75)
        emotional_damage.play()
    else:
        draw_text(screen, "DRAW", 100, loc_x(choiceList[8]),loc_y(choiceList[8])+75)
        crowd_groan.play()
        weak_clapping.play()
    draw_o(screen, loc_x(choiceList[4]), loc_y(choiceList[4])-10)
    draw_x(screen, loc_x(choiceList[6]), loc_y(choiceList[6])-50)
    draw_text(screen, "PLAY", 80, loc_x(choiceList[1])-10, loc_y(choiceList[1])+110)
    draw_text(screen, "AGAIN?", 80, loc_x(choiceList[3])+80, loc_y(choiceList[3])+110)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    xPos, yPos = pygame.mouse.get_pos()
                    if blockList[4].collidepoint(xPos, yPos):
                        print("O")
                        waiting = False
                        return True
                    elif blockList[6].collidepoint(xPos, yPos):
                        print("X")
                        waiting = False
                        return False
#-----------------------------from shmup.py-----------------------------------

def draw_o(surf, x,y):
    font = pygame.font.Font(chalk_font, 270)
    text_surface = font.render("O", True, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_x(surf,x,y):
    font = pygame.font.Font(chalk_font, 280)
    text_surface = font.render("x", True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text(surf, text,size, x, y):
    font = pygame.font.Font(chalk_font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def loc_x(coord):
    return coord[0]+coord[2]/2
def loc_y(coord):
    return coord[1]-50

def finish():
    return False, True, False
def again():
    return False, False, True


pygame.init()

pygame.display.set_caption("Tic Tac Toe")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
chalk_font = pygame.font.match_font('chalkduster') #Name of Font, Size, bold, italic
#chalk_font = pygame.font.SysFont('chalkduster', 45, True, False) #Name of Font, Size, bold, italic
big_font = pygame.font.SysFont('chalkduster', 60, True, False)
OX_font = pygame.font.SysFont('chalkduster', 100, True, False)

chalk_sound = pygame.mixer.Sound(os.path.join(assets_path, 'chalk.wav'))
chalk_sound.set_volume(50)
yay_sound = pygame.mixer.Sound(os.path.join(assets_path, 'Yay.wav'))
yay_sound.set_volume(0.7)
denied_sound = pygame.mixer.Sound(os.path.join(assets_path, 'denied.wav'))
fail_sound = pygame.mixer.Sound(os.path.join(assets_path, 'Spongebob_Disappointed.wav'))
emotional_damage = pygame.mixer.Sound(os.path.join(assets_path, 'emotional_damage.wav'))
crowd_groan = pygame.mixer.Sound(os.path.join(assets_path, 'crowd_groan.wav'))
weak_clapping = pygame.mixer.Sound(os.path.join(assets_path, 'weak_clapping.wav'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.load(os.path.join(assets_path, 'elementary_school_playground.wav'))
pygame.mixer.music.play(-1)

blockList = [[],pygame.Rect(285, 530, 242, 250),pygame.Rect(555, 525, 267, 255),pygame.Rect(860, 525, 245, 255), pygame.Rect(270, 282, 270, 220), pygame.Rect(560, 282, 270, 215), pygame.Rect(860, 278, 255, 220),pygame.Rect(270, 60, 270, 200),pygame.Rect(555, 60, 285, 200),pygame.Rect(860, 60, 255, 200)]
# print(len(blockList))

done = False
begin = True
while not done:
    if begin == True:
        playerLetter = show_start_screen()
        if playerLetter == "O":
            computerLetter = "X"
        else:
            computerLetter = "O"
        #print(playerLetter, computerLetter)
        begin = False
    # Reset the board
    theBoard = [' '] * 10 #10 space strings in a list [' ', ' ' , ' ', ... ,' ']
    turn = whoGoesFirst()
    gameIsPlaying = True
    screen.blit(background,background_rect)
    while gameIsPlaying == True:
        if turn == 'player':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    gameIsPlaying == False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xPos, yPos = pygame.mouse.get_pos()
                    for i in range(1,len(blockList)):
                        if blockList[i].collidepoint(xPos, yPos):
                            if theBoard[i] == ' ':
                                makeMove(theBoard,playerLetter,i)
                                print(theBoard)
                                if playerLetter == "O":
                                    draw_o(screen,loc_x(blockList[i]),loc_y(blockList[i])-20)
                                    pygame.display.flip()
                                else:
                                    draw_x(screen,loc_x(blockList[i]),loc_y(blockList[i])-60)
                                    pygame.display.flip()
                                chalk_sound.play()
                                if playerLetter == isWinner(theBoard):
                                    playAgain = show_fin_screen("Won")
                                    if playAgain == False:
                                        gameIsPlaying, done, begin = finish()
                                    else:
                                        gameIsPlaying, done, begin = again()
                                else:
                                    if 'Draw' == isWinner(theBoard):
                                        playAgain = show_fin_screen("Draw")
                                        if playAgain == False:
                                            gameIsPlaying, done, begin = finish()
                                        else:
                                            gameIsPlaying, done, begin = again()
                                        break
                                    else:
                                        turn = 'computer'
                            else:
                                denied_sound.play()
                                continue
        else: 
            i = getComputerMove(theBoard, computerLetter, playerLetter)
            makeMove(theBoard, computerLetter, i)
            print(theBoard)
            if playerLetter == "O":
                pygame.time.delay(1500)
                draw_x(screen,loc_x(blockList[i]),loc_y(blockList[i])-60)
                pygame.display.flip()
                chalk_sound.play()
            else:
                pygame.time.delay(1500)
                draw_o(screen,loc_x(blockList[i]),loc_y(blockList[i])-20)
                pygame.display.flip()
                chalk_sound.play()

            if computerLetter == isWinner(theBoard):
                playAgain = show_fin_screen("Lost")
                if playAgain == False:
                    gameIsPlaying, done, begin = finish()
                else:
                    gameIsPlaying, done, begin = again()
            else:
                if 'Draw' == isWinner(theBoard):
                    playAgain = show_fin_screen("Draw")
                    if playAgain == False:
                        gameIsPlaying, done, begin = finish()
                    else:
                        gameIsPlaying, done, begin = again()
                    break
                else:
                    turn = 'player'

        pygame.display.flip()



        clock.tick(60)

pygame.quit()
