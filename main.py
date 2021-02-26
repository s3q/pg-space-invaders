import pygame as pg
import random as rd
import math as mt

pg.init()

screenX = 800
screenY = 600
screen = pg.display.set_mode((screenX, screenY))

pg.display.set_caption("new game")

# bgc and icon
background = pg.image.load(r"game\icon\background.png")
icon = pg.image.load(r"game\icon\icon.png")
pg.display.set_icon(icon)

# background sound
pg.mixer.music.load(r"game\music\background.wav")
pg.mixer.music.play(-1)

# player
playerIcon = pg.image.load(r"game\icon\game-icon\player.png")
playerX = (screenX - 32) * 50 / 100
playerY = (screenY - 32) * 80 / 100
steps_playerX = 0
steps_playerY = 0


list_step = [3, 4, 5, 6]

# enemy
enemyIcon = []
enemyX = []
enemyY = []
steps_enemyX = []
steps_enemyY = []
num_of_enemy = 6

def create_enemy(num):
    for i in range(num):
        enemyIcon.append(pg.image.load(r"game\icon\game-icon\enemy.png"))
        enemyX.append(rd.randint(0, 736))
        enemyY.append(rd.randint(0, 136))
        steps_enemyX.append(list_step[rd.randint(0, len(list_step) - 1)])
        steps_enemyY.append(20)
        
create_enemy(num_of_enemy)
        
# enemyIcon = pg.image.load(
#     r"C:\Users\s3q\Desktop\github\sduks\py\game\icon\game-icon\enemy.png")
# enemyX = rd.randint(0, 768)
# enemyY = rd.randint(0, 68)
# steps_enemyX = list_step[rd.randint(0, len(list_step) - 1)]
# steps_enemyY = 20

# bullet
bulletIcon = pg.image.load(r"game\icon\game-icon\bullet.png")
bulletX = 0
bulletY = 10
steps_bulletX = 0
steps_bulletY = 5
bullet_state = "ready"


def player(pos):
    screen.blit(playerIcon, pos)


def enemy(pos):
    for i in range(num_of_enemy):
        screen.blit(enemyIcon[i], pos)


def fire_bullet(pos):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIcon, pos)


def is_collision(X1, Y1, X2, Y2):
    distance = mt.sqrt((pow(X1 - X2, 2)) +
                       (pow(Y1 - Y2, 2)))
    if distance <= 64:
        return True
    else:
        return False


speed_step = 4


# score = 9
score_value = 0
font = pg.font.Font("freesansbold.ttf", 18)

textX = 10
textY = 10

def show_score(pos):
    score = font.render("score : " + str(score_value), True, (255, 255, 255, 0.5))
    screen.blit(score, pos)
    
    

level_value = 1
levelX = 10
levelY = 40

def show_level(pos):
    level = font.render("level : " + str(level_value), True, (255, 255, 255, 0.5))
    screen.blit(level, pos)


print("level" + str(level_value))

running = True

# Main loop
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pg.event.get():

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_SPACE:
                fire_bullet((bulletX, bulletY))
                bullet_sound = pg.mixer.Sound(r"game\music\laser.wav")
                bullet_sound.play()

            if event.key == pg.K_RIGHT and not playerX >= 736:
                steps_playerX = speed_step
            elif event.key == pg.K_LEFT and not playerX <= 0:
                steps_playerX = -speed_step
            if event.key == pg.K_DOWN and not playerY >= 536:
                steps_playerY = speed_step
            elif event.key == pg.K_UP and not playerY <= 200:
                steps_playerY = -speed_step

            if event.key == pg.K_ESCAPE:
                running = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                steps_playerX = 0
            if event.key == pg.K_DOWN or event.key == pg.K_UP:
                steps_playerY = 0

        elif event.type == pg.QUIT:
            running = False
            
        

    # if (posplayer):
    #     player(posplayer)
    # else:
    #     player((playerX, playerY))
    playerX += steps_playerX
    playerY += steps_playerY

    if playerX <= 0:
        playerX = 0
    elif playerX >= 738:
        playerX = 736
    if playerY <= 200:
        playerY = 200
    elif playerY >= 536:
        playerY = 536

    player((playerX, playerY))

    # ---

    for i in range(num_of_enemy):
        
        collision_wine = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        collision_lose = is_collision(enemyX[i], enemyY[i], playerX, playerY)

        if collision_wine and not collision_lose:
            explosion_sound = pg.mixer.Sound(r"game\music\explosion.wav")
            explosion_sound.play()
            score_value += 1
            print(score_value)
            bulletY = 0
            bullet_state = "ready"
            enemyX[i] = rd.randint(0, 736)
            enemyY[i] = rd.randint(0, 436)
            
            if score_value < 10:
                level_value = 1
            elif score_value == 10:
                level_value += 1
                print("level : " + str(level_value))
                list_step.append(7)
                create_enemy(1)
                num_of_enemy += 1
            elif score_value == 20:
                level_value += 1
                print("level : " + str(level_value))
                list_step.append(8)
                create_enemy(1)
                num_of_enemy += 1
            elif score_value == 30:
                level_value += 1
                print("level : " + str(level_value))
                list_step.append(9)
                create_enemy(2)
                num_of_enemy += 2
                speed_step += 2
                steps_bulletY += 2
            elif score_value == 40:
                level_value += 1
                print("level : " + str(level_value))
                list_step.append(10)
                create_enemy(2)
                num_of_enemy += 2
                speed_step += 2
                steps_bulletY += 2
            elif score_value == 50:
                level_value += 1
                print("level : " + str(level_value))
                running = False
                
        elif collision_lose:
            score_value //= 2
            enemyX[i] = rd.randint(0, 736)
            enemyY[i] = rd.randint(0, 436)
                
        enemyX[i] += steps_enemyX[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            steps_enemyX[i] = list_step[rd.randint(0, len(list_step) - 1)]
            enemyY[i] += steps_enemyY[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            steps_enemyX[i] = -list_step[rd.randint(0, len(list_step) - 1)]
            enemyY[i] += steps_enemyY[i]
        if enemyY[i] <= 0:
            enemyY[i] = 0
        elif enemyY[i] >= 436:
            enemyY[i] = 436

        enemy((enemyX[i], enemyY[i]))
    
    
    if bulletY <= 0:
        bulletX = playerX
        bulletY = playerY
        bullet_state = "raedy"

    if bullet_state is "fire":
        fire_bullet((bulletX, bulletY))
        bulletY -= steps_bulletY
    else:
        bulletX = playerX
        bulletY = playerY

    show_score((textX, textY))
    show_level((levelX, levelY))
    
    pg.display.update()

