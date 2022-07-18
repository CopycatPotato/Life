import random
import pygame

PIX = 10
WIDTH = 52 * PIX 
HEIGHT = 52 * PIX 
FOOD = {0: [1], 1: [2], 2: []}
KILL = {0: [], 1: [], 2: [0]}
COLOR = {0: (64, 128, 255), 1: (255, 194, 134), 2: (134, 255, 134)}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life")
clock = pygame.time.Clock()
ocean = [[' ' for i in range(50)] for j in range(50)]

class entity:
    def __init__(self, ID, x, y, food = [], clicked = 0, kill = [], health = 80):
        self.ID = ID
        self.health = health
        self.pos = (x, y)
        self.food = food
        self.kill = kill
        ocean[x][y] = self
        if clicked:
            if x + 1 < 50 and ocean[x + 1][y] != '.':
                entity(ID, x + 1, y, FOOD[ID], 0, KILL[ID])
            if x - 1 >= 0 and ocean[x - 1][y] != '.':
                entity(ID, x - 1, y, FOOD[ID], 0, KILL[ID])
            if y + 1 < 50 and ocean[x][y + 1] != '.':
                entity(ID, x, y + 1, FOOD[ID], 0, KILL[ID])
            if y - 1 >= 0 and ocean[x][y - 1] != '.':
                entity(ID, x, y - 1, FOOD[ID], 0, KILL[ID])
    def getCells(self):
        free = []
        food = []
        enemies = []
        friends = []
        i, j = self.pos
        cells = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        for i in cells:
            if valid(i):
                if ocean[i[0]][i[1]] == ' ':
                    free.append(i)
                elif ocean[i[0]][i[1]] not in [' ', '.']:
                    if ocean[i[0]][i[1]].ID in self.food:
                        food.append(ocean[i[0]][i[1]])
                    elif ocean[i[0]][i[1]].ID in self.kill:
                        enemies.append(ocean[i[0]][i[1]])  
                    elif ocean[i[0]][i[1]].ID == self.ID:
                        friends.append(ocean[i[0]][i[1]])
        return [free, friends, food, enemies]

def valid(pos):
    return pos[0] >= 0 and pos[0] < 50 and pos[1] >= 0 and pos[1] < 50 

def draw():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 52 * PIX, PIX))
    for i in range(0, 50):
        pygame.draw.rect(screen, (0, 0, 0), (0, PIX + i * PIX, PIX, 2 * PIX + i * PIX))
        for j in range(0, 50):
            if ocean[i][j] not in [' ', '.']:
                pygame.draw.rect(screen, COLOR[ocean[i][j].ID], (PIX + j * PIX, PIX + i * PIX, 2 * PIX + j * PIX, 2 * PIX + i * PIX))
            elif ocean[i][j] == '.':
                pygame.draw.rect(screen, (0, 0, 0), (PIX + j * PIX, PIX + i * PIX, 2 * PIX + j * PIX, 2 * PIX + i * PIX))
            elif ocean[i][j] == ' ':
                pygame.draw.rect(screen, (255, 255, 255), (PIX + j * PIX, PIX + i * PIX, 2 * PIX + j * PIX, 2 * PIX + i * PIX))
        pygame.draw.rect(screen, (0, 0, 0), (51 * PIX, PIX + i * PIX, 52 * PIX, 2 * PIX + i * PIX))
    pygame.draw.rect(screen, (0, 0, 0), (0, 51 * PIX, 52 * PIX, 52 * PIX))
    pygame.display.flip()
    
def redraw():
    for i in range(500):
        ocean[random.randint(0,49)][random.randint(0,49)] = '.'
        
run = True
pause = True
redraw()

while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False    
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not(pause)
                if event.key == pygame.K_c:
                    ocean = [[' ' if ocean[j][i] != '.' else ocean[j][i] for i in range(50)] for j in range(50)]
                if event.key == pygame.K_r:
                    ocean = [[' ' for i in range(50)] for j in range(50)]
                    redraw()
            press = pygame.mouse.get_pressed()
            y, x = pygame.mouse.get_pos()
            X, Y = x // PIX - 1, y // PIX - 1
            if valid((X, Y)):
                if press[1]:
                    ocean[X][Y] = '.' if ocean[X][Y] != '.' else ' '
                elif press[0] and press[2] and ocean[X][Y] != '.':
                    entity(2, X, Y , FOOD[2], 1, KILL[2])
                elif press[0] and ocean[X][Y] != '.':
                    entity(0, X, Y, FOOD[0], 1, KILL[0])
                elif press[2] and ocean[X][Y] != '.':
                    entity(1, X, Y, FOOD[1], 1, KILL[1])
    draw()
    if not(pause):
        for i in range(50):
            for j in range(50):
                obj = ocean[i][j]
                if obj not in [' ', '.']:
                    free, friends, food, enemies = obj.getCells()
                    x, y = obj.pos
                    for friend in friends:
                        _free, _friends, _food, _enemies = friend.getCells()
                        _x, _y = friend.pos
                        if random.randint(0, 9) == 1 and friend.health > 15 and obj.health > 15:
                            freeCells = free + _free
                            if freeCells:
                                pos = random.choice(freeCells)
                                newHealth = friend.health + obj.health
                                entity(obj.ID, pos[0], pos[1], FOOD[obj.ID], 0, KILL[obj.ID], min(35, newHealth))
                                if obj.food:
                                    ocean[_x][_y].health -= max(friend.health // 10, 1)
                                    ocean[x][y].health -= max(obj.health // 10, 1)   
                    flag = False
                    for x_x in food:
                        ocean[x_x.pos[0]][x_x.pos[1]] = ' '     
                        ocean[x][y].health += 1
                        flag = True
                    for x_x in enemies:
                        if random.randint(0,4) == 1:
                            ocean[x_x.pos[0]][x_x.pos[1]] = ' '                          
                    if len(friends) not in [2, 3, 4] or obj.health < 1:
                        ocean[x][y] = ' '
                    elif not(flag) and obj.food:
                        ocean[x][y].health -= 1
                        