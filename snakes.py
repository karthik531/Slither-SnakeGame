import pygame
import random

pygame.init()

pygame.mixer.init()
ch_00 = pygame.mixer.Channel(0)
ch_01 = pygame.mixer.Channel(1)

intro_music = pygame.mixer.Sound("intro-sound.ogg")
intro_music.set_volume(1)

BGM = pygame.mixer.Sound("BGM.ogg")
food_music = pygame.mixer.Sound("eat-sound.wav")
gameover_music = pygame.mixer.Sound("gameover-sound.ogg")

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,155)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("slither")

icon = pygame.image.load("snakeicon.jpg")
pygame.display.set_icon(icon)

snakeHeadImg = pygame.image.load('SnakeHead.png')
appleImg = pygame.image.load('apple3.png')

clock = pygame.time.Clock()

block_size = 20
appleThickness = 30
FPS = 20

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 80)
gameOverFont = pygame.font.Font("PAC-FONT.ttf", 70)


def pause():
    paused = True
    message_to_screen("Paused",
                      black,
                      -100,
                      size="large")

    message_to_screen("Press C to continue or Q to quit",
                      black,
                      25)

    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def scoreDisplay(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [3,0])


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - appleThickness))  # / 10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - appleThickness))  # / 10.0) * 10.0

    return randAppleX, randAppleY


def game_intro():

    intro = True

    ch_00.play(intro_music, -1)

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          blue,
                          180)

        pygame.display.update()
        clock.tick(FPS)


def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(snakeHeadImg, 270)
    if direction == "left":
        head = pygame.transform.rotate(snakeHeadImg, 90)
    if direction == "up":
        head = snakeHeadImg
    if direction == "down":
        head = pygame.transform.rotate(snakeHeadImg, 180)

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    elif size == "game_over":
        textSurface = gameOverFont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():

    ch_00.play(BGM, -1)

    gameExit = False
    gameOver = False
    global direction
    direction = "right"

    lead_x = display_width / 2
    lead_y = display_height / 2

    snakelist = []
    snakeLength = 1

    lead_x_change = 0
    lead_y_change = 0

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        if gameOver:
            ch_00.play(gameover_music, 0)

            message_to_screen("Game over", red, y_displace=-50, size="game_over")
            message_to_screen("Press C to play again or Q to quit", black, y_displace=50, size="medium")
            pygame.display.update()

        while gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        gameDisplay.blit(appleImg, (randAppleX, randAppleY))

        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        if len(snakelist) > snakeLength:
            del snakelist[0]

        for eachSegment in snakelist[:-1]:
            if eachSegment == snakehead:
                gameOver = True

        snake(block_size, snakelist)
        scoreDisplay(snakeLength-1)
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:

                ch_01.play(food_music, 0)
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()