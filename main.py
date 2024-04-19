from collections import defaultdict
import pygame 

# Define the background colour 
# using RGB color coding. 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)

window_size = (1800, 1200)

pygame.init()

# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode(window_size) 

# Set the caption of the screen 
pygame.display.set_caption("Tim's Game of Life") 

# Fill the background colour to the screen 
screen.fill(BLACK) 

class Game():
	def __init__(self, screen, window_size, celsize):
		self.screen = screen
		self.celsize = celsize
		self.grid = [[0 for _ in range(0, window_size[0], celsize[0])] for _ in range(0, window_size[1], celsize[1])]
		self.running = True
		self.window_size = window_size

	def	handle_keypress(self, event):
		if event.key == pygame.K_ESCAPE:
			self.running = False

	def	handle_mouse(self, event):
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			self.grid[pos[1] // self.celsize[0]][pos[0] // self.celsize[0]] = 1
		elif pygame.mouse.get_pressed()[2]:
			pos = pygame.mouse.get_pos()
			self.grid[pos[1] // self.celsize[0]][pos[0] // self.celsize[0]] = 0

	def	handle_events(self):
		for event in pygame.event.get():
			# Check for QUIT event	 
			if event.type == pygame.QUIT: 
				self.running = False

			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event)

			self.handle_mouse(event)

	def render(self):
		self.draw_grid()
		pygame.display.flip()
	
	def draw_grid(self):
		for col in range(len(self.grid)):
			for row in range(len(self.grid[0])):
				rect = pygame.Rect(row * self.celsize[0], col * self.celsize[0], self.celsize[0], self.celsize[1])
				if self.grid[col][row]:
					pygame.draw.rect(self.screen, WHITE, rect)
				else:
					pygame.draw.rect(self.screen, BLACK, rect)
					pygame.draw.rect(self.screen, GREY, rect, 1)

	def	run(self):
		while self.running:
			# for loop through the event queue 
			self.handle_events()
			self.render()
			
game = Game(screen, window_size, (25, 25))
game.run()

# An efficient way to implement Conway's Game of Life is to keep track of only the living cells and their neighbors. Instead of iterating over every cell in the grid, you only iterate over the living cells and their neighbors.

# Here's a high-level pseudocode of how you might implement this:

# Initialize an empty set to store the coordinates of living cells.
# For each living cell:
# Add the cell's coordinates to the set.
# For each of the cell's eight neighbors, increment a counter in a dictionary keyed by the neighbor's coordinates.
# Initialize an empty set to store the coordinates of cells that will be alive in the next generation.
# For each cell in the dictionary:
# If the cell has exactly three neighbors, add it to the next generation set (birth rule).
# If the cell is in the current generation set and has two or three neighbors, add it to the next generation set (survival rule).
# Set the current generation set to the next generation set.
# This approach reduces the number of cells you need to check, potentially improving performance for sparse grids. However, it may not be faster for dense grids where a large proportion of cells are alive.

# Here's how you might implement this in Python:

def next_generation(current_gen):
    neighbor_counts = defaultdict(int)
    for cell in current_gen:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    neighbor = (cell[0] + dx, cell[1] + dy)
                    neighbor_counts[neighbor] += 1

    next_gen = set()
    for cell, count in neighbor_counts.items():
        if count == 3 or (count == 2 and cell in current_gen):
            next_gen.add(cell)

    return next_gen

# In this code, current_gen is a set of tuples, where each tuple represents the coordinates of a living cell. The function next_generation calculates the next generation of living cells and returns it as a new set.