import pygame
import intersects

# Window
WIDTH = 1000
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Space Fighters"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

#colors
BLACK = (0,0,0)
RED = (255,0,0)

#images
wiz = pygame.image.load('wiz.png')
skeleton = pygame.image.load('skeleton.png')
background = pygame.image.load('background.png')
battle_room = pygame.image.load('battle.png')
cursor = pygame.image.load('cursor.png')
paper_background = pygame.image.load('paper_background.png')
attack_button = pygame.image.load('attack_button.png')
empty_bar = pygame.image.load('empty_bar.png')

hit0 = pygame.image.load('hit0.png')
hit1 = pygame.image.load('hit1.png')
hit2 = pygame.image.load('hit2.png')
hit3 = pygame.image.load('hit3.png')
hit4 = pygame.image.load('hit4.png')
hit5 = pygame.image.load('hit5.png')
hit6 = pygame.image.load('hit6.png')
hit7 = pygame.image.load('hit7.png')
hit_frames = [hit0,hit1,hit2,hit3,hit4,hit5,hit6,hit7]

#stages
start = 1
battle = 2

#functions
def draw_battle():
    screen.blit(battle_room,[0,0])

#classes
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 6
        self.battling = False

        self.strength = 5
        self.health = 25
        
    def move_up(self):
        self.rect.y -= self.speed
    def move_down(self):
        self.rect.y += self.speed
    def move_left(self):
        self.rect.x -= self.speed
    def move_right(self):
        self.rect.x += self.speed

    def attack(self,other):
        other.health -= self.strength

    def update(self,STAGE):
        
        hit_list = pygame.sprite.spritecollide(self,mobs,True)
        
        for hit in hit_list:
            self.battling = True

class Mob(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.health = 10
        self.strength = 2

    def attack(self,other):
        other.health -= self.strength

class Fight_Gui():
    def __init__(self,monster):
        self.arrow_pos = [250,550]
        
        self.monster = monster
        self.mx_mob_health = self.monster.health
        self.monster_img = self.monster.image

        self.mx_hero_health = wizard.health
        
        self.player_turn = True
        self.cooldown = [60,60]
        self.ready = True
        
    def update(self):
        if self.cooldown[0] != self.cooldown[1]:
            self.cooldown[0] += 1
            self.ready = False
        if self.cooldown[0] == self.cooldown[1]:
            self.ready = True
            
        if self.ready and self.monster.health <= 0:
            wizard.battling = False
            
        if self.player_turn == False and self.monster.health > 0 and self.ready:
            self.monster.attack(wizard)
            print("Monster: " + str(self.monster.health))
            print("Hero: " + str(wizard.health))
            self.player_turn = True
            self.cooldown[0] = 0

    def mob_health(self):
        percent = (self.monster.health)/(self.mx_mob_health)
        screen.blit(empty_bar,[550,320])
        pygame.draw.rect(screen,RED,[571,327,110*percent,19])

    def hero_health(self):
        pass
     
    def draw(self):
        draw_battle()
        screen.blit(paper_background,[0,500])
        screen.blit(self.monster_img,[570,370])
        self.mob_health()
        screen.blit(attack_button,[150,525])
        screen.blit(cursor,self.arrow_pos)
        
    def cursor_up(self):
        self.arrow_pos[1] = 550
    def cursor_down(self):
        self.arrow_pos[1] = 650
    def cursor_left(self):
        self.arrow_pos[0] = 250
    def cursor_right(self):
        self.arrow_pos[0] = 550


    def action(self,effects):
        if self.player_turn and self.ready:
            if self.arrow_pos == [250,550]:
                wizard.attack(self.monster)
                effects.frame_list = hit_frames
            print("Monster: " + str(self.monster.health))
            print("Hero: " + str(wizard.health))
            self.player_turn = False
            self.cooldown[0] = 0

class Effects():
    def __init__(self):
        self.frame_list = []
        self.ticks = 0
        self.index = 0
        self.frame = hit0

    def update(self):
        if len(self.frame_list) > 0:
            self.ticks += 1

            if self.ticks%1 == 0:
                self.index += 1

            if self.index < len(self.frame_list):
                self.frame = self.frame_list[self.index]
                
            if self.index >= len(self.frame_list):
                self.frame_list = []
                self.ticks = 0
                self.index = 0
                self.frame = hit0

    def draw(self):
        if len(self.frame_list) > 0:
            screen.blit(self.frame,[570,370])

        
#objects
wizard = Player(0,0,wiz)
mob1 = Mob(40,200,skeleton)
fight_gui = Fight_Gui(mob1)
effects = Effects()

#sprite groups
character = pygame.sprite.GroupSingle()
mobs = pygame.sprite.Group()
character.add(wizard)
mobs.add(mob1)

done = False
STAGE = start
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    '''processing'''
    pressed = pygame.key.get_pressed()

    if STAGE == start:
        if pressed[pygame.K_UP]:
            wizard.move_up()
        if pressed[pygame.K_DOWN]:
            wizard.move_down()
        if pressed[pygame.K_LEFT]:
            wizard.move_left()
        if pressed[pygame.K_RIGHT]:
            wizard.move_right()

        character.update(STAGE)
        
    if wizard.battling == True:
        STAGE = battle
    if wizard.battling == False:
        STAGE = start

    if STAGE == battle:
        fight_gui.update()
        effects.update()
        if pressed[pygame.K_SPACE]:
            STAGE = start
        if pressed[pygame.K_UP]:
            fight_gui.cursor_up()
        if pressed[pygame.K_DOWN]:
            fight_gui.cursor_down()
        if pressed[pygame.K_LEFT]:
            fight_gui.cursor_left()
        if pressed[pygame.K_RIGHT]:
            fight_gui.cursor_right()
        if pressed[pygame.K_f]:
            fight_gui.action(effects)

    '''drawing'''
    screen.fill(BLACK)
    screen.blit(background,[0,0])
    character.draw(screen)
    mobs.draw(screen)
    
    if STAGE == battle:
        fight_gui.draw()
        effects.draw()

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
