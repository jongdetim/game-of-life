import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from collections import defaultdict
import pygame
import asyncio
import aiohttp
import json

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

url = 'https://pixelcorp.nl/api/single'
headers = {'Content-Type': 'application/json'}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
WINDOW_SIZE = (200, 200)
CEL_SIZE = 1
UPDATE_SPEED = 5
FPS = 3

class Game:
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
		self.living_cells.add((103, 103))
		self.living_cells.add((103, 104))
		self.living_cells.add((101, 105))
		self.living_cells.add((101, 100))
		self.living_cells.add((103, 102))
		self.living_cells.add((104, 102))
		self.living_cells.add((110, 110))
		self.living_cells.add((110, 111))
		self.living_cells.add((110, 112))
		self.living_cells.add((113, 113))
		self.living_cells.add((113, 114))
		self.living_cells.add((111, 112))
		self.living_cells.add((111, 109))
		self.living_cells.add((113, 112))
		self.living_cells.add((114, 112))
		self.living_cells.add((50, 49))
		self.living_cells.add((50, 50))
		self.living_cells.add((49, 48))
		self.living_cells.add((48, 48))
		self.living_cells.add((50, 48))
		self.living_cells.add((48, 52))
		self.living_cells.add((52, 51))
		self.living_cells.add((50, 52))
		self.living_cells.add((48, 47))

	def handle_keypress(self, event):
		if event.key == pygame.K_ESCAPE:
			self.running = False
		elif event.key == pygame.K_SPACE:
			self.pause = not self.pause

	def handle_mouse(self):
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			self.living_cells.add((pos[1] // self.celsize, pos[0] // self.celsize))
		elif pygame.mouse.get_pressed()[2]:
			pos = pygame.mouse.get_pos()
			self.living_cells.discard((pos[1] // self.celsize, pos[0] // self.celsize))

	async def handle_events(self):
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

	def take_step(self, update_speed=5):
		self.clock.tick(self.fps) 
		self.next_generation(self.borderless)

	async def run(self, print_controls=True):
		if print_controls:
			print("Controls:")
			print("  - Left click to add a cell")
			print("  - Right click to remove a cell")
			print("  - Space to pause")
			print("  - Escape to quit")
			print("  - Click the close button to quit")

		async with aiohttp.ClientSession() as session:
			# await paint_canvas_black_semaphore(session)
			while self.running:
				self.take_step(self.update_speed)
				await render_pixelcorp(session, self.living_cells, self.last_gen)

async def paint_canvas_black(session):
	async def send_pixel(pixel):
		async with session.post(url, headers=headers, data=json.dumps(pixel)) as response:
			pass  # No need to wait for response

	tasks = []
	for x in range(0, WINDOW_SIZE[0], CEL_SIZE):
		for y in range(0, WINDOW_SIZE[1], CEL_SIZE):
			pixel = {'x': x, 'y': y, 'color': BLACK, 'key': 'OYUDJBMY'}
			task = send_pixel(pixel)
			tasks.append(task)

	print("painting canvas black")
	await asyncio.gather(*tasks)
	print("finished painting canvas black")

async def paint_canvas_black_semaphore(session):
    async def send_pixel(pixel):
        async with sem:
            async with session.post(url, headers=headers, json=pixel) as _:
                pass  # No need to wait for response

    sem = asyncio.Semaphore(10000)  # Adjust the semaphore limit as needed
    tasks = []
    for x in range(0, WINDOW_SIZE[0], CEL_SIZE):
        for y in range(0, WINDOW_SIZE[1], CEL_SIZE):
            pixel = {'x': x, 'y': y, 'color': BLACK, 'key': 'OYUDJBMY'}
            tasks.append(send_pixel(pixel))

    print("painting canvas black")
    await asyncio.gather(*tasks)
    print("finished painting canvas black")


async def render_pixelcorp(session, living_cells, last_gen):
	async def send_pixel(pixel):
		async with session.post(url, headers=headers, data=json.dumps(pixel)) as response:
			# if response.status != 200:
			# 	print(f"Failed to send pixel: {response.status}")
			# else:
			# 	print(f"Sent {pixel['color']} pixel at ({pixel['x']}, {pixel['y']})")
			pass

	tasks = []
	for pos in last_gen:
		if pos not in living_cells:
			x, y = pos
			pixel = {'x': x, 'y': y, 'color': BLACK, 'key': 'OYUDJBMY'}
			task = send_pixel(pixel)
			tasks.append(task)
	await asyncio.gather(*tasks)

	tasks = []
	for pos in living_cells:
		if pos not in last_gen:
			x, y = pos
			pixel = {'x': x, 'y': y, 'color': WHITE, 'key': 'OYUDJBMY'}
			task = send_pixel(pixel)
			tasks.append(task)
	await asyncio.gather(*tasks)

pygame.init()

game = Game((200, 200), CEL_SIZE, UPDATE_SPEED, FPS, borderless=False)
loop = asyncio.get_event_loop()
loop.run_until_complete(game.run(print_controls=True))
