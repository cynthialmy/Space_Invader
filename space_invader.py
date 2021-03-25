import pygame
import random

pygame.init()

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0,0,0))
pygame.display.set_caption('Space Invaders')

#define fonts
font_small = pygame.font.SysFont('Arial', 30)
font_big = pygame.font.SysFont('Arial', 40)
#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
pink = (254, 52, 110)
blue = (0, 102, 255)
orange = (255, 153, 0)
#define game variable


alien_cooldown = 1000 #milliseconds
last_alien_shot = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()
game_over = 0 #0 is no game over, 1 means player has won, -1 means player has lost


#define function for creating text
def text_display(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((30, 20))
		self.image.fill(pink)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()

	def update(self):
		#set movement speed
		speed = 8
		#set a cooldown variable
		cooldown = 500 #milliseconds
		game_over = 0

		#get key press
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 20:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width+20:
			self.rect.x += speed
		if key[pygame.K_UP] and self.rect.top > 20:
			self.rect.y -= speed
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height+20:
			self.rect.y += speed

		#record current time
		time_now = pygame.time.get_ticks()
		#shoot
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			bullet = Bullets(self.rect.centerx, self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now

		#update mask for collision check
		self.mask = pygame.mask.from_surface(self.image)

		#draw health bar
		pygame.draw.rect(screen, red, (self.rect.x-5, (self.rect.bottom + 10), self.rect.width+10, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x-5, (self.rect.bottom + 10),
											 int((self.rect.width +10) * (self.health_remaining /
																	self.health_start)), 15))
		elif self.health_remaining <= 0:
			self.kill()
			game_over = -1
		return game_over

#create Bullets class
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 5))
		self.image.fill(orange)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()

#create Aliens class
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

#create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 5))
		self.image.fill(blue)
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y += 2
		if self.rect.top > screen_height:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			#reduce spaceship health
			spaceship.health_remaining -= 1

#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

#generate aliens
rows = 4
cols = 4
for row in range(rows):
	for item in range(cols):
		alien = Aliens(100 + item * 100, 100 + row * 70)
		alien_group.add(alien)


#create player
initial_health = 3
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, initial_health)
spaceship_group.add(spaceship)

run = True
while run:
	# define fps
	fps = 60
	clock = pygame.time.Clock()
	clock.tick(fps)
	#draw background
	screen.fill((0,0,0))

	#create random alien bullets
	#record current time
	time_now = pygame.time.get_ticks()
	#shoot
	if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
		attacking_alien = random.choice(alien_group.sprites())
		alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
		alien_bullet_group.add(alien_bullet)
		last_alien_shot = time_now

	#check if all the aliens have been killed
	if len(alien_group) == 0:
		game_over = 1

	if game_over == 0:
		#update spaceship
		game_over = spaceship.update()
		#update sprite groups
		bullet_group.update()
		alien_group.update()
		alien_bullet_group.update()
	else:
		if game_over == -1:
			text_display('GAME OVER >_<', font_big, pink,
						 int(screen_width / 2 - 160), int(screen_height / 2 + 50))
		if game_over == 1:
			text_display('YOU WIN ^_^', font_big, pink,
						 int(screen_width / 2 - 160), int(screen_height / 2 + 50))

	#draw sprite groups
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)

	#event handlers
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()
