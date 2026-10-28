import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path
from utils import *
from random import randint
vec = pg.math.Vector2

#create player class with Sprite as super Class

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits [0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            return True

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits [0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
    
    
    
    
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        #this provides us with raster images for use in animation or otherwise
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        #player motion attributes
    
        self.vel = vec (0,0)
        self.acc = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        #start with current frames and last update at zero so we can cycle through animations
        self.current_frame = 0
        self.last_update = 0
        #accounting for the states of the player
        self.coins = 0
        self.jumping = False
        self.moving = False
        self.load_images()
        
        print("player instance created")


#gets player input
    def get_keys(self):
        # self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            # self.vx = -PLAYER_SPEED
            # self.vel.x = -PLAYER_SPEED
            self.acc.x = -5

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            # self.vx = PLAYER_SPEED
            # self.vel.x = PLAYER_SPEED
            self.acc.x = 5
        if keys[pg.K_w] or keys[pg.K_UP]:
            # self.vy = -PLAYER_SPEED
            # self.vel.y = -PLAYER_SPEED
            self.acc.y = -5
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            # self.vy= PLAYER_SPEED
            # self.vel.y= PLAYER_SPEED
            self.acc.y = 5
        #check to see if player is moving diagonally
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
       

    def jump(self):
        pass


    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]
    
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        self.acc = vec(0,0)
        self.get_keys()
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        
       
        self.animate()

        self.rect.center = self.pos
        self.pos += self.vel + 0.5 * self.acc
        # self.pos += self.vel * self.game.dt
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            self.coins += 1
            self.game.score += 1
            self.game.pickup_snd.play()
            for i in range (100):
                Particle(self.game, hits[0].rect.x, hits[0].rect.y)
                hits[0].kill()
            print(str(len(self.game.all_particles)))

    
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center


#new object type Wall that is green

# class Wall(Sprite):
#     def __init__(self, game, x, y):
        
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # this provides us wtih raster images for use in animation or otherwise
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(64,0,TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.vx, self.vy = 0,0
        self.speed = -100
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.hit_rect = MOB_HIT_RECT
        # animation stuff
        # start with current frames and last update at zero so we can cycle through animations
        self.current_frame = 0
        self.last_update = 0
        # accounting for the states of the player
        self.jumping = False
        self.moving = False
        print("player instance created")
        self.load_images()
    def load_images(self):
            self.idle_frames = [self.spritesheet.get_image(64,0, TILESIZE,TILESIZE), self.spritesheet.get_image(96,0, TILESIZE,TILESIZE)]
    def animate(self):
            now = pg.time.get_ticks()
            if not self.jumping and not self.moving:
                # this determines when to display the next frame
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            elif self.moving:
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                    bottom = self.rect.bottom
                    self.image = self.moving_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom



    def update(self):
        self.animate()
        
        self.hit_rect.centerx = self.pos.x
        if collide_with_walls(self, self.game.all_walls, 'x'):
                print("x collide")
                self.speed *= -1



        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.pos += self.vel * self.speed * self.game.dt
        self.rect.center = self.pos

        self.rect.center = self.hit_rect.center


class Particle(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(randint(-180,180), randint(-180,180))
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.speed = 5
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks() / 1000)
        print("I created a particle")
        print(self.rect.x)
        print(self.rect.y)


    def update(self):
        self.countdown.ticking
        self.pos += self.vel * self.speed * self.game.dt
        # self.rect.x += self.speed * randint(-5, 5)
        # self.rect.y += self.speed * randint(-5, 5)
        if self.countdown.delta > 1:
            self.kill()
            print(str(len(self.game.all_particles)))
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


    
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.vel = vec(0, 0)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, GOLD, (TILESIZE/2, TILESIZE/2), TILESIZE/2)
        # self.image.fill(GREEN)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.vel = vec(0, 0)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")




       









