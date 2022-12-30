import math
import random
from uuid import uuid4
from typing import Optional
import arcade
import arcade.gui
import arcade.background as background
import pyglet
from pyglet.math import Vec2

# wykorzystano:
# Paul Vincent Craven.
# https://arcade.academy/index.html
# https://craftpix.net/
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# muzyka jest dostępna na licencji Creative Commons

# stałe
SCREEN_TITLE = "PyMunk W-Man"
SPRITE_IMAGE_SIZE = 128
global path, full, texturesok
path = "pymunk/images/animated_characters/female_person/femalePerson"
full = False
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_TILES = 0.5
SPRITE_SCALING_ENEMIES = 0.5
SPRITE_SCALING_LASER = 0.5
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
GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
PLAYER_MASS = 2.0
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600
PLAYER_MOVE_FORCE_ON_GROUND = 20000
PLAYER_MOVE_FORCE_IN_AIR = 900
PLAYER_JUMP_IMPULSE = 1800
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 20
BULLET_MOVE_FORCE = 4500
BULLET_ENEMY_FORCE = 5000
BULLET_MASS = 0.1
BULLET_GRAVITY = 300
MUSIC_VOLUME = 0.1
MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)

Shake_direction = random.random() * 2 * math.pi
# How 'far' to shake
Shake_amplitude = 10
# Calculate a vector based on that
shake_vector = (
    math.cos(Shake_direction) * Shake_amplitude,
    math.sin(Shake_direction) * Shake_amplitude)

class Snowflake:
    # płatki śniegu
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)

class MenuView(arcade.View):
    # menu startowe
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("pymunk/images/backgrounds/snow_o1.jpg")
        self.window.sound = 0
        self.window.music = 0
        self.window.level = 1
        self.window.poziomy = False
        self.window.draw_start_time = 0
        self.snowflake_list = None
        self.snowflake_list = []
        self.window.musicp = arcade.sound.load_sound("pymunk/images/ok/musicfree.mp3")
        if self.window.music == 0:
            self.window.media_player = self.window.musicp.play(MUSIC_VOLUME)

        for i in range(350):
            snowflake = Snowflake()
            snowflake.x = random.randrange(SCREEN_WIDTH)
            snowflake.y = random.randrange(SCREEN_HEIGHT + 200)
            snowflake.size = random.randrange(8)
            snowflake.speed = random.randrange(20, 80)
            snowflake.angle = random.uniform(0, math.pi * 2)
            self.snowflake_list.append(snowflake)
        super().__init__()
        self.n_t = arcade.load_texture('pymunk/images/ok/yellow_button02.png')
        self.h_t = arcade.load_texture('pymunk/images/ok/yellow_button03.png')
        self.p_t = arcade.load_texture('pymunk/images/ok/yellow_button00.png')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.load_font("pymunk/Risaltyp.ttf")
        arcade.set_background_color(arcade.color.COOL_GREY)
        self.button1 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH / 4 - 100, y=SCREEN_HEIGHT * 3 / 4,
                                                  text='Sound On/Off')
        self.manager.add(self.button1)
        self.button2 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT * 3 / 4,
                                                  text='Music On/Off')
        self.manager.add(self.button2)
        self.button3 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH * 3 / 4 - 100, y=SCREEN_HEIGHT * 3 / 4,
                                                  text='Instruction', font_name="Risaltyp")
        self.manager.add(self.button3)
        self.button4 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH / 4 - 100, y=SCREEN_HEIGHT / 2.2, text=
                                                  'Characters')
        self.manager.add(self.button4)
        self.button5 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 2.2,
                                                  text='PLAY GAME')
        self.manager.add(self.button5)
        self.button6 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH * 3 / 4 - 100, y=SCREEN_HEIGHT / 2.2,
                                                  text='QUIT GAME')
        self.manager.add(self.button6)

        self.button1.on_click = self.clickbut1
        self.button2.on_click = self.clickbut2
        self.button3.on_click = self.clickbut3
        self.button4.on_click = self.clickbut4
        self.button5.on_click = self.clickbut5
        self.button6.on_click = self.clickbut6

    def clickbut1(self, event):
        if self.window.sound == 0:
            self.window.sound = 1
        else:
            self.window.sound = 0

    def clickbut2(self, event):
        if self.window.music == 0:
            self.window.music = 1
            self.window.musicp.stop(player=self.window.media_player)
        else:
            self.window.music = 0
            self.window.media_player = self.window.musicp.play(MUSIC_VOLUME)

    def clickbut3(self, event):
        self.manager.disable()
        self.window.musicp.stop(player=self.window.media_player)
        self.clear()
        intro_view = IntroView()
        self.window.show_view(intro_view)

    def clickbut4(self, event):
        self.manager.disable()
        self.window.musicp.stop(player=self.window.media_player)
        wybor_view = WyborView()
        self.window.show_view(wybor_view)

    def clickbut5(self, event):
        self.manager.disable()
        self.window.musicp.stop(player=self.window.media_player)
        arcade.cleanup_texture_cache()
        self.clear()
        game_view = GameView()
        self.window.show_view(game_view)

    def clickbut6(self, event):
        arcade.close_window()

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Press the mouse and wait a moment", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6,
                         arcade.color.GENERIC_VIRIDIAN, font_size=30, anchor_x="center", font_name='Risaltyp')

        for snowflake in self.snowflake_list:
            arcade.draw_circle_filled(snowflake.x, snowflake.y,
                                      snowflake.size, arcade.color.WHITE)
        self.manager.draw()

    def on_update(self, delta_time):
        # płatki śniegu animacja
        for snowflake in self.snowflake_list:
            snowflake.y -= snowflake.speed * delta_time
            if snowflake.y < 0:
                snowflake.reset_pos()
            snowflake.x += snowflake.speed * math.cos(snowflake.angle) * delta_time
            snowflake.angle += 1 * delta_time

class IntroView(arcade.View):
    # instrukcja
    def __init__(self):
        super().__init__()
        self.rozm = 10

    def on_show(self):
        arcade.set_background_color(arcade.color.HANSA_YELLOW)

        self.background = arcade.load_texture ("pymunk/images/instr1.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # self.window.musicp.stop()
        menu_view = MenuView()
        self.window.show_view(menu_view)

class WyborView(arcade.View):
    # wybór postaci
    def __init__(self):
        super().__init__()
        self.character = 1
        self.wybor_list = None
        self.wybor: Optional[Wybor] = None
        self.text_left = arcade.load_texture('pymunk/images/ok/yellow_sliderLeft.png')
        self.text_right = arcade.load_texture('pymunk/images/ok/yellow_sliderRight.png')
        self.n_t = arcade.load_texture('pymunk/images/ok/yellow_button02.png')
        self.h_t = arcade.load_texture('pymunk/images/ok/yellow_button03.png')
        self.p_t = arcade.load_texture('pymunk/images/ok/yellow_button00.png')
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.COOL_GREY)
        self.background = arcade.load_texture("pymunk/images/backgrounds/snow_o1.jpg")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.COOL_GREY)
        self.button7 = arcade.gui.UITextureButton(texture=self.text_left,
                                                  x=SCREEN_WIDTH / 4 - 100, y=SCREEN_HEIGHT * 3 / 4,
                                                  )
        self.manager.add(self.button7)
        self.button8 = arcade.gui.UITextureButton(texture=self.text_right,
                                                  x=SCREEN_WIDTH / 4 * 3, y=SCREEN_HEIGHT * 3 / 4,
                                                  )
        self.manager.add(self.button8)
        self.button9 = arcade.gui.UITextureButton(texture=self.n_t, texture_hovered=self.h_t, texture_pressed=self.p_t,
                                                  x=SCREEN_WIDTH / 2 - 100, y=SCREEN_HEIGHT / 3, text='Menu')
        self.manager.add(self.button9)
        arcade.set_background_color(arcade.color.CHROME_YELLOW)
        global path
        self.button7.on_click = self.clickbut7
        self.button8.on_click = self.clickbut8
        self.button9.on_click = self.clickbut9
        self.setup2()

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.manager.draw()
        arcade.draw_text("There is only 1 character in this version", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.GRAY, font_size=30, anchor_x="center", font_name='Kenney Pixel')
        self.wybor_list.draw()

    def setup2(self):
        global path
        self.wybor = Wybor(hit_box_algorithm="Detailed", path=path)
        self.wybor.center_x = SCREEN_WIDTH / 2
        self.wybor.center_y = SCREEN_HEIGHT * 8 / 10
        self.wybor_list = arcade.SpriteList()
        self.wybor_list.append(self.wybor)

    def clickbut7(self, event):
        self.wybor.remove_from_sprite_lists()
        self.character -= 1
        if self.character == 0:
            self.character = 6
        self.wybierzsciezke()

    def clickbut8(self, event):
        self.wybor.remove_from_sprite_lists()
        arcade.pause(0.1)
        self.character += 1
        if self.character == 7:
            self.character = 1
        self.wybierzsciezke()

    def clickbut9(self, event):
        arcade.pause(0.1)
        self.manager.disable()
        self.wybor.remove_from_sprite_lists()
        # self.window.musicp.stop()
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def update(self, delta_time):

        self.wybor.update(delta_time)

    def wybierzsciezke(self):
        global texturesok
        global path
        if self.character == 1:
            path = "pymunk/images/animated_characters/female_person/femalePerson"
            self.setup2()
        if self.character == 2:
            path = "pymunk/images/animated_characters/female_adventurer/femaleAdventurer"
            self.setup2()
        if self.character == 3:
            path = "pymunk/images/animated_characters/male_person/malePerson"
            self.setup2()
        if self.character == 4:
            path = "pymunk/images/animated_characters/male_adventurer/maleAdventurer"
            self.setup2()
        if self.character == 5:
            path = "pymunk/images/animated_characters/zombie/zombie"
            self.setup2()
        if self.character == 6:
            path = "pymunk/images/animated_characters/robot/robot"
            self.setup2()

