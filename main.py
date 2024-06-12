import pygame

pygame.init()

screen = pygame.display.set_mode((800,700))
pygame.display.set_caption('Space Shooter')

class Alien(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        super().__init__()
        self.image = pygame.image.load(img)
        self.get_rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def destroy(self):
        #make noises and disappear 
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self,img):
        super().__init__()
        image = pygame.image.load(img)
        scale = 0.4
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width()/2
        self.rect.y = screen.get_height()-self.rect.height-10
        self.score = 0

    def update(self,keys):
        if keys[pygame.K_RIGHT]:
            player.rect.x += 8
        if keys[pygame.K_LEFT]:
            player.rect.x -= 8

        if player.rect.x < 0:
            player.rect.x = 0
        elif player.rect.x > screen.get_width() - self.rect.width:
            player.rect.x = screen.get_width() - self.rect.width

    def increase_score(self):
        self.score +=1
    
    def shoot(self):
        #shott a bullet, make noise, and put a coldown
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    def update(self):
        pass
#make the player
player = Player('spaceship.png')

#make sprites group
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()

#add objects to the sprites group
players.add(player)
all_sprites.add(player)

running = True
while running:
    screen.fill((33,33,33))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    players.update(keys)

    #Draw all the sprites
    all_sprites.draw(screen)

    # Info update
    pygame.display.flip()
    pygame.time.Clock().tick(60)

        
pygame.quit()


