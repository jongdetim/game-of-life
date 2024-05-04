os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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
	def __init__(self, screen, window_size=(1920, 1080), celsize=20, update_speed=5, fps=60, borderless=False):
		self.screen = screen
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
@@ -94,12 +105,16 @@ def next_generation(self, borderless=False):
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
@@ -111,15 +126,27 @@ def	run(self, print_controls=True):
			print("  - Click the close button to quit")

		while self.running:
			self.handle_events()
			if not self.pause:
				self.take_step(self.update_speed)
			self.clock.tick(self.fps)
			self.render()

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE) 
pygame.display.set_caption("Tim's Game of Life") 

game = Game(screen, WINDOW_SIZE, CEL_SIZE, UPDATE_SPEED, FPS, borderless=False)
			# self.handle_events()
			# if not self.pause:
			self.take_step(self.update_speed)
			# self.clock.tick(self.fps)
			# self.render()
			render_pixelcorp(self.living_cells, self.last_gen)

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

game = Game("haha lol", (200,200), CEL_SIZE, UPDATE_SPEED, FPS, borderless=False)
game.run(print_controls=True)