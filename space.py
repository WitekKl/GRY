import math
import random
from typing import Optional
import arcade
from arcade.experimental import Shadertoy
SCREEN_TITLE = "space invaders"
# wykorzystano:
# Paul Vincent Craven.
# https://arcade.academy/index.html
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# https://www.shadertoy.com/
# muzyka jest dostępna na licencji Creative Commons

SPRITE_IMAGE_SIZE = 128
global path, full
MOVEMENT_SPEED = 15
MUSIC_VOLUME = 0.1
path = "space/OK/"
full = False

#definicja stałych
width, height = arcade.get_display_size()
przelicz = int(width/22)
SPRITE_SCALING_PLAYER = przelicz/128*1.5
SPRITE_SCALING_TILES = przelicz/128
SPRITE_SIZE_MAP = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_TILES)
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
ASPECT=SCREEN_HEIGHT / SCREEN_WIDTH
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 200
TOP_VIEWPORT_MARGIN = 200
VIEWPORT_MARGIN = 0
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 5

class PlayerSprite(arcade.Sprite):
    #definicja głownego statku
    def __init__(self,
                 hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER
        self.use_spatial_hash = True
        self.hit = False
        self.licznik = 0
        self.idle_textures = []
        for i in range(2):
            texture = arcade.load_texture_pair(f"{main_path}ship/ship0_{i}.png",hit_box_algorithm=hit_box_algorithm)
            self.idle_textures.append(texture)
        self.hit_textures = []
        texture = arcade.load_texture(f"{main_path}ship/ship_hit.png")
        self.hit_textures.append(texture)
        self.walk_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(f"{main_path}ship/ship{i}.png")
            self.walk_textures.append(texture)
        self.character_face_direction = RIGHT_FACING
        self.texture = self.walk_textures[0][RIGHT_FACING]
        self.hit_box = self.texture.hit_box_points
        self.texture = self.idle_textures[0][RIGHT_FACING]
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.dx = 0
        self.dy = 0
        self.czas = 0

    def update(self):
        if self.change_x < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        if self.hit:
            self.licznik +=1
            self.texture = self.hit_textures[0]
            if self.licznik==25:
                self.hit = False
                self.licznik =0
                self.texture = self.idle_textures[0][self.character_face_direction]
            return
        self.x_odometer += self.change_x
        self.y_odometer += self.change_y
        self.dy = self.change_y
        self.dx = self.change_x
        if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.y_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(self.dx) <= DEAD_ZONE and abs(self.dy)<=DEAD_ZONE:
            self.czas +=1
            if self.czas >5:
                self.cur_texture += 1
                if self.cur_texture > 1:
                    self.cur_texture = 0
                self.czas =0
                self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class Bullet (arcade.Sprite):
    #definicja pocisku
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.bullet_textures = []
        self.scale = 1.5
        self.kat = 0
        self.wybor = 0
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}other/shot_{i}.png")
            self.bullet_textures.append(texture)
        self.bullet2_textures = []
        for i in range(2):
            texture = arcade.load_texture(f"{main_path}other/missile0_{i}.png")
            self.bullet2_textures.append(texture)
        self.bullet3_textures = []
        for i in range(2):
            texture = arcade.load_texture(f"{main_path}other/miss_{i}.png")
            self.bullet3_textures.append(texture)
        # Start at the first frame
        self.cur_texture = 0
        self.texture = self.bullet_textures[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc += 1
        if self.szybkosc >= 5:
            if self.wybor == 0:
                self.cur_texture += 1
                if self.cur_texture < len(self.bullet_textures):
                    self.texture = self.bullet_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.bullet_textures[self.cur_texture]
                    self.szybkosc = 0
            elif self.wybor ==1:
                self.cur_texture += 1
                if self.cur_texture < len(self.bullet2_textures):
                    self.texture = self.bullet2_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.bullet2_textures[self.cur_texture]
                    self.szybkosc = 0
            elif self.wybor ==2:
                self.cur_texture += 1
                if self.cur_texture < len(self.bullet3_textures):
                    self.texture = self.bullet3_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.bullet3_textures[self.cur_texture]
                    self.szybkosc = 0
            if self.center_y >SCREEN_HEIGHT:
                self.remove_from_sprite_lists()

class BulletEnemy (arcade.Sprite):
    #definicja strzału obcych
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.kat = 0
        self.bullet_textures = []
        self.scale = 0.75
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}other/enemy_shot_{i}.png")
            self.bullet_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.bullet_textures[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc += 1
        if self.szybkosc >=5:
            self.cur_texture += 1
            if self.cur_texture < len(self.bullet_textures):
                self.texture = self.bullet_textures[self.cur_texture]
                self.szybkosc = 0
            else:
                self.cur_texture = 0
                self.szybkosc = 0
        if self.center_y <-5:
            self.remove_from_sprite_lists()

class MenuView(arcade.View):
    #ekran startowy
    def __init__(self):
        super().__init__()
        self.window.sound = 0
        self.window.music=0
        self.window.level=1
        self.window.musicp = arcade.sound.load_sound("space/ok/music/neon-laser.mp3")
        self.window.media_player =self.window.musicp.play(MUSIC_VOLUME)
        file_name = "star_nest.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = width, height
        self.time = 0
        self.shadertoy = Shadertoy(size, shader_sourcecode)

    def on_update(self, dt):
        self.time += dt

    def on_draw(self):
        # efekt ruchu gwiazd - nowa wersja
        arcade.start_render()
        self.shadertoy.render(time=self.time)
        arcade.load_font(font_name="space/ok/Hardsign.ttf")

        arcade.draw_text("Nacisnij klawisz myszki i poczekaj chwile", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-55,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
        arcade.draw_text("SPACE INVADERS", SCREEN_WIDTH /2 , SCREEN_HEIGHT *2/ 3,
                         arcade.color.RED_DEVIL, font_size=60, anchor_x="center", font_name='Hardsign')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.musicp.stop(player=self.window.media_player)
        game_view = GameView()
        self.window.show_view(game_view)

class GameOverView(arcade.View):
    #defincja ekranu po przejsciu wszytskich poziomów
    def __init__(self):
        super().__init__()
        file_name = "star_nest.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = width, height
        self.time = 0
        self.shadertoy = Shadertoy(size, shader_sourcecode)
        self.win_sound = arcade.load_sound("space/ok/music/game_over1.mp3")
        if self.window.music ==0:
            self.media_player =self.win_sound.play(MUSIC_VOLUME)

    def on_update(self, dt):
        self.time += dt

    def on_draw(self):
        # efekt ruchu gwiazd - nowa wersja
        arcade.start_render()
        self.shadertoy.render(time=self.time)
        arcade.load_font(font_name="space/ok/Hardsign.ttf")
        arcade.draw_text("Gratulacje, skonczyles wszystkie poziomy !!!", SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
        arcade.draw_text("Nacisnij klawisz myszki by grac jeszcze raz", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        self.window.level = 1
        if self.window.music == 0:
            self.win_sound.stop(player=self.media_player)
        arcade.cleanup_texture_cache()
        game_view = GameView()
        self.window.show_view(game_view)

class GameOver1View(arcade.View):
    # defincja ekranu po game over - inne napisy
    def __init__(self):
        super().__init__()
        file_name = "star_nest.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = width, height
        self.time = 0
        self.shadertoy = Shadertoy(size, shader_sourcecode)
        self.gameover_sound = arcade.load_sound("space/ok/music/game_over2.mp3")
        if self.window.music ==0:
            self.media_player =self.gameover_sound.play(MUSIC_VOLUME)

    def on_update(self, dt):
        self.time += dt

    def on_draw(self):
        # efekt ruchu gwiazd - nowa wersja
        arcade.start_render()
        self.shadertoy.render(time=self.time)

        arcade.draw_text("Twoj wynik:" + str(self.window.score), SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
        arcade.draw_text("Nacisnij klawisz myszki by grac jeszcze raz", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
        arcade.draw_text("Nacisnij Z aby zaczac od pierwszego poziomu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4,
                         arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        if self.window.music == 0:
            self.gameover_sound.stop(player=self.media_player)
        arcade.cleanup_texture_cache()
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        # sterowanie
        if key == arcade.key.Z:
            self.window.level=1
            self.window.score = 0
            if self.window.music == 0:
                self.gameover_sound.stop(player=self.media_player)
            game_view = GameView()
            self.window.show_view(game_view)


class Wybuch1(arcade.Sprite):
    #definicja wybuchu
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.wybuch_textures = []
        self.scale = 0.5
        for i in range(11):
            texture = arcade.load_texture(f"{main_path}other/Explosion/boom{i}.png")
            self.wybuch_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.wybuch_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc+= 1
        if self.szybkosc ==5:
            self.cur_texture += 1
            if self.cur_texture < len(self.wybuch_textures):
                self.texture = self.wybuch_textures[self.cur_texture]
                self.szybkosc =0
            else:
                self.remove_from_sprite_lists()
                self.cur_texture = 0
                self.szybkosc = 0

class Wybuch2(arcade.Sprite):
    # definicja wybuchu - rodzaj 2
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.wybuch_textures = []
        self.scale = 1
        for i in range(17):
            texture = arcade.load_texture(f"{main_path}other/Explosion2/1_{i}.png")
            self.wybuch_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.wybuch_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc+= 1
        if self.szybkosc ==4:
            self.cur_texture += 1
            if self.cur_texture < len(self.wybuch_textures):
                self.texture = self.wybuch_textures[self.cur_texture]
                self.szybkosc =0
            else:
                self.remove_from_sprite_lists()
                self.cur_texture = 0
                self.szybkosc = 0

class Wybuch3(arcade.Sprite):
    #definicja wybuchu 3 rodzaj
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.wybuch_textures = []
        self.scale = 0.2
        for i in range(6):
            texture = arcade.load_texture(f"{main_path}other/flame/exp_bomb{i}.png")
            self.wybuch_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.wybuch_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc+= 1
        if self.szybkosc ==5:
            self.cur_texture += 1
            if self.cur_texture < len(self.wybuch_textures):
                self.texture = self.wybuch_textures[self.cur_texture]
                self.szybkosc =0
            else:
                self.remove_from_sprite_lists()
                self.cur_texture = 0
                self.szybkosc = 0

class Bomba(arcade.Sprite):
    # wybuch bomby
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.wybuch_textures = []
        self.scale = 0.25
        for i in range(10):
            texture = arcade.load_texture(f"{main_path}other/missw_{i}.png")
            self.wybuch_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.wybuch_textures[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc += 1
        if self.szybkosc == 6:
            self.cur_texture += 1
            if self.cur_texture < len(self.wybuch_textures):
                self.texture = self.wybuch_textures[self.cur_texture]
                self.szybkosc = 0
            else:
                self.remove_from_sprite_lists()
                self.cur_texture = 0
                self.szybkosc = 0

class Spaceenemy(arcade.Sprite):
    #definicja obcych Bosów (3 rodzaje)
    def __init__(self, hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        self.szybkosc = 0
        self.change_x = 10
        self.ktory =0
        self.moc = 10
        self.space1_textures = []
        self.scale = 1
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}ship/boss_{i}.png")
            self.space1_textures.append(texture)
        self.space2_textures = []
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}ship/boss3_{i}.png")
            self.space2_textures.append(texture)
        self.space3_textures = []
        for i in range(5):
            texture = arcade.load_texture(f"{main_path}ship/boss2_{i}.png")
            self.space3_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.space1_textures[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.center_x +=self.change_x
        self.szybkosc += 1
        if self.ktory == 1:
            if self.szybkosc == 5:
                self.cur_texture += 1
                if self.cur_texture < len(self.space1_textures):
                    self.texture = self.space1_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.space1_textures[self.cur_texture]
                    self.szybkosc = 0
        elif self.ktory == 2:
            if self.szybkosc == 5:
                self.cur_texture += 1
                if self.cur_texture < len(self.space2_textures):
                    self.texture = self.space2_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.space2_textures[self.cur_texture]
                    self.szybkosc = 0
        elif self.ktory == 3:
            if self.szybkosc == 5:
                self.cur_texture += 1
                if self.cur_texture < len(self.space3_textures):
                    self.texture = self.space3_textures[self.cur_texture]
                    self.szybkosc = 0
                else:
                    self.cur_texture = 0
                    self.texture = self.space3_textures[self.cur_texture]
                    self.szybkosc = 0

class Punkty(arcade.Sprite):
    #wyświetlenie punktów - animacja
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.szybkosc = 0
        self.ilepunkty = 0
        self.punkty_textures = []
        self.scale = 0.5
        for i in range(18):
            texture = arcade.load_texture("space/OK/sparkle_" + str(i) + ".png")
            self.punkty_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.punkty_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc= self.szybkosc+1
        if self.szybkosc ==5:
            self.cur_texture += 1
            if self.cur_texture < len(self.punkty_textures):
                self.texture = self.punkty_textures[self.cur_texture]
                self.szybkosc =0
            else:
                self.remove_from_sprite_lists()
                self.cur_texture = 0
                self.szybkosc = 0

class Shield(arcade.Sprite):
    #tarcza
    def __init__(self, hit_box_algorithm):
        super().__init__()

        self.ochron = []
        for i in range(4):
            texture = arcade.load_texture("space/OK/other/shield" + str(i) + ".png")
            self.ochron.append(texture)
        self.scale = 0.66
        self.shieldon = 0
        self.szybkosc = 0
        self.cur_texture = 0
        self.texture = self.ochron[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc += 1
        if self.szybkosc >=3:
            self.cur_texture += 1
            if self.cur_texture < len(self.ochron):
                self.texture = self.ochron[self.cur_texture]
                self.szybkosc = 0
            else:
                self.cur_texture = 0
                self.texture = self.ochron[0]
                self.szybkosc = 0

    def follow_sprite(self, player_sprite):
        self.center_y = player_sprite.center_y
        self.center_x = player_sprite.center_x

class GameView(arcade.View):
    #główna część programu
    def __init__(self):
        super().__init__()
        #definicja sprite-ów
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.player_sprite: Optional[PlayerSprite] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.asteroid_list: Optional[arcade.SpriteList] = None
        self.extra_list: Optional[arcade.SpriteList] = None
        self.wybuch1_list:Optional[arcade.SpriteList] = None
        self.wybuch2_list:Optional[arcade.SpriteList] = None
        self.wybuch3_list:Optional[arcade.SpriteList] = None
        self.bullet_list:Optional[arcade.SpriteList] = None
        self.enemy_bullet_list:Optional[arcade.SpriteList] = None
        self.bomb_list : Optional[arcade.SpriteList] = None
        self.enemy_list: Optional[arcade.SpriteList] = None
        self.shield_list:Optional[arcade.SpriteList] = None
        self.bomba_list:Optional[arcade.SpriteList] = None
        self.spaceenemy_list: Optional[arcade.SpriteList] = None
        self.punkty: Optional[arcade.SpriteList] = None
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.background = None
        self.max_level = 5
        self.tile_map = None
        file_name = "star_nest.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = width, height
        self.shadertoy = Shadertoy(size, shader_sourcecode)
        self.setup()

    def setup(self):
        #definicja zmiennych
        self.player_list = arcade.SpriteList()
        self.ruch_speed = 5
        self.czas_ruchspeed = 0
        self.czas_ruchfrozen = 0
        self.view_bottom = 0
        self.view_left = 0
        self.life=3
        self.gun1 = 0
        self.bomb =0
        self.shield1 = 0
        self.time = 0
        self.background = arcade.Sprite("space/OK/background.jpg")
        self.background.left = self.background.bottom = 0
        self.gun_active = 0
        self.shield_active = 0
        self.bomb_active = 0
        self.czyinwazja = 0
        self.koniecpoziomu_czas = 0

        # Odczyt map
        map_name = "space/OK/space_"+str(self.window.level) + ".json"

        self.my_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
        #self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.my_map.width* SPRITE_SIZE_MAP
        self.end_of_map_y =self.my_map.height* SPRITE_SIZE_MAP
        #obrazy informacyjne do wyświetlenia
        self.scr2 = texture = arcade.load_texture("space/OK/tiles/shieldGold.png")
        self.scr4 = texture = arcade.load_texture("space/OK/ship/ship0.png")
        self.scr3 = texture = arcade.load_texture("space/OK/tiles/bullet1.png")
        self.scr1 = texture = arcade.load_texture("space/OK/tiles/gun.png")
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        self.stars = arcade.load_texture("space/ok/stars.png")
        #dzwięki
        self.posbobme_sound = arcade.sound.load_sound("space/ok/music/wypbomb2.wav")
        self.wybbombe_sound= arcade.sound.load_sound("space/ok/music/wypbomb.ogg")
        self.hit_sound = arcade.sound.load_sound("space/ok/music/kick.ogg")
        self.boss_sound = arcade.load_sound("space/ok/music/fall4.wav")
        self.zbior_sound = arcade.load_sound("space/ok/music/upgrade.ogg")
        self.shot_sound = arcade.load_sound("space/ok/music/shot.wav")
        self.wybuch_sound = arcade.load_sound("space/ok/music/explosion2.wav")
        self.level_sound = arcade.load_sound("space/ok/music/level2.ogg")
        #muzyka
        self.win_sound = arcade.load_sound("space/ok/music/game_over1.mp3")
        self.window.musicp = arcade.sound.load_sound("space/ok/music/neon-laser.mp3")
        if self.window.music ==0:
            self.window.media_player =self.window.musicp.play(MUSIC_VOLUME)

        # główne sprite-y
        self.bullet_list = arcade.SpriteList()
        self.bullet = Bullet(hit_box_algorithm="Simple")
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemybullet = BulletEnemy(hit_box_algorithm="Simple")
        self.wybuch1_list = arcade.SpriteList()
        self.wybuch1 = Wybuch1(hit_box_algorithm="Simple")
        self.wybuch2_list = arcade.SpriteList()
        self.wybuch2 = Wybuch1(hit_box_algorithm="Simple")
        self.wybuch3_list = arcade.SpriteList()
        self.wybuch3 = Wybuch1(hit_box_algorithm="Simple")
        self.shield_list = arcade.SpriteList()
        self.shield = Shield(hit_box_algorithm="Simple")
        self.bomba_list = arcade.SpriteList()
        self.bomba = Bomba(hit_box_algorithm="Simple")
        self.spaceenemy_list = arcade.SpriteList()
        self.spaceenemy = Spaceenemy(hit_box_algorithm="Simple")
        self.punkty_list = arcade.SpriteList()
        self.punkty = Punkty(hit_box_algorithm="Simple")

        self.asteroid_list = self.my_map.sprite_lists['asteroid']
        self.bomb_list = self.my_map.sprite_lists['bomb']
        self.extra_list = self.my_map.sprite_lists['extra']
        self.exit_list = self.my_map.sprite_lists['exit']
        self.enemy_list = self.my_map.sprite_lists ['enemy']

        # Definicja statku
        self.player_sprite = PlayerSprite( hit_box_algorithm="Simple")
        self.player_sprite.center_x = 160*SPRITE_SCALING_PLAYER
        self.player_sprite.center_y = 160*SPRITE_SCALING_PLAYER
        self.player_sprite.physics_engine = self.physics_engine
        self.player_list.append(self.player_sprite)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.asteroid_list,
                                                             gravity_constant=0)

        for enemy in self.enemy_list:
            enemy.change_x = 3
        self.iloscast = len (self.asteroid_list)

    def on_key_press(self, key, modifiers):
        # sterowanie
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.SPACE:
            if self.window.sound == 0:
                arcade.sound.play_sound(self.shot_sound)
            self.strzal(self.gun1)
        elif key == arcade.key.Z:
            if self.bomb >0 and self.bomb_active ==0:
                    self.bomb_active = 1
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.posbobme_sound)
                    self.postaw_bombe()
                    self.bomb -=1
            if self.bomb_active >10:
                self.wybuch_bomby()
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.wybuch_sound)
                self.bomb_active=0
        elif key == arcade.key.ENTER:
            if self.koniecpoziomu_czas >0:
                self.koniecpoziomu_czas = 1
        elif key == arcade.key.S:
            if self.window.sound== 0:
                self.window.sound = 1
            else:
                self.window.sound = 0
        elif key == arcade.key.M:
            if self.window.music == 0:
                self.window.music = 1
                self.window.musicp.stop(player=self.window.media_player)

            else:
                self.window.music = 0
                self.window.media_player =self.window.musicp.play(MUSIC_VOLUME)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def strzal(self, gun):
        # wystrzał
        if self.gun1 == 0:
            self.bullet = Bullet(hit_box_algorithm="Simple")
            self.bullet.center_x = self.player_sprite.center_x
            self.bullet.center_y = self.player_sprite.top
            self.bullet.kat = 0
            self.bullet_list.append(self.bullet)
        elif self.gun1 >0:
            if int(random.randrange(3))==0:
                for i in range(5):
                    self.bullet = Bullet(hit_box_algorithm="Simple")
                    self.bullet.center_x = self.player_sprite.center_x
                    self.bullet.center_y = self.player_sprite.top
                    self.bullet.kat = i/10 - 0.17
                    self.bullet.texture = self.bullet.bullet2_textures[0]
                    self.bullet.scale = 0.5
                    self.bullet.wybor = 1
                    self.bullet_list.append(self.bullet )
            else:
                for i in range(4):
                    self.bullet = Bullet(hit_box_algorithm="Simple")
                    self.bullet.center_x = self.player_sprite.center_x
                    self.bullet.center_y = self.player_sprite.top
                    self.bullet.kat =i/10 - 0.17
                    self.bullet_list.append(self.bullet)

    def postaw_bombe (self):
        # wystrzelenie pocisku
        self.bullet = Bullet(hit_box_algorithm="Simple")
        self.bullet.center_x = self.player_sprite.center_x
        self.bullet.center_y = self.player_sprite.top
        self.bullet.kat = 0
        self.bullet.texture = self.bullet.bullet3_textures[0]
        self.bullet.scale = 0.2
        self.bullet.wybor = 2
        self.bullet_list.append(self.bullet)

    def wybuch_bomby (self):
        #wybuch pocisku
        self.bomba = Bomba(hit_box_algorithm="Simple")
        for bullet in self.bullet_list:
            if bullet.wybor == 2:
                self.bomba.center_x = bullet.center_x
                self.bomba.center_y = bullet.center_y
                bullet.remove_from_sprite_lists()
                self.bomba_list.append(self.bomba)

    def strzalenemy(self, gun, x,y):
        #strzelanie wroga
        if self.czyinwazja == 0:
            self.enemybullet = BulletEnemy(hit_box_algorithm="Simple")
            self.enemybullet.center_x = x
            self.enemybullet.center_y = y
            self.enemybullet.kat = 0
            self.enemy_bullet_list.append(self.enemybullet)
        else:
            for i in range(5):
                self.enemybullet = BulletEnemy(hit_box_algorithm="Simple")
                self.enemybullet.center_x = x
                self.enemybullet.center_y = y
                self.enemybullet.kat = i / 10 - 0.17
                self.enemy_bullet_list.append(self.enemybullet)

    def nowywybuch1(self,  x,y):
        #ustawianie pozycji startowych wybuchów
        self.wybuch1 = Wybuch1(hit_box_algorithm="Simple")
        self.wybuch1.center_x = x
        self.wybuch1.center_y = y
        self.wybuch1.update()
        self.wybuch1_list.append(self.wybuch1)

    def nowywybuch2(self,  x,y):
        # ustawianie pozycji startowych wybuchów - 2 rodzaj
        self.wybuch2 = Wybuch2(hit_box_algorithm="Simple")
        self.wybuch2.center_x = x
        self.wybuch2.center_y = y
        if self.czyinwazja >0:
            self.wybuch2.scale = 2
        else:
            self.wybuch2.scale = 1
        self.wybuch2.update()
        self.wybuch2_list.append(self.wybuch2)

    def nowywybuch3(self,  x,y):
        # ustawianie pozycji startowych wybuchów - 3 rodzaj
        self.wybuch3 = Wybuch3(hit_box_algorithm="Simple")
        self.wybuch3.center_x = x
        self.wybuch3.center_y = y
        self.wybuch3.update()
        self.wybuch3_list.append(self.wybuch3)

    def uzyjshield(self):
        #włączenie tarczy
        self.shield = Shield(hit_box_algorithm="Simple")
        self.shield.center_x = self.player_sprite.center_x
        self.shield.center_y = self.player_sprite.center_y
        self.shield.update()
        self.shield_list.append(self.shield)
        self.shield_active = 1

    def inwazja (self):
        # pojawienie się Bossa
        self.spaceenemy = Spaceenemy(hit_box_algorithm="Simple")
        self.spaceenemy.center_x = width/4
        self.spaceenemy.top = height
        self.spaceenemy.change_x = 10
        self.spaceenemy.ktory = self.window.level
        if self.spaceenemy.ktory ==1:
            self.spaceenemy.texture = (self.spaceenemy.space1_textures)[0]
        elif self.spaceenemy.ktory ==2:
            self.spaceenemy.texture = (self.spaceenemy.space2_textures)[0]
        else:
            self.spaceenemy.texture = (self.spaceenemy.space3_textures)[0]
        self.spaceenemy.scale = 1
        self.spaceenemy.moc = 15 + self.window.level * 5
        self.spaceenemy_list.append(self.spaceenemy)

    def nowy_level(self):
        #po zniszczeniu Bossa
        self.koniecpoziomu_czas = 0
        self.czyinwazja = 0
        if self.window.music == 0:
            self.window.musicp.stop(player=self.window.media_player)
            self.mediaplayer2 = self.win_sound.play(MUSIC_VOLUME)
            self.win_sound.stop(player=self.mediaplayer2)
        if self.window.level < self.max_level:
            self.window.level += 1
            self.setup()
        else:
            arcade.cleanup_texture_cache()
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def nowy_punkty(self, center_x, center_y, points):
        #ustawianie pozycji startowych punktów
        self.punkty = Punkty(hit_box_algorithm="Simple")
        self.punkty.center_x = center_x
        self.punkty.center_y = center_y
        self.punkty.ilepunkty = points
        self.punkty_list.append(self.punkty)

    def on_update(self, delta_time):
        self.time +=delta_time
        #główna część, uaktualnienie danych
        self.enemy_list.update_animation()
        self.bomb_list.update_animation()
        self.extra_list.update_animation()
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.wybuch1_list.update()
        self.wybuch2_list.update()
        self.wybuch3_list.update()
        self.spaceenemy_list.update()
        self.bomba_list.update()
        self.punkty_list.update()
        if self.czas_ruchspeed>0:
            self.czas_ruchspeed -=1
        if self.czas_ruchfrozen>0:
            self.czas_ruchfrozen -=1
        if self.shield1>0:
            self.shield_list.update()
            self.shield.follow_sprite(self.player_sprite)
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.ruch_speed = 4+ 4*len(self.asteroid_list)/self.iloscast
        if self.czas_ruchspeed >0:
            self.ruch_speed +=5
        if self.czas_ruchfrozen >0:
            self.ruch_speed = self.ruch_speed/2
        if self.up_pressed and not self.down_pressed :
            self.player_sprite.change_y = MOVEMENT_SPEED
            if self.player_sprite.center_y>SCREEN_HEIGHT-SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5:
                self.player_sprite.center_y=SCREEN_HEIGHT-SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
            if self.player_sprite.center_y<SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5:
                self.player_sprite.center_y=SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            if self.player_sprite.center_x<SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5:
                self.player_sprite.center_x=SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
            if self.player_sprite.center_x>self.end_of_map-SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5:
                self.player_sprite.center_x=self.end_of_map-SPRITE_IMAGE_SIZE*SPRITE_SCALING_PLAYER*0.5

        #sprawdzanie kolizji sprite-ów
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.spr_game_over()
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.bomb_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bomb_list)
            for bomb in hit_list:
                bomb.remove_from_sprite_lists()
                self.spr_game_over()
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.wybuch3_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.wybuch3_list)
            for wybuch3 in hit_list:
                wybuch3.remove_from_sprite_lists()
                self.spr_game_over()
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
            for enemybul in hit_list:
                enemybul.remove_from_sprite_lists()
                self.spr_game_over()
        if len(arcade.check_for_collision_with_list(self.shield, self.enemy_bullet_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.shield, self.enemy_bullet_list)
            for enemybul in hit_list:
                enemybul.remove_from_sprite_lists()
                #self.player_sprite.hit = True
                if self.life <=0:
                    self.window.musicp.stop(player=self.window.media_player)
                    if self.window.sound == 0:
                        self.window.mediaplayer1=self.window.gameover_sound.play(MUSIC_VOLUME)
                        self.window.mediaplayer2=self.window.win_sound.play(MUSIC_VOLUME)
                    arcade.cleanup_texture_cache()
                    game_over_view = GameOver1View()
                    self.window.show_view(game_over_view)
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.extra_list)) > 0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.extra_list)
            for extra in hit_list:
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.zbior_sound)
                if str(extra.properties['Ext']) == "Live":
                    self.life += 1
                elif str(extra.properties['Ext']) == "Gun":
                    self.gun1 += 1
                    self.gun_active =1
                elif str(extra.properties['Ext']) == "Bomb":
                    self.bomb += 5
                elif str(extra.properties['Ext']) == "frozen":
                    self.czas_ruchfrozen += 200
                elif str(extra.properties['Ext']) == "speed":
                    self.czas_ruchspeed += 200
                elif str(extra.properties['Ext']) == "Shield":
                    self.shield1 +=1
                extra.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            enemy.draw_hit_box(color=arcade.csscolor.RED, line_thickness=10)
            if int(random.randrange(20))==0:
                x=enemy.center_x
                y=enemy.bottom
                gun = 1
                if enemy.center_y<height:
                    self.strzalenemy(gun,x,y)
            if len(arcade.check_for_collision_with_list(enemy, self.asteroid_list)) > 0:
                enemy.change_x *= -1
            if len(arcade.check_for_collision_with_list(enemy, self.bomb_list)) > 0:
                enemy.change_x *= -1
            if len(arcade.check_for_collision_with_list(enemy, self.enemy_list)) > 0:
                enemy.change_x *= -1
            if enemy.center_x<0:
                enemy.change_x *= -1
            if enemy.center_x>self.end_of_map:
                enemy.change_x *= -1
            if enemy.center_y < -50:
                enemy.remove_from_sprite_lists()
            if enemy.bottom<height:
                if enemy.change_x>0:
                    enemy.center_x += self.ruch_speed
                else:
                    enemy.center_x -= self.ruch_speed
            enemy.center_y -=self.ruch_speed
            if len(arcade.check_for_collision_with_list(enemy, self.bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(enemy, self.bullet_list)
                for bullet in hit_list:
                    bullet.remove_from_sprite_lists()
                    x=enemy.center_x
                    y = enemy.center_y
                    enemy.remove_from_sprite_lists()
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.wybuch_sound)
                    self.nowywybuch1(x,y)
                    self.window.score +=10
            if len(arcade.check_for_collision_with_list(enemy, self.bomba_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(enemy, self.bomba_list)
                for bomba in hit_list:
                    bomba.remove_from_sprite_lists()
                    x=enemy.center_x
                    y = enemy.center_y
                    enemy.remove_from_sprite_lists()
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.wybuch_sound)
                    self.nowywybuch1(x,y)
                    self.window.score +=10

        for asteroid in self.asteroid_list:
            asteroid.center_y -=self.ruch_speed
            if asteroid.bottom<height:
                asteroid.angle -= 5 + int(random.randrange(5))
            if asteroid.center_y<-50:
                asteroid.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(asteroid, self.bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(asteroid, self.bullet_list)
                for bullet in hit_list:
                    bullet.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(asteroid, self.enemy_bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(asteroid, self.enemy_bullet_list)
                for enemybul in hit_list:
                    enemybul.remove_from_sprite_lists()

        for bomb in self.bomb_list:
            bomb.center_y -=self.ruch_speed
            if bomb.bottom<height:
                bomb.angle += self.ruch_speed + int(random.randrange(5))
            if bomb.center_y<-50:
                bomb.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(bomb, self.bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(bomb, self.bullet_list)
                for bullet in hit_list:
                    bullet.remove_from_sprite_lists()
                    x=bomb.center_x
                    y=bomb.center_y
                    bomb.remove_from_sprite_lists()
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.wybuch_sound)
                    self.nowywybuch2(x,y)
                    self.window.score +=20
            if len(arcade.check_for_collision_with_list(bomb, self.bomba_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(bomb, self.bomba_list)
                for bomba in hit_list:
                    bomba.remove_from_sprite_lists()
                    x = bomb.center_x
                    y = bomb.center_y
                    bomb.remove_from_sprite_lists()
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.wybuch_sound)
                    self.nowywybuch2(x,y)
                    self.window.score +=20
            if bomb.center_y<2*height/3 and int(random.randrange(40))==0:
                x = bomb.center_x
                y = bomb.center_y
                bomb.remove_from_sprite_lists()
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.wybbombe_sound)
                self.nowywybuch3(x,y)

        for extra in self.extra_list:
            extra.center_y -=self.ruch_speed
            if extra.bottom<height:
                extra.angle += 5 + int(random.randrange(5))
            if len(arcade.check_for_collision_with_list(extra, self.bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(extra, self.bullet_list)
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.zbior_sound)
                for bullet in hit_list:
                    if str(extra.properties['Ext']) == "Live":
                        self.life += 1
                    elif str(extra.properties['Ext']) == "Gun":
                        self.gun1 += 1
                        self.gun_active =1
                    elif str(extra.properties['Ext']) == "Bomb":
                        self.bomb += 5
                    elif str(extra.properties['Ext']) == "Shield":
                        self.shield1 += 1
                    bullet.remove_from_sprite_lists()
                    extra.remove_from_sprite_lists()
            if extra.center_y<-50:
                extra.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            if bullet.wybor<3:
                bullet.center_y +=self.ruch_speed* 2* math.cos(bullet.kat)
                bullet.center_x += self.ruch_speed * 2 * math.sin(bullet.kat)
            else:
                bullet.center_y +=self.ruch_speed * 2

        for bullet_enemy in self.enemy_bullet_list:
            if self.czyinwazja ==0:
                bullet_enemy.center_y -=self.ruch_speed*2
            else:
                bullet_enemy.center_y -=self.ruch_speed*2 * math.cos(bullet_enemy.kat)
                bullet_enemy.center_x -= self.ruch_speed * 2 * math.sin(bullet_enemy.kat)

        for exit in self.exit_list:
            exit.center_y -=self.ruch_speed
            if self.player_sprite.center_y > exit.top:
                if self.czyinwazja ==0:
                    self.czyinwazja = 1
                    self.inwazja ()
                    if self.window.sound == 0:
                        self.window.musicp.stop(player=self.window.media_player)
                        arcade.sound.play_sound(self.level_sound)
            if exit.center_y < -150:
                exit.remove_from_sprite_lists()

        if self.czyinwazja ==1:
            for statek in self.spaceenemy_list:
                statek.center_y -= 1
                if statek.left < 0:
                    statek.change_x *= -1
                if statek.right > self.end_of_map:
                    statek.change_x *= -1
                if int(random.randrange(25)) == 0:
                    x = statek.center_x
                    y = statek.bottom
                    gun = 1
                    self.strzalenemy(gun, x, y)
                if len(arcade.check_for_collision_with_list(statek, self.bullet_list)) > 0:
                    hit_list = arcade.check_for_collision_with_list(statek, self.bullet_list)
                    for bullet in hit_list:
                        if self.window.sound == 0:
                            arcade.sound.play_sound(self.boss_sound)
                        statek.moc -=1
                        points = 20
                        self.window.score += points
                        center_x = bullet.center_x
                        center_y = bullet.center_y
                        self.window.score +=points
                        self.nowy_punkty(center_x, center_y, points)
                        bullet.remove_from_sprite_lists()
                if len(arcade.check_for_collision_with_list(statek, self.bomba_list)) > 0:
                    hit_list = arcade.check_for_collision_with_list(statek, self.bomba_list)
                    for bomba in hit_list:
                        if self.window.sound == 0:
                            arcade.sound.play_sound(self.boss_sound)
                        statek.moc -= 3
                        points = 50
                        self.window.score += points
                        center_x = bomba.center_x
                        center_y = bomba.center_y
                        self.window.score += points
                        self.nowy_punkty(center_x, center_y, points)
                        bomba.remove_from_sprite_lists()
                if statek.moc <=0:
                    x = statek.center_x
                    y = statek.center_y
                    self.nowywybuch2(x, y)
                    statek.remove_from_sprite_lists()
                    if self.window.music == 0:
                        self.window.musicp.stop(player=self.window.media_player)
                        self.mediaplayer2=self.win_sound.play (MUSIC_VOLUME)
                    self.koniecpoziomu_czas = 500
                if statek.bottom<0:
                    self.inwazja()
                    statek.remove_from_sprite_lists()
        if self.shield_active ==0 and self.shield1>0:
            self.uzyjshield()
        if self.shield_active >0:
            self.shield_active+=1
            if self.shield_active >= 300:
                self.shield_active =0
                self.shield1 -=1
                self.shield.remove_from_sprite_lists()
        if self.gun_active >0:
            self.gun_active+=1
            if self.gun_active >= 300:
                self.gun_active =0
                self.gun1 -= 1
        if self.bomb_active >0:
            self.bomb_active +=1

        self.physics_engine.update()
        self.player_sprite.update()

    def spr_game_over(self ):
        if self.window.sound == 0:
            arcade.sound.play_sound(self.hit_sound)
        self.life -= 1
        self.player_sprite.hit = True
        if self.life <= 0:
            if self.window.music == 0:
                self.window.musicp.stop(player=self.window.media_player)
            arcade.cleanup_texture_cache()
            game_over_view = GameOver1View()
            self.window.show_view(game_over_view)

    def on_draw(self):
        #rysowanie wszystkich obiektów
        arcade.start_render()
        self.shadertoy.render(time=self.time)
        self.asteroid_list.draw()
        self.enemy_list.draw()
        self.bomb_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.extra_list.draw()
        self.player_list.draw()
        self.wybuch1_list.draw()
        self.wybuch2_list.draw()
        self.wybuch3_list.draw()
        self.spaceenemy_list.draw()
        self.bomba_list.draw()
        self.punkty_list.draw()
        if self.shield1>0:
            self.shield_list.draw()
        self.wynik()

    def wynik(self):
        #napisy po zakońzceniu poziomu

        if self.koniecpoziomu_czas >0:
            arcade.draw_text("Gratulacje, skonczyles poziom " + str(self.window.level), SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3,
                             arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
            arcade.draw_text("Nacisnij klawisz ENTER by grac dalej", SCREEN_WIDTH / 2,
                             SCREEN_HEIGHT / 2,
                             arcade.color.RED_BROWN, font_size=40, anchor_x="center", font_name='Hardsign')
            self.koniecpoziomu_czas -=1
            if self.koniecpoziomu_czas ==0:
                self.czyinwazja = 0
                self.nowy_level()

        #aktualizacja danych informacyjnych
        arcade.draw_rectangle_filled(10, 0 , 1900, 130,
                                     arcade.csscolor.WHITE)

        arcade.draw_scaled_texture_rectangle(300 , 50, self.scr2, scale=0.5)
        arcade.draw_text(str(self.shield1), 325 , 35 ,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')

        arcade.draw_scaled_texture_rectangle(200 , 50 , self.scr1, scale=0.5)
        arcade.draw_text(str(self.gun1), 240 , 35 ,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')

        arcade.draw_scaled_texture_rectangle(100, 50, self.scr4, scale=0.5)
        arcade.draw_text(str(self.life), 130 , 35,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')

        arcade.draw_scaled_texture_rectangle(400, 50, self.scr3, scale=0.5)
        arcade.draw_text(str(self.bomb), 440, 35,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')
        arcade.draw_text("Points:" + str(self.window.score) + "    " + "Level;" + str(self.window.level), 500, 35,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')
        arcade.draw_text("Frozen:" + str(self.czas_ruchfrozen) + "    " + "Speed:" + str(self.czas_ruchspeed), 750, 35,
                         arcade.csscolor.BLACK, 20, font_name='Hardsign')

        for punkt in self.punkty_list:
            x = punkt.center_x
            y = punkt.center_y
            wartosc = punkt.ilepunkty
            #arcade.load_font(font_name='space/ok/Kenney Future.ttf')
            arcade.draw_text(str(wartosc), x, y,arcade.csscolor.GREENYELLOW, 20, font_name='Hardsign')

def main():
    # Metoda główna
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen= full)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
