
img_bullet = "bullet.png" #пуля
from random import randint
from pygame import *
import pygame
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" #враг
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
font.init()
font2 = font.Font(None, 36)
text_loser = font2.render('WIN', 1, (255, 255, 0))
text_winer = font2.render('LOSE', 1, (220, 20, 60))
text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
window = display.set_mode((700, 500))
display.set_caption("Догонялки")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
win_width = 700
win_height = 500
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
        
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
           

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
           self.kill()
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None,36)
bullets = sprite.Group()



ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy('ufo.png' , randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

window.blit(background,(0, 0))
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
run = True
mixer.music.play()
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0, 0))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_win = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text_lose,(10,50))
        window.blit(text_win,(10,20))
        monsters.update()
        bullets.update()
        ship.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprites_list:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
        if lost > 3:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(text_winer, (200, 200))
        if score == 2:
            finish = True
            window.blit(text_loser, (200, 200))
            
        


        display.update()

