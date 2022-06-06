import pygame
from pygame import  mixer,display,image,transform
from pygame import event,font
import random
import os

'''
           

'''
# ------------------------------------------------------------------------------------------------

"""
Author - Parth Arora
Purpose - Practice
"""

SCREENWIDTH = 1200
SCREENHEIGHT = 600
YELLOW = (255,255,0)
WHITE = (255,255,255)

class CarGame():
    """Base Class For Our Game"""
    def __init__(self) -> None:
        self.exitgame = False
        self.gameover = False
        self.clock = pygame.time.Clock()
        self.FPS = 70
        self.event = event
        self.welcomeimg =  image.load("welcome.jpg")
        self.welcomeimg =  transform.scale(self.welcomeimg,[SCREENWIDTH,SCREENHEIGHT])
        self.welcomesong = "poc.mp3"
        self.road1 = image.load("road.png")
        self.road2 = image.load("road.png")
        self.velocityroadY = 0
        self.yposroad = 0
        self.enemies = [

          
            (image.load("enimies\simple.png"),4),
             (image.load("enimies\medium.png"),6),
            (image.load("enimies\hard.png"),9),
            (image.load("enimies\crazy.png"),10),


        ]
        
        self.carOptions = [
            image.load("option1 car red.jpg"),
            image.load("option2 car.jpg"),
            image.load("option3 car.jpg")
        ]
        self.enemyx = random.randint(100,SCREENWIDTH-350)
        self.enemy = random.choice(self.enemies)
        self.enemyY = -SCREENHEIGHT
        self.velenemy = 0
        self.playerx = ((SCREENWIDTH/8))-100
        self.cars = {
        0: image.load("playeropition1.png"),
        1: image.load("playeroption2.png"),
        2: image.load("playerOption3.png")
        }
        self.gameovermp3 = "gameover.mp3"
        if os.path.exists("highscore(car).txt"):
            file = open("highscore(car).txt")
        else:
            file =  open("highscore(car).txt","w")
            file.write("0")
            file =  open("highscore(car).txt","r")
        self.hiscore = int(file.read())
        self.score = 0
        
        

        
    
    def playsound(self,sound,loop=0):
        """Used To Play The Sound"""
        mixer.init()
        mixer.music.load(sound)
        mixer.music.play(loops=loop)

    def displaytext(self,text,color,x,y,name="Headliner No. 45",size =55):
        """This Will blit The Text On The Game Window"""
        self.font = font.SysFont(name,size)
        screentext = self.font.render(text,True,color)
        gamewindow.blit(screentext,[x,y])

    def WelcomeScreen(self):
        """This Will Show The Welcome Screen"""
        self.playsound(self.welcomesong)
        while not self.exitgame:
            for event in self.event.get():
                if (event.type==pygame.QUIT):
                    self.exitgame=True

                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        self.exitgame=True

                    elif event.key==pygame.K_SPACE:
                        self.ChooseCar() 


            gamewindow.blit(self.welcomeimg,[0,0])
            display.update()
            self.clock.tick(self.FPS)

    def ChooseCar(self):
        """This Displays A Car Chooser Window"""
        img = 0
        CarOptions = self.carOptions
        while not self.exitgame:
            for event in self.event.get():
                if (event.type==pygame.QUIT):
                    self.exitgame=True

                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        self.exitgame=True
                        
                    elif event.key==pygame.K_RIGHT:
                        img += 1
                    elif event.key==pygame.K_LEFT:
                            img -=1

                    elif event.key==pygame.K_RETURN:
                        self.carselected = img
                        self.MainGame()

            try:
                gamewindow.blit(CarOptions[img],[0,0])
            except IndexError:
                img = 0

            display.update()
            self.clock.tick(self.FPS)

    def MainGame(self):
        """Here's The Logic For Our Main Game"""
        
        while not self.exitgame:
            

            if self.gameover:
                self.displaytext("GAME OVER!",WHITE,(SCREENWIDTH//2)-200,(SCREENHEIGHT//2)-10,size=100)
                self.displaytext("Press K To Continue",WHITE,(SCREENWIDTH//2)-200,(SCREENHEIGHT//2)+50,size=100)

                with open("highscore(car).txt","w") as file:
                    file.write(str(self.hiscore))


                for event in self.event.get():
                    if (event.type==pygame.QUIT):
                        with open("highscore(car).txt","w") as file:
                            file.write(str(self.hiscore))


                        self.exitgame=True

                    elif event.type==pygame.KEYDOWN:

                        if event.key==pygame.K_ESCAPE:
                            with open("highscore(car).txt","w") as file:
                                file.write(str(self.hiscore))

                            self.exitgame=True

                        elif event.key==pygame.K_k:
                            self.gameover = False
                            self.playerx = ((SCREENWIDTH/8))+150
                            self.playery = (SCREENHEIGHT-self.playerheight)-10
                            self.enemyY = -SCREENHEIGHT
                            self.score=0
                            self.MainGame()
                display.update()

            else:
                for event in self.event.get():
                    if (event.type==pygame.QUIT):
                        self.exitgame=True

                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_ESCAPE:
                            self.exitgame=True

                        elif event.key==pygame.K_LEFT:
                            self.playerx -=50

                        elif event.key==pygame.K_RIGHT:
                            self.playerx +=50

                        elif event.key:
                            self.velocityroadY = 2
                            self.velenemy = self.enemy[1]
                


                #Logic For Moving Road
                self.yposroad += self.velocityroadY      
                self.enemyY += self.velenemy    
                gamewindow.blit(self.road1,[0,self.yposroad])
                gamewindow.blit(self.road2,[0,self.yposroad-(SCREENHEIGHT-10)])

                if self.yposroad>SCREENHEIGHT:
                    self.yposroad = self.yposroad-SCREENHEIGHT
                    gamewindow.blit(self.road2,[0,self.yposroad-(SCREENHEIGHT-10)])
  
                #Logic For Player
                self.player = self.cars[self.carselected]
                self.playerheight = self.player.get_height()
                self.playerwidth = self.player.get_width()
                self.playery = (SCREENHEIGHT-self.playerheight)-10
                gamewindow.blit(self.player,[self.playerx,self.playery])
                

                #Logic For Enemies
                gamewindow.blit(self.enemy[0],[self.enemyx,self.enemyY])
                self.displaytext(f"Score : - {self.score} HighScore :- {self.hiscore}",WHITE,10,10,size=40)
                

                if self.enemyY>SCREENHEIGHT:
                    self.enemyY = -SCREENHEIGHT
                    self.enemyx = random.randint(100,SCREENWIDTH-350)
                    self.enemy = random.choice(self.enemies)
                    self.velenemy = self.enemy[1]
                    gamewindow.blit(self.enemy[0],[self.enemyx,self.enemyY])


                #Logic For Collison With Wall
                if (self.playerx>(SCREENWIDTH-400)) or (self.playerx<-120):
                    self.gameover = True
                #Logic for two cars collison
                # For Y coords:
                #10 9 6 4 TODO: All Veocities
                #For Difffernt Cars different Conditions (Matching Velocities With Cars )


                # RHS AND LHS OF PLAYER"S SIDE LOGIC
                elif  ((self.playerx>(SCREENWIDTH-400)) or (self.playerx<-120))==False:
                    #LOgic For LHS LOGIC
                    if self.enemyx>self.playerx:
                        if self.velenemy==10:
                            if abs(self.playery-self.enemyY)<290 and abs(self.playerx-self.enemyx)<240:
                                self.gameover=True
                            else:
                                self.gameover = False

                        elif self.velenemy==9:
                            if abs(self.playery-self.enemyY)<280 and abs(self.playerx-self.enemyx)<260:
                                self.gameover=True
                            else:
                                self.gameover = False

                        elif self.velenemy==4:
                            if abs(self.playery-self.enemyY)<400 and abs(self.playerx-self.enemyx)<250:
                                self.gameover=True
                            else:
                                self.gameover = False
                    
                        elif self.velenemy==6:
                            if abs(self.playery-self.enemyY)<390 and abs(self.playerx-self.enemyx)<293:
                                self.gameover=True
                            else:
                                self.gameover = False

                    # lOGIC FOR RHS (RIGHT HAND SIDE)
                    elif self.playerx>self.enemyx:
                        
                        if self.velenemy==10:
                            if abs(self.playery-self.enemyY)<290 and abs(self.playerx-self.enemyx)<22:
                                self.gameover=True
                            else:
                                self.gameover = False

                        elif self.velenemy==9:
                            if abs(self.playery-self.enemyY)<280 and abs(self.playerx-self.enemyx)<20:
                                self.gameover=True
                            else:
                                self.gameover = False

                        elif self.velenemy==4:
                            if abs(self.playery-self.enemyY)<400 and abs(self.playerx-self.enemyx)<80:
                                self.gameover=True
                            else:
                                self.gameover = False
                    
                        elif self.velenemy==6:
                            if abs(self.playery-self.enemyY)<390 and abs(self.playerx-self.enemyx)<3:
                                self.gameover=True
                            else:
                                self.gameover = False
                if not self.gameover:
                    if self.velocityroadY==0:
                        pass
                    else:
                        self.score += 1

                if self.score>self.hiscore:
                    self.hiscore =  self.score

                display.update()
                self.clock.tick(self.FPS)

                

            

if __name__=='__main__':   
    pygame.init()
    mixer.init()
    gamewindow = display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    display.set_caption("Cars - By Parth")
    display.set_icon(image.load("car.ico"))
    app = CarGame()                                       
    app.WelcomeScreen()
    pygame.quit()
    quit()

    

