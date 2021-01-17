import pygame
import os
import sys


def load_image2(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (550, 550)
screen = pygame.display.set_mode(screen_size)
FPS = 60

tile_images = {
    'wall': load_image2('box.png'),
    'empty': load_image2('grass.png'),
    'button': load_image2('button1.png'),
    'button_down': load_image2('button2.png')
}
player_image = load_image2('dude_4.png')

tile_width = tile_height = 50


class ScreenFrame2(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup2(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite2(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile2(Sprite2):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class MagicButton(Sprite2):
    def __init__(self, pos_x, pos_y):
        super().__init__(sprite_group)
        self.pos = (pos_x, pos_y)
        self.enabled = False
        self.frames = []
        self.frames.append(tile_images['button'])
        self.frames.append(tile_images['button_down'])
        self.image = self.frames[int(self.enabled)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def switch(self):
        self.enabled = not self.enabled
        self.image = self.frames[int(self.enabled)]


class Player2(Sprite2):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup2()
hero_group = SpriteGroup2()


def terminate2():
    pygame.quit()
    sys.exit


def start_screen2():
    intro_text = ["В Лесу",
                  "для начала игры нажмите любую кнопку"]

    fon = pygame.transform.scale(load_image2('fon.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate2()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level2(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile2('empty', x, y)
            elif level[y][x] == '#':
                Tile2('wall', x, y)
            elif level[y][x] == '@':
                Tile2('empty', x, y)
                new_player = AnimatedSprite2(load_image2("dude_4.png"), 4, 1, x, y)
                level[y][x] = "."
    return new_player, x, y


def generate_buttons(level):
    mb1, mb2, mb3, mb4, mb5 = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                mb1 = MagicButton(x, y)
            elif level[y][x] == '2':
                mb2 = MagicButton(x, y)
            elif level[y][x] == '3':
                mb3 = MagicButton(x, y)
            elif level[y][x] == '4':
                mb4 = MagicButton(x, y)
            elif level[y][x] == '5':
                mb5 = MagicButton(x, y)
    return mb1, mb2, mb3, mb4, mb5


def move2(hero, movement):

    global mb1, mb2, mb3, mb4, mb5
    x, y = hero.pos
    if movement == "up":
        if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] == "1" or level_map[y - 1][x] == "2" or
                      level_map[y - 1][x] == "3" or level_map[y - 1][x] == "4" or level_map[y - 1][x] == "5"):
            hero.move(x, y - 1)
            if level_map[y - 1][x] == '1':
                if not mb1.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb4.switch()
            elif level_map[y - 1][x] == '2':
                if not mb2.enabled:
                    mb2.switch()
                    mb4.switch()
                    mb5.switch()
            elif level_map[y - 1][x] == '3':
                if not mb3.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb5.switch()
            elif level_map[y - 1][x] == '4':
                if not mb4.enabled:
                    mb4.switch()
                    mb1.switch()
                    mb2.switch()
            elif level_map[y - 1][x] == '5':
                if not mb5.enabled:
                    mb5.switch()
                    mb2.switch()
                    mb3.switch()
    elif movement == "down":
        if y < max_y - 1 and (level_map[y + 1][x] == "." or level_map[y + 1][x] == "1" or level_map[y + 1][x] == "2" or
                              level_map[y + 1][x] == "3" or level_map[y + 1][x] == "4" or level_map[y + 1][x] == "5"):
            hero.move(x, y + 1)
            if level_map[y + 1][x] == '1':
                if not mb1.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb4.switch()
            elif level_map[y + 1][x] == '2':
                if not mb2.enabled:
                    mb2.switch()
                    mb4.switch()
                    mb5.switch()
            elif level_map[y + 1][x] == '3':
                if not mb3.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb5.switch()
            elif level_map[y + 1][x] == '4':
                if not mb4.enabled:
                    mb4.switch()
                    mb1.switch()
                    mb2.switch()
            elif level_map[y + 1][x] == '5':
                if not mb5.enabled:
                    mb5.switch()
                    mb2.switch()
                    mb3.switch()
    elif movement == "left":
        if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] == "1" or level_map[y][x - 1] == "2" or
                      level_map[y][x - 1] == "3" or level_map[y][x - 1] == "4" or level_map[y][x - 1] == "5"):
            hero.move(x - 1, y)
            if level_map[y][x - 1] == '1':
                if not mb1.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb4.switch()
            elif level_map[y][x - 1] == '2':
                if not mb2.enabled:
                    mb2.switch()
                    mb4.switch()
                    mb5.switch()
            elif level_map[y][x - 1] == '3':
                if not mb3.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb5.switch()
            elif level_map[y][x - 1] == '4':
                if not mb4.enabled:
                    mb4.switch()
                    mb1.switch()
                    mb2.switch()
            elif level_map[y][x - 1] == '5':
                if not mb5.enabled:
                    mb5.switch()
                    mb2.switch()
                    mb3.switch()
    elif movement == "right":
        if x < max_x - 1 and (level_map[y][x + 1] == "." or level_map[y][x + 1] == "1" or level_map[y][x + 1] == "2" or
                              level_map[y][x + 1] == "3" or level_map[y][x + 1] == "4" or level_map[y][x + 1] == "5"):
            hero.move(x + 1, y)
            if level_map[y][x + 1] == '1':
                if not mb1.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb4.switch()
            elif level_map[y][x + 1] == '2':
                if not mb2.enabled:
                    mb2.switch()
                    mb4.switch()
                    mb5.switch()
            elif level_map[y][x + 1] == '3':
                if not mb3.enabled:
                    mb1.switch()
                    mb3.switch()
                    mb5.switch()
            elif level_map[y][x + 1] == '4':
                if not mb4.enabled:
                    mb4.switch()
                    mb1.switch()
                    mb2.switch()
            elif level_map[y][x + 1] == '5':
                if not mb5.enabled:
                    mb5.switch()
                    mb2.switch()
                    mb3.switch()
    if mb1.enabled and mb2.enabled and mb3.enabled and mb4.enabled and mb5.enabled:
        Tile2('empty', 10, 5)


class AnimatedSprite2(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(all_sprites)
        self.frames = []
        self.pos = (pos_x, pos_y)
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # self.rect = self.rect.move(x, y)
        self.move(1, 1)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(50 * self.pos[0], 50 * self.pos[1], sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.rect = self.rect.move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


map2 = ['###########',
        '#@........#',
        '#....1....#',
        '#.........#',
        '#.5.....2.#',
        '#.........#',
        '#.........#',
        '#.........#',
        '#.4.....3.#',
        '#.........#',
        '###########']
x = 1
y = 1
clock = pygame.time.Clock()
running = True
i = 0
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
# dragon = AnimatedSprite(load_image("dude_3.png"), 4, 1, 66, 106)

start_screen2()
level_map = load_level2("map2.txt")
hero, max_x, max_y = generate_level(level_map)
mb1, mb2, mb3, mb4, mb5 = generate_buttons(level_map)
all_sprites.add(hero)
hero_group.add(hero)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move2(hero, "up")
                if map2[y - 1][x] != '#':
                    y = y - 1
            elif event.key == pygame.K_DOWN:
                move2(hero, "down")
                if map2[y + 1][x] != '#':
                    y = y + 1
            elif event.key == pygame.K_LEFT:
                move2(hero, "left")
                if map2[y][x - 1] != '#':
                    x = x - 1
            elif event.key == pygame.K_RIGHT:
                move2(hero, "right")
                if map2[y][x + 1] != '#':
                    x = x + 1
                if mb1.enabled and mb2.enabled and mb3.enabled and mb4.enabled and mb5.enabled:
                    if hero.pos[0] == 9 and hero.pos[1] == 5:
                        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.draw(screen)
    if i % 40 == 0:
        hero.update()
    i += 1
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 550
HEIGHT = 550
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(filename):
    filename = 'data/' + filename
    return pygame.image.load(filename).convert_alpha()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = AnimatedSprite(load_image("dude_4.png"), 4, 1, x, y)
                level[y] = level[y][:x] + '.' + level[y][x + 1:]
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["В ЛЕСУ",
                  "для начала игры нажмите любую кнопку"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('dude_4.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(all_sprites)
        self.frames = []
        self.pos = (pos_x, pos_y)
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.move(3, 19)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(50 * self.pos[0], 50 * self.pos[1], sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self, pos_x, pos_y):
        self.pos = (pos_x, pos_y)
        self.rect = self.rect.move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)


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


clock = pygame.time.Clock()
running = True
i = 0
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
start_screen()

player, level_x, level_y = generate_level(load_level("map3.txt"))
camera = Camera((level_x, level_y))
all_sprites.add(player)
player_group.add(player)

running = True

map = load_level('map3.txt')

x = 3
y = 19

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if map[y][x - 1] != '#':
                    player.rect.x -= 50
                    x = x - 1
            if event.key == pygame.K_RIGHT:
                if map[y][x + 1] != '#':
                    player.rect.x += 50
                    x = x + 1
            if event.key == pygame.K_UP:
                if y == 4 and x == 17:
                    terminate()
                elif map[y - 1][x] != '#':
                    player.rect.y -= 50
                    y = y - 1
            if event.key == pygame.K_DOWN:
                if map[y + 1][x] != '#':
                    player.rect.y += 50
                    y = y + 1

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    if i % 40 == 0:
        player.update()
    i += 1
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()


