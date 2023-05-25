#Создай собственный Шутер!
from pygame import *
from random import*
from time import time as timer
font.init()
mixer.init()
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x <700 - 80:
            self.rect.x+= self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15,20,15)
        bullets.add(bullet)
fire_sound = mixer.Sound('fire.ogg') 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y>500:
            self.rect.x = randint(80,620)
            self.rect.y =0
            lost +=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()
img_bullet = 'bullet.png'
text = font.SysFont("Arial",50)
text2 = font.SysFont("Arial",100)
num_fire = 0
rel_time = False
score = 0
lost = 0
life = 3
window = display.set_mode((700,500))
background = transform.scale(image.load("galaxy.jpg"),(700,500))
mixer.music.load('space.ogg')
mixer.music.play()
player = Player('rocket.png',200,420,65,80,12)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1,):
    asteroid = Enemy('asteroid.png',randint(80,620),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,620),-40,80,50,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    num_fire +=1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background,(0,0))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload1 = text.render('Wait,reload...',1,(150,0,0))
                window.blit(reload1,(260,460))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        for i in sprites_list:
            score +=1
            monster = Enemy('ufo.png',randint(80,620),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life -=1
        text_win = text2.render('You win!',1,(255,255,255)) 
        text_los = text2.render('You lose!',1,(255,255,255))
          
        if score >= 10:
            finish = True
            window.blit(text_win,(170,260))
        if life == 0 or lost >= 10:
            finish = True
            window.blit(text_los,(170,260))
        if life >=3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_lose =text.render('Пропущено:'+ str(lost),1,(255,255,255))
        text_score = text.render('Счет:'+str(score),1,(255,255,255))
        text_life = text.render('Жизни:'+str(life),1,life_color) 
        window.blit(text_lose,(50,50))
        window.blit(text_score,(50,10))
        window.blit(text_life,(500,10))
        display.update()
        
    time.delay(60) 
