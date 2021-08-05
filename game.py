import pygame
import random
import os

w=800
h=600
fps=60
#define colours
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
#f l    olders for art and sound
img_folder=os.path.dirname('E:\python\Space-Game\images/')
sound_folder=os.path.dirname('E:\python\Space-Game\sound/')


#img_folder=os.path.join(game_folder,"img")
font_name=pygame.font.match_font('ComicSansMS')
def draw(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,white)
    text_rect=text_surface.get_rect()
    text_rect.midtop= (x,y)
    surf.blit(text_surface,text_rect)

def newmob():
    m=Mob()
    all.add(m)
    mobs.add(m)

def draw_shield(s,x,y,p):
    if p<0:
        p=0
    BAR_LENGTH=100
    BAR_HEIGHT=10
    fill=(p/100)*BAR_LENGTH
    o_rect=pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(s,green,fill_rect)
    pygame.draw.rect(s,white,o_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)

class Player(pygame.sprite.Sprite):
    #sprite for Player
    def __init__(s):
        pygame.sprite.Sprite.__init__(s)
        s.image=pygame.image.load(os.path.join(img_folder, "ship_16_colour.png")).convert()
        s.image.set_colorkey(white)
        s.rect=s.image.get_rect()
        s.radius=15
        #pygame.draw.circle(s.image,black,s.rect.center,s.radius)
        s.rect.centerx=w/2
        s.rect.bottom=h-10
        s.speedx=0
        s.speedy=0
        s.shield=100
        s.shoot_delay=200
        s.last_shot=pygame.time.get_ticks()
        s.lives=3
        s.hidden=False
        s.hide_timer=pygame.time.get_ticks()


    def update(s):
        if s.hidden and pygame.time.get_ticks()-s.hide_timer>1000:
            s.hidden=False
            s.rect.centerx=w/2
            s.rect.bottom=h-10

        s.speedx=0
        s.speedy=0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            s.speedx=-5
        if s.rect.left<0:
            s.rect.left=0
        if keystate[pygame.K_UP]:
            s.speedy=-5
        if keystate[pygame.K_RIGHT]:
            s.speedx=5
        if s.rect.right>w:
            s.rect.right=w
        if keystate[pygame.K_DOWN]:
            s.speedy=5
        if keystate[pygame.K_SPACE]:
            s.shoot()
        if s.rect.bottom>h:
            s.rect.bottom=h
        if s.rect. top<0:
            s.rect.top=0
        s.rect.x +=s.speedx
        s.rect.y +=s.speedy
    def shoot(s):
        now=pygame.time.get_ticks()
        if now-s.last_shot>s.shoot_delay:
            s.last_shot=now
            bullet=Bullet(s.rect.centerx,s.rect.top)
            all.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    def hide(s):
        #temporary hide player
        s.hidden=True
        s.hide_timer=pygame.time.get_ticks()
        s.rect.center=(w/2,h+200)

class Mob(pygame.sprite.Sprite):
    def __init__(s):
        pygame.sprite.Sprite.__init__(s)
        s.image=random.choice(enemy_images)
        s.image.set_colorkey(white)
        s.rect=s.image.get_rect()
        s.radius=int(s.rect.width*.85 / 2)
        #pygame.draw.circle(s.image,black,s.rect.center,s.radius)
        s.rect.x=random.randrange(800)
        s.rect.y=random.randrange(-100,-40)
        s.speedy=random.randrange(1,7)
        s.speedx=random.randrange(-3,3)
    def update(s):
        s.rect.y+=s.speedy
        s.rect.x+=s.speedx
        if s.rect.top>h+10 or s.rect.left<-10 or s.rect.right>w+10:
            s.rect.x=random.randrange(800)
            s.rect.y=random.randrange(-150,-100)
            s.speedy=random.randrange(1,7)

