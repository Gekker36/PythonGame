mapWidth  = 20
mapHeight = 20
tileSize  = 64
SCREEN_SIZE = (800, 608)


##Tile ID

grass = 0
water = 1
stone = 2
road = 3

##Colors
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)
brown = (153,76,0)

lightblue = (100,100,255)

## Main menu options

menu_options = ['Character Sheet', 'Inventory', 'Crafting', 'Spells', 'Talents', 'Options', 'Save', 'Load']

##Crafting recipes
crafting_recipes = {"sword" :["wood", "iron"]}

##GAME STATES
LEVEL = 'level'
# TOWN = 'town'
# MAIN_MENU = 'main menu'
# CASTLE = 'castle'
# INN = 'Inn'
# POTION_SHOP = 'potion shop'
# ARMOR_SHOP = 'armor shop'
# WEAPON_SHOP = 'weapon shop'
# MAGIC_SHOP = 'magic shop'
# HOUSE = 'house'
# OVERWORLD = 'overworld'
# BROTHER_HOUSE = 'brotherhouse'
# BATTLE = 'battle'
# DUNGEON = 'dungeon'
# DUNGEON2 = 'dungeon2'
# DUNGEON3 = 'dungeon3'
# DUNGEON4 = 'dungeon4'
# DUNGEON5 = 'dungeon5'
# INSTRUCTIONS = 'instructions'
# DEATH_SCENE = 'death scene'
# LOADGAME = 'load game'
# CREDITS = 'credits'


##LEVEL STATES

NORMAL = 'normal'
TRANSITION_IN = 'transition in'
TRANSITION_OUT = 'transition out'