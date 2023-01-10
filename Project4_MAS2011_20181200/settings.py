import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
PURPLE = (143, 0, 255)
GRASS = (0, 154, 23)
SKY_BLUE = (0,204, 255)
D_GREEN = (1,50,32)

# game settings
WIDTH = 1500#1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 900#768  # 16 * 48 or 32 * 24 or 64 * 12
# WIDTH = pg.display.get_desktop_sizes()[0]
# HEIGHT = pg.display.get_desktop_sizes()[1]

FPS = 60
TITLE = "MAS 2011"
BGCOLOR = BROWN

TILESIZE = 128
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 350
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'student.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 30)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 150,
                     'kickback': 50,
                     'spread': 5,
                     'damage': 6,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 100,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
WEAPONS['machine gun'] = {'bullet_speed': 600,
                      'bullet_lifetime': 800,
                      'rate': 50,
                      'kickback': 60,
                      'spread': 8,
                      'damage': 5,
                      'bullet_size': 'lg',
                      'bullet_count': 1}

# Mob settings

MOBS = {}
MOBS['zombie'] = {
    'img' : 'pysnake.png',
    'speed' : [150, 100, 75, 125],
    'hit_rect' : pg.Rect(0, 0, 30, 30),
    'health' : 75,
    'damage' : 10,
    'knockback' : 20,
    'avoid_radius' : 50,
    'detect_radius' : 400
}
PYSNAKE_IMG = 'pysnake.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 80
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

NP_HEALTH = 150
NP_SPEED = 80

WM_HEALTH = 250
WM_SPEED = 55
WM_RADIUS = 300

HM_HEALTH = 60
HM_SPEED = 70
HM_RADIUS = 500

SH_HEALTH = 70
SH_SPEED = 160

PROF_HEALTH = 3000
PROF_SPEED = 450
PROF_RADIUS = 450

SUN_SPEED = 10
SUN_HIT_RECT = pg.Rect(0,0,230,230)
WM_HIT_RECT = pg.Rect(0,0,30,90)

STAR1_HEALTH = 300
STAR2_HEALTH = 180
STAR3_HEALTH = 270
STAR4_HEALTH = 500
STAR7_HEALTH = 120
STAR8_HEALTH = 290

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (45, 45, 45)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_soft.png"

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'stack_overflow.svg.png',
               'shotgun': 'obj_shotgun.png',
               'machine gun': 'machine_gun.png',
               'github' : 'github.svg.png'}
HEALTH_PACK_AMOUNT = 50
BOB_RANGE = 10
BOB_SPEED = 0.3

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'machine gun': ['pistol.wav']}
EFFECTS_SOUNDS = {'level_start': 'sogang_bell.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'github': 'health_pack.wav',
                  'metal_slug': 'heavy-machine-gun.wav'}
