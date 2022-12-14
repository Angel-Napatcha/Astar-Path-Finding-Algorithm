import pygame
import math
from queue import PriorityQueue

WIDTH = 500
GRID = 25
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("AStar Visualiser")

CLOSED = RED = (250,128,114)
OPEN = GREEN = (152,251,152)
DEFAULT = WHITE = (255, 255, 255)
BARRIER = BLACK = (0, 0, 0)
PATH = PURPLE = (230,230,250)
START = YELLOW = (255,215,0)
GREY = (128, 128, 128)
END = TURQUOISE = (64, 224, 208)

class Square:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.width = WIDTH // GRID
        self.x = row * self.width
        self.y = col * self.width
        self.state = DEFAULT
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.state, (self.x, self.y, self.width, self.width))

    def create_neighbors(self, table):
        if self.row < GRID - 1:
            if table[self.row + 1][self.col].state != BARRIER:  # DOWN
                self.neighbors.append(table[self.row + 1][self.col])
        if self.row > 0:
            if table[self.row - 1][self.col].state != BARRIER:  # UP
                self.neighbors.append(table[self.row - 1][self.col])
        if self.col < GRID - 1 and table[self.row][self.col + 1].state != BARRIER:  # RIGHT
            self.neighbors.append(table[self.row][self.col + 1])
        if self.col > 0 and table[self.row][self.col - 1].state != BARRIER:  # LEFT
            self.neighbors.append(table[self.row][self.col - 1])

def h(p1, p2):
    x1, y1 = p1.get_pos()
    x2, y2 = p2.get_pos()
    return math.floor(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

def create_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.state = PATH
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g = {sq: float('inf') for row in grid for sq in row}
    g[start] = 0
    f = {sq: float('inf') for row in grid for sq in row}
    f[start] = h(start, end)
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            create_path(came_from, end, draw)
            end.state = END
            start.state = START
            return
        for neighbor in current.neighbors:
            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.state = OPEN
        draw()
        if current != start:
            current.state = CLOSED
    return

def make_grid():
    grid = []
    for row in range(GRID):
        grid.append([])
        for col in range(GRID):
            sq = Square(row, col)
            grid[row].append(sq)
    return grid

def draw_grid(win):
    gap = WIDTH // GRID
    for line in range(GRID):
        pygame.draw.line(win, GREY, (0, line * gap), (WIDTH, line * gap))
        pygame.draw.line(win, GREY, (line * gap, 0), (line * gap, WIDTH))

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for col in row:
            col.draw(win)
    draw_grid(win)
    pygame.display.update()

def get_clicked_pos(pos):
    gap = WIDTH // GRID
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win):
    grid = make_grid()
    start = end = None
    run = True
    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                sq = grid[row][col]
                if not start and sq != end:
                    start = sq
                    start.state = START
                elif not end and sq != start:
                    end = sq
                    end.state = END
                elif sq != end and sq != start:
                    sq.state = BARRIER
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                sq = grid[row][col]
                sq.state = DEFAULT
                if sq == start:
                    start = None
                if sq == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for sq in row:
                            sq.create_neighbors(grid)
                    algorithm(lambda: draw(win, grid), grid, start, end)
                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid()

main(WIN)