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
            self.rect.x += 8
        if keys[pygame.K_LEFT]:
            self.rect.x -= 8

        if self.rect.x < -self.rect.width/2 + 10:
            self.rect.x = -self.rect.width/2 + 10
        elif self.rect.x > screen.get_width() - self.rect.width/2 - 10:
            self.rect.x = screen.get_width() - self.rect.width/2 - 10

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

def show_text(text, size, color, center):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.fill((0,0,0))
        show_text("Space Shooter", 72, (255,255,255), (screen.get_width() / 2, screen.get_height() / 2 - 50))
        show_text("Press ENTER to Start", 36, (255,255,255), (screen.get_width() / 2, screen.get_height() / 2 + 20))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def game_over_menu(score, high_score):
    while True:
        screen.fill((0,0,0))
        show_text("Game Over", 72,(255,255,255) , (screen.get_width() / 2, screen.get_height() / 2 - 50))
        show_text(f"Score: {score}", 36, (255,255,255), (screen.get_width() / 2, screen.get_height() / 2 + 20))
        show_text(f"High Score: {high_score}", 36, (255,255,255), (screen.get_width() / 2, screen.get_height() / 2 + 60))
        show_text("Press ENTER to Play Again", 36, (255,255,255), (screen.get_width() / 2, screen.get_height() / 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

hight_score = 0
def game_loop(high_score):
    #make the player
    player = Player()

    #make sprites group
    global all_sprites, players, bullets, aliens
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    #add objects to the sprites group
    players.add(player)
    all_sprites.add(player)

    font = pygame.font.Font(None, 36)

    running = True
    aliens_delay = 0.5
    last_aliens_time = time.time()
    while running:
        current_time = time.time()
        screen.fill((33,33,33))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        collitions = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for collition in collitions:
            player.increase_score()

        for alien in aliens:
            if alien.rect.bottom >= player.rect.top:
                running = False  # Terminar el juego
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
    if player.score > high_score:
        high_score = player.score
    game_over_menu(player.score, high_score)

main_menu()
while True:
    game_loop(hight_score)
    main_menu()


