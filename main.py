
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from collections import defaultdict
import pygame 
import requests
import json

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

url = 'https://pixelcorp.nl/api/single'
headers = {'Content-Type': 'application/json'}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
WINDOW_SIZE = (1920, 1080)
CEL_SIZE = 20
UPDATE_SPEED = 5
FPS = 30
CEL_SIZE = 1
UPDATE_SPEED = 1
FPS = 1

class Game():
	def __init__(self, window_size=(1920, 1080), celsize=20, update_speed=5, fps=60, borderless=False):
		self.celsize = celsize
		self.grid = [[0 for _ in range(0, window_size[0], celsize)] for _ in range(0, window_size[1], celsize)]
		self.living_cells = set()
		self.last_gen = set()
		self.last_generation_time = 0
		self.borderless = borderless
		self.update_speed = update_speed
		self.fps = fps
		self.pause = False
		self.clock = pygame.time.Clock()
		self.running = True
		self.living_cells.add((100, 100))
		self.living_cells.add((100, 101))
		self.living_cells.add((100, 102))

	def	handle_keypress(self, event):
		if event.key == pygame.K_ESCAPE:
			self.running = False
		elif event.key == pygame.K_SPACE:
			self.pause = not self.pause

	def	handle_mouse(self):
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			self.living_cells.add((pos[1] // self.celsize, pos[0] // self.celsize))
		elif pygame.mouse.get_pressed()[2]:
			pos = pygame.mouse.get_pos()
			self.living_cells.discard((pos[1] // self.celsize, pos[0] // self.celsize))

	def	handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				self.running = False
			if event.type == pygame.KEYDOWN:
				self.handle_keypress(event)
				
			self.handle_mouse()

	def render(self):
		self.draw_grid()
		self.draw_living_cells()
		pygame.display.flip()
	
	def draw_living_cells(self):
		for cell in self.living_cells:
			rect = pygame.Rect(cell[1] * self.celsize, cell[0] * self.celsize, self.celsize, self.celsize)
			pygame.draw.rect(self.screen, WHITE, rect)
 
	def draw_grid(self):
		for col in range(len(self.grid)):
			for row in range(len(self.grid[0])):
				rect = pygame.Rect(row * self.celsize, col * self.celsize, self.celsize, self.celsize)
				pygame.draw.rect(self.screen, GREY, rect, 1)

	def next_generation(self, borderless=False):
		'''
			- Initialize an empty set to store the coordinates of living cells.
			- For each living cell:
			- Add the cell's coordinates to the set.
			- For each of the cell's eight neighbors, increment a counter in a dictionary keyed by the neighbor's coordinates.
			- Initialize an empty set to store the coordinates of cells that will be alive in the next generation.
			- For each cell in the dictionary:
			- If the cell has exactly three neighbors, add it to the next generation set (birth rule).
			- If the cell is in the current generation set and has two or three neighbors, add it to the next generation set (survival rule).
			- Set the current generation set to the next generation set.
			- This approach reduces the number of cells you need to check, potentially improving performance for sparse grids. However, it may not be faster for dense grids where a large proportion of cells are alive.
		'''
		neighbor_counts = defaultdict(int)
		for cell in self.living_cells:
			for dx in [-1, 0, 1]:
				for dy in [-1, 0, 1]:
					if dx != 0 or dy != 0:
						if borderless or (cell[0] + dx >= 0 and cell[0] + dx < len(self.grid) and cell[1] + dy >= 0 and cell[1] + dy < len(self.grid[0])):
							neighbor = (cell[0] + dx, cell[1] + dy)
							neighbor_counts[neighbor] += 1
		next_gen = set()
		for cell, count in neighbor_counts.items():
			if count == 3 or (count == 2 and cell in self.living_cells):
				next_gen.add(cell)

		self.last_gen = self.living_cells
		self.living_cells = next_gen
		print(self.living_cells)
		print(self.last_gen)

	def take_step(self, update_speed=5):
		if pygame.time.get_ticks() - self.last_generation_time >= (1000 / update_speed):
			self.next_generation(self.borderless)
			self.last_generation_time = pygame.time.get_ticks()
		# if pygame.time.get_ticks() - self.last_generation_time >= (1000 / update_speed):
		self.clock.tick(self.fps) 
		self.next_generation(self.borderless)
		self.last_generation_time = pygame.time.get_ticks()

	def	run(self, print_controls=True):
		if print_controls:
			print("Controls:")
			print("  - Left click to add a cell")
			print("  - Right click to remove a cell")
			print("  - Space to pause")
			print("  - Escape to quit")
			print("  - Click the close button to quit")

		while self.running:
			self.take_step(self.update_speed)
			render_pixelcorp(self.living_cells, self.last_gen)

			# self.handle_events()
			# if not self.pause:
			# 	self.take_step(self.update_speed)
			# self.clock.tick(self.fps)
			# self.render()

pygame.init()
# screen = pygame.display.set_mode(WINDOW_SIZE) 
# pygame.display.set_caption("Tim's Game of Life") 

game = Game(WINDOW_SIZE, CEL_SIZE, UPDATE_SPEED, FPS, borderless=False)

def render_pixelcorp(living_cells, last_gen):
	for pos in last_gen:
		x, y = pos
		pixel = {'x': x, 'y': y, 'color': BLACK, 'key': 'OYUDJBMY' }
		response = requests.post(url, headers=headers, data=json.dumps(pixel))

	for pos in living_cells:
		x, y = pos
		pixel = {'x': x, 'y': y, 'color': WHITE, 'key': 'OYUDJBMY' }
		response = requests.post(url, headers=headers, data=json.dumps(pixel))

# pygame.init()
# screen = pygame.display.set_mode(WINDOW_SIZE) 
# pygame.display.set_caption("Tim's Game of Life") 

game = Game((200, 200), CEL_SIZE, UPDATE_SPEED, FPS, borderless=False)
game.run(print_controls=True)