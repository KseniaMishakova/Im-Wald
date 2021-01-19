import pygame
import os
import sys
from levels import start_screen, load_image2, load_level, load_level2
from im_wald import SpriteGroup2, MagicButton, AnimatedHero, Tile


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
screen_size = (550, 550)
screen = pygame.display.set_mode(screen_size)

FPS = 60

# словарь с загруженными изображениями
tile_images = {
    'wall': load_image2('box.png'),
    'empty': load_image2('grass.png'),
    'button': load_image2('button1.png'),
    'button_down': load_image2('button2.png'),
    'bro': load_image2('bro.png')
}
# фоны для диалогов
tile_fones = {
    'fon1': load_image2('fon.png'),
    'fon2': load_image2('screen5.jpg'),
    'fon3': load_image2('fon3.png'),
    'fon4': load_image2('screen4.jpg'),
    'fon5': load_image2('screen6.jpg'),
    'fon6': load_image2('screen8.png')
}
player_image = load_image2('dude_4.png')

tile_width = tile_height = 50
tile_size = (tile_width, tile_height)

player = None
running = True
clock = pygame.time.Clock()
map_group = SpriteGroup2()
hero_group = SpriteGroup2()


# Генерация первого уровня
def generate_level(level, m_group, p_group, a_group):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tile_images['empty'], tile_size, x, y, m_group, a_group)
            elif level[y][x] == '#':
                Tile(tile_images['wall'], tile_size, x, y, m_group, a_group)
            elif level[y][x] == '@':
                Tile(tile_images['empty'], tile_size, x, y, m_group, a_group)
                new_player = AnimatedHero(load_image2("dude_4.png"), tile_size, 4, 1, x, y, p_group, a_group)
                level[y][x] = '.'
            elif level[y][x] == '$':
                Tile(tile_images['empty'], tile_size, x, y, m_group, a_group)
                Tile(tile_images['bro'], tile_size, x, y, m_group, a_group)
                level[y][x] = '.'
    return new_player, x, y


def generate_buttons(level, sprite_group):
    # todo предусмотреть передачу в класс MagicButton 2 изобрежений, не всего словаря
    # todo избавиться от использования глобальной переменной tile_size
    mb1, mb2, mb3, mb4, mb5 = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                mb1 = MagicButton(tile_images, tile_size, x, y, sprite_group)
            elif level[y][x] == '2':
                mb2 = MagicButton(tile_images, tile_size, x, y, sprite_group)
            elif level[y][x] == '3':
                mb3 = MagicButton(tile_images, tile_size, x, y, sprite_group)
            elif level[y][x] == '4':
                mb4 = MagicButton(tile_images, tile_size, x, y, sprite_group)
            elif level[y][x] == '5':
                mb5 = MagicButton(tile_images, tile_size, x, y, sprite_group)
    return mb1, mb2, mb3, mb4, mb5


# Передвижение героя
def move_hero(hero, level_map, movement, sprite_group):
    global mb1, mb2, mb3, mb4, mb5
    x, y = hero.pos
    if movement == "up":
        if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] == "1" or level_map[y - 1][x] == "2" or
                      level_map[y - 1][x] == "3" or level_map[y - 1][x] == "4" or level_map[y - 1][x] == "5"):
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and (level_map[y + 1][x] == "." or level_map[y + 1][x] == "1" or level_map[y + 1][x] == "2" or
                              level_map[y + 1][x] == "3" or level_map[y + 1][x] == "4" or level_map[y + 1][x] == "5"):
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] == "1" or level_map[y][x - 1] == "2" or
                      level_map[y][x - 1] == "3" or level_map[y][x - 1] == "4" or level_map[y][x - 1] == "5"):
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and (level_map[y][x + 1] == "." or level_map[y][x + 1] == "1" or level_map[y][x + 1] == "2" or
                              level_map[y][x + 1] == "3" or level_map[y][x + 1] == "4" or level_map[y][x + 1] == "5"):
            hero.move(x + 1, y)
    if level_map[hero.pos[1]][hero.pos[0]] == '1':
        if not mb1.enabled:
            mb1.switch()
            mb3.switch()
            mb4.switch()
    elif level_map[hero.pos[1]][hero.pos[0]] == '2':
        if not mb2.enabled:
            mb2.switch()
            mb4.switch()
            mb5.switch()
    elif level_map[hero.pos[1]][hero.pos[0]] == '3':
        if not mb3.enabled:
            mb1.switch()
            mb3.switch()
            mb5.switch()
    elif level_map[hero.pos[1]][hero.pos[0]] == '4':
        if not mb4.enabled:
            mb4.switch()
            mb1.switch()
            mb2.switch()
    elif level_map[hero.pos[1]][hero.pos[0]] == '5':
        if not mb5.enabled:
            mb5.switch()
            mb2.switch()
            mb3.switch()


# map2 = ['###########',
#         '#@........#',
#         '#....1....#',
#         '#.........#',
#         '#.5.....2.#',
#         '#.........#',
#         '#.........#',
#         '#.........#',
#         '#.4.....3.#',
#         '#.........#',
#         '###########']


if start_screen(screen, FPS, clock,
                ['Im_Wald',
                 'Для продолжения нажмите любую кнопку'],
                tile_fones['fon1'], 'black') == 1:
    terminate()
