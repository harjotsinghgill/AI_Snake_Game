import pygame
global LEFT, RIGHT, UP, DOWN

class cube(object):
    rows = 28
    w = 700
    def __init__(self,start,dirnx=1,dirny=0,color=(0,150,0 )):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def distToCube(self, coord):                         #determines the distance between the head and snack
        return (abs(self.pos[0] - coord[0]) + abs(self.pos[1] - coord[1]), coord)

    def getRightCubeCoords(self):                        #coordinates of right cube
        return (self.pos[0] + 1, self.pos[1])

    def getLeftCubeCoords(self):                         #coordinates of left cube
        return (self.pos[0] - 1, self.pos[1])

    def getUpCubeCoords(self):                           #coordinates of above cube
        return (self.pos[0] , self.pos[1] + 1)

    def getDownCubeCoords(self):                         #coordinates of lower cube
        return (self.pos[0], self.pos[1] - 1)

    def move(self, dirnx, dirny):                        #moves the snake forward
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #change our position (updates coordinates of the self)                      #moves the snake

    def draw(self, surface, eyes=False):                 #customize the appearence of the snake
        dis = self.w // self.rows   #width/height of each cube
        i = self.pos[0]             #current row
        j = self.pos[1]             #current column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))#By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it
        if eyes:                    #draw the eyes
            centre = dis//2
            radius = 4
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            circleMiddle3 = (i*dis+2+centre-radius,j*dis+20)
            circleMiddle4 = (i*dis -2+ dis -radius*2, j*dis+20)

            pygame.draw.circle(surface, (255,51,51), circleMiddle, 5)
            pygame.draw.circle(surface, (255,51,51), circleMiddle2, 5)
            pygame.draw.circle(surface, (255,255,255), circleMiddle, 3)
            pygame.draw.circle(surface, (255,255,255), circleMiddle2, 3)
            pygame.draw.circle(surface, (0,0,0), circleMiddle3, 1)
            pygame.draw.circle(surface, (0,0,0), circleMiddle4, 1)

