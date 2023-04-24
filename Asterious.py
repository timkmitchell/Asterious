"""

 
"""
 
import pygame
import random
from player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
W = (200, 200, 200)
DARKBLUE = (7, 117, 125)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
 
def main():
    
    pygame.init()
 
    size = [550, 600]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Asterious")
 
    done = False
 
    clock = pygame.time.Clock()
    
    #Images
    background = pygame.image.load("img/Space.png").convert()
    b_img = pygame.image.load("img/boss.png").convert()
    boss_img = pygame.transform.scale(b_img, (178, 220))
    e_img = pygame.image.load("img/endless.png").convert()
    endless_img = pygame.transform.scale(e_img, (178, 220))
    player_img = pygame.image.load("img/playership.png").convert()
    player_img.set_colorkey(WHITE)
    meteor_img = pygame.image.load("img/meteor.png").convert()
    meteor_img.set_colorkey(BLACK)
    meteor2_img = pygame.image.load("img/meteor2.png").convert()
    meteor2_img.set_colorkey(BLACK)
    bullet_img = pygame.image.load("img/lazer.png").convert()
    bullet_img.set_colorkey(BLACK)
    hench_img = pygame.image.load("img/ufo/ufo0.png").convert()
    hench_img.set_colorkey(BLACK)
    enemy_img = pygame.image.load("img/enemy.png").convert()
    enemy_img.set_colorkey(BLACK)
    ufo_img = pygame.image.load("img/ufo/ufo1.png").convert()
    u_img = pygame.transform.scale(ufo_img, (150,150))
    ufo_img.set_colorkey(BLACK)
    u_img.set_colorkey(BLACK)
        
    explosion_anim = {}
    explosion_anim['med'] = []
    explosion_anim['sm'] = []
    for i in range(9):
        filename = 'img/explode/regularExplosion0{}.png'.format(i)
        img = pygame.image.load(filename).convert()
        img.set_colorkey(BLACK)
        
        img_med = pygame.transform.scale(img, (40, 35))
        explosion_anim['med'].append(img_med)
        
        img_sm = pygame.transform.scale(img, (25, 20))
        explosion_anim['sm'].append(img_sm)
    
    powerup_imgs = {}
    powerup_imgs['shield'] = pygame.image.load("img/shldpwr.png").convert()
    
    #Sounds
    laser_sound = pygame.mixer.Sound("snd/sfx_laser1.ogg") 
    explosion_sound = pygame.mixer.Sound("snd/boom3.wav")
    explosion_sound2 = pygame.mixer.Sound("snd/boom7.wav")
    hit_sound = pygame.mixer.Sound("snd/boom2.wav")
    powerup_sound = pygame.mixer.Sound("snd/pwrup.ogg")
    pygame.mixer.music.load('snd/through space.ogg')
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    
    #Text_Fonts
    font = pygame.font.SysFont("Tempus Sans ITC", 30)
    font1 = pygame.font.SysFont("Ravie", 50)
    font2 = pygame.font.Font(None, 22)
    font3 = pygame.font.SysFont("Tempus Sans ITC", 22)
    #Lists
    starlist = []
    for i in range(45):
        x = random.randrange(0, 550)
        y = random.randrange(0, 600)
        w = random.randrange(3, 7)
        h = random.randrange(3, 7)
        starlist.append([x,y,w,h])
        
    star_list = []
    for i in range(50):
         random_index = random.randrange(240, 255)
         random_index2 = random.randrange(240, 255)
         random_index3 = random.randrange(240, 255)
         clay = [random_index, random_index2, random_index3]
         x = random.randrange(0, 550)
         y = random.randrange(0, 600)
         w = 4
         h = 4
         star_list.append([x,y,w,h])
         
    #Joystick
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("Error, I didn't find any joysticks.")
    else:
        a_joystick = pygame.joystick.Joystick(0)
        a_joystick.init()
    '----------------------------------------------------------------------'
    #Classes
    class Powerup(pygame.sprite.Sprite):
        def __init__(self, center):
            
            super().__init__()
            
            self.type = random.choice(['shield'])
            self.image = powerup_imgs[self.type]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 2
     
        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom > 600:
                self.kill()
                
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            
            super().__init__()
     
            self.image = pygame.transform.scale(bullet_img, (6, 15))
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
     
        def update(self):
            self.rect.y -= 5
            if self.rect.bottom < 0:
                self.kill()
                
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            
            super().__init__()
            
            self.size = size
            self.image = explosion_anim[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50
            
        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_anim[self.size]):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = explosion_anim[self.size][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    
    class Mob(pygame.sprite.Sprite):
        def __init__(self, img, w, h):
            
            super().__init__()
            
            self.image_orig = pygame.transform.scale(img, (w, h))
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .9 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
            self.rect.x = random.randrange(550 - 20)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 11)
            self.speedx = random.randrange(-2, 2)
            self.rotate = 0
            self.rotate_speed = random.randrange(-8, 8)
            self.prev_update = pygame.time.get_ticks()
        
        def rotate(self):
            cur_update = pygame.time.get_ticks()
            if cur_update - self.prev_update > 50:
                self.prev_update = cur_update
                self.rotate = (self.rotate + self.rotate_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rotate)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
            
        def update(self):
            Mob.rotate(self)
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > 715 or self.rect.right > 565 or self.rect.left < -15:
                self.rect.x = random.randrange(550 - 20)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 9)
        
    class Boss(pygame.sprite.Sprite):
        def __init__(self, img, w, h, yspeed):
            
            super().__init__()
            
            self.image_orig = pygame.transform.scale(img, (w, h))
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .9 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
            self.rect.x = random.randrange(550 - 20)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = yspeed
            self.speedx = random.randrange(-2, 2)
            self.rotate = 0
            
            self.prev_update = pygame.time.get_ticks()
            
        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.left < -10:
                self.speedx = random.randrange(4, 7)
                self.speedy = random.randrange(10, 13)
            if self.rect.right > 560: 
                self.speedx = random.randrange(-7, -4)
                self.speedy = random.randrange(10, 13)
            if self.rect.top > 715: 
                self.rect.x = random.randrange(550 - 20)
                self.rect.y = random.randrange(-100, - 40)
                self.speedx = random.choice([-5, 5])
                self.speedy = random.randrange(10, 13)
        
    
    '----------------------------------------------------------------------'
    #Functions
    def introduce():
        pygame.mixer.music.load('snd/intro.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
        
        introlist = []
        for i in range(1):
            x = random.randrange(0, 500)
            y = random.randrange(255, 350)
            w = random.randrange(11, 25)
            h = 2
            introlist.append([x,y,w,h])
            
        done = False
   
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    boss_mode()
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(7)
                    if joy_button_pressed != 0:
                        boss_mode()
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.") 
                    
            for i,center in enumerate(introlist):
                center[0] -= 4
                if center[0] < 0 :
                    center[0] = random.randrange(550, 600)
                    for i in range(1):
                        x = random.randrange(600, 700)
                        y = random.randrange(255, 350)
                        w = 11
                        h = 2
                        introlist.append([x,y,w,h])
                     
            screen.fill(DARKBLUE)
            text = font2.render("*Click to contiue", True, WHITE, True)
            screen.blit(text, [205,0])
            text = font2.render("(Press Start)", True, GREEN, True)
            screen.blit(text, [225,40])
            text = font1.render("Zygoid", True, RED, True)
            screen.blit(text, [165,185])
            text = font1.render("Zygoid", True, WHITE, True)
            screen.blit(text, [160,189])
            text = font1.render("Mothership", True, RED, True)
            screen.blit(text, [95,385])
            text = font1.render("Mothership", True, WHITE, True)
            screen.blit(text, [90,389])
            pygame.draw.rect(screen, WHITE, [0, 250, 550, 5])
            pygame.draw.rect(screen, RED, [0, 255, 550, 95])
            pygame.draw.rect(screen, WHITE, [0, 350, 550, 5])
            for center in introlist:
                pygame.draw.rect(screen, WHITE, center)
                
            screen.blit(u_img, [200, 240])
           
            clock.tick(60)
    
            pygame.display.flip()
            
        pygame.quit()
        
    def quit_game():
        pygame.quit()
        quit()
        
    def draw_text(surface, text, x, y):
        text_surface = font2.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    
    def draw_shield(surface, x, y, percent, barlength, perdivide):
        if percent < 0:
            percent = 0
        bar_length = barlength
        bar_height = 10
        fill = (percent / perdivide) * bar_length
        outline_bar = pygame.Rect(x, y, bar_length, bar_height)
        fill_bar = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, GREEN, fill_bar)
        pygame.draw.rect(surface, WHITE, outline_bar, 2)
        
    def gameover(x, mode):
        game_over = x
        done = False
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(7)
                    if joy_button_pressed != 0:
                        select_screen()
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                    
            if game_over == True:
                screen.fill(WHITE)
                text = font1.render("Game Over", True, RED)
                screen.blit(text, [100, 250])
                
                text = font.render("Continue?", True, BLACK)
                screen.blit(text, [200, 325])
                
                text = font.render("Yes", True, BLACK)
                screen.blit(text, [100, 375])
                buttons(80, 375, 80, 40, GREEN, BLACK, mode)
                text = font2.render("(Doesn't Work with Controller)", True, GREEN)
                screen.blit(text, [10, 420])
                
                text = font.render("No", True, BLACK)
                screen.blit(text, [380, 375])
                buttons(360, 375, 80, 40, RED, BLACK, select_screen)
                text = font2.render("(Press Start)", True, GREEN)
                screen.blit(text, [357, 420])
                
            clock.tick(60)
    
            pygame.display.flip()
        
        pygame.quit()        
        
    def win(x):
        wins = x
        pygame.mixer.music.load('snd/win.mp3')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
    
        while wins:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wins = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(6)
                    if joy_button_pressed != 0:
                        select_screen()
                    joy_button_pressed = a_joystick.get_button(7)
                    if joy_button_pressed != 0:
                        quit_game()
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                 
            if wins == True:
                screen.fill(BLACK)
                #PUT MUSIC
                text = font1.render("You Barely", True, WHITE)
                screen.blit(text, [100, 200])
                text = font1.render("Made it", True, WHITE)
                screen.blit(text, [140, 250])
                
                text = font.render("Choose game mode", True, WHITE)
                screen.blit(text, [150, 350])
                buttons(150, 350, 255, 40, GREEN, BLACK, select_screen)
                text = font2.render("(Press Select)", True, GREEN)
                screen.blit(text, [230, 330])
                
                text = font.render("Quit", True, RED)
                screen.blit(text, [240, 440])
                buttons(240, 440, 60, 40, RED, BLACK, quit_game)
                text = font2.render("(Press Start)", True, GREEN)
                screen.blit(text, [226, 480])
            
            
            clock.tick(60)
    
            pygame.display.flip()
        
        pygame.quit()
        
    def Instructions():
        
        done = False
        
        display_instructions = True
        instruction_page = 1
    
        while not done and display_instructions:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    instruction_page += 1
                    if instruction_page == 2:
                        display_instructions = False
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(6)
                    if joy_button_pressed != 0:
                        main()
                if event.type == pygame.JOYBUTTONUP:
                        print("Joystick button released.")      
                        
            for i,center in enumerate(star_list):
                center[1] += 5
                if center[1] > 600:
                    center[1] = 0
        
            for i,center in enumerate(starlist):
                center[1] += 2
                if center[1] > 600:
                    center[1] = 0
        
            screen.blit(background, [0,0])
            for center in star_list:
                pygame.draw.rect(screen, clay, center)
            
            for center in starlist:
                pygame.draw.rect(screen, W, center)
    
            if instruction_page == 1:
                text = font.render('Controls', True, WHITE)
                pygame.draw.line(screen, WHITE, [210, 205], [320, 205])
                screen.blit(text, [210, 175])
    
                text = font3.render('Use WASD to move the character', True, WHITE)
                screen.blit(text, [135, 250])
                
                text = font3.render('L: Shoots laser', True, WHITE)
                screen.blit(text, [200, 295])
                
                screen.blit(powerup_imgs['shield'], [165, 400])
                text = font2.render("Yellow Pill", True, YELLOW)
                screen.blit(text, [135, 430])
                text = font3.render("Increases health", True, WHITE)
                screen.blit(text, [215, 400])
    
                text = font2.render("Page 1", True, WHITE)
                screen.blit(text, [490, 570])
                
                text = font2.render("(Press Select for Main Screen)", True, GREEN)
                screen.blit(text, [170, 0])
    
            clock.tick(60)
    
            pygame.display.flip()
            
    def select_screen():
        pygame.mixer.music.load('snd/through space.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
        
        done = False
    
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(6)
                    if joy_button_pressed != 0:
                        endless_mode()
                    joy_button_pressed = a_joystick.get_button(7)
                    if joy_button_pressed != 0:
                        introduce()
                    joy_button_pressed = a_joystick.get_button(0)
                    if joy_button_pressed != 0:
                        quit_game()
                    joy_button_pressed = a_joystick.get_button(1)
                    if joy_button_pressed != 0:
                        main()
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                    
            for i,center in enumerate(star_list):
                center[1] += 4
                if center[1] > 600:
                    center[1] = 0
        
            for i,center in enumerate(starlist):
                center[1] += 2
                if center[1] > 600:
                    center[1] = 0
            
            screen.fill(BLACK)
            screen.blit(background, [0,0])
            
            for center in star_list:
                pygame.draw.rect(screen, clay, center)
            
            for center in starlist:
                pygame.draw.rect(screen, W, center)
                
            buttons(230, 475, 90, 15, WHITE, BLACK, main)
            buttons(340, 300, 140, 40, GREEN, BLACK, introduce)
            buttons(50, 300, 180, 40, GREEN, BLACK, endless_mode)
            buttons(255, 500, 35, 15, RED, BLACK, quit_game)
            
            screen.blit(endless_img, [50, 70])
            pygame.draw.rect(screen, WHITE, [50, 70, 178, 220], 2)
            text = font.render("Endless Mode", True, WHITE)
            screen.blit(text, [50, 300])
            text = font2.render("(Press Select)", True, GREEN)
            screen.blit(text, [85, 350])
            
            screen.blit(boss_img, [320, 70])
            pygame.draw.rect(screen, WHITE, [320, 70, 178, 220], 2)
            text = font.render("Boss Mode", True, WHITE)
            screen.blit(text, [340, 300])
            text = font2.render("(Press Start)", True, GREEN)
            screen.blit(text, [365, 350])
            
            text = font2.render("Title Screen", True, WHITE)
            screen.blit(text, [230, 475])
            text = font2.render("(Press B)", True, GREEN)
            screen.blit(text, [240, 455])
            
            text = font2.render("Quit", True, WHITE)
            screen.blit(text, [255, 500])
            text = font2.render("(Press A)", True, GREEN)
            screen.blit(text, [240, 520])
                  
            text = font.render("Which Mode", True, WHITE)
            screen.blit(text, [200, 0])
            
            clock.tick(60)
    
            pygame.display.flip()
        
    
    def endless_mode():
        pygame.mixer.music.load('snd/railjet.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
            
        done = False
        
        all_sprites_list = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        enemy = pygame.sprite.Group()
        mobs2 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        
        player = Player(player_img)
        all_sprites_list.add(player)
        player.rect.y = 600 - 20
        player.rect.x = 225
        
        def newmob():
            met = Mob(meteor_img, 30, 24)
            all_sprites_list.add(met)
            mobs.add(met)
        def newmob2():
            met2 = Mob(meteor2_img, 45, 40)
            all_sprites_list.add(met2)
            mobs2.add(met2)
        def enemys():
            ene = Boss(enemy_img, 52, 54, 9)
            all_sprites_list.add(ene)
            enemy.add(ene)
            
        for i in range(2):
           newmob()
        for i in range(1):
           newmob2()
        
        score = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    laser_sound.play()
                    bullet = Bullet(player.rect.centerx, player.rect.y)
                    all_sprites_list.add(bullet)
                    bullets.add(bullet)
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(2)
                    if joy_button_pressed != 0:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                    joy_button_pressed = a_joystick.get_button(3)
                    if joy_button_pressed != 0:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
   
            all_sprites_list.update()      
           
            if joystick_count != 0:
                horiz_axis_pos = a_joystick.get_axis(0)
                vert_axis_pos = a_joystick.get_axis(1)

                player.rect.x = player.rect.x + int(horiz_axis_pos * 6)
                player.rect.y = player.rect.y + int(vert_axis_pos * 6)
            
            attack = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in attack:
                explosion_sound.play()
                score += 50 - hit.radius
                explo = Explosion(hit.rect.center, 'med')
                all_sprites_list.add(explo)
                if random.random() > 0.95:
                    pwr = Powerup(hit.rect.center)
                    all_sprites_list.add(pwr)
                    powerups.add(pwr)
                if random.random() > .9:
                    for i in range(1):
                        newmob()
                for i in range(1):
                    newmob()
            attack2 = pygame.sprite.groupcollide(mobs2, bullets, True, True)
            for hit in attack2:
                explosion_sound.play()
                score += 50 - hit.radius
                explo2 = Explosion(hit.rect.center, 'med')
                all_sprites_list.add(explo2)
                if random.random() > 0.95:
                    pwr = Powerup(hit.rect.center)
                    all_sprites_list.add(pwr)
                    powerups.add(pwr)
                if random.random() > .85:
                    enemys()
                if random.random() > .9:
                    for i in range(1):
                        newmob2()
                for i in range(1):
                    newmob2()
            attack3 = pygame.sprite.groupcollide(enemy, bullets, True, True)
            for hit in attack3:
                explosion_sound.play()
                score += 50 - hit.radius
                explo2 = Explosion(hit.rect.center, 'med')
                all_sprites_list.add(explo2)
                    
            hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                hit_sound.play()
                player.shield -= hit.radius * 2
                explo = Explosion(hit.rect.center, 'sm')
                all_sprites_list.add(explo)
                newmob()
                if player.shield <= 0:
                    gameover(True, endless_mode)
            
            hits2 = pygame.sprite.spritecollide(player, mobs2, True, pygame.sprite.collide_circle)
            for hit in hits2:
                hit_sound.play()
                player.shield -= hit.radius
                explo2 = Explosion(hit.rect.center, 'sm')
                all_sprites_list.add(explo2)
                newmob2()
                if player.shield <= 0:
                    gameover(True, endless_mode)
                    
            hits3 = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
            for hit in hits3:
                hit_sound.play()
                player.shield -= hit.radius
                explo2 = Explosion(hit.rect.center, 'sm')
                all_sprites_list.add(explo2)
                enemys()
                if player.shield <= 0:
                    gameover(True, endless_mode)
                    
            pwrup_hit = pygame.sprite.spritecollide(player, powerups, True)
            for hit in pwrup_hit:
                powerup_sound.play()
                if hit.type == 'shield':
                    player.shield += random.randrange(5, 10)
                    if player.shield >= 100:
                        player.shield = 100
                    
            for i,center in enumerate(star_list):
                center[1] += 4
                if center[1] > 600:
                    center[1] = 0
        
            for i,center in enumerate(starlist):
                center[1] += 2
                if center[1] > 600:
                    center[1] = 0
            
            for bullet in bullet_list:
                if bullet.rect.y < -10:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)
            
            screen.fill(BLACK)
            screen.blit(background, [0,0])
            for center in star_list:
                pygame.draw.rect(screen, clay, center)
            
            for center in starlist:
                pygame.draw.rect(screen, W, center)
                  
            fps = "fps = {}".format(clock)
            text = font2.render(str(fps), True, WHITE)
            screen.blit(text, [0, 580])
            
            all_sprites_list.draw(screen)
           
            draw_text(screen, str(score), 275, 10)
            draw_shield(screen, 440, 580, player.shield, 100, 100)
         
            clock.tick(60)
    
            pygame.display.flip()
    
        pygame.quit()
            
    def boss_mode():
        pygame.mixer.music.load('snd/bossmusic1.mp3')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()
        
        done = False
        
        all_sprites_list = pygame.sprite.Group()
        boss = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        
        player = Player(player_img)
        all_sprites_list.add(player)
        player.rect.y = 600 - 20
        player.rect.x = 225
        boss_shield = 4000
        
        def newmob():
            met = Mob(hench_img, 35, 35)
            all_sprites_list.add(met)
            mobs.add(met)
       
        def newboss():
            bss = Boss(ufo_img, 100, 100, 4)
            all_sprites_list.add(bss)
            boss.add(bss)
        
        for i in range(1):
           newboss()
           
        score = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    laser_sound.play()
                    bullet = Bullet(player.rect.centerx, player.rect.y)
                    all_sprites_list.add(bullet)
                    bullets.add(bullet)
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(2)
                    if joy_button_pressed != 0:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                    joy_button_pressed = a_joystick.get_button(3)
                    if joy_button_pressed != 0:
                        laser_sound.play()
                        bullet = Bullet(player.rect.centerx, player.rect.y)
                        all_sprites_list.add(bullet)
                        bullets.add(bullet)
                if event.type == pygame.JOYBUTTONUP:
                        print("Joystick button released.")  
                        
            if joystick_count != 0:
                horiz_axis_pos = a_joystick.get_axis(0)
                vert_axis_pos = a_joystick.get_axis(1)

                player.rect.x = player.rect.x + int(horiz_axis_pos * 6)
                player.rect.y = player.rect.y + int(vert_axis_pos * 6) 
                
            all_sprites_list.update()
            
            attack2 = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in attack2:
                explosion_sound.play()
                score += 50 - hit.radius
                explo = Explosion(hit.rect.center, 'med')
                all_sprites_list.add(explo)
                if random.random() > 0.9:
                    pwr = Powerup(hit.rect.center)
                    all_sprites_list.add(pwr)
                    powerups.add(pwr)

            attack = pygame.sprite.groupcollide(boss, bullets, False, True)
            for hit in attack:
                explosion_sound2.play()
                for i in range(1):
                    newmob()
                boss_shield -= 25
                score += 50 - hit.radius
                explo = Explosion(hit.rect.center, 'med')
                all_sprites_list.add(explo)
                if boss_shield <= 0:
                    win(True)
                
            hits = pygame.sprite.spritecollide(player, boss, True, pygame.sprite.collide_circle)
            for hit in hits:
                hit_sound.play()
                player.shield -= hit.radius * 2
                explo = Explosion(hit.rect.center, 'sm')
                all_sprites_list.add(explo)
                newboss()
                if player.shield <= 0:
                    gameover(True, boss_mode)
                    
            hits2 = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits2:
                hit_sound.play()
                player.shield -= 5
                explo = Explosion(hit.rect.center, 'sm')
                all_sprites_list.add(explo)
                if player.shield <= 0:
                    gameover(True, boss_mode)
                    
            pwrup_hit = pygame.sprite.spritecollide(player, powerups, True)
            for hit in pwrup_hit:
                powerup_sound.play()
                if hit.type == 'shield':
                    player.shield += random.randrange(5, 30)
                    if player.shield >= 100:
                        player.shield = 100
                
            for i,center in enumerate(star_list):
                center[1] += 4
                if center[1] > 600:
                    center[1] = 0
        
            for i,center in enumerate(starlist):
                center[1] += 2
                if center[1] > 600:
                    center[1] = 0
            
            for bullet in bullet_list:
                if bullet.rect.y < -10:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)
            
            screen.fill(BLACK)
            screen.blit(background, [0,0])
            
            for center in star_list:
                pygame.draw.rect(screen, clay, center)
            
            for center in starlist:
                pygame.draw.rect(screen, W, center)
                  
            text = font2.render(str(clock), True, WHITE)
            screen.blit(text, [0, 580])
            
            all_sprites_list.draw(screen)
           
            draw_text(screen, str(score), 275, 10)
            draw_shield(screen, 0, 0, boss_shield, 4000, 4000)
            draw_shield(screen, 440, 580, player.shield, 100, 100)
            
            clock.tick(60)
    
            pygame.display.flip()
    
        pygame.quit()
        
    def buttons(x, y, width, height, actcolor, inacolor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x+width > mouse[0] > x and y+height > mouse[1] > y:
            pygame.draw.rect(screen, actcolor, [x, y, width, height], 1)
            if click[0] == 1 and action != None:
               action()       
        else:
            pygame.draw.rect(screen, inacolor, [x, y, width, height], 1)
   
    # -------- Title Loop -----------
         
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    joy_button_pressed = a_joystick.get_button(7)
                    if joy_button_pressed != 0:
                        select_screen()
                    joy_button_pressed = a_joystick.get_button(6)
                    if joy_button_pressed != 0:
                        Instructions()
                    joy_button_pressed = a_joystick.get_button(0)
                    if joy_button_pressed != 0:
                        quit_game()
                    if event.type == pygame.JOYBUTTONUP:
                            print("Joystick button released.")
            
        for i,center in enumerate(star_list):
            center[1] += 4
            if center[1] > 600:
                center[1] = 0
        
        for i,center in enumerate(starlist):
            center[1] += 2
            if center[1] > 600:
                center[1] = 0
                      
        screen.blit(background,[0,0])
        for center in star_list:
            pygame.draw.rect(screen, clay, center)
            
        for center in starlist:
            pygame.draw.rect(screen, W, center)
            
        buttons(190, 375, 155, 40, WHITE, BLACK, Instructions)
        buttons(240, 300, 60, 40, WHITE, BLACK, select_screen)
        buttons(240, 450, 62, 40, RED, BLACK, quit_game)
        
        text = font2.render("* This game uses keyboard and mouse", True, WHITE)
        screen.blit(text, [135,0])
        text = font2.render("and joystcks", True, WHITE)
        screen.blit(text, [145,15])
        
        text = font.render("Green is for Controller", True, GREEN)
        screen.blit(text, [136,550])
        
        text = font1.render("Asterious", True, GREEN)
        screen.blit(text, [100,100])
        
        text = font.render("Start", True, WHITE)
        screen.blit(text, [240,300])
        text = font2.render("(Press Start)", True, GREEN)
        screen.blit(text, [225,350])
        
        text = font.render("Instructions", True, WHITE)
        screen.blit(text, [190,375])
        text = font2.render("(Press Select)", True, GREEN)
        screen.blit(text, [220,425])
        
        text = font.render("Quit", True, WHITE)
        screen.blit(text, [240,450])
        text = font2.render("(Press A)", True, GREEN)
        screen.blit(text, [240,500])
 
        pygame.display.flip()
 
        
        clock.tick(60)
 
    pygame.quit()
 
if __name__ == "__main__":
    main()