if start_screen(screen, FPS, clock,
                ["В игре есть две небольшие мини-игры.",
                 "Для того чтобы найти брата нужно их пройти.",
                 "Сюжетная линия будет отмечена как история."],
                tile_fones['fon1'], 'black') == 1:
    terminate()
if start_screen(screen, FPS, clock,
                ["История...",
                 "",
                 "Этот лес знаком нам с давно.",
                 "Я и мой брат часто приходим сюда.",
                 "Сегодня утром брат опять решил прогулять по лесу,",
                 "но до сих не вернулся.",
                 "Надо его поискать."],
                tile_fones['fon2'], 'black') == 1:
    terminate()
if start_screen(screen, FPS, clock,
                ["Перед вами кнопки",
                 "При нажатии кнопки лежащие против неё кнопки",
                 "меняют своё положение",
                 "Сделайте так, чтобы кнопки были все нажаты.",
                 "Найдите вашего любимого брата."],
                tile_fones['fon3'], 'blue') == 1:
    terminate()

# первая головоломка
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
running = True
i = 0
map_level_1 = load_level2("map2.txt")
player, max_x, max_y = generate_level(map_level_1, map_group, hero_group, all_sprites)
mb1, mb2, mb3, mb4, mb5 = generate_buttons(map_level_1, map_group)
# all_sprites.add(player)
# hero_group.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # у нас несколько циклов подряд, выход из цикла не приводит к закрытию приложения
            # принудительно закрываем приложение
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_hero(player, map_level_1, "up", map_group)
            elif event.key == pygame.K_DOWN:
                move_hero(player, map_level_1, "down", map_group)
            elif event.key == pygame.K_LEFT:
                move_hero(player, map_level_1, "left", map_group)
            elif event.key == pygame.K_RIGHT:
                move_hero(player, map_level_1, "right", map_group)
            if mb1.enabled and mb2.enabled and mb3.enabled and mb4.enabled and mb5.enabled:
                Tile(tile_images['empty'], tile_size, 10, 5, map_group)
            if mb1.enabled and mb2.enabled and mb3.enabled and mb4.enabled and mb5.enabled:
                if player.pos[0] == 9 and player.pos[1] == 5:
                    running = False

    # all_sprites.draw(screen)
    all_sprites.update()
    # if i % 40 == 0:
    #     player.update()
    # i += 1
    screen.fill(pygame.Color("black"))
    map_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()


if start_screen(screen, FPS, clock,
                ["История...",
                 "",
                 "Мне знакомо это место.",
                 "Думаю, я иду в правильном направлении."],
                tile_fones['fon4'], 'black') == 1:
    terminate()


# Камера
class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        # вычислим координату клитки, если она уехала влево за границу экрана
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        # вычислим координату клитки, если она уехала вправо за границу экрана
        if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
            obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
        obj.rect.y += self.dy
        # вычислим координату клитки, если она уехала вверх за границу экрана
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        # вычислим координату клитки, если она уехала вниз за границу экрана
        if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
            obj.rect.y += -obj.rect.height * (1 + self.field_size[1])

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 550
HEIGHT = 550
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player, all_sprites, tiles_group, player_group = None, None, None, None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_image = load_image2('dude_4.png')

tile_width = tile_height = 50
clock = pygame.time.Clock()
running = True
i = 0
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
if start_screen(screen, FPS, clock,
                ["История...",
                 "",
                 "Здесь очень много деревьев и кустов."],
                tile_fones['fon5'], 'black') == 1:
    terminate()
if start_screen(screen, FPS, clock,
                ["Вы в лабиринте",
                 "Вы не можете ходить сквозь деревья.",
                 "Лабиринт будет считаться пройденным, когда вы ",
                 "достигните своей цели.",
                 "Найдите своего любимого брата."],
                tile_fones['fon5'], 'black') == 1:
    terminate()

map_level_2 = load_level2('map3.txt')
player, level_x, level_y = generate_level(map_level_2, tiles_group, player_group, all_sprites)
camera = Camera((level_x, level_y))
# all_sprites.add(player)
# player_group.add(player)

running = True
x = 3
y = 19

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()  # принудительно закрываем приложение, чтобы не смотреть на следующие экраны
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_hero(player, map_level_2, "left", tiles_group)
            elif event.key == pygame.K_RIGHT:
                move_hero(player, map_level_2, "right", tiles_group)
            elif event.key == pygame.K_UP:
                move_hero(player, map_level_2, "up", tiles_group)
            if event.key == pygame.K_DOWN:
                move_hero(player, map_level_2, "down", tiles_group)
            if player.pos[0] == 17 and player.pos[1] == 4:
                running = False

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    # if i % 40 == 0:
    #     player.update()
    # i += 1
    pygame.display.flip()

    clock.tick(FPS)

if start_screen(screen, FPS, clock,
                ["История...",
                 "",
                 "Я нашёл своего брата.",
                 "Из-за большого количества кустов и деревьев",
                 "здесь можно легко заблудиться.",
                 "Но теперь всё хорошо, и мы возвращаемся домой."],
                tile_fones['fon6'], 'black') == 1:
    terminate()
if start_screen(screen, FPS, clock,
                ["Конец - это начало новой истории..."],
                tile_fones['fon1'], 'black') == 1:
    terminate()
pygame.quit()