class Bullet(pygame.sprite.Sprite):
    def __init__(s,x,y):
        pygame.sprite.Sprite.__init__(s)
        s.image=pygame.image.load(os.path.join(img_folder, "bulet_3.png")).convert()
        s.image.set_colorkey(white)
        s.rect=s.image.get_rect()
        s.rect.bottom=y
        s.rect.centerx=x
        s.speedy=-10
    def update(s):
        s.rect.y+=s.speedy
        if s.rect.bottom<0:
            s.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(s,center,size):
        pygame.sprite.Sprite.__init__(s)
        s.size=size
        s.image=explosion_anim[s.size][0]
        s.rect=s.image.get_rect()
        s.rect.center=center
        s.frame=0
        s.last_update=pygame.time.get_ticks()
        s.frame_rate=50

    def update(s):
        now=pygame.time.get_ticks()
        if now-s.last_update>s.frame_rate:
            s.last_update=now
            s.frame+=1
            if s.frame==len(explosion_anim[s.size]):
                s.kill()
            else:
                center=s.rect.center
                s.image=explosion_anim[s.size][s.frame]
                s.rect=s.image.get_rect()
                s.rect.center=center

class Pow(pygame.sprite.Sprite):
    def __init__(s,center):
        pygame.sprite.Sprite.__init__(s)
        s.image=pygame.image.load(os.path.join(img_folder, "bulet_3.png")).convert()
        s.image.set_colorkey(white)
        s.rect=s.image.get_rect()
        s.rect.center=center
        s.speedy=-10
    def update(s):
        s.rect.y+=s.speedy
        if s.rect.bottom<0:
            s.kill()
# initialize pygame and make window
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((w,h))
pygame.display.set_caption("SPACE ENEMIE")
clock=pygame.time.Clock()

bg=pygame.image.load(os.path.join(img_folder,"nebula.jpg")).convert()
bg_rect=bg.get_rect()
player_img=pygame.image.load(os.path.join(img_folder, "ship_16_colour.png")).convert()
player_mini_img=pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(white)
enemy_images=[]
enemy_list=['a_big_1.png','a_big_2.png','a_big_3.png','a_big_4.png']
for img in enemy_list:
    enemy_images.append(pygame.image.load(os.path.join(img_folder,img)).convert())
explosion_anim={}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
for i in range(9):
    filename='regularExplosion0{}.png'.format(i)
    img=pygame.image.load(os.path.join(img_folder,filename)).convert()
    img.set_colorkey(black)
    img_lg=pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
#LOAD GAME sound
shoot_sound=pygame.mixer.Sound(os.path.join(sound_folder,'laser4.wav'))
bomb_sound=pygame.mixer.Sound(os.path.join(sound_folder,'mobs.wav'))
player_die_sound=pygame.mixer.Sound(os.path.join(sound_folder,'Explosion.wav'))

#death_sound=pygame.mixer.Sound(os.path.join(game_folder,'DeathFlash.wav'))
pygame.mixer.music.load(os.path.join(sound_folder,'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
pygame.mixer.music.set_volume(0.4)

all=pygame.sprite.Group()
mobs=pygame.sprite.Group()
bullets=pygame.sprite.Group()
healths=pygame.sprite.Group()
player=Player()
all.add(player)

for i in range(10):
    newmob()

#for i in range(1):
    #healthkit()
score=0
pygame.mixer.music.play(loops=-1)
#game loop
running=True
while running:
    #keep loop running at speed
    clock.tick(fps)
    #process input
    for event in pygame.event.get():
        #closing window pressing # X
        if event.type==pygame.QUIT:
            running=False

    #update
    all.update()
    #check if bullet hit mobs
    hits=pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 40-hit.radius
        bomb_sound.play()
        expl=Explosion(hit.rect.center,'lg')
        all.add(expl)
        newmob()

    #check if mob hit Player
    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield-=hit.radius*2
        expl=Explosion(hit.rect.center,'sm')
        all.add(expl)

        #death_sound.play()
        if player.shield<=0:
            player_die_sound.play()
            player.hide()
            player.lives-=1
            player.shield=100
    if player.lives==0:
        player_die_sound.play()
        running=False


    #draw
    screen.fill(black)
    screen.blit(bg,bg_rect)
    all.draw(screen)
    draw(screen,str(score),18,w/2,10)
    draw(screen,str(player.shield),14,15,15)
    draw_shield(screen,5,5,player.shield)
    draw_lives(screen,w-90,5,player.lives,player_mini_img)
    # after drawing every thing
    pygame.display.flip()

pygame.quit()
