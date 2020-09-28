import pygame, sys, random, time
import Tkinter as tk
from Tkinter import *


pygame.init()

##########################################################################

display_width = 500
display_height = 500
NORM_FONT = ("Verdana",12)
black = (0,0,0)
white = (255,255,255)
red = (140,8,8)
green = (8,140,10)
yellow = (209,209,8)
blue = (66,92,244)
bright_green =(137,244,66)
bright_yellow = (239,239,98)
bright_red = (226,77,61)
gray = (0,0,255)

#DISPLAY SETTINGS
display =  pygame.display.set_mode((display_width,display_height))      #Sets a screen of a 500x500 pixel size
pygame.display.set_caption("SNAKE XENZIA")
fps = pygame.time.Clock()                           #Checks the speed of the SNAKE
clock = pygame.time.Clock()


pygame.mixer.music.load("snake_music.wav")
loser = pygame.mixer.Sound("loser.wav")
score_point = pygame.mixer.Sound("score.wav")
############################################################################
#MAIN MENU SCREEN
#GAME SETTINGS

def game_intro():

    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(white)


        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects("SNAKE XENZIA", largeText)
        TextRect.center = ((display_width/2),(display_height/8))
        display.blit(TextSurf, TextRect)

        button("Noob",100,150,100,50,green,bright_green,game_play)
        button("Pro",300,150,100,50,green,bright_green,game_start)
        button("Instructions",200,250,100,50,yellow,bright_yellow,instructions)
        button("Quit",200,350,100,50,red,bright_red,quitgame)

        pygame.display.update()
        fps.tick(15)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    display.blit(textSurf, textRect)

def instructions():
  popup = tk.Tk()
  popup.wm_title("INSTRUCTIONS")
  msg = "CONTROLS\n Use UP arrow key to move up. \n Use DOWN arrow key to move down. \n Use RIGHT and LEFT arrow keys to move right and left respectively.\n\n Level : NOOB \n\n The snake can pass through the boundaries of the walls and emerge from the other side. Gameplay ends only if snake eats itself.\n\nLevel : PRO \n\n The snake dies on hitting the boundaries of the wall. The gameplay also ends if snake eats itself."
  label = tk.Label(popup, text=msg, font=NORM_FONT)
  label.pack(side="top", fill="x", pady=10)
  B1 = tk.Button(popup, text="Okay", command = popup.destroy)
  B1.pack()
  popup.mainloop()


def quitgame():
  sys.exit()

