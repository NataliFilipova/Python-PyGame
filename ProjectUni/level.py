from support import *
from support import *
from tiles import StaticTile, Crate,Coin, Palm
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from enemy import Enemy



class Level:
    def __init__(self, level_data, surface):
        #general setup
        self.display_surface = surface
        self.world_shift = 0

        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        #crate
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        #coin
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        #foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

        #background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphicss/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphicss/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size, x, y, 'graphicss/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, 'graphicss/coins/silver')

                    if type == 'fg palms':
                        if val == '0': sprite = Palm(tile_size, x, y, 'graphicss/terrain/palm_small', 38)
                        if val == '1': sprite = Palm(tile_size, x, y, 'graphicss/terrain/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, 'graphicss/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)


                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # backgroud_palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)


        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        #
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)


        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)