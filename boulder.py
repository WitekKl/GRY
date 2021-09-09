import math
import random
import os
from typing import Optional
import arcade

# wykorzystano:
# Paul Vincent Craven.
# https://arcade.academy/index.html
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# muzyka jest dostępna na licencji Creative Commons

#stałe
SCREEN_TITLE = "PyMunk Boulder"
SPRITE_IMAGE_SIZE = 128
global path, full
GRAVITY = 500
FRICTION = 0.5
PLAYER_MAX_HORIZONTAL_SPEED = 1000
PLAYER_MAX_VERTICAL_SPEED = 1000
PLAYER_FORCE = 8000
path = "pymunk/images/diament/Warrior_"
full = False
# Skala sprite-ów
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.5
SPRITE_SIZE_MAP = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_TILES)
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15
width, height = arcade.get_display_size()
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 200
TOP_VIEWPORT_MARGIN = 200
VIEWPORT_MARGIN = 0
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 10

class PlayerSprite(arcade.Sprite):
    #definicja gracza
    def __init__(self,
                 hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        # definicja stałych gracza
        self.kop = False
        self.czas = 0
        self.poczatek = True
        self.scale = SPRITE_SCALING_PLAYER
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}IDLE.png",
                                                          hit_box_algorithm=hit_box_algorithm)
        # Textury gracza
        self.walk_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(f"{main_path}WALK_{i}.png")
            self.walk_textures.append(texture)
        self.kop_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(f"{main_path}ATTACK{i}.png")
            self.kop_textures.append(texture)
        # Kierunek twarzy
        self.character_face_direction = RIGHT_FACING
        # Początkowe textury
        self.texture = self.walk_textures[0][RIGHT_FACING]
        self.hit_box = self.texture.hit_box_points
        self.texture = self.idle_texture_pair[0]
        # Numeracja tekstór
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.dx=0
        self.dy=0
        self.pymunk.gravity = (0, 0)
        self.pymunk.damping = 0.0001

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        # wykorzystanie pymunk do ruchu
        if self.kop == True:
            self.czas +=1
            if self.poczatek - True:
                self.texture = self.cur_texture = 0
                self.poczatek = False
                self.texture = self.kop_textures[self.cur_texture][self.character_face_direction]
            if self.czas==5:
                self.czas =0
                self.texture = self.kop_textures[self.cur_texture][self.character_face_direction]
                self.cur_texture +=1
                if self.cur_texture >9:
                    self.cur_texture = 0
                    self.poczatek =True
                    self.kop = False
                    self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        # kiedy zmiana kierunku
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        self.x_odometer += dx
        self.y_odometer += dy
        self.dx = dx
        self.dy = dy
        #czy zmiana textury
        if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.y_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(dx) <= DEAD_ZONE and abs(dy)<=DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 9:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class Wall (arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.5

class Zanik(arcade.Sprite):
    # definicja klasy - zanik
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.szybkosc = 0
        self.wybor =0
        self.zanik_textures = []
        self.scale = 0.5
        for i in range(4):
            texture = arcade.load_texture("pymunk/images/diament/12_" + str(i) + ".png")
            self.zanik_textures.append(texture)
        self.zanik1_textures = []
        self.scale = 0.5
        for i in range(4):
            texture = arcade.load_texture("pymunk/images/diament/13_" + str(i) + ".png")
            self.zanik1_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.zanik_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        if self.wybor ==0:
            self.texture = self.zanik_textures[self.cur_texture]
            self.szybkosc= self.szybkosc+1
            if self.szybkosc ==5:
                self.cur_texture += 1
                if self.cur_texture < len(self.zanik_textures):
                    self.texture = self.zanik_textures[self.cur_texture]
                    self.szybkosc =0
                else:
                    self.remove_from_sprite_lists()
                    self.cur_texture = 0
                    self.szybkosc = 0
        if self.wybor ==1:
            self.texture = self.zanik1_textures[self.cur_texture]
            self.szybkosc= self.szybkosc+1
            if self.szybkosc ==5:
                self.cur_texture += 1
                if self.cur_texture < len(self.zanik1_textures):
                    self.texture = self.zanik_textures[self.cur_texture]
                    self.szybkosc =0
                else:
                    self.remove_from_sprite_lists()
                    self.cur_texture = 0
                    self.szybkosc = 0

class Punkty(arcade.Sprite):
    # klasa punkty
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.szybkosc = 0
        self.ilepunkty = 0
        self.punkty_textures = []
        self.scale = 0.5
        for i in range(18):
            texture = arcade.load_texture("pymunk/images/diament/sparkle_" + str(i) + ".png")
            self.punkty_textures.append(texture)
        # Start at the first frame
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

class Dynamit1(arcade.Sprite):
    #Klasa dynamit
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.szybkosc = 0
        self.scale = 0.5
        self.wybuch = 0
        self.czywybuchdynamit = False
        self.dynamit1_textures = []
        for i in range(6):
            texture = arcade.load_texture("pymunk/images/diament/dynamite0" + str(i) + ".png")
            self.dynamit1_textures.append(texture)
        self.explosion1_textures= []
        for i in range(16):
            texture = arcade.load_texture("pymunk/images/diament/ekspozja_" + str(i) + ".png")
            self.explosion1_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.explosion1_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points
        self.texture = self.dynamit1_textures [self.cur_texture]

    def update(self):
        self.szybkosc= self.szybkosc+1
        if self.wybuch ==  0:
            if self.szybkosc ==10:
                self.cur_texture += 1
                if self.cur_texture < len(self.dynamit1_textures):
                    self.texture = self.dynamit1_textures[self.cur_texture]
                    self.hit_box = self.texture.hit_box_points
                    self.szybkosc =0
                else:
                    self.cur_texture = 0
                    self.szybkosc = 0
                    self.wybuch = 1
        else:
            if self.szybkosc ==5:
                if self.cur_texture < len(self.explosion1_textures):
                    self.texture = self.explosion1_textures[self.cur_texture]
                    self.hit_box = self.texture.hit_box_points
                    self.cur_texture += 1
                    self.szybkosc =0
                    return
                else:
                    self.wybuch = 0
                    self.szybkosc = 0
                    self.cur_texture = 0
                    self.texture = self.dynamit1_textures[self.cur_texture]
                    self.hit_box = self.texture.hit_box_points
                    self.czywybuchdynamit = True

class Wybuchdynamit(arcade.Sprite):
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class GameOverView(arcade.View):
    # ekrany po Game Over
    def __init__(self):
        super().__init__()
        if width<1400:
            self.background = arcade.Sprite("pymunk/images/diament/st.jpg")
        else:
            self.background = arcade.Sprite("pymunk/images/diament/st1.jpg")
        self.background.left = self.background.bottom = 0

    def on_draw(self):
        self.view_bottom = 0
        self.view_left = 0
        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom)
        arcade.start_render()
        self.background.draw()
        score_text1 = " GAME OVER "
        arcade.draw_text(score_text1 , SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4,arcade.csscolor.RED, 64,anchor_x="center",font_name='pymunk/images/diament/Retro.otf')
        score_text1 = "Twoj wynik " + str(self.window.score)
        arcade.draw_text(score_text1 , SCREEN_WIDTH/2, SCREEN_HEIGHT/2,arcade.csscolor.RED, 64,anchor_x="center",font_name='pymunk/images/diament/Retro.otf')
        arcade.draw_text("Nacisnij klawisz myszki i poczekaj chwile", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,
                         arcade.color.RED_BROWN, font_size=30, anchor_x="center",font_name='pymunk/images/diament/Retro.otf')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        game_view = GameView()
        self.window.show_view(game_view)