class Wybor(arcade.Sprite):
    # która postać - chodzenie w menu startowym
    def __init__(self, hit_box_algorithm, path):
        super().__init__()
        self.zmianatex = 0
        global texturesok
        self.walk_textures1 = []

        for i in range(8):
            path1 = path
            #texture = arcade.load_texture(f"{path1}_walk{i}.png")
            texture = arcade.load_texture("pymunk/images/animated_characters/female_person/Idle_0.png")
            self.walk_textures1.append(texture)

        self.cur_texture = 0
        self.texture = self.walk_textures1[0]
        self.hit_box = self.texture.hit_box_points
        self.scale = SPRITE_SCALING_PLAYER * 2

    def update(self, delta_time):
        self.texture = self.walk_textures1[self.cur_texture]

        self.zmianatex += 1
        if self.zmianatex == 10:
            self.zmianatex = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures1[self.cur_texture]

class PlayerSprite(arcade.Sprite):
    # definicja gracza
    def __init__(self, ladder_list,
                 hit_box_algorithm, scala):
        super().__init__()
        global path
        main_path = path
        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER * scala
        self.hit = False
        self.jumping = False
        self.climbing = False
        self.snorkl = False
        self.czas_min_snorkl=100
        self.ladder_list = ladder_list
        self.is_on_ladder = False
        self.czydrugiskok = False
        self.licznik = 0
        self.idlelicz = 0
        self.idle_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Idle_"+str(i)+".png")
            self.idle_textures.append(texture)
        #texture = arcade.load_texture_pair(f"{main_path}_idle.png",
        #                                   hit_box_algorithm=hit_box_algorithm)
        #self.idle_textures.append(texture)
        #texture = arcade.load_texture_pair(f"{main_path}_idle_1.png",
        #                                   hit_box_algorithm=hit_box_algorithm)
        #self.idle_textures.append(texture)
        self.jump_textures = []
        #for i in range(8):
        #    texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Jump_"+str(i)+".png")
        #   self.jump_textures.append(texture)
        #self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.jump_texture_pair = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Jump_3.png")
        self.jump_textures.append(texture)
        self.fall_textures = []
        #for i in range(4):
        #    texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Slide_"+str(i)+".png")
        #    self.fall_textures.append(texture)
        #self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")
        self.fall_texture_pair = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Slide_2.png")
        self.fall_textures.append(texture)
        self.hit_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/GetHit_"+str(i)+".png")
            self.hit_textures.append(texture)
        #texture = arcade.load_texture(f"{main_path}_hit.png")
        #self.hit_textures.append(texture)
        self.walk_textures = []
        for i in range(16):
            texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Walk_"+str(i)+".png")
            self.walk_textures.append(texture)
        self.tele_textures = []
        for i in range(11):
            texture = arcade.load_texture("pymunk/images/animated_characters/tornado"+ str(i+1) +".png")
            self.tele_textures.append(texture)

        self.snorkl_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair("pymunk/images/animated_characters/female_person/Snorkling_"+str(i)+".png")
            self.snorkl_textures.append(texture)

        self.climbing_textures = []
        #texture = arcade.load_texture(f"{main_path}_climb0.png")
        #self.climbing_textures.append(texture)
        #texture = arcade.load_texture(f"{main_path}_climb1.png")
        #self.climbing_textures.append(texture)
        for i in range(8):
            texture = arcade.load_texture("pymunk/images/animated_characters/female_person/Climb_"+str(i)+".png")
            self.climbing_textures.append(texture)
        self.dead_textures = []
        for j in range(3):
            for i in range(20):
                texture = arcade.load_texture("pymunk/images/spritesheets/czaszka_" + str(i) + ".png")
                self.dead_textures.append(texture)
        self.dead_textures.append(texture)
        # inicjowanie textur
        self.texture = self.idle_textures[0][RIGHT_FACING]
        self.hit_box = self.texture.hit_box_points
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.dead = False
        self.tele = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        # ruch postaci
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        if self.dead:
            self.cur_texture += 1
            if self.cur_texture > 21:
                self.cur_texture = 0
            self.texture = self.dead_textures[self.cur_texture]
            return
        if self.tele:
            self.cur_texture += 1
            if self.cur_texture > 10:
                self.cur_texture = 0
            self.texture = self.tele_textures[self.cur_texture]
            return
        if self.hit == True:
            self.licznik += 1
            if self.licznik==1:
                self.texture = self.hit_textures[0][self.character_face_direction]
                self.cur_texture=0
            if self.licznik % 3 ==0:
                self.cur_texture+=1
                self.texture = self.hit_textures[self.cur_texture][self.character_face_direction]
            if self.licznik == 22:
                self.hit = False
                self.licznik = 0
                self.texture = self.idle_textures[0][self.character_face_direction]
            return

        if self.snorkl == True :
            self.czas_min_snorkl -=1
            if self.czas_min_snorkl % 5==0:
                self.cur_texture += 1
                if self.cur_texture > 7:
                    self.cur_texture = 0
                self.texture = self.snorkl_textures[self.cur_texture][self.character_face_direction]
            if self.czas_min_snorkl ==0:
                self.czas_min_snorkl = 10
                self.snorkl = False
                #self.texture = self.idle_textures[0][self.character_face_direction]
            return
        # czy ziemia
        is_on_ground = physics_engine.is_on_ground(self)
        if is_on_ground:
            self.czydrugiskok = False
        # czy drabina
        if len(arcade.check_for_collision_with_list(self, self.ladder_list)) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = 0.0001
                self.pymunk.max_vertical_velocity = PLAYER_MAX_HORIZONTAL_SPEED
        else:
            if self.is_on_ladder:
                self.pymunk.damping = 1.0
                self.pymunk.max_vertical_velocity = PLAYER_MAX_VERTICAL_SPEED
                self.is_on_ladder = False
                self.pymunk.gravity = None
        self.x_odometer += dx
        self.y_odometer += dy
        if self.is_on_ladder and not is_on_ground:
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
                self.y_odometer = 0
                self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture]
            return
        # skok
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return
        # bezczynność
        if abs(dx) <= DEAD_ZONE:
            self.idlelicz += 1
            #if self.idlelicz == 50:
            if self.idlelicz == 10:
                self.idlelicz = 0
                self.cur_texture += 1
                if self.cur_texture > 7:
                    self.cur_texture = 0
                self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]
            return
        # czy zmieniamy texturę
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 15:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class BulletSprite(arcade.Sprite):
    # strzał
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()
        self.angle += dy
        self.change_angle = self.angle
        self.update()

