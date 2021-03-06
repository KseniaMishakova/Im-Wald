import pygame
from levels import load_level2


class LevelMap:
    def __init__(self, file_name):
        self.map = load_level2(file_name)

    # Обратите внимание развернули координаты в более привычный на математике вид
    def get_cell(self, x, y):
        return self.map[y][x]

    def is_passage(self, x, y):
        return self.get_cell(x, y) != '#'


class SpriteGroup2(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite2(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = None

    def get_event(self, event):
        pass


# class Tile(pygame.sprite.Sprite):
#     def __init__(self, tile_type, pos_x, pos_y):
#         super().__init__(tiles_group, all_sprites)
#         self.image = tile_images[tile_type]
#         self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
#
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__(player_group, all_sprites)
#         self.image = player_image
#         self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Tile(Sprite2):
    def __init__(self, tile_image, tile_size, pos_x, pos_y, *sprite_group):
        super().__init__(*sprite_group)
        self.image = tile_image
        self.rect = self.image.get_rect().move(
            tile_size[0] * pos_x, tile_size[1] * pos_y)


class MagicButton(Sprite2):
    def __init__(self, tile_images, tile_size, pos_x, pos_y, *sprite_group):
        super().__init__(*sprite_group)
        self.pos = (pos_x, pos_y)
        self.enabled = False
        self.frames = []
        self.frames.append(tile_images['button'])
        self.frames.append(tile_images['button_down'])
        self.image = self.frames[int(self.enabled)]
        self.rect = self.image.get_rect().move(
            tile_size[0] * pos_x, tile_size[1] * pos_y)

    def switch(self):
        self.enabled = not self.enabled
        self.image = self.frames[int(self.enabled)]


class AnimatedHero(pygame.sprite.Sprite):
    def __init__(self, sheet, tile_size, columns, rows, pos_x, pos_y, *sprite_group):
        super().__init__(*sprite_group)
        self.frames = []
        self.tile_size = tile_size
        self.pos = (pos_x, pos_y)
        self.x = pos_x
        self.y = pos_y
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # self.rect = self.rect.move(x, y)
        self.move(pos_x, pos_y)
        self.tick = 0

    def set_pos(self, x, y):
        self.pos = (x, y)
        self.x = x
        self.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(50 * self.pos[0], 50 * self.pos[1], sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.tick == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.tick = (self.tick + 1) % 30

    def move(self, pos_x, pos_y):
        self.set_pos(pos_x, pos_y)
        self.rect = self.rect.move(self.tile_size[0] * self.pos[0] + 15, self.tile_size[1] * self.pos[1] + 5)
        self.rect = self.image.get_rect().move(
            self.tile_size[0] * self.pos[0] + 15, self.tile_size[1] * self.pos[1] + 5)