class GameOverWygralesView(arcade.View):
    #ekran to przejściu wszystich poziomów
    def __init__(self):
        super().__init__()
        if width<1400:
            self.background = arcade.Sprite("pymunk/images/diament/st.jpg")
        else:
            self.background = arcade.Sprite("pymunk/images/diament/st1.jpg")
        self.background.left = self.background.bottom = 0

    def on_draw(self):
        self.view_bottom = 0
        self.view_left = 0
        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom)
        arcade.start_render()
        self.background.draw()
        score_text1 = "Jesteś mistrzem !!! "
        arcade.draw_text(score_text1 , SCREEN_WIDTH/2, 3*SCREEN_HEIGHT/4,arcade.csscolor.RED, 64,anchor_x="center",font_name='comic')
        score_text1 = "Twój wynik " + str(self.window.score)
        arcade.draw_text(score_text1 , SCREEN_WIDTH/2, SCREEN_HEIGHT/2,arcade.csscolor.RED, 64,anchor_x="center",font_name='comic')
        arcade.draw_text("Przeszedleś wszystkie poziomy !!!", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,
                         arcade.color.RED_BROWN, font_size=30, anchor_x="center",font_name='comic')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        game_view = GameView()
        self.window.show_view(game_view)

class MenuView(arcade.View):
    #ekran startowy
    def __init__(self):
        super().__init__()
        if width<1400:
            self.background = arcade.Sprite("pymunk/images/diament/stars.png")
        else:
            self.background = arcade.Sprite("pymunk/images/diament/starsd.png")
        self.background.left = self.background.bottom = 0
        self.window.sound = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()

        arcade.draw_text("Naciśnij klawisz myszki i poczekaj chwilkę", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,
                         arcade.color.RED_ORANGE, font_size=36, bold=True, anchor_x="center",font_name='comic')
        arcade.draw_text("ZBIERACZ DIAMENTOW", SCREEN_WIDTH/2, 3*(SCREEN_HEIGHT/4),
                         arcade.color.RED_BROWN, font_size=60,  bold=True, anchor_x="center",font_name='pymunk/images/diament/Retro.otf')

        arcade.draw_text("Zbierz 3 klucze i uwazaj na kamienie i robaki", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,\
                         arcade.color.RED_DEVIL, font_size=40, anchor_x="center",font_name='pymunk/images/diament/Retro.otf')

    def on_mouse_press(self, _x, _y, _button, _modifiers):

        game_view = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    #główna część programu
    def __init__(self):
        super().__init__()
        #definicja spritów i części zmiennych
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.player_sprite: Optional[PlayerSprite] = None
        self.background_list: Optional[arcade.SpriteList] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.kopanie_list: Optional[arcade.SpriteList] = None
        self.extra_list: Optional[arcade.SpriteList] = None
        self.kamienie_list: Optional[arcade.SpriteList] = None
        self.enemy_list: Optional[arcade.SpriteList] = None
        self.diamenty_list: Optional[arcade.SpriteList] = None
        self.exit: Optional[arcade.SpriteList] = None
        self.zanik:Optional[arcade.SpriteList] = None
        self.punkty: Optional[arcade.SpriteList] = None
        self.dynamit1:Optional[arcade.SpriteList] = None
        self.wybuchdynamit:Optional[arcade.SpriteList] = None
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.background = None
        self.level = 1
        self.max_level = 2
        self.przes_y = 0
        self.przes_x = 0
        self.ost_x= True
        self.ost_y=True
        self.setup()

    def setup(self):
        # zmienne w poziomie
        self.player_list = arcade.SpriteList()
        self.view_bottom = 0
        self.view_left = 0
        self.life=3
        self.dynamit = 2
        self.key =0
        self.czas = 0
        self.ruchpion = 0
        self.ruchpoziom = 0
        self.dystans = 0
        self.dystans2 = 0
        self.stary = 0
        self.rozwojscian = 0
        self.gdziex = 352
        self.gdziey = 96
        self.postawok = 0
        #obrazy informacyjne
        self.scr1 = texture = arcade.load_texture("pymunk/images/diament/diam1.png")
        self.scr2 = texture = arcade.load_texture("pymunk/images/diament/keyBlue.png")
        self.scr3 = texture = arcade.load_texture("pymunk/images/diament/dynamite00.png")
        self.scr4 = texture = arcade.load_texture("pymunk/images/diament/Warrior_IDLE.png")
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        self.background = arcade.Sprite("pymunk/images/diament/st1.jpg")
        self.background.left = self.background.bottom = 0
        #definicja dzwięków
        self.postawbobme_sound = arcade.sound.load_sound("pymunk/images/diament/fall2.wav")
        self.hit_sound = arcade.sound.load_sound("pymunk/images/diament/hurt5.wav")
        self.gameover_sound = arcade.load_sound ("pymunk/images/diament/gameover1.wav")
        self.diament_sound = arcade.load_sound("pymunk/images/diament/jump1.wav")
        self.wybuch_sound = arcade.load_sound("pymunk/images/diament/explosion1.wav")
        self.zbior_sound = arcade.load_sound("pymunk/images/diament/upgrade.ogg")
        self.kop_sound = arcade.load_sound("pymunk/images/diament/hit2.wav")
        self.postaw_sound = arcade.load_sound("pymunk/images/diament/laser5.ogg")
        self.win_sound = arcade.load_sound("pymunk/images/diament/win.ogg")
        self.enemy_dead_sound = arcade.load_sound("pymunk/images/diament/enemy.ogg")
        self.level_win = arcade.load_sound("pymunk/images/diament/level.ogg")
        # deinicja sprite-ów
        self.zanik_list = arcade.SpriteList()
        self.zanik = Zanik(hit_box_algorithm="Simple")
        self.punkty_list = arcade.SpriteList()
        self.punkty = Punkty(hit_box_algorithm="Simple")
        self.dynamit_list = arcade.SpriteList()
        self.dynamit1 = Dynamit1(hit_box_algorithm="Detailed")
        self.wybuchdynamit_list = arcade.SpriteList()
        self.wybuchdynamit = Wybuchdynamit(hit_box_algorithm="Simple")
        #odczyt mapy
        map_name = "pymunk/tmx_maps/boul_"+str(self.level) + ".tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.end_of_map = my_map.map_size.width* SPRITE_SIZE_MAP
        self.end_of_map_y = my_map.map_size.height* SPRITE_SIZE_MAP

        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      'Wall',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")
        self.kopanie_list = arcade.tilemap.process_layer(my_map,
                                                      'Kopanie',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")

        self.extra_list = arcade.tilemap.process_layer(my_map,
                                                      'Extra',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")
        self.kamienie_list = arcade.tilemap.process_layer(my_map,
                                                      'Kamienie',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")
        self.enemy_list = arcade.tilemap.process_layer(my_map,
                                                      'Enemy',
                                                      SPRITE_SCALING_TILES,
                                                       hit_box_algorithm="Simple")
        self.diamenty_list = arcade.tilemap.process_layer(my_map,
                                                      'Diamenty',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")
        self.exit_list = arcade.tilemap.process_layer(my_map,
                                                      'Exit',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")

        # Utworzenie fizyki w grze
        damping = 0.9
        gravity = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=FRICTION,
                                            elasticity=0.6,
                                            collision_type="wall",
                                            mass = 5,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.kopanie_list,
                                            collision_type="kopanie",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.diamenty_list,
                                        friction=FRICTION,
                                        elasticity=0.8,
                                        mass = 1,
                                        collision_type="diamenty")

        self.physics_engine.add_sprite_list(self.kamienie_list,
                                        friction=FRICTION,
                                        mass = 2,
                                        elasticity=0.8,
                                        collision_type="kamienie")

        self.physics_engine.add_sprite_list(self.extra_list,
                                        friction=FRICTION,
                                        elasticity=0.8,
                                        collision_type="extra")
        self.physics_engine.add_sprite_list(self.enemy_list,
                                        friction=FRICTION,
                                        elasticity=0.5,
                                        moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="enemy")

        # sprawdzenie kolizji sprte-ów (część)
        def kopanie_hit_handler(player_sprite, kopanie_sprite, _arbiter, _space, _data):
            kopanie_sprite.remove_from_sprite_lists()
            center_x = kopanie_sprite.center_x
            center_y = kopanie_sprite.center_y
            self.nowy_zanik(center_x,center_y,0)
            self.player_sprite.kop = True
        self.physics_engine.add_collision_handler("player", "kopanie", post_handler=kopanie_hit_handler)

        def enemy_hit_handler(enemy, player_sprite, _arbiter, _space, _data):
            self.life -= 1
            if self.window.sound == 0:
                arcade.sound.play_sound(self.hit_sound)
            enemy.change_x *= -1
            enemy.change_y *= -1
            if self.life == 0:
                self.gameover()
        self.physics_engine.add_collision_handler("enemy", "player", post_handler=enemy_hit_handler)

        def enemy2_hit_handler(enemy, kamienie_sprite, _arbiter, _space, _data):
            if kamienie_sprite.dead == True and kamienie_sprite.center_y - enemy.center_y > 40 and abs(enemy.center_x - kamienie_sprite.center_x) < 32:
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.enemy_dead_sound)
                points = 100
                self.window.score += points
                center_x = enemy.center_x
                center_y = enemy.center_y
                enemy.remove_from_sprite_lists()
                self.nowy_punkty(center_x, center_y, points)
            else:
                if enemy.dystans > 5:
                    enemy.change_x *= -1
                    enemy.change_y *= -1
                    enemy.czas += 1
                    enemy.dystans = 0
        self.physics_engine.add_collision_handler("enemy", "kamienie", post_handler=enemy2_hit_handler)

        def enemy3_hit_handler(enemy, diamenty, _arbiter, _space, _data):
            enemy.change_x *= -1
            enemy.change_y *= -1
            enemy.czas += 1
            enemy.dystans = 0
        self.physics_engine.add_collision_handler("enemy", "diamenty", post_handler=enemy3_hit_handler)

        def enemy4_hit_handler(enemy, wall, _arbiter, _space, _data):
            if enemy.dystans>10:
                enemy.change_x *= -1
                enemy.change_y *= -1
                enemy.czas += 1
                enemy.dystans = 0
        self.physics_engine.add_collision_handler("enemy", "wall", post_handler=enemy4_hit_handler)

        def enemy5_hit_handler(enemy, kopanie, _arbiter, _space, _data):
            if enemy.dystans > 5:
                enemy.change_x *= -1
                enemy.change_y *= -1
                enemy.czas += 1
                enemy.dystans = 0
        self.physics_engine.add_collision_handler("enemy", "kopanie", post_handler=enemy5_hit_handler)

        def extra_hit_handler(player_sprite, extra_sprite, _arbiter, _space, _data):
            if str(extra_sprite.properties['Ext']) == "Heart":
                self.life += 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.zbior_sound)
            elif str(extra_sprite.properties['Ext']) == "Key":
                self.key += 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.zbior_sound)
            elif str(extra_sprite.properties['Ext']) == "Dynamit":
                self.dynamit += 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.zbior_sound)
            extra_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("player", "extra", post_handler=extra_hit_handler)

        def diamenty_hit_handler(player_sprite, diamenty_sprite, _arbiter, _space, _data):
           diamenty_sprite.remove_from_sprite_lists()
           points = int(diamenty_sprite.properties['Point'])
           self.window.score += points
           center_x = diamenty_sprite.center_x
           center_y = diamenty_sprite.center_y
           diamenty_sprite.remove_from_sprite_lists()
           if self.window.sound == 0:
               arcade.sound.play_sound(self.diament_sound)
           self.nowy_punkty(center_x, center_y, points)
        self.physics_engine.add_collision_handler("player", "diamenty", post_handler=diamenty_hit_handler)

        def kamienie_hit_handler(player_sprite, kamienie_sprite, _arbiter, _space, _data):
            if kamienie_sprite.dead ==True and kamienie_sprite.center_y - player_sprite.center_y>40 and abs(player_sprite.center_x-kamienie_sprite.center_x)<32:
                kamienie_sprite.remove_from_sprite_lists()
                self.life -=1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.hit_sound)
                if self.life ==0:
                    self.gameover ()
        self.physics_engine.add_collision_handler("player", "kamienie", post_handler=kamienie_hit_handler)

        #ustawienie pozycji startowej gracza
        x = 95
        y = 95
        self.nowy_player(center_x=x, center_y=y)
        #przypisanie danych tymczasowych
        for kamienie_sprite in self.kamienie_list:
            kamienie_sprite.stx = kamienie_sprite.center_x
            kamienie_sprite.sty = kamienie_sprite.center_y
            kamienie_sprite.tymczasy = 0
            kamienie_sprite.dead = False
        for enemy in self.enemy_list:
            enemy.czas = 0
            enemy.pierwszykierunek = 1
            enemy.dystans = 0

    def nowy_zanik(self, center_x, center_y, wybor):
        #kopanie
        if self.window.sound == 0:
            arcade.sound.play_sound(self.kop_sound)
        self.zanik = Zanik(hit_box_algorithm="Simple")
        self.zanik.center_x = center_x
        self.zanik.center_y = center_y
        self.zanik.wybor = wybor
        self.zanik_list.append(self.zanik)

    def nowy_punkty(self, center_x, center_y, points):
        #poyzcja startowa punktów
        self.punkty = Punkty(hit_box_algorithm="Simple")
        self.punkty.center_x = center_x
        self.punkty.center_y = center_y
        self.punkty.ilepunkty = points
        self.punkty_list.append(self.punkty)

    def postawdynamit(self):
        # pozycja startowa dynamitu
        self.dynamit1 = Dynamit1(hit_box_algorithm="Detailed")
        self.dynamit1.center_x = self.player_sprite.center_x
        self.dynamit1.center_y = self.player_sprite.center_y
        self.dynamit_list.append(self.dynamit1)

    def postawwall(self, zm_x, zm_y):
        #stawianie dodatkowego elementu
        self.wall = Wall ()
        self.wall.center_x = zm_x
        self.wall.center_y = zm_y
        spr = (self.wall.center_x, )
        self.wall.texture = arcade.load_texture("pymunk/images/diament/01.png")
        self.wall_list.append(self.wall)
        self.physics_engine.add_sprite(self.wall,
                                                collision_type="wall",
                                                mass = 5,
                                                body_type=arcade.PymunkPhysicsEngine.STATIC)
        #sprawdzenie czy można postawic dodatkowy element
        if len(arcade.check_for_collision_with_list(self.wall, self.wall_list)) > 0:
            self.wall.remove_from_sprite_lists()
            self.postawok = 0
        elif len(arcade.check_for_collision_with_list(self.wall, self.kopanie_list)) > 0:
            self.wall.remove_from_sprite_lists()
            self.postawok = 0
        elif len(arcade.check_for_collision_with_list(self.wall, self.kamienie_list)) > 0:
            self.wall.remove_from_sprite_lists()
            self.postawok = 0
        elif len(arcade.check_for_collision_with_list(self.wall, self.diamenty_list)) > 0:
            self.wall.remove_from_sprite_lists()
            self.postawok = 0
        else:
            self.postawok = 1
            self.rozwojscian = 0
            self.gdziex = zm_x
            self.gdziey = zm_y
            if self.window.sound == 0:
                arcade.sound.play_sound(self.postaw_sound)

    def nowy_player (self, center_x, center_y):
        #definicja gracza
        self.player_sprite = PlayerSprite( hit_box_algorithm="Detailed")
        self.use_spatial_hash=True
        self.player_sprite.center_x=center_x
        self.player_sprite.center_y=center_y
        self.player_list.append(self.player_sprite)
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=1,
                                       mass=2,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

    def on_key_press(self, key, modifiers):
        #sterowanie
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.SPACE:
            if self.dynamit>0:
                self.dynamit -=1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.postawbobme_sound)
                self.postawdynamit()
        elif key == arcade.key.S:
            if self.window.sound== 0:
                self.window.sound = 1
            else:
                self.window.sound = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_update(self, delta_time):
        #uaktualnienine danych
        changed = False
        self.enemy_list.update_animation(delta_time)
        self.extra_list.update_animation(delta_time)
        self.kamienie_list.update_animation(delta_time)
        self.diamenty_list.update_animation(delta_time)
        self.zanik_list.update()
        self.punkty_list.update()
        self.dynamit_list.update()
        self.wybuchdynamit_list.update()
        self.stary = 1
        # czy stawiamy ścianę dodatkową
        if int(random.randrange(100000)) ==0:
            zm_x = self.gdziex
            zm_y = self.gdziey
            self.postawwall(zm_x, zm_y)
            if self.postawok ==0:
                zm_x = self.gdziex + 64
                zm_y = self.gdziey
                self.postawwall(zm_x, zm_y)
                if self.postawok == 0:
                    zm_x = self.gdziex - 64
                    zm_y = self.gdziey
                    self.postawwall(zm_x, zm_y)
                    if self.postawok == 0:
                        zm_x = self.gdziex
                        zm_y = self.gdziey+64
                        self.postawwall(zm_x, zm_y)
                        if self.postawok == 0:
                            zm_x = self.gdziex
                            zm_y = self.gdziey - 64
                            self.postawwall(zm_x, zm_y)
                            if self.postawok == 0:
                               self.rozwojscian = 0
        #czy wybucha dynamit
        if self.dynamit1.czywybuchdynamit == True:
            x = self.dynamit1.center_x
            y = self.dynamit1.center_y
            for dyna in self.dynamit_list:
                dyna.remove_from_sprite_lists()
            self.dynamit1.czywybuchdynamit = False
            self.wybuchdynamit = Wybuchdynamit("pymunk/images/diament/kula0.png",0.67)
            self.wybuchdynamit.center_x = x
            self.wybuchdynamit.center_y = y
            self.wybuchdynamit_list.append(self.wybuchdynamit)
            if self.window.sound == 0:
                arcade.sound.play_sound(self.wybuch_sound)

        #co robimy po naciśnieciu klawiszy sterowania
        if self.left_pressed and not self.right_pressed:
            self.ost_x = False
            force = (-PLAYER_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary = 0
            self.physics_engine.set_friction(self.player_sprite, 0)

        elif self.right_pressed and not self.left_pressed:
            self.ost_x = True
            force = (PLAYER_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary = 0
            self.physics_engine.set_friction(self.player_sprite, 0)

        elif self.up_pressed and not self.down_pressed:
            self.ost_y = True
            force = (0, PLAYER_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary = 0
            self.physics_engine.set_friction(self.player_sprite, 0)

        elif self.down_pressed and not self.up_pressed:
            self.ost_y = False
            force = (0, -PLAYER_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary = 0
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            self.physics_engine.set_friction(self.player_sprite, 1.0)
        #dodatkowy ruch gracza, aby był na srodku kafelka
        self.przes_x = int(self.player_sprite.center_x - 31) % 64
        if self.stary >0 and self.przes_x != 0:
            if self.ost_x == False:
                if len(arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)) > 0:
                    hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
                    for wall in hit_list:
                        if abs(self.player_sprite.left - wall.right) < 2:
                            force = (PLAYER_FORCE * (65 - self.przes_x) / 20, 0)
                            self.ost_x = True
                        else:
                            force = (-PLAYER_FORCE * self.przes_x / 200, 0)
                else:
                    force = (-PLAYER_FORCE * self.przes_x / 200, 0)
            else:
                if len(arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)) > 0:
                    hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
                    for wall in hit_list:
                        if abs(self.player_sprite.right - wall.left) < 2:
                            force = (-PLAYER_FORCE * (self.przes_x) / 20, 0)
                            self.ost_x = False
                        else:
                            force = (PLAYER_FORCE * (65 - self.przes_x) / 200, 0)
                else:
                    force = (PLAYER_FORCE * (65-self.przes_x) / 200, 0)
            self.physics_engine.set_friction(self.player_sprite, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary=0
        if self.przes_x==0:
            force = (0, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 1.0)
        self.przes_y = int(self.player_sprite.center_y - 31) % 64
        if self.stary >0 and self.przes_y != 0:
            self.przes_y = int(self.player_sprite.center_y - 31) % 64
            if self.ost_y ==False:
                if self.ost_y<3:
                    force = (0, PLAYER_FORCE * (-self.przes_y) / 250)
                else:
                    force = (0, PLAYER_FORCE * (-self.przes_y) / 100)
            else:
                force = (0,PLAYER_FORCE * (65-self.przes_y) / 200)
            self.physics_engine.set_friction(self.player_sprite, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.stary=0
        if self.przes_y==0:
            force = (0, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 1.0)
        self.physics_engine.step()

        #czy kamienie mogą spaść
        for kamienie_sprite in self.kamienie_list:
            if (kamienie_sprite.sty - kamienie_sprite.center_y)>10:
                kamienie_sprite.dead = True
                if int (kamienie_sprite.tymczasy) == int (kamienie_sprite.center_y):
                    kamienie_sprite.dead = False
                    kamienie_sprite.sty =kamienie_sprite.center_y
                else:
                    kamienie_sprite.tymczasy =kamienie_sprite.center_y
            else:
                kamienie_sprite.dead = False
        #po wybuchu dynamitu
        for wybuchsprite in self.wybuchdynamit_list:
            if len(arcade.check_for_collision_with_list(wybuchsprite, self.wall_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(wybuchsprite, self.wall_list)
                for wall in hit_list:
                    if wall.center_x ==32 or wall.center_y ==32 or wall.top ==self.end_of_map_y or wall.right ==self.end_of_map:
                        pass
                    else:
                        center_x = wall.center_x
                        center_y = wall.center_y
                        self.nowy_zanik(center_x, center_y, 1)
                        wall.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(wybuchsprite, self.kamienie_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(wybuchsprite, self.kamienie_list)
                for kamienie in hit_list:
                    kamienie.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(wybuchsprite, self.kopanie_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(wybuchsprite, self.kopanie_list)
                for kopanie in hit_list:
                    kopanie.remove_from_sprite_lists()
                    center_x = kopanie.center_x
                    center_y = kopanie.center_y
                    self.nowy_zanik(center_x, center_y,0)

            if len(arcade.check_for_collision_with_list(wybuchsprite, self.diamenty_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(wybuchsprite, self.diamenty_list)
                for diamenty in hit_list:
                    points = int(diamenty.properties['Point'])
                    self.window.score += points
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.diament_sound)
                    center_x = diamenty.center_x
                    center_y = diamenty.center_y
                    diamenty.remove_from_sprite_lists()
                    self.nowy_punkty(center_x, center_y, points)
            if len(arcade.check_for_collision_with_list(wybuchsprite, self.enemy_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(wybuchsprite, self.enemy_list)
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
            if len(arcade.check_for_collision_with_list(wybuchsprite, self.player_list)) > 0:
                self.life -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.hit_sound)
                if self.life == 0:
                    self.gameover()
            wybuchsprite.remove_from_sprite_lists()

        #czy koniec poziomu
        for exit in self.exit_list:
            if len (arcade.check_for_collision_with_list(exit,self.player_list)) >0:
                if self.key >= 3:
                    if self.level < self.max_level:
                        self.level += 1
                        if self.window.sound == 0:
                            arcade.sound.play_sound(self.win_sound)
                        self.view_bottom = 0
                        self.view_left = 0
                        arcade.set_viewport(self.view_left,
                                            SCREEN_WIDTH + self.view_left,
                                            self.view_bottom,
                                            SCREEN_HEIGHT + self.view_bottom)
                        self.setup()
                    else:
                        self.wygrales()
        # przesunięcie planszy w lewo
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            if self.view_left < -50:
                self.view_left = -50
            changed = True
        # przesunięcie planszy w prawo
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            if self.view_left > self.end_of_map-SCREEN_WIDTH +50:
                self.view_left=self.end_of_map-SCREEN_WIDTH +50
            changed = True
        # przesunięcie planszy w górę
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            if self.view_bottom > self.end_of_map_y -2 * TOP_VIEWPORT_MARGIN:
                self.view_bottom = self.end_of_map_y - 2 * TOP_VIEWPORT_MARGIN
            changed = True
        # przesunięcie planszy w dół
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            if self.view_bottom < -50:
                self.view_bottom = -50
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)
        # uaktualnienie planszy
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        # ruch obcych
        for enemy in self.enemy_list:
            enemy.dystans += 1
            if enemy.dystans > 100 or enemy.czas>5:
                wktoratrone = int(random.randrange(3)) + 1
                if wktoratrone == 1:
                    enemy.change_x = enemy.change_y
                    enemy.change_y = 0
                    enemy.dystans = 0
                    enemy.czas = 0
                elif wktoratrone == 2:
                    enemy.change_y = enemy.change_x
                    enemy.change_x = 0
                    enemy.dystans = 0
                    enemy.czas = 0
                elif wktoratrone == 3:
                    enemy.dystans = 0
                    enemy.czas = 0
                    enemy.change_y = - enemy.change_x
                    enemy.change_x = 0
                elif wktoratrone == 4:
                    enemy.dystans = 0
                    enemy.czas = 0
                    enemy.change_x = -enemy.change_y
                    enemy.change_y = 0
            if enemy.change_x == 0 and enemy.change_y == 0:
                kierunek = int(random.randrange(3)) + 1
                if kierunek ==1:
                    enemy.change_x = 5
                elif kierunek ==2:
                    enemy.change_x = -5
                elif kierunek ==3:
                    enemy.change_y = -5
                elif kierunek ==4:
                    enemy.change_y = 5
                enemy.dystans = 0
                enemy.czas =0
            velocity1 = (enemy.change_x / delta_time, enemy.change_y / delta_time)
            self.physics_engine.set_velocity(enemy, velocity1)

    def on_draw(self):
        #rysowanie wszystkiego
        arcade.start_render()
        self.background.draw()
        self.kopanie_list.draw()
        self.wall_list.draw()
        self.kamienie_list.draw()
        self.extra_list.draw()
        self.diamenty_list.draw()
        self.zanik_list.draw()
        self.enemy_list.draw()
        self.exit_list.draw()
        self.player_list.draw()
        self.punkty_list.draw()
        self.dynamit_list.draw()
        self.wybuchdynamit_list.draw()
        self.wynik()

    def wynik(self):
        #informacje o wyniku i danych
        arcade.draw_rectangle_filled(10 + self.view_left, 0 + self.view_bottom, 900, 130,
                                     arcade.csscolor.WHITE)
        arcade.draw_scaled_texture_rectangle(300 + self.view_left, 50 + self.view_bottom, self.scr2, scale=0.5)
        arcade.draw_text(str(self.key), 325 + self.view_left, 35 + self.view_bottom,
                         arcade.csscolor.BLACK, 16, font_name='pymunk/images/diament/Retro.otf')

        arcade.draw_scaled_texture_rectangle(180 + self.view_left, 50 + self.view_bottom, self.scr1, scale=0.25)
        arcade.draw_text(str(self.window.score), 200 + self.view_left, 35 + self.view_bottom,
                         arcade.csscolor.BLACK, 16, font_name='pymunk/images/diament/Retro.otf')

        arcade.draw_scaled_texture_rectangle(100 + self.view_left, 50 + self.view_bottom, self.scr4, scale=0.25)
        arcade.draw_text(str(self.life), 120 + self.view_left, 35 + self.view_bottom,
                         arcade.csscolor.BLACK, 16, font_name='pymunk/images/diament/Retro.otf')

        arcade.draw_scaled_texture_rectangle(400 + self.view_left, 50 + self.view_bottom, self.scr3, scale=0.5)
        arcade.draw_text(str(self.dynamit), 440 + self.view_left, 35 + self.view_bottom,
                         arcade.csscolor.BLACK, 16, font_name='pymunk/images/diament/Retro.otf')
        # punkty
        for punkt in self.punkty_list:
            x = punkt.center_x
            y = punkt.center_y
            wartosc = punkt.ilepunkty
            arcade.draw_text(str(wartosc), x, y,arcade.csscolor.ORANGE_RED, 20, font_name='comic')

    def gameover (self):
        #przegrana
        if self.window.sound == 0:
            arcade.sound.play_sound(self.gameover_sound)
        arcade.cleanup_texture_cache()
        game_over_view = GameOverView()
        self.window.show_view(game_over_view)
    def wygrales (self):
        #przejście wszystkich poziomów
        if self.window.sound == 0:
            arcade.sound.play_sound(self.win_sound)
        arcade.cleanup_texture_cache()
        game_over_view = GameOverWygralesView()
        self.window.show_view(game_over_view)

def main():
    #główna metoda
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen= full)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
if __name__ == "__main__":
    main()