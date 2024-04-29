#Создай собственный Шутер!
from random import *
from pygame import *
from time import time as timer
window = display.set_mode((700, 500))
display.set_caption('lol')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
window.blit(background,(0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20 ,-15)
        bullets.add(bullet)

lost = 0
score = 0
max_lost = 250
goal = 15
life = 5

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y = self.rect.y + self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 650)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620), -40, 65, 60, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 65, 60, randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()

ship = Player('rocket.png', 250, 400, 70, 90, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

FPS = 160

game =  True
finish = False
rel_time = False
num_fire = 0

font.init()
font1 = font.SysFont('Arial', 80 )
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))
        ship.update()
        bullets.update()
        asteroids.update()
        monsters.update()
        ship.reset()
        bullets.draw(window)
        asteroids.draw(window)
        monsters.draw(window)

        if rel_time == True:
            now_time = timer()
            
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

            if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
                sprite.spritecollide(ship, monsters, True)
                sprite.spritecollide(ship, asteroids, True)
                life = life -1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        text_score = font1.render('Счет:' + str(score), 1, (0, 255, 200))
        window.blit(text_score, (10, 30))

        text_lost = font1.render('Пропущено:' + str(lost), 1, (255, 100, 200))
        window.blit(text_lost, (10, 75))

        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))


        display.update()

    else:
        finish = False
        score = 0 
        lost = 0 
        num_fire = 0
        life = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)       
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(30, 700 - 30), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)       
    time.delay(50)

