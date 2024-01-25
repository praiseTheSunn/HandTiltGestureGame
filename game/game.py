import pygame, random, sys ,os,time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8

# adjust difficulty
# EASY
ADDNEWBADDIERATE_EASY = 45
# MID
ADDNEWBADDIERATE_MID = 30
# HARD
ADDNEWBADDIERAT_HARD = 15
addnewbaddierate = ADDNEWBADDIERATE_EASY
addsiderate = 10
PLAYERMOVERATE = 5
count=5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    global addnewbaddierate  # Add this line to access the global variable
    global addnewbaddierate_label

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                if event.key == K_1:
                    addnewbaddierate = ADDNEWBADDIERATE_EASY
                    addnewbaddierate_label = 'Nhap'
                    return
                if event.key == K_2:
                    addnewbaddierate = ADDNEWBADDIERATE_MID  # Fix variable name
                    addnewbaddierate_label = 'De'
                    return
                if event.key == K_3:
                    addnewbaddierate = ADDNEWBADDIERAT_HARD  # Fix variable name
                    addnewbaddierate_label = 'Kho'
                    return

def playerHasHitBaddie(playerRect, baddies):
    res = [[], False]
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            res[0].append(b)
            res[1] = True
    return res

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')


# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3,car4,baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')

def contain(lst, name):
    for b in lst:
        if (b['name'] == name):
            return True
    return False
# "Start" screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
pygame.display.update()
waitForPlayerToPressKey()
zero=0
if not os.path.exists("data/save.dat"):
    f=open("data/save.dat",'w')
    f.write(str(zero))
    f.close()   
v=open("data/save.dat",'r')
topScore = addnewbaddierate_label
v.close()
while (count>0):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    sideCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()
            

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
            sideCounter += 1
        if baddieAddCounter == addnewbaddierate:
            baddieAddCounter = 0
            baddieSize =30 
            newBaddie = {'rect': pygame.Rect(random.randint(140, 570), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                        'name': 'baddie'
                        }
            baddies.append(newBaddie)

        if sideCounter == addsiderate:
            sideCounter = 0
            sideLeft= {'rect': pygame.Rect(10,-100,126,600),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface':pygame.transform.scale(wallLeft, (126, 599)),
                'name': 'left'
                }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(600,-100,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                          'name': 'right'
                       }
            baddies.append(sideRight)
            

        # Move the player around.
        # if moveLeft and playerRect.left > 0:
        #     playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        # if moveRight and playerRect.right < WINDOWWIDTH:
        #     playerRect.move_ip(PLAYERMOVERATE, 0)
        # if moveUp and playerRect.top > 0:
        #     playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        # if moveDown and playerRect.bottom < WINDOWHEIGHT:
        #     playerRect.move_ip(0, PLAYERMOVERATE)
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Diem: %s' % (score), font, windowSurface, 135, 0)
        drawText('Do kho: %s' % (topScore), font, windowSurface,135, 20)
        drawText('So mang con lai: %s' % (count), font, windowSurface,135, 40)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.

        res = playerHasHitBaddie(playerRect, baddies)
        if (len(res[0]) > 0):
            if moveLeft and playerRect.left > 0 and not contain(res[0], 'left'):
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH and not contain(res[0], 'right'):
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)
        else:
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)
        if (res[1] == True):
            # if score > topScore:
            #     g=open("data/save.dat",'w')
            #     g.write(str(score))
            #     g.close()
            #     topScore = score
            if (contain(res[0], 'baddie')):
                break
            # if (res[0]['name'] == 'baddie'):
            #     break

        if (score >= 1000):
            # drawText('You Win', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
            # drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
            # pygame.display.update()
            # time.sleep(2)
            # waitForPlayerToPressKey()
            # count=5
            # # gameOverSound.stop()
            break

        mainClock.tick(FPS)

    # "Game Over" screen.
    pygame.mixer.music.stop()
    count=count-1
    gameOverSound.play()
    time.sleep(1)

    if (score >= 1000):
        drawText('You Win', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count=5
        gameOverSound.stop()

    if (count==0):
     laugh.play()
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=5
     gameOverSound.stop()


