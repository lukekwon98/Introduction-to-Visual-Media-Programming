# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 23
# Lighting Effect
# Video link: https://youtu.be/IWm5hi5Yrvk
import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *
import math
# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.sogang_img = pg.image.load(path.join(img_folder, '서강대학교.png')).convert_alpha()
        self.sogang_img = pg.transform.scale(self.sogang_img, (420, 420))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.prof_img = pg.image.load(path.join(img_folder, 'Prof.png')).convert_alpha()
        self.sun_img = pg.image.load(path.join(img_folder, 'sun2.png')).convert_alpha()
        self.sun_img = pg.transform.scale(self.sun_img, (250, 250))
        self.player_img = pg.transform.scale(self.player_img, (65, 60))
        self.player_img = pg.transform.rotate(self.player_img, -90)
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.pysnake_img = pg.image.load(path.join(img_folder, PYSNAKE_IMG)).convert_alpha()
        self.pysnake_img = pg.transform.scale(self.pysnake_img, (64, 64))
        self.pysnake_img = pg.transform.rotate(self.pysnake_img, -90)
        self.shmup_img = pg.image.load(path.join(img_folder, 'shmup.png')).convert_alpha()
        self.shmup_img = pg.transform.scale(self.shmup_img, (72, 72))
        self.shmup_img = pg.transform.rotate(self.shmup_img, -90)
        self.numpy_img = pg.image.load(path.join(img_folder, 'numpy.png')).convert_alpha()
        self.numpy_img = pg.transform.scale(self.numpy_img, (64, 64))
        self.numpy_img = pg.transform.rotate(self.numpy_img, -90)
        self.profPNG_img = pg.image.load(path.join(img_folder, 'Prof_removedbg.png')).convert_alpha()
        self.profPNG_img = pg.transform.scale(self.profPNG_img, (150, 150))
        self.profPNG_img = pg.transform.rotate(self.profPNG_img, -90)
        self.windmill_img = pg.image.load(path.join(img_folder, 'windmill3.png')).convert_alpha()
        self.windmill_img = pg.transform.scale(self.windmill_img, (80, 120))
        self.windmill_img = pg.transform.rotate(self.windmill_img, 90)
        self.hangman_img = pg.image.load(path.join(img_folder, 'hangman.png')).convert_alpha()
        self.hangman_img = pg.transform.scale(self.hangman_img, (70, 90))
        self.star1_img = pg.image.load(path.join(img_folder, 'star1.png')).convert_alpha()
        self.star1_img = pg.transform.scale(self.star1_img, (100, 100))
        self.star2_img = pg.image.load(path.join(img_folder, 'star2.png')).convert_alpha()
        self.star2_img = pg.transform.scale(self.star2_img, (100, 100))
        self.star3_img = pg.image.load(path.join(img_folder, 'star3.png')).convert_alpha()
        self.star3_img = pg.transform.scale(self.star3_img, (100, 100))
        self.star4_img = pg.image.load(path.join(img_folder, 'star4.png')).convert_alpha()
        self.star4_img = pg.transform.scale(self.star4_img, (100, 100))
        self.star7_img = pg.image.load(path.join(img_folder, 'star7.png')).convert_alpha()
        self.star7_img = pg.transform.scale(self.star7_img, (100, 100))
        self.star8_img = pg.image.load(path.join(img_folder, 'star8.png')).convert_alpha()
        self.star8_img = pg.transform.scale(self.star8_img, (100, 100))
        #self.hangman_img = pg.transform.rotate(self.windmill_img, 90)
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.splat.set_colorkey(BLACK)
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
            if item == 'health' or item == 'github' or item == 'machine gun':
                self.item_images[item] = pg.transform.scale(self.item_images[item], (56, 56))
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            if type == 'level_start':
                self.effects_sounds[type].set_volume(0.3)
        self.emotional_damage = pg.mixer.Sound(path.join(snd_folder, 'emotional_damage.wav'))
        self.emotional_damage.set_volume(0.7)
        self.failure = pg.mixer.Sound(path.join(snd_folder, 'failure.wav'))
        self.failure.set_volume(1)
        self.heartbeat = pg.mixer.Sound(path.join(snd_folder, 'heartbeat.wav'))
        self.heartbeat.set_volume(3)
        self.weak_clapping = pg.mixer.Sound(path.join(snd_folder, 'weak_clapping.wav'))
        self.weak_clapping.set_volume(8)
        self.yay = pg.mixer.Sound(path.join(snd_folder, 'yay.wav'))
        self.yay.set_volume(50)
        self.tadaa = pg.mixer.Sound(path.join(snd_folder, 'tadaa.wav'))
        self.tadaa.set_volume(8)
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobList = []
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'sun':
                Sun(self, obj_center.x, obj_center.y)
            if tile_object.name == 'numpy':
                Numpy(self, obj_center.x, obj_center.y)
            if tile_object.name == 'windmill':
                Windmill(self, obj_center.x, obj_center.y)
            if tile_object.name == 'hangman':
                Hangman(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'starone':
                star1(self, obj_center.x, obj_center.y)
            if tile_object.name == 'startwo':
                star2(self, obj_center.x, obj_center.y)
            if tile_object.name == 'starthree':
                star3(self, obj_center.x, obj_center.y)
            if tile_object.name == 'starfour':
                star4(self, obj_center.x, obj_center.y)
            if tile_object.name == 'starseven':
                star7(self, obj_center.x, obj_center.y)
            if tile_object.name == 'stareight':
                star8(self, obj_center.x, obj_center.y)
            if tile_object.name == 'shmup':
                shmup(self, obj_center.x, obj_center.y) 
            if tile_object.name == 'professor':
                Professor(self, obj_center.x, obj_center.y) 
            if tile_object.name in ['health','github', 'shotgun', 'machine gun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()
        self.score = 0
        self.github = 0
        self.start = True
        self.prof = True
        self.startTime = pg.time.get_ticks()
        self.nightDelay = 9000
        self.FA = True
        self.OOT = False
        #self.eclipse = False
        #self.eclipseTime = pg.time.get_ticks()
        #self.eclipseDelay = 9000

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        # pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        #print(self.mobList)
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over
        if len(self.mobs) == 1:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
            if hit.type == 'machine gun':
                hit.kill()
                self.effects_sounds['metal_slug'].play()
                self.player.weapon = 'machine gun'
            if hit.type == 'github':
                hit.kill()
                self.effects_sounds['github'].play()
                a1 = choice(self.mobList[:]) 
                a1.kill()
                self.mobList.remove(a1)
                a2 = choice(self.mobList[:])
                a2.kill()
                self.mobList.remove(a2)
                self.github += 1
                self.score += 2
        if self.github >= 4:
            self.playing = False
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = mob.vel*0.85
        
        if self.prof == False:
            self.playing = False
        
        if pg.time.get_ticks() - self.startTime >= 300000:
            self.FA = False

        if pg.time.get_ticks() - self.startTime >= 1500000: #150000:
            self.OOT = True
            self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("MAS 2011")
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob) or isinstance(sprite, Professor) or isinstance(sprite, shmup) or isinstance(sprite,Sun) or isinstance(sprite, Numpy) or isinstance(sprite, Windmill) or isinstance(sprite, Hangman)or isinstance(sprite, star1) or isinstance(sprite, star2) or isinstance(sprite, star3) or isinstance(sprite, star4) or isinstance(sprite, star7) or isinstance(sprite, star8):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        seconds = (math.floor((pg.time.get_ticks() - self.startTime)/1000))%60
        minutes = (math.floor((pg.time.get_ticks() - self.startTime)/1000/60))
        day = (math.floor((pg.time.get_ticks() - self.startTime)/1000/100))
        #print((math.floor((pg.time.get_ticks() - self.startTime)/1000%110)))
        if (math.floor((pg.time.get_ticks() - self.startTime)/1000%50)) == 0:
            if pg.time.get_ticks() - self.nightDelay > 1000:
                self.night = not self.night
                self.nightDelay = pg.time.get_ticks()

        if self.night:
            self.render_fog()
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Assignments: {}'.format(len(self.mobs)-1), self.hud_font, 30, BLUE,
                       WIDTH -120, 20, align="center")
        self.draw_text('Score: {}'.format(self.score), self.hud_font, 30, WHITE,
                       WIDTH/2-200, 20, align="center")
        self.draw_text('Day{} {}:{}'.format(day, minutes, seconds), self.hud_font, 30, WHITE,
                       WIDTH/2+200, 20, align="center")
        self.draw_text('Github: {}'.format(self.github), self.hud_font, 30, BLACK,
                       WIDTH-80, HEIGHT-40, align="center")
        self.draw_text('F/A: {}'.format(self.FA), self.hud_font, 30, BLACK,
                       80, HEIGHT-40, align="center")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.hud_font, 105, RED, WIDTH / 2, HEIGHT / 2 - 100, align="center")
            self.draw_text("Press P to Resume", self.hud_font, 80, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("or ESC to Quit", self.hud_font, 80, WHITE, WIDTH / 2, HEIGHT / 2 + 100, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night

    def show_start_screen(self):
        pg.mixer.music.play(loops=-1)
        self.screen.blit(self.dim_screen, (0,0))
        self.screen.blit(self.sogang_img, (WIDTH/2 - 210, 30))
        self.draw_text("MAS 2011", self.title_font, 130, WHITE, WIDTH / 2, HEIGHT / 2 + 30, align="center")
        self.draw_text("Press Any Key ", self.title_font, 75, RED, WIDTH / 2, HEIGHT / 2 + 190, align="center")
        self.draw_text("If You Dare", self.title_font, 75, RED, WIDTH / 2, HEIGHT / 2 + 240, align="center")
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        if self.OOT == True:
            self.screen.fill(BLACK)
            self.screen.blit(self.prof_img, (WIDTH/2 - 210, 50))
            self.draw_text("YOU'RE OUT OF TIME!", self.hud_font, 100, RED,
                        WIDTH / 2, HEIGHT / 2 + 160, align="center")
            # self.draw_text("YOU GET AN INSTANT F!", self.hud_font, 75, WHITE,
            #             WIDTH / 2, HEIGHT * 3.1 / 4, align="center")
            pg.display.flip()
            pg.time.delay(2000)
            self.wait_for_key()


        if self.github >=4 : 
            self.screen.fill(BLACK)
            self.screen.blit(self.prof_img, (WIDTH/2 - 210, 50))
            self.draw_text("PLAGIARISM!", self.hud_font, 100, RED,
                        WIDTH / 2, HEIGHT / 2 + 160, align="center")
            self.draw_text("YOU GET AN INSTANT F!", self.hud_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3.2 / 4, align="center")
            pg.display.flip()
            pg.time.delay(2000)
            self.wait_for_key()
        
        if self.prof == False:
            self.screen.fill(BLACK)
            self.screen.blit(self.prof_img, (WIDTH/2 - 210, 50))
            self.draw_text("HOW DARE YOU", self.hud_font, 100, RED,
                        WIDTH / 2, HEIGHT / 2 + 160, align="center")
            # self.draw_text("YOU GET AN INSTANT F!", self.hud_font, 75, WHITE,
            #             WIDTH / 2, HEIGHT * 3.1 / 4, align="center")
            pg.display.flip()
            pg.time.delay(2000)
            self.wait_for_key()
        
        if self.FA == True and len(self.mobs) != 1 and self.prof != False and self.github < 4: #and self.github <4
            self.screen.fill(BLACK)
            self.screen.blit(self.prof_img, (WIDTH/2 - 210, 50))
            self.draw_text("YOU DIDN'T LAST 3 DAYS", self.hud_font, 100, RED,
                        WIDTH / 2, HEIGHT / 2 + 160, align="center")
            self.draw_text("F/A!", self.hud_font, 75, WHITE,
                         WIDTH / 2, HEIGHT * 3.2 / 4, align="center")
            pg.display.flip()
            pg.time.delay(2000)
            self.wait_for_key()


        if self.github >=4 or self.prof == False or (self.FA == True and len(self.mobs)!=1):
            self.score = 0
        if self.score >= 0 and self.score<= 12:
            grade = 'F'
            self.emotional_damage.play()
        elif self.score <=24:
            grade = 'D'
            self.failure.play()
        elif self.score <=36:
            grade = 'C'
            self.failure.play()
        elif self.score <=48:
            grade = 'B'
            self.weak_clapping.play()
        elif self.score <=69:
            grade = 'A'
            self.yay.play()
        else:
            grade = 'A+'
            self.tadaa.play()

        self.screen.fill(BLACK)
        #if 0<=self.score and self.score<=30:
            #self.emotional_damage.play()
        self.screen.blit(self.prof_img, (WIDTH/2 - 210, 50))
        # self.draw_text("GAME OVER", self.hud_font, 100, RED,
        #                WIDTH / 2, HEIGHT*0.5 / 2, align="center")
        self.draw_text("YOUR GRADE IS : {}".format(grade), self.hud_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2+160, align="center")
        if self.score <=36:
            self.draw_text("PRESS ANY KEY TO JAESOOGANG", self.hud_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3.2 / 4, align="center")
        elif self.score <= 48:
             self.draw_text("NOT BAD, PRESS ESC TO GRADUATE", self.hud_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3.2 / 4, align="center")
        elif self.score <= 69:
             self.draw_text("VERY GOOD, PRESS ESC TO GRADUATE", self.hud_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3.2 / 4, align="center")
        else:
             self.draw_text("CONGRATULATIONS, WELCOME TO MY LAB", self.hud_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3.2 / 4, align="center")        
        pg.display.flip()
        pg.time.delay(1500)
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
running = True
while running:
    g.new()
    g.run()
    g.show_go_screen()
    waiting = True
    while waiting:
        g.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                g.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    waiting = False
                else:
                    waiting = False