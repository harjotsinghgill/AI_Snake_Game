import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from snake import snake
from cube import cube
import sys

def drawGrid(w, rows, surface):         # draws the grid
    sizeBtwn = w // rows                # size of squares that is round off to non decimals

    x = 0   # Keeps track of the current x
    y = 0   # Keeps track of the current y
    for l in range(rows):   # We will draw one vertical and one horizontal line each loop
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (155, 155, 155), (x, 0), (x, w))  #draws line on the surface along y axis 
        pygame.draw.line(surface, (155, 155, 155), (0, y), (w, y))  #draws line on the surface allong x axis


def redrawWindow(surface):              # refreshes the screen
    global rows, width, s, snack  # global rows and width
    surface.fill((150,150,150))   #background color
    s.draw(surface)               #draws the snake body
    snack.draw(surface)           #draws the snack
    drawGrid(width,rows, surface)       
    pygame.display.update()       #updates the pygame             

def randomSnack(rows, item):            # random snack

    positions = item.body

    while True:                   # Keep generating random positions until we get a valid one
        x = random.randrange(rows)# random x coordinate foe snack
        y = random.randrange(rows)# random y coordinate for snack
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:# This wll check if the position we generated is occupied by the snake
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):      # generates the message box
    root = tk.Tk()

    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.withdraw()
    try:
        root.destroy()
    except:
        pass

def game_over(s, argv):                 #performs resets when player loses
    print('Score: ', len(s.body))
    s.clear_visited() #clears all visited cubes

def main(argv):                         #the main game loop
    global width, rows, s, snack, scores
    width = 700    #width of the pygame window
    scores = []
    rows = 28

    win = pygame.display.set_mode((width, width))       #window in which its is goin  to be
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(255,51,51)) # calls random snack func to create a random snack
    flag = True
    redrawWindow(win)
    clock = pygame.time.Clock()
    count = 0

    #speed controls
    while flag and count < 50:
        pygame.time.delay(0)       #This will delay the game so it doesn't run too quickly lower this goes faster its gonna be
        clock.tick(1000000)              #Frames Per Second   lower this goes slower its gonna be
        s.move_with_mode(argv[0], snack)
        if s.body[0].pos == snack.pos:# Checks if the head collides with the snack
            s.add_cube()# adds the cube to snake
            snack = cube(randomSnack(rows, s), color=(255,51,51))# creates a new snack object
        # if snake fills entire grid
        if len(s.body) == rows*rows-1:
            message_box('You Won!', 'YOU WON!!!')
            s.reset((14,14))
            game_over(s, argv)
            count = count + 1
            break
        # Lose from collision with wall
        for x in range(len(s.body)):
            if ((s.body[0].pos[0] == -1) or
            (s.body[0].pos[0] == rows) or
            (s.body[0].pos[1] == -1) or
            (s.body[0].pos[1] == rows)):
                message_box('You Lost!!!', 'Play again...')
                
                game_over(s, argv)
                count = count + 1
                s.reset((14,14))
                break
        redrawWindow(win)

        # Lose by collision with body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                message_box('You Lost!!!', 'Play again...')
                
                
                game_over(s, argv)
                count = count + 1
                s.reset((14,14)) 
                break


        redrawWindow(win)

if __name__ == "__main__":
   main(sys.argv[1:])
