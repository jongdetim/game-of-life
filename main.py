# import the pygame module 
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

# Update the display using flip 
# pygame.display.flip()

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