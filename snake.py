from cube import cube
import pygame
import random
#numeric values for directions
LEFT = (-1, 0) 
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)

class snake(object):  
    body = []
    visited = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.visited.append(pos)

    def clear_visited(self):                        #clears all the visited cubes
        self.visited.clear()

    def update_dir(self, dirnx, dirny):             #changes the direction
        self.dirnx = dirnx
        self.dirny = dirny

    def move_body(self):                            #keeps the body moving
        for i, c in enumerate(self.body):
            p = c.pos[:]

            #If there is a turn
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction

    def move_with_mode(self, mode, snack):          #chooses the mode
    
        if   mode == "--keys":
            self.move_keys()
        elif mode == "--better-shortest":
            self.move_shortest_enhanced(snack)
        elif mode == "--shortest":
            self.move_shortest(snack)
        elif mode == "--hamiltonian":
            self.move_hamiltonian()
        else:
            self.move_keys()

    def body_to_list(self):                         #saves body into a list
        return list(map(lambda i: i.pos, self.body))
    def move_shortest(self, snack):                 #algorithm for shortest mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        currDir = (self.dirnx, self.dirny)
        rDist = (snack.distToCube(self.body[0].getRightCubeCoords()), RIGHT)
        lDist = (snack.distToCube(self.body[0].getLeftCubeCoords()), LEFT)
        upDist = (snack.distToCube(self.body[0].getUpCubeCoords()), UP)
        downDist = (snack.distToCube(self.body[0].getDownCubeCoords()), DOWN)

        if currDir == RIGHT:
            res = min([rDist, upDist, downDist], key = lambda i: i[0])[1]
        elif currDir == LEFT:
            res = min([lDist, upDist, downDist], key = lambda i: i[0])[1]
        elif currDir == UP:
            res = min([rDist, upDist, lDist], key = lambda i: i[0])[1]
        elif (currDir == DOWN):
            res = min([rDist, lDist, downDist], key = lambda i: i[0])[1]

        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_hamiltonian(self):                     #algorithm for hamiltonian mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        self.visited.append(self.head.pos)

        if self.head.pos == (0, 0):
            self.update_dir(UP[0], UP[1])
            self.clear_visited()
        elif self.head.pos[1] == 0:
            self.update_dir(LEFT[0], LEFT[1])

        elif self.head.pos == (27, 1):
            self.update_dir(DOWN[0], DOWN[1])

        elif ((self.head.pos[1] == 1 and self.head.getUpCubeCoords() in self.visited) or
            self.head.pos[1] ==27 and self.head.getDownCubeCoords() in self.visited):
            self.update_dir(RIGHT[0], RIGHT[1])

        elif self.head.pos[0] % 2 == 1:
            self.update_dir(DOWN[0], DOWN[1])

        elif self.head.pos[0] % 2 == 0:
            self.update_dir(UP[0], UP[1])


        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def move_shortest_enhanced(self, snack):        #algorithm for shortest enhanced mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            break
        

        lst = [(self.body[0].getRightCubeCoords(), RIGHT), (self.body[0].getLeftCubeCoords(), LEFT),
        (self.body[0].getUpCubeCoords(), UP), (self.body[0].getDownCubeCoords(), DOWN)]

        availible_dirs = list(filter(lambda i: i[0] not in self.body_to_list(), lst)) # list of girections to all possible shortest paths
        # Reduces bias in picking direction of snake when it cannot get closer to the snack

        random.shuffle(lst)

        # Snake has closed itself in. Choose any direction and restart
        if len(availible_dirs) == 0:# if there is no possible direction or is closed in a loop
            res = UP
        else: res = min(availible_dirs, key = lambda i: snack.distToCube(i[0]))[1]
        self.update_dir(res[0], res[1])
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()


    def move_keys(self):                            #to move the snake with keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.update_dir(-1, 0)

                elif keys[pygame.K_RIGHT]:
                    self.update_dir(1, 0)

                elif keys[pygame.K_UP]:
                    self.update_dir(0, -1)

                elif keys[pygame.K_DOWN]:
                    self.update_dir(0, 1)

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        self.move_body()

    def reset(self, pos):                           #resets all the values
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):                             #adds a cube to the body when collides with snack
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0: #if going right add a cube on left
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:#if going left add a cube to right
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:#if going up add a cube to down
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:#if going down add a cube above
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        # We then set the cubes direction to the direction of the snake.

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):                        #draws the body of the snake
        for i, c in enumerate(self.body):
            if i ==0:               # for first cude we want to draw eyes
                c.draw(surface, True)
            else:
                c.draw(surface)     #otherwise we will just draw a cube
