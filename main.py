from pygame import*

init()


class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y): 
        super().__init__()
        # each sprite must store an image property
        self.image = transform.scale(image.load(picture), (w, h))
  
       # each sprite must store the rect property - the rectangle which it's inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        super().__init__(player_image, player_x, player_y,size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        ''' moves the character by applying the current horizontal and vertical speed '''
        #horizontal movement first
        if packman.rect.x <= width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        #if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) 

        if packman.rect.y <=height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        #if we go behind the wall, we'll stand right up to it
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # going down
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: #going up
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('Shape/Circle.png', self.rect.right, self.rect.centery, 20, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, x, y, size_x, size_y)
        self.speed = speed
    
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= width - 85:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
           
class Bullet(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, size_x, size_y,  x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

        if self.rect.x >= width + 10:
            self.kill()

GREEN = (132, 252, 3)
width = 700
height = 500
window = display.set_mode((width, height))

clock = time.Clock()

wall_1 = GameSprite("Shape/Rect.png",300, 25,width / 2 - width / 3,height / 2)
wall_2 = GameSprite('Shape/Rect.png',25, 400, 370, 100)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)

bullets = sprite.Group()

run = True
packman = Player('Heros/pacman/cyborg.png', 80, 80,5, height - 80, 0, 0)
final = GameSprite("Heros/pacman/2-2.png", 80, 80 ,width -80, height -80)
enemy = Enemy("Heros/pacman/pac-2.png", 80, 80,width -80, height -250, 3)
enemies = sprite.Group()
enemies.add(enemy)

finish = False
win = transform.scale(image.load('backgrounds/thumb_1.jpg'), (700,500))
lose = transform.scale(image.load("backgrounds/game-over_2.png"), (700,500))
while run :
    time.delay(50)
     
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                packman.fire()
                
            if e.key == K_a:
               packman.x_speed = -5
            elif e.key == K_d:
               packman.x_speed = 5
            elif e.key == K_w:
               packman.y_speed = -5
            elif e.key == K_s:
               packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_a:
               packman.x_speed = 0
            elif e.key == K_d:
               packman.x_speed = 0
            elif e.key == K_w:
               packman.y_speed = 0
            elif e.key == K_s:
               packman.y_speed = 0
    
    if finish != True:
        window.fill(GREEN)
        barriers.draw(window)
        packman.reset()
        packman.update()
        final.reset()
        bullets.update()
        bullets.draw(window)

        enemies.draw(window)
        enemies.update()
        sprite.groupcollide(bullets, enemies, True, True)
        sprite.groupcollide(bullets, barriers, True, False)


        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (0,0))

        if sprite.spritecollide(packman, enem ies, False):
            finish = True
            window.blit(lose,(0,0))
    display.update()

    

