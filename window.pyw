import pygame
import time
import sys


#pygame basic settings
pygame.init()
pygame.font.init()

screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Athena")

#import graphic and display background ones
background_img = pygame.image.load('media/background.png')
background_img = pygame.transform.scale(background_img,(screen_width,screen_height))
healthbar_img = pygame.image.load('media/healthbar.png')
healthbar_img = pygame.transform.scale(healthbar_img,(450,150))
platform_img = pygame.image.load('media/platform.png')
platform1 = pygame.transform.scale(platform_img,(750,40))
platform2= pygame.transform.scale(platform_img,(380,40))

platform1rect = platform1.get_rect()
platform1rect.x,platform1rect.y= 410,600

platform2rect = platform2.get_rect()
platform2rect.x,platform2rect.y= 250,400

platform3rect = platform2.get_rect()
platform3rect.x,platform3rect.y= 950,400

platform4rect = platform1.get_rect()
platform4rect.x,platform4rect.y= 410,210

platforms = [platform1rect,platform2rect,platform3rect,platform4rect]
players = []
def drawgame():
	screen.blit(background_img,(0,0))
	screen.blit(healthbar_img,(screen_width-400,-50))

	screen.blit(platform1,platform1rect)
	screen.blit(platform2,platform2rect)
	screen.blit(platform2,platform3rect)
	screen.blit(platform1,platform4rect)




#creates class character
class Player():
	def __init__(self,x,y,i,health,lives):
		self.i = i
		self.health = health
		self.lives = lives
		self.rebirthcounter = 0

		#animation sprites
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.permafall = False
		self.counter = 0
		for num in range(0,7):
					skin_right = pygame.image.load(f'media/Knight/Idle/{num}.png')
					skin_right = pygame.transform.scale(skin_right,(125,110))
					self.images_right.append(skin_right)
					skin_left = pygame.transform.flip(skin_right,True,False)
					self.images_left.append(skin_left)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()


		#position & movment variables
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_width()
		self.vel_y = 0
		self.jumped = False
		self.direction = 'right'
		self.mode = 'idle'

	#basic functions
	def getxpos(self):
		return self.rect.x
	def getypos(self):
		return self.rect.y
	def setxpos(self,nx):
		self.rect.x = nx
	def setypos(self,ny):
		self.rect.y = ny
	def getname(self):
		return self.i
	def get_lives(self):
		return self.lives
	def get_health(self):
		return self.health
	def set_health(self,nhealth):
		self.health = nhealth
	def set_lives(self,nlives):
		self.lives = nlives
	def getdirection(self):
		return self.direction
	def getmode(self):
		return self.mode

	#update function: updates player at every moment
	def update(self):
		dx =0
		dy = 0
		cooldown = 1
		key = pygame.key.get_pressed()
	#if the player is me, i can control its movement and modes with keyboard, else its other player that only he can control them
		if(self.i):

			#movement:
					if( key[pygame.K_SPACE] and self.jumped == False):
						self.vel_y = -35
						self.jumped = True
					if(key[pygame.K_SPACE] == False):
						self.jumped = False	

					if key[pygame.K_LEFT]:
						dx-=10
						self.counter+=1
						self.direction = 'left'
					if key[pygame.K_RIGHT]:
						dx+=10
						self.counter+=1
						self.direction = 'right'

					if key[pygame.K_DOWN]:
						self.permafall = True


					if key[pygame.K_x]:
						self.mode = 'attack'

					if(key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False):
						self.counter=0
						idle_skin = pygame.image.load('media/Knight/Idle/0.png')
						if(self.direction == 'right'):
							self.image = pygame.transform.scale(idle_skin,(125,110)) 
						else:
							self.image = pygame.transform.scale(pygame.transform.flip(idle_skin,True,False),(125,110))
		
		else:


					if( key[pygame.K_w] and self.jumped == False):
						self.vel_y = -35
						self.jumped = True
					if(key[pygame.K_w] == False):
						self.jumped = False	

					if key[pygame.K_a]:
						dx-=10
						self.counter+=1
						self.direction = 'left'
					if key[pygame.K_d]:
						dx+=10
						self.counter+=1
						self.direction = 'right'

					if key[pygame.K_s]:
						self.permafall = True


					if key[pygame.K_z]:
						self.mode = 'attack'

					if(key[pygame.K_a] == False and key[pygame.K_d] == False):
						self.counter=0
						idle_skin = pygame.image.load('media/Knight/Idle/0.png')
						if(self.direction == 'right'):
							self.image = pygame.transform.scale(idle_skin,(125,110)) 
						else:
							self.image = pygame.transform.scale(pygame.transform.flip(idle_skin,True,False),(125,110))
		#gravity
		self.vel_y +=5
		dy += self.vel_y
		if(self.vel_y >40):
			self.vel_y =40


		#handle animation
		if self.counter > cooldown:
			self.counter = 0
			self.index +=1
			if(self.index < len(self.images_right)):
				if(self.direction == 'right'):
					self.image = self.images_right[self.index]
				else:
					self.image = self.images_left[self.index]
			else:
				self.index = 0


		#collision
		for rect in platforms:
			if rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
				if(self.permafall == False):
						if(self.vel_y >=0 and self.rect.bottom < rect.bottom+40 ):
							dy = rect.top - self.rect.bottom
				else:
					self.permafall = False

		#attacks
		for player in players:
			if(player.getname()!=self.i):
				if(self.mode =='attack'):
					if player.rect.colliderect(self.rect.x,self.rect.y,self.width,self.height):
						self.attackcounter =0
						if(self.direction=='right'):
							player.setxpos(player.getxpos()+80)
						else:
							player.setxpos(player.getxpos()-80)
						player.setypos(player.getypos()-60)

						if(player.get_health()-20>0):
							player.set_health(player.get_health()-20)
						
						else:
							player.set_lives(player.get_lives()-1)
							player.set_health(100)
							player.setxpos(200)
							player.setypos(300)
					self.mode = 'idle'




		#draw to screen
		self.rect.x +=dx
		self.rect.y+=dy

		def respawn():
			self.rebirthcounter+=1
			if(self.rebirthcounter ==10):
				self.rebirthcounter=0
				self.rect.x = 200
				self.rect.y = 300
				self.health = 100
				self.lives -=1
		#death by alling
		if(self.rect.y>screen_height):
			respawn()
			print("fallen off map")


		if(self.lives > 0):
			screen.blit(self.image,self.rect)
			pygame.draw.rect(screen,(255,255,255),self.rect,2)
		elif(self.i):
			print('dead forever')
			sys.exit()


	



font = pygame.font.Font(None,50)

player1 = Player(200,200,True,100,3)
player2 = Player(500,200,False,100,3)
players = [player1,player2]
run = True
while run:
	drawgame()
	myhealth = player1.get_health()
	text = font.render(f'{player1.get_lives()},{player1.get_health()}', True, (0, 0, 0))
	screen.blit(text, (screen_width-150, 20))
	player1.update()
	player2.update()
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			run = False
	pygame.display.update()
pygame.quit()