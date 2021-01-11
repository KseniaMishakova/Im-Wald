import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('dude_4.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
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
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Герой двигается",
                  "Карта на месте"]

    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
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
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
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
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = AnimatedSprite(load_image("dude_4.png"), 4, 1, x, y)
                level[y][x] = "."
    return new_player, x, y


def move(hero1, movement):
    x, y = hero1.pos
    if movement == "up":
        if y > 0 and level_map[y - 1][x] == ".":
            hero1.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map[y + 1][x] == ".":
            hero1.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[y][x - 1] == ".":
            hero1.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map[y][x + 1] == ".":
            hero1.move(x + 1, y)

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60


class AnimatedSprite(pygame.sprite.Sprite):
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


clock = pygame.time.Clock()
running = True
i = 0
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
# dragon = AnimatedSprite(load_image("dude_3.png"), 4, 1, 66, 106)

start_screen()
level_map = load_level("map.txt")
hero, max_x, max_y = generate_level(level_map)
all_sprites.add(hero)
hero_group.add(hero)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
            elif event.key == pygame.K_ESCAPE:
                start_screen()
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
pygame.quit()