def gameOver():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(loser)
    popup = tk.Tk()
    popup.wm_title("STATUS")
    msg = ("Your Score : "+ str( score) )
    label = tk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", padx=50, pady=50)
    B1 = tk.Button(popup, text="QUIT", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    sys.exit()					#Shuts the game we are playing


############################################################################
#LEVEL PRO
class Snake():

    def __init__(self):
        self.position = [100,40]               #Initial position of the Snake
        self.body = [[100,40],[80,40],[60,40]] #Initial length of the body [x,y]
        self.direction = "RIGHT"               #Initial direction
        self.changeDirection = self.direction  #To change the direction

    def changeDir(self,direction):             #Created a method to change the direction of snake
        if direction == "RIGHT" and not self.direction == "LEFT" :
            self.direction = "RIGHT"
        if direction == "LEFT" and not self.direction == "RIGHT" :
            self.direction = "LEFT"
        if direction == "UP" and not self.direction == "DOWN" :
            self.direction = "UP"
        if direction == "DOWN" and not self.direction == "UP" :
            self.direction = "DOWN"

    def move(self, foodPos):                    #Created the movement co-ordinate changes
        if self.direction == "RIGHT":           #If moved to right x-coordinate in list increases by 20 units
            self.position[0] += 20
        if self.direction == "LEFT":            #If moved to left x-coordinate in list decreases by 20 units
            self.position[0] -= 20
        if self.direction == "UP":              #If moved up y-coordinate in list decreases by 20 units
            self.position[1] -= 20
        if self.direction == "DOWN":            #If moved down y-coordinate in list increases by 20 units
            self.position[1] += 20

        self.body.insert(0,list(self.position))

        if self.position[0]+5 == foodPos[0] and self.position[1]+5 == foodPos[1] :
            return 1
        else :
            self.body.pop()
            return 0

    def checkCollision(self):                    #Checks whether the snake collides with wall or itself
        if self.position[0] > 460 or self.position[0] < 20 or self.position[1] > 460 or self.position[1] < 20:
            return 1

        for bodyPart in self.body[1:] :          #Checks whether the head collides with the body
            if self.position == bodyPart :
                return 1
        return 0

    def getHeadPos(self):                        #Just to detect the position of head
        return self.position

    def getBody(self):                           #Just meant as a reference for body pos.
        return self.body


class FoodSpawn():
    def __init__(self):                           #Initialise with random food position
        self.position = [random.randrange(2,24)*20+5, random.randrange(2,24)*20+5]
        self.isFoodOnScreen = True

    def spawnFood(self):                           #Regenerates food when there isnt any on the screen
        if self.isFoodOnScreen == False :
            self.position = [random.randrange(2,24)*20+5, random.randrange(2,24)*20+5]
            self.isFoodOnScreen = True
        return self.position

    def respawnFood(self,boolean):                      #Tells the foodSpawner that we ate the food and there is not any on screen
        self.isFoodOnScreen =  boolean

##################################################################################################

snake = Snake()
foodSpawner = FoodSpawn()

###################################################################################################
#GAME INITIALISER FOR LEVEL PRO

def game_start():
  global score
  score = 0
  pygame.mixer.music.play(-1)
  while True :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                #GAMEOVER Call
            gameOver()
        elif event.type == pygame.KEYDOWN:          #Module containing functions for dealing with keyboard
            if event.key == pygame.K_RIGHT:
                snake.changeDir("RIGHT")
            if event.key == pygame.K_LEFT:
                snake.changeDir("LEFT")
            if event.key == pygame.K_UP:
                snake.changeDir("UP")
            if event.key == pygame.K_DOWN:
                snake.changeDir("DOWN")

    foodPos = foodSpawner.spawnFood()               #Spawns the food

    if (snake.move(foodPos) == True):
        score += 1
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(score_point)
        pygame.mixer.music.unpause()

        foodSpawner.respawnFood(False)

    display.fill(pygame.Color(0,0,0))             #BG Color
    pygame.draw.rect(display, gray, [0,0,500,20])
    pygame.draw.rect(display, gray, [0,0,20,500])
    pygame.draw.rect(display, gray, [480,0,20,500])
    pygame.draw.rect(display, gray, [0,480,500,20])

#######################################################################################################
#Draws the rows and columns for the game
    for x in range(25 + 1):
        startx = (x * 20)
        starty = 0
        endx = (x * 20)
        endy = (25 * 20)
        pygame.draw.line(display, (7,7,7), (startx, starty), (endx, endy))

    for y in range(25 + 1):
        startx = 0
        starty = (y * 20)
        endx = (25 * 20)
        endy = (y * 20)
        pygame.draw.line(display, (7,7,7), (startx, starty), (endx, endy))

######################################################################################################

    for position in snake.getBody():                #Draws the body of the snake with a circle using a given position
        pygame.draw.circle(display, pygame.Color(0,225,0),(position[0]+10, position[1]+10), 10)

    pygame.draw.rect(display, pygame.Color(225,0,0), pygame.Rect(foodPos[0],foodPos[1], 10, 10))          #Draws the food

    if (snake.checkCollision() == 1 ):           #Close the game when collides with anything
        gameOver()

    pygame.display.set_caption("SNAKE XENZIA ||| SCORE : "+ str(score))

    pygame.display.flip()                           #Refreshes the full display Surface to the screen
    fps.tick(10)                                    #Controls the fps


#########################################################################################################
#LEVEL PRO
class Snake_l1():

    def __init__(self):
        self.position = [100,40]               #Initial position of the Snake
        self.body = [[100,40],[80,40],[60,40]] #Initial length of the body [x,y]
        self.direction = "RIGHT"               #Initial direction
        self.changeDirection = self.direction  #To change the direction

    def changeDir(self,direction):             #Created a method to change the direction of snake
        if direction == "RIGHT" and not self.direction == "LEFT" :
            self.direction = "RIGHT"
        if direction == "LEFT" and not self.direction == "RIGHT" :
            self.direction = "LEFT"
        if direction == "UP" and not self.direction == "DOWN" :
            self.direction = "UP"
        if direction == "DOWN" and not self.direction == "UP" :
            self.direction = "DOWN"


    def move(self, foodPos):                    #Created the movement co-ordinate changes
        if self.direction == "RIGHT":           #If moved to right x-coordinate in list increases by 20 units
            self.position[0] += 20
        if self.direction == "LEFT":            #If moved to left x-coordinate in list decreases by 20 units
            self.position[0] -= 20
        if self.direction == "UP":              #If moved up y-coordinate in list decreases by 20 units
            self.position[1] -= 20
        if self.direction == "DOWN":            #If moved down y-coordinate in list increases by 20 units
            self.position[1] += 20

        self.body.insert(0,list(self.position))

        if self.position[0]+5 == foodPos[0] and self.position[1]+5 == foodPos[1] :
            return 1
        else :
            self.body.pop()
            return 0

    def checkCollision(self):                    #Checks whether the snake moves through the wall or itself

	if self.position[1] < 0 and self.direction=="UP":
			self.position[1]=500
	if self.position[1] > 480 and self.direction=="DOWN":
			self.position[1]=-20
	if self.position[0] < 0 and self.direction=="LEFT":
			self.position[0]=500
	if self.position[0] > 480 and self.direction=="RIGHT":
			self.position[0]=-20

        for bodyPart in self.body[1:] :          #Checks whether the head collides with the body
            if self.position == bodyPart :
                return 1
        return 0

    def getHeadPos(self):                        #Just to detect the position of head
        return self.position

    def getBody(self):                           #Just meant as a reference for body pos.
        return self.body

class FoodSpawn_l1():
    def __init__(self):                           #Initialise with random food position
        self.position = [random.randrange(1,25)*20+5, random.randrange(1,25)*20+5]
        self.isFoodOnScreen = True

    def spawnFood(self):                           #Regenerates food when there isnt any on the screen
        if self.isFoodOnScreen == False :
            self.position = [random.randrange(1,25)*20+5, random.randrange(1,25)*20+5]
            self.isFoodOnScreen = True
        return self.position

    def respawnFood(self,boolean):                      #Tells the foodSpawner that we ate the food and there is not any on screen
        self.isFoodOnScreen =  boolean


######################################################################################################################
snake_noob = Snake_l1()
foodSpawner_noob = FoodSpawn_l1()
######################################################################################################################

#DEFINING GAMEPLAY SET FOR PRO MODE
def game_play():

  global score
  score = 0
  pygame.mixer.music.play(-1)
  while True :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                #GAMEOVER Call
            gameOver()
        elif event.type == pygame.KEYDOWN:          #Module containing functions for dealing with keyboard
            if event.key == pygame.K_RIGHT:
                snake_noob.changeDir("RIGHT")
            if event.key == pygame.K_LEFT:
                snake_noob.changeDir("LEFT")
            if event.key == pygame.K_UP:
                snake_noob.changeDir("UP")
            if event.key == pygame.K_DOWN:
                snake_noob.changeDir("DOWN")

    foodPos = foodSpawner_noob.spawnFood()               #Spawns the food

    if (snake_noob.move(foodPos) == True):
        score += 1
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(score_point)
        pygame.mixer.music.unpause()

        foodSpawner_noob.respawnFood(False)

    display.fill(pygame.Color(0,0,0))             #BG Color
######################################################################################################
#Draws the rows and columns for the game

    for x in range(25 + 1):
        startx = (x * 20)
        starty = 0
        endx = (x * 20)
        endy = (25 * 20)
        pygame.draw.line(display, (7,7,7), (startx, starty), (endx, endy))

    for y in range(25 + 1):
        startx = 0
        starty = (y * 20)
        endx = (25 * 20)
        endy = (y * 20)
        pygame.draw.line(display, (7,7,7), (startx, starty), (endx, endy))
######################################################################################################
    for position in snake_noob.getBody():                #Draws the body of the snake_noob with a circle using a given position
        pygame.draw.circle(display, pygame.Color(0,225,0),(position[0]+10, position[1]+10), 10)

    pygame.draw.rect(display, pygame.Color(225,0,0), pygame.Rect(foodPos[0],foodPos[1], 10, 10))          #Draws the food

    if (snake_noob.checkCollision() == 1 ):           #Close the game when collides with anything
        gameOver()

    pygame.display.set_caption("SNAKE XENZIA ||| SCORE : "+ str(score))

    pygame.display.flip()                           #Refreshes the full display Surface to the screen
    fps.tick(10)                                    #Controls the fps

###########################################################################################################
game_intro()                        #Call to begin the game
