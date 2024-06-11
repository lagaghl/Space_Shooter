import pygame

pygame.init()

screen = pygame.display.set_mode((800,700))

class Alien:
    def __init__(self,img,x,y):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
    def move(self,x,y):
        self.x = x
        self.y = y
        screen.blit(self.img,(x,y))
    def destroy(self):
        #make noises and disappear 
        pass

class Player:
    def __init__(self,img):
        image = pygame.image.load(img)
        ext = image.get_rect()[2:4]
        scale = 0.4
        self.img = pygame.transform.scale(image, (int(ext[0] * scale), int(ext[1] * scale)))
        self.x = screen.get_width()/2
        self.y = screen.get_height()-self.img.get_height()-10
        self.score = 0
    def move(self,x):
        self.x = x
        screen.blit(self.img,(x,self.y))
    def increase_score(self):
        self.score +=1
    def shoot(self):
        #shott a bullet, make noise, and put a coldown
        pass

player = Player('spaceship.png')
running = True
while running:
    screen.fill((33,33,33))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.x += 10
    if keys[pygame.K_LEFT]:
        player.x -= 10

    if player.x < 0:
        player.x = 0
    elif player.x > screen.get_width() - player.img.get_width():
        player.x = screen.get_width() - player.img.get_width()
    
    player.move(player.x)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

        
pygame.quit()


