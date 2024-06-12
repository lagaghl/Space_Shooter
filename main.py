import pygame
import time
from random import randint, sample
from numpy import linspace

pygame.init()

screen = pygame.display.set_mode((800,700))
pygame.display.set_caption('Space Shooter')

class Alien(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.velocity = self.image.get_width()
    def update(self):
        self.rect.y += self.velocity

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width()/2
        self.rect.y = screen.get_height()-self.rect.height-10
        self.score = 0
        self.shoot_delay = 0.3
        self.last_shot_time = time.time()

    def increase_score(self):
        self.score +=1

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot_time = current_time
        #add sound

    def update(self,keys):
        if keys[pygame.K_RIGHT]:
            player.rect.x += 8
        if keys[pygame.K_LEFT]:
            player.rect.x -= 8

        if player.rect.x < -self.rect.width/2 + 10:
            player.rect.x = -self.rect.width/2 + 10
        elif player.rect.x > screen.get_width() - self.rect.width/2 - 10:
            player.rect.x = screen.get_width() - self.rect.width/2 - 10

        if keys[pygame.K_SPACE]:
            self.shoot()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_x,player_y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = player_x
        self.rect.bottom = player_y
    def update(self):
        self.rect.y -= 7
        if self.rect.y<-30:
            self.kill()

def create_alien():
    numberOfAliens = randint(1,17)
    aliens_spaces = linspace(0,screen.get_width(),17)
    space = sample(sorted(aliens_spaces),k=numberOfAliens)
    for i in range(numberOfAliens):
        alien = Alien(space[i])
        all_sprites.add(alien)
        aliens.add(alien)
#make the player
player = Player()

#make sprites group
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()

#add objects to the sprites group
players.add(player)
all_sprites.add(player)

font = pygame.font.Font(None, 36)

running = True
aliens_delay = 3
last_aliens_time = time.time()
while running:
    current_time = time.time()
    screen.fill((33,33,33))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for alien in aliens:
        if alien.rect.y >= player.rect.y:
            running = False  # Terminar el juego
    collitions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    for collition in collitions:
        player.increase_score()
    # Player movement
    keys = pygame.key.get_pressed()
    players.update(keys)
    bullets.update()
    # Make aliens
    if current_time-last_aliens_time>=aliens_delay:
        aliens.update()
        create_alien()
        last_aliens_time = time.time()
    #Draw all the sprites
    all_sprites.draw(screen)

    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
    screen.blit(score_text, score_rect)

    # Info update
    pygame.display.flip()
    pygame.time.Clock().tick(60)

        
pygame.quit()