class Golem(arcade.Sprite):
    # definicja golema
    def __init__(self, n1, n2, n3, hit_box_algorithm):
        super().__init__()
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.character_face_direction = RIGHT_FACING
        self.czasbezruchu = 0
        self.temposlash = 0
        self.pierwszeuderzenie = 0
        self.slash = 0
        self.scale = SPRITE_SCALING_ENEMIES * 1.5
        self.walk_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(n1 + str(i) + ".png")
            self.walk_textures.append(texture)
        self.texture = self.walk_textures[0][self.character_face_direction]
        self.fall_texture = arcade.load_texture_pair(n2)
        self.slash_textures = []
        for i in range(10):
            texture = arcade.load_texture_pair(n3 + str(i) + ".png")
            self.slash_textures.append(texture)

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        is_on_ground = physics_engine.is_on_ground(self)
        self.x_odometer += dx
        self.y_odometer += dy
        if self.slash == 1:
            self.temposlash += 1
            if self.temposlash == 10:
                self.cur_texture += 1
                self.temposlash = 0
                if self.cur_texture == len(self.slash_textures):
                    self.cur_texture = 0
                    self.slash = 0
                    self.pierwszeuderzenie = 0
                self.texture = self.slash_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.walk_textures[0][self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE / 2:
            self.x_odometer = 0
            self.czasbezruchu = 0
            self.cur_texture += 1
            if self.cur_texture == len(self.walk_textures):
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        if not is_on_ground:
            self.texture = self.fall_texture[self.character_face_direction]
            return

class Golem1(Golem):
    def __init__(self):
        # Set up parent class
        super().__init__("pymunk/images/enemies/golem/0_Golem_Walking_",
                         "pymunk/images/enemies/golem/0_Golem_Falling Down_000.png",
                         "pymunk/images/enemies/golem/0_Golem_Run Slashing_",
                         hit_box_algorithm="Simple")

class Golem2(Golem):
    def __init__(self):
        # Set up parent class
        super().__init__("pymunk/images/enemies/golem/Troll_03_1_WALK_",
                         "pymunk/images/enemies/golem/Troll_03_1_JUMP_005.png",
                         "pymunk/images/enemies/golem/Troll_03_1_ATTACK_",
                         hit_box_algorithm="Simple")

class Golem3(Golem):
    def __init__(self):
        # Set up parent class
        super().__init__("pymunk/images/enemies/golem/Cyclops_01_WALK_",
                         "pymunk/images/enemies/golem/Cyclops_01_JUMP_005.png",
                         "pymunk/images/enemies/golem/Cyclops_01_ATTACK_",
                         hit_box_algorithm="Detailed")

class Bullet_Enemy(arcade.Sprite):
    # strzały obcych
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class Shield(arcade.Sprite):
    # tarcza
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.ochron = []
        for i in range(4):
            texture = arcade.load_texture("pymunk/images/enemies/kula" + str(i) + ".png")
            self.ochron.append(texture)
        self.scale = SPRITE_SCALING_ENEMIES
        self.shieldon = 1
        self.predkkuli = 0
        self.texture = self.ochron[0]
        self.current_texture = 0

    def update(self):
        self.predkkuli += 1
        if self.predkkuli == 3:
            self.current_texture += 1
            self.predkkuli = 0
            if self.current_texture > 3:
                self.current_texture = 0
                self.texture = self.ochron[self.current_texture]
            else:
                self.texture = self.ochron[self.current_texture]

    def follow_sprite(self, player_sprite):
        self.center_y = player_sprite.center_y
        self.center_x = player_sprite.center_x

class Bomb(arcade.Sprite):
    # stawianie bomby przez enemy
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.x_out = 0
        self.y_out = 0
        self.czaswybuchu = 200
        self.czywybuch = False
        self.czywybuchtrwa = False
        self.pozbawzycia = False
        self.bomb_textures = []
        for i in range(15):
            texture = arcade.load_texture("pymunk/images/enemies/granat_frame_" + str(i) + ".png")
            self.bomb_textures.append(texture)
        self.explosion1_textures = []
        for i in range(16):
            texture = arcade.load_texture("pymunk/images/spritesheets/ekspozja_" + str(i) + ".png")
            self.explosion1_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.bomb_textures[self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if not self.czywybuchtrwa:
            self.czaswybuchu -= 1
            self.cur_texture += 1
            if self.cur_texture == len(self.bomb_textures):
                self.cur_texture = 0
            self.texture = self.bomb_textures[self.cur_texture]

        if self.czaswybuchu <= 0:
            if not self.czywybuchtrwa:
                self.texture = self.explosion1_textures[0]
                self.czywybuchtrwa = True
                self.pozbawzycia = True
                self.czywybuch = True
            self.cur_texture += 1
            if self.cur_texture < len(self.explosion1_textures):
                self.texture = self.explosion1_textures[self.cur_texture]
                return
            else:
                self.remove_from_sprite_lists()
                return
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class Explosion(arcade.Sprite):
    # wybuch
    def __init__(self):
        super().__init__()
        self.time = 0
        self.explosion_t = []
        for i in range(8):
            texture = arcade.load_texture("pymunk/images/spritesheets/2_" + str(i + 1) + ".png")
            self.explosion_t.append(texture)
        self.scale = SPRITE_SCALING_ENEMIES
        self.current_texture = 0
        self.texture = self.explosion_t[0]

    def update(self):
        self.time += 1
        if self.time == 5:
            self.time = 0
            self.current_texture += 1
            if self.current_texture < len(self.explosion_t):
                self.texture = self.explosion_t[self.current_texture]
            else:
                self.remove_from_sprite_lists()
                self.current_texture = 0

class Wybuch2(arcade.Sprite):
    # definicja wybuchu - rodzaj 2
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.szybkosc = 0
        self.wybuch_textures = []
        self.scale = 1
        self.czywybuch = False
        for i in range(17):
            texture = arcade.load_texture("pymunk/images/tiles/level8/Explosion2/1_" + str(i) + ".png")
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
                self.czywybuch = False
                self.cur_texture = 0
                self.szybkosc = 0

class GameOverView(arcade.View):
    # przegrana/wszystkie poziomy
    def __init__(self):
        super().__init__()
        self.window.musicp.stop(player=self.window.media_player)
        self.background = arcade.load_texture("pymunk/images/backgrounds/background1.jpg")
        if self.window.music == 0:
            self.window.media_player = self.window.musicp.play(MUSIC_VOLUME)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        if not self.window.poziomy:
            score_text1 = "Your score : " + str(self.window.score)
            arcade.draw_text(score_text1, SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3,
                             arcade.csscolor.RED, 64, anchor_x="center", font_name='Kenney Pixel')
            arcade.draw_text("1 - from the beginning,  2 - the same level", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 55,
                             arcade.color.RED_BROWN, font_size=46, anchor_x="center", font_name='Kenney Pixel')
        else:
            score_text1 = "Congratulations, you've passed all the levels, Your score : " + str(self.window.score)
            arcade.draw_text(score_text1, SCREEN_WIDTH / 2,
                             2 * SCREEN_HEIGHT / 3, arcade.csscolor.RED, 62, anchor_x="center",
                             font_name='Kenney Pixel')
            arcade.draw_text("Press the mouse and wait a moment", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 55,
                             arcade.color.RED_BROWN, font_size=46, anchor_x="center", font_name='Kenney Pixel')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        self.window.musicp.stop(player=self.window.media_player)
        self.window.poziomy = False
        self.window.level=1
        game_view = GameView()
        self.window.show_view(game_view)
    def on_key_press(self, key, modifiers):
        # sterowanie
        if key == arcade.key.KEY_1:
            self.window.level=1
            self.window.score = 0

            if self.window.music == 0:
                self.window.musicp.stop(player=self.window.media_player)
            game_view = GameView()
            self.window.show_view(game_view)
        if key == arcade.key.KEY_2:
            self.window.score = 0
            if self.window.music == 0:
                self.window.musicp.stop(player=self.window.media_player)
            game_view = GameView()
            self.window.show_view(game_view)

class GameView(arcade.View):
    # główne okno
    def __init__(self):
        super().__init__()
        self.player_sprite: Optional[PlayerSprite] = None
        arcade.set_background_color(arcade.color.BLACK)
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.odliczamdo_drugiego = 0
        # prawie nieśmiertelność
        self.extra_life = False
        self.tym_extra_life = False
        self.max_level = 9
        self.ilosczyc = 3
        self.camera = None
        self.gui_camera = None
        self.tile_map = None
        self.scene = None
        self.czymap = True
        # dzwięki
        self.gun_sound = arcade.sound.load_sound("pymunk/sounds/laser4.wav")
        self.hit_sound = arcade.sound.load_sound("pymunk/sounds/explosion2.wav")
        self.bomb_kill_sound = arcade.load_sound("pymunk/sounds/fall1.wav")
        self.xenemy_hurt_sound = arcade.load_sound("pymunk/sounds/fall3.wav")
        self.xenemy_kill_sound = arcade.load_sound("pymunk/sounds/lose4.wav")
        self.strata_zycia_sound = arcade.load_sound("pymunk/sounds/lose5.wav")
        self.game_over_sound = arcade.load_sound("pymunk/sounds/gameover4.wav")
        self.tarcza_sound = arcade.load_sound("pymunk/sounds/hurt4.wav")
        self.extrai_sound = arcade.load_sound("pymunk/sounds/jump3.wav")
        self.coin_sound = arcade.load_sound("pymunk/sounds/coin1.wav")
        self.golem_sound = arcade.load_sound("pymunk/sounds/kick.ogg")
        self.upgrade_sound = arcade.load_sound("pymunk/sounds/upgrade5.wav")
        self.zamiana_sound = arcade.load_sound("pymunk/sounds/upgrade1.wav")
        self.level_sound = arcade.load_sound("pymunk/sounds/level2.ogg")
        self.tele_sound = arcade.load_sound("pymunk/sounds/upgrade2.wav")
        if self.window.music == 0:
            self.window.media_player = self.window.musicp.play(MUSIC_VOLUME)
        self.scr1 = texture = arcade.load_texture("pymunk/images/ok/gemBlue.png")
        self.scr2 = texture = arcade.load_texture("pymunk/images/ok/keyBlue.png")
        self.scr3 = texture = arcade.load_texture("pymunk/images/ok/gun_blue.png")
        self.scr4 = texture = arcade.load_texture("pymunk/images/ok/tarcza0.png")
        self.scr5 = texture = arcade.load_texture("pymunk/images/items/snorkling1.png")
        self.setup()

    def setup(self):
        # główna część gry
        arcade.load_font("pymunk/Kenney Pixel.ttf")
        self.zamiana_x = 0
        self.zamiana_y = 0
        self.zamiana_tekst = ""
        self.view_bottom = 0
        self.view_left = 0
        self.mocshield = 20
        self.diamond = 0
        self.diamond_czas = 0
        self.key = 0
        self.gun1 = 0
        self.gun2 = 0
        self.snork_ile=1
        self.gun_active = 0
        self.czas_gun = 0
        self.czas_snorkl = 0
        self.koniec = False
        self.zliczdead = 0
        self.music = 0
        self.player_golem = False
        self.score_text = ""
        #minimap
        self.minimap_sprite_list = None
        self.minimap_texture = None
        self.minimap_sprite = None

        size = (int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT/4))
        self.minimap_texture = arcade.Texture.create_empty(str(uuid4()), size)
        self.minimap_sprite = arcade.Sprite(center_x=256 / 2,
                                            center_y=SCREEN_HEIGHT - 256 / 2,
                                            texture=self.minimap_texture)

        self.minimap_sprite_list = arcade.SpriteList()
        self.minimap_sprite_list.append(self.minimap_sprite)

        self.scoreT = arcade.Text(text=self.score_text,
                                  start_x=10,
                                  start_y=32,
                                  color=arcade.csscolor.BLACK,
                                  font_size=28,
                                  font_name='Kenney Pixel')
        self.key_tekst = "0"
        self.diamond_tekst = "0"
        self.gun1_tekst = "0"
        self.gun2_tekst = "0"
        self.snork_tekst="0"
        self.keyT = arcade.Text(text=self.key_tekst,
                                start_x=465,
                                start_y=32,
                                color=arcade.csscolor.BLACK,
                                font_size=28,
                                font_name='Kenney Pixel')

        self.diamondT = arcade.Text(text=self.diamond_tekst,
                                    start_x=545,
                                    start_y=32,
                                    color=arcade.csscolor.BLACK,
                                    font_size=28,
                                    font_name='Kenney Pixel')

        self.gun1T = arcade.Text(text=self.gun1_tekst,
                                 start_x=640,
                                 start_y=32,
                                 color=arcade.csscolor.BLACK,
                                 font_size=28,
                                 font_name='Kenney Pixel')

        self.gun2T = arcade.Text(text=self.gun2_tekst,
                                 start_x=760,
                                 start_y=32,
                                 color=arcade.csscolor.BLACK,
                                 font_size=28,
                                 font_name='Kenney Pixel')
        self.snorkT = arcade.Text(text=self.snork_tekst,
                                 start_x=850,
                                 start_y=32,
                                 color=arcade.csscolor.BLACK,
                                 font_size=28,
                                 font_name='Kenney Pixel')

        self.background = arcade.load_texture("pymunk/images/backgrounds/galaxy" + str(self.window.level) + ".jpg")

        self.camera = arcade.Camera(width, height)
        self.gui_camera = arcade.Camera(width, height)
        map_name = "pymunk/tmx_maps/pymunk_wito_" + str(self.window.level) + ".json"
        self.my_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
        layer_options = {
            "Ladders": {
                "use_spatial_hash": True,
                "hit_box_algorithm": 'None',
            },
            "Dont touch": {
                "use_spatial_hash": True,
                "hit_box_algorithm": 'Simple',
            },
            "Water": {
                "use_spatial_hash": True,
                "hit_box_algorithm": 'Simple',
            },
            "Platforms": {
                "use_spatial_hash": True,
                "hit_box_algorithm": 'Simple',
            },
            "Coins": {
                "use_spatial_hash": False,
            },
            "Background": {
                "hit_box_algorithm": 'None',
            },
            "Background2": {
                "hit_box_algorithm": 'None',
            },
            "Moving Platforms": {
                "hit_box_algorithm": 'None',
            },
            "Xenemy": {
                "hit_box_algorithm": 'Detailed',
            },
            "Dynamic Item": {
                "hit_box_algorithm": 'Detailed',
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.end_of_map = self.tile_map.width * SPRITE_SIZE_MAP
        self.end_of_map_y = self.tile_map.height * SPRITE_SIZE_MAP
        self.player_sprite = PlayerSprite(self.scene.name_mapping["Ladders"],
                                          hit_box_algorithm="Detailed", scala=1)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.scene.add_sprite("player", self.player_sprite)
        self.center_camera_to_player()
        #aktywacja pozostałych sprite
        self.explosion = Explosion()
        self.scene.add_sprite("explosion", self.explosion)
        self.explosion.remove_from_sprite_lists()
        self.wybuch2 = Wybuch2(hit_box_algorithm="simple")
        self.scene.add_sprite("wybuch2", self.wybuch2)
        self.wybuch2.remove_from_sprite_lists()
        self.shield = Shield(hit_box_algorithm="Simple")
        self.scene.add_sprite("shield", self.shield)
        self.bomb = Bomb(hit_box_algorithm="simple")
        self.scene.add_sprite("bomb", self.bomb)
        self.bomb.remove_from_sprite_lists()
        self.czy_mozna_teleport = True
        self.licznik_teleport = 120

        #definicja fizyki
        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       collision_type="player",
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
        self.nowy_golem()

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Platforms"],
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Dynamic Items"],
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            elasticity=0.5,
                                            collision_type="item")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Extra_item"],
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="extra_item")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Moving Platforms"],
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
                                            friction=WALL_FRICTION,
                                            collision_type="wall")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Xenemy"],
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="xenemy")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Coins"],
                                            elasticity=0.5,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="coins")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Dont touch"],
                                            body_type=arcade.PymunkPhysicsEngine.STATIC,
                                            collision_type="touch")
        self.physics_engine.add_sprite_list(self.scene.name_mapping["Water"],
                                            body_type=arcade.PymunkPhysicsEngine.STATIC,
                                            collision_type="water")

        self.physics_engine.add_sprite_list(self.scene.name_mapping["Teleport"],
                                            body_type=arcade.PymunkPhysicsEngine.STATIC,
                                            collision_type="teleport")

        # kolizje sprite- ów

        def tele_hit_handler(player_sprite, tele_sprite, _arbiter, _space, _data):
            if self.czy_mozna_teleport:
                zm_poz_x= tele_sprite.poz_x-self.player_sprite.center_x
                zm_poz_y= tele_sprite.poz_y-self.player_sprite.center_y
                # teleport
                self.tym_extra_life = True
                force = (0, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.player_sprite.pymunk.gravity = (0, 0)
                self.player_sprite.pymunk.damping = 0.0001
                impulse = (int(110*zm_poz_x), int(110*zm_poz_y))
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
                self.player_sprite.update()
                if self.window.sound == 0:
                    arcade.play_sound(self.tele_sound   )
                self.player_sprite.pymunk.gravity = gravity
                self.player_sprite.pymunk.damping = damping
                self.czy_mozna_teleport = False
                self.player_sprite.tele = True
                self.player_sprite.cur_texture

        self.physics_engine.add_collision_handler("player", "teleport", post_handler=tele_hit_handler)


        def bomb_hit_handler(bomb_sprite, bullet_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            self.window.score += 2
            bomb_sprite.czaswybuchu = 0
            if self.window.sound == 0:
                arcade.play_sound(self.bomb_kill_sound)
        self.physics_engine.add_collision_handler("bomb", "bullet", post_handler=bomb_hit_handler)

        def bomb_hit_handler2(bomb_sprite, bullet_enemy_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bomb", "bullet_enemy", post_handler=bomb_hit_handler2)

        def bomb_hit_handler3(bomb_sprite, wall_sprite, _arbiter, _space, _data):
            if bomb_sprite.czywybuch:
                bomb_sprite.czywybuch = False
                if self.window.sound == 0:
                    arcade.play_sound(self.hit_sound)

        self.physics_engine.add_collision_handler("bomb", "wall", post_handler=bomb_hit_handler3)

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        def bullet_hit_handler(bullet_sprite, _dont_touch_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "touch", post_handler=bullet_hit_handler)

        def wall_hit_handler2(bullet_enemy_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet_enemy", "wall", post_handler=wall_hit_handler2)

        def wall_hit_handler3(wall_sprite, item, _arbiter, _space, _data):
            item.ilosc += 1
            if item.ilosc == 20:
                item.sila = False
                item.ilosc = 0

        self.physics_engine.add_collision_handler("wall", "item", post_handler=wall_hit_handler3)

        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)

        def item_hit_handler2(bullet_enemy_sprite, item_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet_enemy", "item", post_handler=item_hit_handler2)

        def item_hit_handler3(item_sprite, xenemy, _arbiter, _space, _data):
            points = int(xenemy.properties['Points'])
            if item_sprite.sila and points < 100:
                points = int(xenemy.properties['Points'])
                self.window.score += points
                # Make an explosion
                self.explosion.center_x = xenemy.center_x
                self.explosion.center_y = xenemy.center_y
                xenemy.remove_from_sprite_lists()
                # Add to a list of sprites that are explosions
                self.scene.add_sprite("explosion", self.explosion)
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.xenemy_kill_sound)

        self.physics_engine.add_collision_handler("item", "xenemy", post_handler=item_hit_handler3)

        def extra_item_hit_handler(bullet_enemy_sprite, extra_item_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet_enemy", "extra_item", post_handler=extra_item_hit_handler)

        def extra_item_hit_handler2(bullet_sprite, extra_item_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            extra_item_sprite.remove_from_sprite_lists()
            if self.window.sound == 0:
                arcade.play_sound(self.extrai_sound)
            if str(extra_item_sprite.properties['Ext']) == "heart":
                self.mocshield += 1
            elif str(extra_item_sprite.properties['Ext']) == "key":
                self.key += 1
            elif str(extra_item_sprite.properties['Ext']) == "diamond":
                self.diamond += 1
            elif str(extra_item_sprite.properties['Ext']) == "gun1":
                self.gun1 += 1
            elif str(extra_item_sprite.properties['Ext']) == "gun2":
                self.gun2 += 1
            elif str(extra_item_sprite.properties['Ext']) == "snorkl":
                self.snork_ile +=1
            self.window.score += 1

        self.physics_engine.add_collision_handler("bullet", "extra_item", post_handler=extra_item_hit_handler2)

        def extra_item_hit_handler3(player_sprite, extra_item_sprite, _arbiter, _space, _data):
            if self.window.sound == 0:
                arcade.play_sound(self.extrai_sound)
            if str(extra_item_sprite.properties['Ext']) == "heart":
                self.mocshield += 1
            elif str(extra_item_sprite.properties['Ext']) == "key":
                self.key += 1
            elif str(extra_item_sprite.properties['Ext']) == "diamond":
                self.diamond += 1
            elif str(extra_item_sprite.properties['Ext']) == "gun1":
                self.gun1 += 1
            elif str(extra_item_sprite.properties['Ext']) == "gun2":
                self.gun2 += 1
            elif str(extra_item_sprite.properties['Ext']) == "snorkl":
                self.snork_ile +=1
            self.window.score += 1
            extra_item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "extra_item", post_handler=extra_item_hit_handler3)

        def coins_hit_handler(bullet_sprite, coins_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            coins_sprite.remove_from_sprite_lists()
            if self.window.sound == 0:
                arcade.play_sound(self.coin_sound)
            points = int(coins_sprite.properties['Points'])
            self.window.score += points

        self.physics_engine.add_collision_handler("bullet", "coins", post_handler=coins_hit_handler)

        def coins_hit_handler2(bullet_enemy_sprite, coins_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet_enemy", "coins", post_handler=coins_hit_handler2)

        def coins_hit_handler3(player_sprite, coins_sprite, _arbiter, _space, _data):
            points = int(coins_sprite.properties['Points'])
            self.window.score += points
            if self.window.sound == 0:
                arcade.play_sound(self.coin_sound)
            coins_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("player", "coins", post_handler=coins_hit_handler3)

        def player_hit_handler(player_sprite, xenemy, _arbiter, _space, _data):
            self.player_sprite.hit = True
            if self.window.sound == 0 and not self.koniec:
                arcade.sound.play_sound(self.strata_zycia_sound)
            if not (self.extra_life or self.tym_extra_life):
                self.game_over()

        self.physics_engine.add_collision_handler("player", "xenemy", post_handler=player_hit_handler)

        def player_hit_handler3(player_sprite, touch, _arbiter, _space, _data):
            if self.diamond_czas == 0:
                if self.window.sound == 0 and not self.koniec:
                    arcade.sound.play_sound(self.strata_zycia_sound)
                self.player_sprite.hit = True
                if not (self.extra_life or self.tym_extra_life):
                    self.game_over()
            arcade.pause(0.01)
        self.physics_engine.add_collision_handler("player", "touch", post_handler=player_hit_handler3)

        def player_hit_handler7(player_sprite, water, _arbiter, _space, _data):
            if self.czas_snorkl==0 and self.snork_ile>0:
                self.czas_snorkl=700
                self.snork_ile-=1
                self.player_sprite.snorkl= True
            if self.czas_snorkl>0:
                self.player_sprite.snorkl=True
            if self.czas_snorkl==0 and self.snork_ile==0:
                if not (self.extra_life or self.tym_extra_life):
                    if self.window.sound == 0 and not self.koniec:
                        arcade.sound.play_sound(self.strata_zycia_sound)
                    self.player_sprite.hit = True
                    self.game_over()
                self.player_sprite.snorkl = True
                arcade.pause(0.001)
        self.physics_engine.add_collision_handler("player", "water", post_handler=player_hit_handler7)

        def player_hit_handler4(player_sprite, bomb_sprite, _arbiter, _space, _data):
            if bomb_sprite.pozbawzycia:
                bomb_sprite.pozbawzycia = False
                if not (self.extra_life or self.tym_extra_life):
                    self.mocshield -= 1
                self.player_sprite.hit = True
                self.camera.shake((3, 6))
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.tarcza_sound)
                    arcade.sound.play_sound(self.hit_sound)
                if self.mocshield == 0:
                    self.shield.remove_from_sprite_lists()
                    if self.window.sound == 0 and not self.koniec:
                        arcade.sound.play_sound(self.strata_zycia_sound)
                    self.game_over()

        self.physics_engine.add_collision_handler("player", "bomb", post_handler=player_hit_handler4)

        def player_hit_handler5(player_sprite, item, _arbiter, _space, _data):
            if not item.zamiana and  len(self.wybuch2.sprite_lists) == 0:
                if item.sila == False:
                    item.sila = True
                item.ilosc = 0
                if "sup" in item.properties:
                    item.zamiana = True
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.zamiana_sound)
                    # wybych i zamiana
                    self.wybuch2.center_x = item.center_x
                    self.wybuch2.center_y = item.center_y
                    self.zamiana_x = item.center_x
                    self.zamiana_y = item.center_y
                    tekst = int(random.randrange(4))
                    if tekst == 0:
                        self.zamiana_tekst = "Uwaga bomba"
                        x = self.zamiana_x + 10
                        y = self.zamiana_y + 250
                        self.upadek_bomb(x, y)
                    elif tekst == 1:
                        self.zamiana_tekst = "50 Points"
                        self.window.score += 50
                    elif tekst == 2:
                        if self.ilosczyc < 3:
                            self.zamiana_tekst = "Extra live"
                            self.ilosczyc += 1
                        else:
                            self.zamiana_tekst = "50 Points"
                            self.window.score += 50
                    elif tekst == 3:
                        self.zamiana_tekst = "Super power"
                        self.diamond_czas = 700
                    item.remove_from_sprite_lists()
                    # Add to a list of sprites
                    self.scene.add_sprite("wybuch2", self.wybuch2)
                    self.wybuch2.czywybuch = True
        self.physics_engine.add_collision_handler("player", "item", post_handler=player_hit_handler5)

        def player_hit_handler6(player_sprite,bullet_enemy_sprite, _arbiter, _space, _data):
            if not (self.extra_life or self.tym_extra_life):
                self.mocshield -= 1
                self.player_sprite.hit = True
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.tarcza_sound)
                if self.mocshield==0:
                    self.shield.remove_from_sprite_lists()
                    if self.window.sound == 0 and self.koniec == 0:
                        arcade.sound.play_sound(self.strata_zycia_sound)
                    self.game_over()
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("player", "bullet_enemy", post_handler=player_hit_handler6)

        def bullet_hit_handler(bullet_sprite, xenemy, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            if xenemy.zycie < 100:
                xenemy.zycie -= 1
            predkosc = int(random.randrange(4))
            if xenemy.change_x > 0:
                nowa_predkosc = min(xenemy.change_x + predkosc, 6)
                xenemy.change_x = -nowa_predkosc
            elif xenemy.change_x < 0:
                nowa_predkosc = min(xenemy.change_x - predkosc, -6)
                xenemy.change_x = -nowa_predkosc
            elif xenemy.change_y > 0:
                nowa_predkosc = min(xenemy.change_y + predkosc, 6)
                xenemy.change_y = -nowa_predkosc
            elif xenemy.change_y < 0:
                nowa_predkosc = min(xenemy.change_y - predkosc, -6)
                xenemy.change_y = -nowa_predkosc

            if xenemy.zycie == 0:
                points = int(xenemy.properties['Points'])
                self.window.score += points
                # Make an explosion
                self.explosion.center_x = xenemy.center_x
                self.explosion.center_y = xenemy.center_y
                xenemy.remove_from_sprite_lists()
                # Add to a list of sprites that are explosions
                self.scene.add_sprite("explosion", self.explosion)
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.xenemy_kill_sound)
            else:
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.xenemy_hurt_sound)

        self.physics_engine.add_collision_handler("bullet", "xenemy", post_handler=bullet_hit_handler)

        def bullet_hit_handler2(bullet, golem_sprite, _arbiter, _space, _data):
            bullet.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "golem", post_handler=bullet_hit_handler2)

        def bullete_hit_handler2(bullet_enemy_sprite, touch, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet_enemy", "touch", post_handler=bullete_hit_handler2)

        def golem_hit_handler(player_sprite, golem_sprite, _arbiter, _space, _data):
            self.player_golem = True

        self.physics_engine.add_collision_handler("player", "golem", post_handler=golem_hit_handler)

        self.zaczyt_punktow()

    def update_minimap(self):
        self.minimap_sprite.center_x=self.screen_center_x+int(SCREEN_WIDTH/8)
        self.minimap_sprite.center_y=self.screen_center_y+SCREEN_HEIGHT-int(SCREEN_HEIGHT/8)-10
        proj = 0, self.end_of_map, 0, self.end_of_map_y
        with self.minimap_sprite_list.atlas.render_into(self.minimap_texture, projection=proj) as fbo:
            fbo.clear(MINIMAP_BACKGROUND_COLOR)
            self.scene.draw()

    def nowy_golem(self):
        # ustawienie golema
        ktory = int(random.randrange(3))
        if ktory == 0:
            self.golem = Golem1()
        elif ktory == 1:
            self.golem = Golem2()
        else:
            self.golem = Golem3()
        # self.player_sprite.center_x -width/8 - (self.camera.viewport_width /
        self.golem.center_x = 50 + + int(random.randrange(self.end_of_map))
        while self.golem.center_x < self.player_sprite.center_x - self.camera.viewport_width / 2 or self.golem.center_x > self.player_sprite.center_x + self.camera.viewport_width / 2:
            self.golem.center_x = 50 + int(random.randrange(self.end_of_map))
        self.golem.center_y = self.end_of_map_y + 100
        self.scene.add_sprite("golem", self.golem)

        self.physics_engine.add_sprite(self.golem,
                                       friction=0,
                                       mass=PLAYER_MASS * 2,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="golem",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

    def upadek_bomb(self, x, y):
        # wystrzał bobmy przez obcego
        self.bomb = Bomb(hit_box_algorithm="Detailed")
        self.bomb.texture = self.bomb.bomb_textures[0]
        self.bomb.hit_box = self.bomb.texture.hit_box_points
        self.bomb.center_x = x + int(random.randrange(50))
        self.bomb.center_y = y + int(random.randrange(50))
        self.bomb.angle = int(random.randrange(180))
        self.scene.add_sprite("bomb", self.bomb)
        self.bomb.scale = 1
        self.bomb.czaswybuchu = 150 + int(random.randrange(200))
        bomb_gravity = (-BULLET_GRAVITY / 2, -BULLET_GRAVITY * 8)
        self.physics_engine.add_sprite(self.bomb,
                                       mass=BULLET_MASS * 4,
                                       damping=0.5,
                                       friction=0.7,
                                       collision_type="bomb",
                                       gravity=bomb_gravity,
                                       elasticity=0.9)
        force_bomb = (BULLET_ENEMY_FORCE * 3, 0)
        self.physics_engine.apply_force(self.bomb, force_bomb)
        if self.window.sound == 0:
            arcade.play_sound(self.bomb_kill_sound)

    def zaczyt_punktow(self):
        # ile punktów ma obcy
        for xenemy_sprite in self.scene.name_mapping["Xenemy"]:
            points = int(xenemy_sprite.properties['Points'])
            xenemy_sprite.zycie = points
        # zaczyt sila do item:
        for item_sprite in self.scene.name_mapping["Dynamic Items"]:
            item_sprite.sila = False
            item_sprite.ilosc = 0
            # czy robimy zamiane
            item_sprite.zamiana = False
        for tele_sprite in self.scene.name_mapping["Teleport"]:
            if "poz_x" in tele_sprite.properties:
                tele_sprite.poz_x = int(tele_sprite.properties['poz_x'])
            if "poz_y" in tele_sprite.properties:
                tele_sprite.poz_y = int(tele_sprite.properties['poz_y'])

    def skok(self):
        # skok postaci
        if self.player_sprite.czydrugiskok and self.odliczamdo_drugiego > 10 and not self.player_sprite.is_on_ladder:
            impulse = (0, PLAYER_JUMP_IMPULSE / 2)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)
            self.player_sprite.czydrugiskok = False
            self.odliczamdo_drugiego = 0

        elif self.physics_engine.is_on_ground(self.player_sprite) \
                and not self.player_sprite.is_on_ladder:
            impulse = (0, PLAYER_JUMP_IMPULSE)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)
            self.player_sprite.czydrugiskok = True

    def on_key_press(self, key, modifiers):
        # sterowanie
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
            self.skok()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.SPACE:
            self.strzal(self.gun_active)
        elif key == arcade.key.KEY_1:
            if self.gun1 > 0 and self.czas_gun == 0:
                self.czas_gun = 1000
                self.gun1 -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 1
                self.strzal(self.gun_active)
        elif key == arcade.key.Z:
            if self.diamond > 0:
                self.diamond -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.diamond_czas = 700
        elif key == arcade.key.KEY_2:
            if self.gun2 > 0 and self.czas_gun == 0:
                self.czas_gun = 1000
                self.gun2 -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 2
                self.strzal(self.gun_active)
        elif key == arcade.key.S:
            if self.window.sound == 0:
                self.window.sound = 1
            else:
                self.window.sound = 0
        elif key == arcade.key.M:
            if self.window.music == 0:
                self.window.music = 1
                self.window.musicp.stop(player=self.window.media_player)
            else:
                self.window.music = 0
                self.window.media_player = self.window.musicp.play(MUSIC_VOLUME)
        elif key == arcade.key.Q:
            arcade.close_window()
        elif key == arcade.key.I:
            if self.extra_life:
                self.extra_life = False
            else:
                self.extra_life = True
        elif key == arcade.key.N:
            if self.czymap:
                self.czymap = False
            else:
                self.czymap = True

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
        # strzał playera
        self.rodzaj = gun
        for strzal in range(self.rodzaj * 3 + 1):
            if self.rodzaj == 0:
                bullet = BulletSprite("pymunk/images/ok/fireball.png", SPRITE_SCALING_LASER)
            elif self.rodzaj == 1:
                bullet = BulletSprite("pymunk/images/ok/tarcza_mala.png", SPRITE_SCALING_LASER)
            elif self.rodzaj == 2:
                bullet = BulletSprite("pymunk/images/ok/star_mala.png", SPRITE_SCALING_LASER)
            self.scene.add_sprite("bullet", bullet)
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.position = self.player_sprite.position
            zmkata = 0
            if strzal > 1:
                zmkata = random.randrange(30) / 10
            if self.player_sprite.character_face_direction == LEFT_FACING:
                angle = -3 + zmkata
            else:
                angle = -0.03 + zmkata
            size = max(self.player_sprite.width, self.player_sprite.height) / 2
            bullet.center_x += size * math.cos(angle)
            bullet.center_y += size * math.sin(angle)
            bullet.angle = math.degrees(angle)
            bullet_gravity = (0, -BULLET_GRAVITY)
            self.physics_engine.add_sprite(bullet,
                                           mass=BULLET_MASS,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet",
                                           gravity=bullet_gravity,
                                           elasticity=0.9)

            force = (BULLET_MOVE_FORCE, 0)
            self.physics_engine.apply_force(bullet, force)
            if self.window.sound == 0:
                arcade.sound.play_sound(self.gun_sound)

    def strzal_enemy(self, x, y):
        # strzał obcego
        if random.randrange(2) == 0:
            bullet_enemy = Bullet_Enemy("pymunk/images/ok/laserBlue01.png", SPRITE_SCALING_LASER)
        else:
            bullet_enemy = Bullet_Enemy("pymunk/images/ok/laserRed01.png", SPRITE_SCALING_LASER)
        if random.randrange(20) == 0:
            self.scene.add_sprite("bullet_enemy", bullet_enemy)
            bullet_enemy.center_x = x
            bullet_enemy.center_y = y
            zmkata = random.randrange(30) / 10
            if random.randrange(2) == 0:
                angle = -3 + zmkata
            else:
                angle = -0.03 + zmkata
            size = max(bullet_enemy.width, bullet_enemy.height) / 2
            bullet_enemy.center_x += size * math.cos(angle)
            bullet_enemy.center_y += size * math.sin(angle)
            bullet_enemy.angle = math.degrees(angle)
            bullet_gravity = (0, -BULLET_GRAVITY)
            self.physics_engine.add_sprite(bullet_enemy,
                                           mass=BULLET_MASS * 1.5,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet_enemy",
                                           gravity=bullet_gravity,
                                           elasticity=0.9)

            zmniejszssile = random.randrange(1000)
            force_enemy = (BULLET_ENEMY_FORCE - zmniejszssile, 0)
            self.physics_engine.apply_force(bullet_enemy, force_enemy)
        if random.randrange(250) == 0:
            if x > self.view_left and x < self.view_left + SCREEN_WIDTH:
                self.upadek_bomb(x, y)

    def on_update(self, delta_time):
        if not self.koniec:
            self.scene.update_animation(delta_time,
                                        ["Dynamic Items", "Coins", "Xenemy", "Background", "Background2","Extra_item", "Dont touch"])
            self.scene.update(["explosion", "shield", "golem", "wybuch2"])
            self.shield.follow_sprite(self.player_sprite)

            if self.player_sprite.czydrugiskok:
                self.odliczamdo_drugiego += 1
            if self.player_sprite.center_y > self.end_of_map_y + 150:
                self.player_sprite.center_y = self.end_of_map_y + 150
                impulse = (0, 0)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)

            # czy jesteśmy poza mapą
            if self.player_sprite.right > self.end_of_map:
                if self.key < 3:
                    self.player_sprite.hit = True
                    self.game_over()
                else:
                    if self.window.level < self.max_level:
                        self.window.level += 1
                        if self.window.sound == 0:
                            arcade.play_sound(self.level_sound)
                        self.setup()
                    else:
                        # koniec wszystkich poziomów
                        arcade.pause(1)
                        self.window.poziomy = True
                        arcade.cleanup_texture_cache()
                        game_over_view = GameOverView()
                        self.window.show_view(game_over_view)
            if self.player_sprite.center_y < -100:
                # self.shield.remove_from_sprite_lists()
                if self.window.sound == 0 and not self.koniec:
                    arcade.play_sound(self.strata_zycia_sound)
                self.game_over()

            is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

            if self.left_pressed and not self.right_pressed:
                # fizyka gracza
                if is_on_ground or self.player_sprite.is_on_ladder:
                    force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
                else:
                    force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.physics_engine.set_friction(self.player_sprite, 0)
            elif self.right_pressed and not self.left_pressed:
                if is_on_ground or self.player_sprite.is_on_ladder:
                    force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
                else:
                    force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.physics_engine.set_friction(self.player_sprite, 0)
            elif self.up_pressed and not self.down_pressed:
                if self.player_sprite.is_on_ladder:
                    force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    self.physics_engine.set_friction(self.player_sprite, 0)
            elif self.down_pressed and not self.up_pressed:
                if self.player_sprite.is_on_ladder:
                    force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    self.physics_engine.set_friction(self.player_sprite, 0)
            else:
                self.physics_engine.set_friction(self.player_sprite, 1.0)

            # uaktualnienie fizyki
            self.physics_engine.step()

            # uaktualnienie ruchomych sprite-ów
            for moving_sprite in self.scene.name_mapping["Moving Platforms"]:
                if moving_sprite.boundary_right and \
                        moving_sprite.change_x > 0 and \
                        moving_sprite.right > moving_sprite.boundary_right:
                    moving_sprite.change_x *= -1
                elif moving_sprite.boundary_left and \
                        moving_sprite.change_x < 0 and \
                        moving_sprite.left < moving_sprite.boundary_left:
                    moving_sprite.change_x *= -1
                if moving_sprite.boundary_top and \
                        moving_sprite.change_y > 0 and \
                        moving_sprite.top > moving_sprite.boundary_top:
                    moving_sprite.change_y *= -1
                elif moving_sprite.boundary_bottom and \
                        moving_sprite.change_y < 0 and \
                        moving_sprite.bottom < moving_sprite.boundary_bottom:
                    moving_sprite.change_y *= -1
                velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(moving_sprite, velocity)
            for xenemy_sprite in self.scene.name_mapping["Xenemy"]:
                x = xenemy_sprite.center_x
                y = xenemy_sprite.center_y
                if int(xenemy_sprite.properties['Points']) < 100:
                    self.strzal_enemy(x, y)
                    pass
                if xenemy_sprite.boundary_right and xenemy_sprite.change_x > 0 and \
                        xenemy_sprite.right > xenemy_sprite.boundary_right:
                    xenemy_sprite.change_x *= -1
                elif xenemy_sprite.boundary_left and xenemy_sprite.change_x < 0 and \
                        xenemy_sprite.left < xenemy_sprite.boundary_left:
                    xenemy_sprite.change_x *= -1
                if xenemy_sprite.boundary_top and \
                        xenemy_sprite.change_y > 0 and \
                        xenemy_sprite.top > xenemy_sprite.boundary_top:
                    xenemy_sprite.change_y *= -1
                elif xenemy_sprite.boundary_bottom and \
                        xenemy_sprite.change_y < 0 and \
                        xenemy_sprite.bottom < xenemy_sprite.boundary_bottom:
                    xenemy_sprite.change_y *= -1
                velocity1 = (xenemy_sprite.change_x * 1 / delta_time, xenemy_sprite.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(xenemy_sprite, velocity1)

             # czy mozna teleport
            if not self.czy_mozna_teleport:
                self.licznik_teleport -= 1
                if self.licznik_teleport == 0:
                    self.licznik_teleport = 120
                    self.tym_extra_life = False
                    self.czy_mozna_teleport = True
                    self.player_sprite.tele = False
                    self.player_sprite.texture = self.player_sprite.idle_textures[1][RIGHT_FACING]
            if len(self.scene.name_mapping["golem"]) <= 1:
                self.nowy_golem()

            #aktualizacja tekstów
            self.score_text = f"Score: {self.window.score}" + "  Power:" + str(self.mocshield) + "  Live:" + str(
                self.ilosczyc) + "   Level:" + str(self.window.level)
            self.scoreT.text=self.score_text
            self.key_tekst = str(self.key)
            self.keyT.text= self.key_tekst
            self.gun1_tekst = str(self.gun1)
            self.gun1T.text = self.gun1_tekst
            self.gun2_tekst =str(self.gun2)
            self.gun2T.text = self.gun2_tekst
            self.snork_tekst = str(self.snork_ile)
            self.snorkT.text= self.snork_tekst
            self.diamond_tekst = str(self.diamond)
            self.diamondT.text = self.diamond_tekst

            # inteligencja golema
            for golem in (self.scene.name_mapping["golem"]):
                if golem.character_face_direction == RIGHT_FACING:
                    self.physics_engine.apply_force(golem, (1000, 0))
                if golem.character_face_direction == LEFT_FACING:
                    self.physics_engine.apply_force(golem, (-1000, 0))
                if golem.czasbezruchu >= 50 and golem.character_face_direction == RIGHT_FACING:
                    self.physics_engine.apply_force(golem, (-5000, 1000))
                    impulse = (0, PLAYER_JUMP_IMPULSE * 1.5)
                    self.physics_engine.apply_impulse(golem, impulse)
                    golem.czasbezruchu = 0
                if golem.czasbezruchu >= 50 and golem.character_face_direction == LEFT_FACING:
                    self.physics_engine.apply_force(golem, (5000, 1000))
                    impulse = (0, PLAYER_JUMP_IMPULSE * 1.5)
                    self.physics_engine.apply_impulse(golem, impulse)
                    golem.czasbezruchu = 0
                golem.czasbezruchu += 1
                if golem.slash == 0 and int(random.randrange(100)) == 0 and self.physics_engine.is_on_ground(golem):
                    golem.cur_texture = 0
                    golem.slash = 1
                    if self.window.sound == 0 and self.golem.center_x > self.view_left and self.golem.center_x < self.view_left + SCREEN_WIDTH:
                        arcade.sound.play_sound(self.golem_sound)
                if self.player_golem:
                    self.player_golem = False
                    if golem.pierwszeuderzenie == 0 and golem.slash == 1:
                        self.mocshield -= 1
                        golem.pierwszeuderzenie = 1
                        self.player_sprite.hit = True
                        self.camera.shake((3, 6))
                        if self.window.sound == 0:
                            arcade.sound.play_sound(self.tarcza_sound)
                        if self.mocshield == 0:
                            self.shield.remove_from_sprite_lists()
                            if self.window.sound == 0 and not self.koniec:
                                arcade.sound.play_sound(self.strata_zycia_sound)
                            self.game_over()
                if golem.center_y < -100:
                    golem.remove_from_sprite_lists()

            # Position the camera
            self.center_camera_to_player(panning_fraction=0.5)
            # aktualizacja pozostałych danych
            if self.czas_gun > 0:
                self.czas_gun -= 1
                if self.czas_gun == 0:
                    self.gun_active = 0
            if self.diamond_czas > 0:
                self.diamond_czas -= 1
            if self.czas_snorkl>0:
                self.czas_snorkl-=1
        else:
            self.scene.update_animation(delta_time, ["Coins", "Xenemy", "Background", "Extra_item", "Dont touch"])
            self.scene.update(["explosion", "shield"])
            self.shield.follow_sprite(self.player_sprite)
            for moving_sprite in self.scene.name_mapping["Moving Platforms"]:
                velocity = (0, 0)
                self.physics_engine.set_velocity(moving_sprite, velocity)
            for xenemy_sprite in self.scene.name_mapping["Xenemy"]:
                velocity1 = (0, 0)
                self.physics_engine.set_velocity(xenemy_sprite, velocity1)
            force = (0, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
            self.physics_engine.step()
            self.center_camera_to_player(panning_fraction=0.1)

    def on_draw(self):
        # Rysowanie wszystkiego
        # arcade.start_render()
        self.clear()
        self.camera.use()
        arcade.draw_lrwh_rectangle_textured(self.screen_center_x - 100, self.screen_center_y - 100,
                                            SCREEN_WIDTH * 1.2, SCREEN_HEIGHT * 1.2,
                                            self.background)

        self.scene.draw()
        if self.czymap:
            # Update the minimap
            self.update_minimap()
            # Draw the minimap
            self.minimap_sprite_list.draw()

        if self.wybuch2.czywybuch:
            arcade.draw_text(self.zamiana_tekst, self.zamiana_x, self.zamiana_y,
                             arcade.csscolor.RED, 30, font_name="Kenney Pixel")
        self.gui_camera.use()
        if self.koniec:
            self.wynik()
        else:
            self.wynik2()

    def wynik(self):
        # wyświetlenie wyniku po game over
        self.zliczdead += 1
        if self.ilosczyc == 3:
            score_text = "Again - you still have " + str(self.ilosczyc - 1) + " lifes"
        elif self.ilosczyc == 2:
            score_text = "Again - you still have " + str(self.ilosczyc - 1) + " life"
        elif self.ilosczyc == 1:
            score_text = "unfortunately - failure"
        arcade.draw_text(score_text, SCREEN_WIDTH / 2 + self.view_left, 2 * SCREEN_HEIGHT / 3 + self.view_bottom,
                         arcade.csscolor.RED, 48, anchor_x="center", font_name="Kenney Pixel")
        score_text1 = "Your score - "
        arcade.draw_text(score_text1 + str(self.window.score), SCREEN_WIDTH / 2 + self.view_left,
                         SCREEN_HEIGHT / 2 + self.view_bottom,
                         arcade.csscolor.RED, 64, anchor_x="center", font_name="Kenney Pixel")

        if self.zliczdead >= 100:
            self.ilosczyc -= 1
            arcade.pause(1)
            self.view_bottom = 0
            self.view_left = 0
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
            if self.ilosczyc == 0:
                self.wyw_gameover()
            self.setup()

    def wynik2(self):
        arcade.draw_rectangle_filled(5, 0, 1750, 100, arcade.csscolor.WHITE)
        if self.gun_active == 2:
            if self.czas_gun > 150:
                arcade.draw_rectangle_filled(735, 0, 100, 100, arcade.csscolor.RED)
            else:
                arcade.draw_rectangle_filled(735, 0, 100, 100, arcade.csscolor.SLATE_GREY)
        if self.gun_active == 1:
            if self.czas_gun > 150:
                arcade.draw_rectangle_filled(645, 0, 79, 100, arcade.csscolor.PALE_VIOLET_RED)
            else:
                arcade.draw_rectangle_filled(645, 0, 79, 100, arcade.csscolor.SLATE_GRAY)
        if self.diamond_czas >= 150:
            arcade.draw_rectangle_filled(535, 0, 79, 100, arcade.csscolor.MEDIUM_PURPLE)
        if self.diamond_czas < 150 and self.diamond_czas > 0:
            arcade.draw_rectangle_filled(535, 0, 79, 100, arcade.csscolor.DARK_GREY)
        if self.czas_snorkl > 0:
            arcade.draw_rectangle_filled(842, 0, 79, 100, arcade.csscolor.GREENYELLOW)
        if self.key >= 3:
            arcade.draw_rectangle_filled(455, 0, 79, 100, arcade.csscolor.ORANGE_RED)
        arcade.draw_scaled_texture_rectangle(520, 40, self.scr1, scale=0.5)
        arcade.draw_texture_rectangle(440, 40, 40, 40, self.scr2)
        arcade.draw_scaled_texture_rectangle(620, 40, self.scr4, scale=0.25)
        arcade.draw_scaled_texture_rectangle(720, 40, self.scr3, scale=0.5)
        arcade.draw_scaled_texture_rectangle(820, 40, self.scr5, scale=0.5)
        self.scoreT.draw()
        self.keyT.draw()
        self.diamondT.draw()
        self.gun1T.draw()
        self.gun2T.draw()
        self.snorkT.draw()

    def game_over(self):
        # koniec życia
        if not self.koniec:
            self.koniec = True
        self.player_sprite.dead = True

    def wyw_gameover(self):
        arcade.cleanup_texture_cache()
        # wywołanie końca gry - przegrana
        game_over_view = GameOverView()
        # game_over_view = GameView()
        self.window.show_view(game_over_view)

    def center_camera_to_player(self, panning_fraction: float = 0.1):
        self.screen_center_x = self.player_sprite.center_x - width / 8 - (self.camera.viewport_width / 2)
        self.screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2)
        if self.screen_center_x < -width / 8:
            self.screen_center_x = -width / 8
        if self.screen_center_y < -50:
            self.screen_center_y = -50
        player_centered = self.screen_center_x, self.screen_center_y

        self.camera.move_to(player_centered, panning_fraction)

def main():
    # głowna metoda
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=full)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
