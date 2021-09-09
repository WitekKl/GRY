import math
import random
import os
from typing import Optional
import arcade
import arcade.gui
from arcade.gui import UIManager

# wykorzystano:
# Paul Vincent Craven.
# https://arcade.academy/index.html
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# muzyka jest dostępna na licencji Creative Commons

#stałe
SCREEN_TITLE = "PyMunk W-Mam"
SPRITE_IMAGE_SIZE = 128
global path, full
path = "pymunk/images/animated_characters/female_person/femalePerson"
full = False
SPRITE_SCALING_PLAYER = 0.75
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
PLAYER_MOVE_FORCE_ON_GROUND = 8000
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
MUSIC_VOLUME = 0.01

class Snowflake:
    #płatki śniegu
    def __init__(self):
        self.x = 0
        self.y = 0
    def reset_pos(self):
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)

class MyButton(arcade.gui.UIImageButton):
    #przyciski w menu startowym
    def __init__(self, center_x, center_y, text):
        super().__init__(text = text, center_x = center_x, center_y= center_y,
                            normal_texture = arcade.load_texture('pymunk/images/ok/yellow_button02.png'),
                            hover_texture=arcade.load_texture('pymunk/images/ok/yellow_button03.png'),
                            press_texture = arcade.load_texture('pymunk/images/ok/yellow_button00.png'))
    def on_press(self):
        self.pressed = 1
    def on_release(self):
        if self.pressed ==1:
            self.pressed = 0

class MyButtonleft(arcade.gui.UIImageButton):
    #przycisk lewo
    def __init__(self, center_x, center_y, text):
        super().__init__(text = text, center_x = center_x, center_y= center_y,
                        normal_texture = arcade.load_texture('pymunk/images/ok/yellow_sliderLeft.png'),
                         press_texture = arcade.load_texture('pymunk/images/ok/yellow_sliderLeft.png'),
                         hover_texture = arcade.load_texture('pymunk/images/ok/yellow_sliderLeft.png'))
    def on_press(self):
        self.pressed = 1
    def on_release(self):
        if self.pressed ==1:
            self.pressed = 0

class MyButtonRight(arcade.gui.UIImageButton):
    #przycisk prawo
    def __init__(self, center_x, center_y, text):
        super().__init__(text=text, center_x=center_x, center_y=center_y,
                         normal_texture=arcade.load_texture('pymunk/images/ok/yellow_sliderRight.png'),
                         hover_texture=arcade.load_texture('pymunk/images/ok/yellow_sliderRight.png'),
                         press_texture=arcade.load_texture('pymunk/images/ok/yellow_sliderRight.png'))
    def on_press(self):
        self.pressed = 1
    def on_release(self):
        if self.pressed ==1:
           self.pressed = 0

class MenuView(arcade.View):
    #menu startowe
    def __init__(self):
        super().__init__()
        self.window.sound = 0
        self.window.music = 0
        self.window.draw_start_time = 0
        self.snowflake_list = None
        self.snowflake_list = []
        self.ui_manager = UIManager()
        self.window.musicp = arcade.sound.load_sound("pymunk/images/ok/musicfree.mp3")
        self.window.musicp.play(MUSIC_VOLUME)
        for i in range(150):
            snowflake = Snowflake()
            snowflake.x = random.randrange(SCREEN_WIDTH)
            snowflake.y = random.randrange(SCREEN_HEIGHT + 200)
            snowflake.size = random.randrange(7)
            snowflake.speed = random.randrange(20, 80)
            snowflake.angle = random.uniform(0, math.pi * 2)
            self.snowflake_list.append(snowflake)
    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.CHROME_YELLOW)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Naciśnij klawisz myszki i poczekaj chwilkę", SCREEN_WIDTH/2, SCREEN_HEIGHT/6,
                         arcade.color.GRAY, font_size=30, anchor_x="center", font_name='comic')
        for snowflake in self.snowflake_list:
            arcade.draw_circle_filled(snowflake.x, snowflake.y,
                                      snowflake.size, arcade.color.WHITE)

    def setup(self):
        #wyświetlenie przycisków
        self.button1 = MyButton (center_x = SCREEN_WIDTH/4, center_y = SCREEN_HEIGHT*3/4,text = 'Sound On/Off')
        self.ui_manager.add_ui_element(self.button1)
        self.button2 = MyButton (center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT*3/4,text = 'Music On/Off')
        self.ui_manager.add_ui_element(self.button2)
        self.button3 = MyButton (center_x = SCREEN_WIDTH*3/4, center_y = SCREEN_HEIGHT*3/4,text = 'Instruction')
        self.ui_manager.add_ui_element(self.button3)
        self.button4 = MyButton (center_x = SCREEN_WIDTH/4, center_y = SCREEN_HEIGHT/2.5,text = 'Characters')
        self.ui_manager.add_ui_element(self.button4)
        self.button5 = MyButton (center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT/2.5,text = 'PLAY GAME')
        self.ui_manager.add_ui_element(self.button5)
        self.button6 = MyButton (center_x = SCREEN_WIDTH*3/4, center_y = SCREEN_HEIGHT/2.5,text = 'QUIT GAME')
        self.ui_manager.add_ui_element(self.button6)

    def on_update(self, delta_time):
        #płatki śniegu animacja
        for snowflake in self.snowflake_list:
            snowflake.y -= snowflake.speed * delta_time
            if snowflake.y < 0:
                snowflake.reset_pos()
            snowflake.x += snowflake.speed * math.cos(snowflake.angle) * delta_time
            snowflake.angle += 1 * delta_time

        #czy naciśnieto przycisk
        if self.button1.pressed == 1:
            if self.window.sound == 0:
                self.window.sound = 1
                self.button1.remove_from_sprite_lists()
                self.button1 = MyButton(center_x = SCREEN_WIDTH/4, center_y = SCREEN_HEIGHT*3/4, text='Sound Off')
                self.ui_manager.add_ui_element(self.button1)
            else:
                self.window.sound = 0
                self.button1.remove_from_sprite_lists()
                self.button1 = MyButton(center_x = SCREEN_WIDTH/4, center_y = SCREEN_HEIGHT*3/4, text='Sound On')
                self.ui_manager.add_ui_element(self.button1)

        if self.button2.pressed == 1:
            if self.window.music == 0:
                self.window.music = 1
                self.window.musicp.stop()
                self.button2.remove_from_sprite_lists()
                self.button2 = MyButton(center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT*3/4, text='Music Off')
                self.ui_manager.add_ui_element(self.button2)
            else:
                self.button2.remove_from_sprite_lists()
                self.button2 = MyButton(center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT*3/4, text='Music On')
                self.ui_manager.add_ui_element(self.button2)
                self.window.music = 0
                self.window.musicp.play(MUSIC_VOLUME)
        if self.button3.pressed == 1:
            self.delete_b()
            intro_view = IntroView()
            self.window.show_view(intro_view)
        if self.button4.pressed == 1:
            self.delete_b()
            wybor_view = WyborView()
            self.window.show_view(wybor_view)
        if self.button5.pressed == 1:
            self.delete_b()
            self.window.musicp.stop()
            arcade.pause(0.1)
            game_view = GameView()
            self.window.show_view(game_view)
        if self.button6.pressed == 1:
            arcade.close_window()
        if self.window.musicp.is_complete() and self.window.music == 0:
            self.window.musicp.play(MUSIC_VOLUME)

    def delete_b(self):
        self.button1.remove_from_sprite_lists()
        self.button2.remove_from_sprite_lists()
        self.button3.remove_from_sprite_lists()
        self.button4.remove_from_sprite_lists()
        self.button5.remove_from_sprite_lists()
        self.button6.remove_from_sprite_lists()

class IntroView (arcade.View):
    #instrukcja
    def __init__(self):
        super().__init__()
        self.rozm = 10
    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN_YELLOW)

    def on_update(self, delta_time):
        self.rozm += 1
        if self.rozm ==64:
            self.rozm = 63

    def on_draw(self):
        arcade.start_render()
        text1 = "Instrukcja "
        arcade.draw_text(text1, SCREEN_WIDTH / 2, SCREEN_HEIGHT*8/10, arcade.csscolor.RED, self.rozm, anchor_x="center",
                         font_name='comic')
        if self.rozm == 63:
            text2 = " Gra platformowa\nW-Man"
            text3 = "Sterowanie - kursor\nspacja - strzał\n 1,2 - wybór broni\nz - włącz dont touch\nm - music on/off,  s - sound on/of \nq- wyjście z gry" \
                    "\nzabijaj wrogów, zbierz 3 klucze i dojdź do końca poziomu"
            arcade.draw_text(text2, SCREEN_WIDTH / 2, SCREEN_HEIGHT*5/10, arcade.csscolor.ROYAL_BLUE, self.rozm,
                             anchor_x="center", align="center", font_name='comic')
            arcade.draw_text(text3, SCREEN_WIDTH / 2, SCREEN_HEIGHT*4.5/10, arcade.csscolor.RED, self.rozm - 32,
                             anchor_x="center", anchor_y="top", align="center",
                             font_name='comic')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.musicp.stop()
        menu_view = MenuView()
        self.window.show_view(menu_view)

class WyborView(arcade.View):
    #wybór postaci
    def __init__(self):
        super().__init__()
        self.character = 1
        self.ui_manager = UIManager()
        self.wybor_list = None
        self.wybor: Optional[Wybor] = None
        global texturesok
        texturesok = 1

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.CHROME_YELLOW)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text("Wybierz postać", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.GRAY, font_size=30, anchor_x="center", font_name='comic')
        self.wybor_list.draw ()

    def setup (self):
        self.button7 = MyButtonleft (SCREEN_WIDTH/4, SCREEN_HEIGHT*3/4,text = '')
        self.ui_manager.add_ui_element(self.button7)
        self.button8 = MyButtonRight (SCREEN_WIDTH*3/4, SCREEN_HEIGHT*3/4,text = '')
        self.ui_manager.add_ui_element(self.button8)
        self.button9 = MyButton (SCREEN_WIDTH/2, SCREEN_HEIGHT/3,text = 'Menu')
        self.ui_manager.add_ui_element(self.button9)
        self.setup2()
    def setup2 (self):
        self.wybor = Wybor(hit_box_algorithm="Detailed")
        self.wybor.center_x = SCREEN_WIDTH/2
        self.wybor.center_y = SCREEN_HEIGHT*8/10
        self.wybor_list = arcade.SpriteList ()
        self.wybor_list.append(self.wybor)

    def on_update(self, delta_time):
        global path
        if self.button7.pressed == 1:
            arcade.pause(0.1)
            self.wybor.remove_from_sprite_lists()
            self.character -=1
            if self.character ==0:
                self.character =6
            self.wybierzsciezke()

        if self.button8.pressed == 1:
            self.wybor.remove_from_sprite_lists()
            arcade.pause(0.1)
            self.character += 1
            if self.character == 7:
                self.character = 1
            self.wybierzsciezke()
        if self.button9.pressed == 1:
            arcade.pause(0.1)
            self.button7.remove_from_sprite_lists()
            self.button8.remove_from_sprite_lists()
            self.wybor.remove_from_sprite_lists()
            self.button9.remove_from_sprite_lists()
            self.window.musicp.stop()
            menu_view = MenuView()
            self.window.show_view(menu_view)
        self.wybor.update(delta_time)

    def wybierzsciezke(self):
        global texturesok
        global path
        if self.character == 1:
            path = "pymunk/images/animated_characters/female_person/femalePerson"
            texturesok = 1
            self.setup2()
        if self.character == 2:
            path = "pymunk/images/animated_characters/female_adventurer/femaleAdventurer"
            texturesok = 2
            self.setup2()
        if self.character == 3:
            path = "pymunk/images/animated_characters/male_person/malePerson"
            texturesok = 3
            self.setup2()
        if self.character == 4:
            path = "pymunk/images/animated_characters/male_adventurer/maleAdventurer"
            texturesok = 4
            self.setup2()
        if self.character == 5:
            path = "pymunk/images/animated_characters/zombie/zombie"
            texturesok = 5
            self.setup2()
        if self.character == 6:
            path = "pymunk/images/animated_characters/robot/robot"
            texturesok = 6
            self.setup2()

class PlayerSprite(arcade.Sprite):
    #definicja gracza
    def __init__(self,
                 ladder_list: arcade.SpriteList,
                 hit_box_algorithm):
        super().__init__()
        global path
        main_path = path
        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER
        self.hit = False
        self.czydrugiskok = False
        self.licznik = 0
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png",
                                                          hit_box_algorithm=hit_box_algorithm)
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")
        self.hit_textures = []
        texture = arcade.load_texture(f"{main_path}_hit.png")
        self.hit_textures.append(texture)
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)
        self.dead_textures = []
        for j in range(3):
            for i in range(20):
                texture = arcade.load_texture("pymunk/images/spritesheets/czaszka_" + str(i) + ".png")
                self.dead_textures.append(texture)
        self.dead_textures.append(texture)
        # inicjowanie textur
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.dead = 0
        self.ladder_list = ladder_list
        self.is_on_ladder = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        #ruch postaci
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        if self.dead == 1:
            self.cur_texture += 1
            if self.cur_texture > 21:
                self.cur_texture = 0
            self.texture = self.dead_textures[self.cur_texture]
            return
        if self.hit == True:
            self.licznik +=1
            self.texture = self.hit_textures[0]
            if self.licznik==25:
                self.hit = False
                self.licznik =0
                self.texture = self.idle_texture_pair[self.character_face_direction]
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
            if self.cur_texture > 1:
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
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        #czy zmieniamy texturę
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class BulletSprite(arcade.Sprite):
    #strzał
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()
        self.angle += dy
        self.change_angle = self.angle
        self.update()

class Golem (arcade.Sprite):
    # definicja golema
    def __init__(self, hit_box_algorithm):
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.character_face_direction = RIGHT_FACING
        self.czasbezruchu = 0
        self.temposlash = 0
        self.pierwszeuderzenie =0
        self.slash = 0
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.walk_textures = []
        for i in range(12):
            texture = arcade.load_texture_pair("pymunk/images/enemies/golem/0_Golem_Walking_" + str(i) + ".png")
            self.walk_textures.append(texture)
        self.texture = self.walk_textures[0][self.character_face_direction]
        self.fall_texture = arcade.load_texture_pair("pymunk/images/enemies/golem/0_Golem_Falling Down_000.png")
        self.slash_textures = []
        for i in range(12):
            texture = arcade.load_texture_pair("pymunk/images/enemies/golem/0_Golem_Run Slashing_"+ str(i) + ".png" )
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
            self.temposlash +=1
            if self.temposlash == 10:
                self.cur_texture += 1
                self.temposlash = 0
                if self.cur_texture > 11:
                    self.cur_texture = 0
                    self.slash = 0
                    self.pierwszeuderzenie = 0
                self.texture = self.slash_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.walk_textures[0][self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE/2:
            self.x_odometer = 0
            self.czasbezruchu = 0
            self.cur_texture += 1
            if self.cur_texture > 11:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        if not is_on_ground:
            self.texture = self.fall_texture[self.character_face_direction]
            return

class Bullet_Enemy(arcade.Sprite):
    #strzały obcych
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class Shield(arcade.Sprite):
    #tarcza
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

class Explosion(arcade.Sprite):
    #wybuch
    def __init__(self):
        super().__init__()
        self.explosion_texture_list = []
        columns = 16
        count = 60
        sprite_width = 128
        sprite_height = 128
        file_name = "pymunk/images/spritesheets/explosion1.png"
        change_x = 0
        change_y = 0
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)
        self.current_texture = 0
        self.textures = self.explosion_texture_list[0]

    def update(self):
        self.stop()
        self.current_texture += 1
        if self.current_texture < len(self.explosion_texture_list):
            self.texture = self.explosion_texture_list[self.current_texture]
        else:
            self.remove_from_sprite_lists()
            self.current_texture = 0

class Wybor(arcade.Sprite):
    #która postać - chodzenie w menu startowym
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.zmianatex = 0
        global texturesok
        global path
        self.walk_textures1 = []
        self.walk_textures2 = []
        self.walk_textures3 = []
        self.walk_textures4 = []
        self.walk_textures5 = []
        self.walk_textures6 = []
        for i in range(8):
            path1 = "pymunk/images/animated_characters/female_person/femalePerson"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures1.append(texture)
        for i in range(8):
            path1 = "pymunk/images/animated_characters/female_adventurer/femaleAdventurer"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures2.append(texture)
        for i in range(8):
            path1 = "pymunk/images/animated_characters/male_person/malePerson"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures3.append(texture)
        for i in range(8):
            path1 = "pymunk/images/animated_characters/male_adventurer/maleAdventurer"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures4.append(texture)
        for i in range(8):
            path1 = "pymunk/images/animated_characters/zombie/zombie"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures5.append(texture)
        for i in range(8):
            path1 = "pymunk/images/animated_characters/robot/robot"
            texture = arcade.load_texture(f"{path1}_walk{i}.png")
            self.walk_textures6.append(texture)
        self.cur_texture = 0
        self.texture = self.walk_textures1[0]
        self.hit_box = self.texture.hit_box_points
        self.scale = SPRITE_SCALING_PLAYER * 2

    def update(self, delta_time):
        global texturesok
        if texturesok == 1:
            self.co = self.walk_textures1
            self.texture = self.co[self.cur_texture]
        if texturesok == 2:
            self.co = self.walk_textures2
            self.texture = self.co[self.cur_texture]
        if texturesok == 3:
            self.co = self.walk_textures3
            self.texture = self.co[self.cur_texture]
        if texturesok == 4:
            self.co = self.walk_textures4
            self.texture = self.co[self.cur_texture]
        if texturesok == 5:
            self.co = self.walk_textures5
            self.texture = self.co[self.cur_texture]
        if texturesok == 6:
            self.co = self.walk_textures6
            self.texture = self.co[self.cur_texture]
        self.zmianatex += 1
        if self.zmianatex == 10:
            self.zmianatex = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.co[self.cur_texture]

class GameOverView(arcade.View):
    #przegrana
    def __init__(self):
        super().__init__()
        self.window.musicp.stop ()
        if width<1400:
            self.background = arcade.Sprite("pymunk/images/backgrounds/stars.png")
        else:
            self.background = arcade.Sprite("pymunk/images/backgrounds/starsd.png")
        self.background.left = self.background.bottom = 0
        if self.window.music == 0:
            self.window.musicp.play(MUSIC_VOLUME)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        score_text1 = "Twój wynik " + str(self.window.score)
        arcade.draw_text(score_text1 ,SCREEN_WIDTH/2, 2*SCREEN_HEIGHT/3,arcade.csscolor.RED, 64,anchor_x="center",font_name='comic')
        arcade.draw_text("Naciśnij klawisz myszki i poczekaj chwilkę", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-55,
                         arcade.color.RED_BROWN, font_size=30, anchor_x="center",font_name='comic')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.score = 0
        self.window.musicp.stop ()
        game_view = GameView()
        self.window.show_view(game_view)

class Bomb (arcade.Sprite):
    #stawianie bomby przez obcych
    def __init__(self, hit_box_algorithm):
        super().__init__()
        self.x_out = 0
        self.y_out = 0
        self.czaswybuchu = 200
        self.czywybuch = 0
        self.bomb_textures = []
        for i in range(15):
            texture = arcade.load_texture("pymunk/images/enemies/granat_frame_" + str(i) + ".png")
            self.bomb_textures.append(texture)
        self.explosion1_textures= []
        for i in range(16):
            texture = arcade.load_texture("pymunk/images/spritesheets/ekspozja_" + str(i) + ".png")
            self.explosion1_textures.append(texture)
        self.cur_texture = 0
        self.texture = self.bomb_textures [self.cur_texture]
        self.zmiana = 0
        self.hit_box = self.texture.hit_box_points

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.zmiana +=1
        self.czaswybuchu -=1
        if self.czaswybuchu== 1:
            self.czywybuch = 1
        if self.czaswybuchu <= 0:
            self.cur_texture += 1
            if self.zmiana <=3:
                self.cur_texture -=1
            else:
                self.zmiana =0
            if self.cur_texture <len(self.explosion1_textures):
                self.texture = self.explosion1_textures[self.cur_texture]
                self.hit_box = self.texture.hit_box_points
                return
            else:
                self.remove_from_sprite_lists()
                self.x_out = self.center_x
                self.y_out = self.center_y
                self.texture = self.bomb_textures[0]
                self.hit_box = self.texture.hit_box_points
                self.cur_texture = 0
                return
        self.cur_texture += 1
        if self.cur_texture > 14:
            self.cur_texture = 0
        self.texture = self.bomb_textures [self.cur_texture]
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class GameView(arcade.View):
    #główne okno
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.player_sprite: Optional[PlayerSprite] = None
        # definicja sprite-ów
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.bullet_enemy_list :Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.extra_item_list: Optional[arcade.SpriteList] = None
        self.background_list: Optional[arcade.SpriteList] = None
        self.moving_sprites_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None
        self.coins_list: Optional[arcade.SpriteList] = None
        self.xenemy_sprites_list: Optional[arcade.SpriteList] = None
        self.dont_touch_list:Optional[arcade.SpriteList] = None
        self.golem_list:Optional[arcade.SpriteList] = None
        #inne zmienne - część
        self.explosions_list = None
        self.shield_list = None
        self.bomb_list = None
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.odliczamdo_drugiego = 0
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.background = None
        self.level = 5
        self.max_level = 5
        self.ilosczyc = 3
        self.button = 10
        self.joy_y = False
        #dzwięki
        self.gun_sound = arcade.sound.load_sound("pymunk/sounds/laser4.wav")
        self.hit_sound = arcade.sound.load_sound("pymunk/sounds/explosion2.wav")
        self.bomb_kill_sound = arcade.load_sound ("pymunk/sounds/fall1.wav")
        self.xenemy_hurt_sound = arcade.load_sound("pymunk/sounds/fall3.wav")
        self.strata_zycia_sound = arcade.load_sound("pymunk/sounds/lose5.wav")
        self.game_over_sound = arcade.load_sound ("pymunk/sounds/gameover4.wav")
        self.tarcza_sound = arcade.load_sound ("pymunk/sounds/hurt4.wav")
        self.extrai_sound = arcade.load_sound("pymunk/sounds/jump3.wav")
        self.coin_sound = arcade.load_sound("pymunk/sounds/coin1.wav")
        self.golem_sound = arcade.load_sound("pymunk/sounds/kick.ogg")
        self.upgrade_sound = arcade.load_sound ("pymunk/sounds/upgrade5.wav")
        self.scr1 = texture = arcade.load_texture("pymunk/images/ok/gemBlue.png")
        self.scr2 = texture = arcade.load_texture("pymunk/images/ok/keyBlue.png")
        self.scr3 = texture = arcade.load_texture("pymunk/images/ok/gun_blue.png")
        self.scr4 = texture = arcade.load_texture("pymunk/images/ok/tarcza0.png")
        #definicja joysticka
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
        else:
            self.joystick = None
        self.setup()

    def setup(self):
        # główna część gry
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.bullet_enemy_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.golem_list = arcade.SpriteList ()
        self.view_bottom = 0
        self.view_left = 0
        self.mocshield = 20
        self.diamond = 0
        self.diamond_czas = 0
        self.key = 0
        self.gun1 = 0
        self.gun2 = 0
        self.gun_active = 0
        self.czas_gun = 0
        self.koniec = 0
        self.zliczdead = 0
        self.music = 0
        self.background = arcade.Sprite("pymunk/images/backgrounds/galaxy" + str(self.level) + ".png")
        self.background.left = self.background.bottom = 0

        if self.window.music == 0:
            self.window.musicp.stop()
            arcade.play_sound(self.tarcza_sound)
            self.window.musicp.play(MUSIC_VOLUME)
        # odczyt mapy
        map_name = "pymunk/tmx_maps/pymunk_wito_"+str(self.level) + ".tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        self.end_of_map = my_map.map_size.width * SPRITE_SIZE_MAP
        self.end_of_map_y = my_map.map_size.height * SPRITE_SIZE_MAP
        # Read in the map layers
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      'Platforms',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Simple")
        self.item_list = arcade.tilemap.process_layer(my_map,
                                                      'Dynamic Items',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")
        self.extra_item_list = arcade.tilemap.process_layer(my_map,
                                                      'Extra_item',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")
        self.ladder_list = arcade.tilemap.process_layer(my_map,
                                                        'Ladders',
                                                        SPRITE_SCALING_TILES,
                                                        use_spatial_hash=True,
                                                        hit_box_algorithm="Simple")
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            'Dont touch',
                                                            SPRITE_SCALING_TILES,
                                                            hit_box_algorithm="Detailed")
        self.coins_list = arcade.tilemap.process_layer(my_map,
                                                       'Coins',
                                                       SPRITE_SCALING_TILES,
                                                       hit_box_algorithm="Simple")
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            'Background',
                                                            SPRITE_SCALING_TILES,
                                                            hit_box_algorithm="None")


        # definicja playera i lokalizacji startowej
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed")
        self.bomb = Bomb(hit_box_algorithm="Detailed")
        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)
        self.explosion = Explosion()
        self.shield = Shield(hit_box_algorithm="Simple")
        self.shield_list.append(self.shield)
        self.moving_sprites_list = arcade.tilemap.process_layer(my_map,
                                                                'Moving Platforms',
                                                                SPRITE_SCALING_TILES)

        self.xenemy_sprites_list = arcade.tilemap.process_layer(my_map,
                                                                'Xenemy',
                                                                SPRITE_SCALING_ENEMIES)
        #fizyka gry
        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)
        #kolizje sprite- ów
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
            if bomb_sprite.czywybuch == 1:
                bomb_sprite.czywybuch = 0
                if self.window.sound == 0:
                    arcade.play_sound(self.hit_sound)
        self.physics_engine.add_collision_handler("bomb", "wall", post_handler=bomb_hit_handler3)

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        def wall_hit_handler2(bullet_enemy_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet_enemy", "wall", post_handler=wall_hit_handler2)

        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)

        def bullet_hit_handler3(bullet, golem_sprite, _arbiter, _space, _data):
            bullet.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet", "golem", post_handler=bullet_hit_handler3)

        def item_hit_handler2(bullet_enemy_sprite, item_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet_enemy", "item", post_handler=item_hit_handler2)

        def coins_hit_handler(bullet_sprite, coins_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            coins_sprite.remove_from_sprite_lists()
            if self.window.sound== 0:
                arcade.play_sound(self.coin_sound)
            points = int(coins_sprite.properties['Points'])
            self.window.score += points
        self.physics_engine.add_collision_handler("bullet", "coins", post_handler=coins_hit_handler)

        def extra_item_hit_handler2(bullet_sprite, extra_item_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            extra_item_sprite.remove_from_sprite_lists()
            if self.window.sound == 0:
                arcade.play_sound(self.extrai_sound)
            if str(extra_item_sprite.properties['Ext']) == "heart":
                self.mocshield += 1
            elif str(extra_item_sprite.properties['Ext']) == "key":
                self.key +=1
            elif str(extra_item_sprite.properties['Ext']) == "diamond":
                self.diamond +=1
            elif str(extra_item_sprite.properties['Ext']) == "gun1":
                self.gun1 += 1
            elif str(extra_item_sprite.properties['Ext']) == "gun2":
                self.gun2 += 1
            self.window.score +=1
        self.physics_engine.add_collision_handler("bullet", "extra_item", post_handler=extra_item_hit_handler2)

        def coins_hit_handler2(bullet_enemy_sprite, coins_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet_enemy", "coins", post_handler=coins_hit_handler2)

        def extra_item_hit_handler(bullet_enemy_sprite, extra_item_sprite, _arbiter, _space, _data):
            bullet_enemy_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet_enemy", "extra_item", post_handler=extra_item_hit_handler)

        #definicje startowe postaci i przedmiotów
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.nowy_golem()
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            elasticity=0.5,
                                            collision_type="item")

        self.physics_engine.add_sprite_list(self.extra_item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="extra_item")

        self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
                                            friction=WALL_FRICTION,
                                            collision_type="wall")

        self.physics_engine.add_sprite_list(self.xenemy_sprites_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="xenemy")

        self.physics_engine.add_sprite_list(self.coins_list,
                                            elasticity=0.5,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="coins")
        self.zaczyt_punktow()

    def nowy_golem (self):
        #ustawienie golema
        self.golem = Golem(hit_box_algorithm="Detailed")
        self.golem.center_x = 50+ + int(random.randrange(self.end_of_map))
        while  self.golem.center_x < self.view_left or self.golem.center_x > self.view_left + SCREEN_WIDTH:
            self.golem.center_x = 50 + int(random.randrange(self.end_of_map))
        self.golem.center_y = self.end_of_map_y + 100
        self.golem_list.append(self.golem)
        self.physics_engine.add_sprite(self.golem,
                                       friction=0,
                                       mass=PLAYER_MASS*2,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="golem",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

    def zaczyt_punktow (self):
        #ile punktów ma obcy
        for xenemy_sprite in self.xenemy_sprites_list:
            points = int(xenemy_sprite.properties['Points'])
            xenemy_sprite.zycie = points

    def on_joybutton_press(self, _joystick, button):
        #sterowanie joystickiem
        if button ==6:
            if self.gun1 > 0 and self.czas_gun == 0:
                self.czas_gun = 1000
                self.gun1 -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 1
                self.strzal(self.gun_active)
        elif button ==4:
            if self.gun2 > 0 and self.czas_gun == 0:
                self.czas_gun = 1000
                self.gun2 -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 2
                self.strzal(self.gun_active)
        elif button ==0:
            if self.diamond > 0:
                self.diamond -= 1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.diamond_czas = 500
        elif button == 1:
            self.strzal(self.gun_active)

    def on_joybutton_release(self, _joystick, button):
        self.button = 10


    def skok (self):
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
        #sterowanie
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
            if self.gun1>0 and self.czas_gun == 0 :
                self.czas_gun = 1000
                self.gun1 -=1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 1
                self.strzal(self.gun_active)
        elif key == arcade.key.Z:
            if self.diamond>0:
                self.diamond -=1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.diamond_czas = 500
        elif key == arcade.key.KEY_2:
            if self.gun2>0 and self.czas_gun == 0:
                self.czas_gun = 1000
                self.gun2 -=1
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.upgrade_sound)
                self.gun_active = 2
                self.strzal(self.gun_active)
        elif key == arcade.key.S:
            if self.window.sound== 0:
                self.window.sound = 1
            else:
                self.window.sound = 0
        elif key == arcade.key.M:
            if self.window.music == 0:
                self.window.music = 1
                self.window.musicp.stop()
            else:
                self.window.music = 0
                self.window.musicp.play(MUSIC_VOLUME)
        elif key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def upadek_bomb (self, x, y):
        #wystrzał bobmy przez obcego
        self.bomb = Bomb(hit_box_algorithm="Detailed")
        self.bomb.texture = self.bomb.bomb_textures[0]
        self.bomb.hit_box = self.bomb.texture.hit_box_points
        self.bomb.center_x = x + int(random.randrange(50))
        self.bomb.center_y = y + int(random.randrange(50))
        self.bomb.angle = int(random.randrange(180))
        self.bomb_list.append(self.bomb)
        self.bomb.scale = 1
        self.bomb.czaswybuchu = 150 + int(random.randrange(200))
        bomb_gravity = (-BULLET_GRAVITY/2, -BULLET_GRAVITY*8)
        self.physics_engine.add_sprite(self.bomb,
                                       mass=BULLET_MASS * 4,
                                       damping=0.5,
                                       friction=0.7,
                                       collision_type="bomb",
                                       gravity=bomb_gravity,
                                       elasticity=0.9)
        force_bomb = (BULLET_ENEMY_FORCE*3 , 0)
        self.physics_engine.apply_force(self.bomb, force_bomb)

    def strzal(self, gun):
        #strzał playera
        self.rodzaj = gun
        for strzal in range(self.rodzaj*3+1):
            if self.rodzaj == 0:
                bullet = BulletSprite("pymunk/images/ok/fireball.png", SPRITE_SCALING_LASER)
            elif self.rodzaj == 1:
                bullet = BulletSprite("pymunk/images/ok/tarcza_mala.png", SPRITE_SCALING_LASER)
            elif self.rodzaj == 2:
                bullet = BulletSprite("pymunk/images/ok/star_mala.png", SPRITE_SCALING_LASER)
            self.bullet_list.append(bullet)
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.position = self.player_sprite.position
            zmkata = 0
            if strzal>1:
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
        #strzał obcego
        if random.randrange(2) == 0:
            bullet_enemy = Bullet_Enemy("pymunk/images/ok/laserBlue01.png", SPRITE_SCALING_LASER)
        else:
            bullet_enemy = Bullet_Enemy("pymunk/images/ok/laserRed01.png", SPRITE_SCALING_LASER)
        if random.randrange(20) == 0:
            self.bullet_enemy_list.append(bullet_enemy)
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
        if random.randrange(100) == 0:
            if x>self.view_left and x< self.view_left+SCREEN_WIDTH:
                self.upadek_bomb(x, y)

    def on_update(self, delta_time):
    #uaktualnieie danych gry
        #serowanie joystickiem
        if self.joystick:
            if self.joystick.y < - 0.01:
                self.up_pressed = True
                if self.joy_y == False:
                    self.joy_y = True
                    self.skok()
            elif self.joystick.y > 0.01:
                self.down_pressed = True
            elif self.joystick.y <0.01 and self.joystick.y >-0.01:
                self.up_pressed = False
                self.down_pressed = False
                self.joy_y = False
            if self.joystick.x < -0.007:
                self.left_pressed = True
            elif self.joystick.x > 0.01:
                self.right_pressed = True
            elif self.joystick.x <0.01 and self.joystick.x >-0.01:
                self.left_pressed = False
                self.right_pressed = False
        #animacje rzeczy i obcych
        self.coins_list.update_animation(delta_time)
        self.xenemy_sprites_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.extra_item_list.update_animation(delta_time)
        self.explosions_list.update()
        self.shield.follow_sprite(self.player_sprite)
        self.shield_list.update()
        self.golem_list.update()
        changed_viewport = False
        #czy można zrobić 2 skok
        if self.player_sprite.czydrugiskok:
            self.odliczamdo_drugiego += 1
        if self.player_sprite.center_y >self.end_of_map_y+150:
            self.player_sprite.center_y = self.end_of_map_y+150
            impulse = (0, 0)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)
        #czy jesteśmy poza mapą
        if self.player_sprite.right > self.end_of_map:
            if self.key<3:
                self.game_over()
            else:
                if self.level < self.max_level:
                    self.level += 1
                    arcade.pause(1)
                    self.view_bottom = 0
                    self.view_left = 0
                    arcade.set_viewport(self.view_left,
                                        SCREEN_WIDTH + self.view_left,
                                        self.view_bottom,
                                        SCREEN_HEIGHT + self.view_bottom)
                    self.setup()
                else:
                    arcade.pause(1)
                    self.game_over()
        if self.player_sprite.center_y < -100:
            self.shield.remove_from_sprite_lists()
            if self.window.sound == 0 and self.koniec == 0:
                arcade.play_sound(self.strata_zycia_sound)
            self.game_over()
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        if len (self.golem_list) ==0:
            self.nowy_golem()
        #inteligencja golema
        for golem in self.golem_list:
            if golem.character_face_direction == RIGHT_FACING:
                self.physics_engine.apply_force(golem, (1000,0))
            if golem.character_face_direction == LEFT_FACING:
                self.physics_engine.apply_force(golem, (-1000, 0))
            if golem.czasbezruchu >= 50 and golem.character_face_direction == RIGHT_FACING:
                self.physics_engine.apply_force(golem, (-5000, 1000))
                impulse = (0, PLAYER_JUMP_IMPULSE *1.5)
                self.physics_engine.apply_impulse(golem, impulse)
                golem.czasbezruchu = 0
            if golem.czasbezruchu >= 50 and golem.character_face_direction == LEFT_FACING:
                self.physics_engine.apply_force(golem, (5000, 1000))
                impulse = (0, PLAYER_JUMP_IMPULSE*1.5)
                self.physics_engine.apply_impulse(golem, impulse)
                golem.czasbezruchu = 0
            golem.czasbezruchu +=1
            if golem.slash ==0 and int(random.randrange(100))==0 and self.physics_engine.is_on_ground(golem):
                golem.cur_texture = 0
                golem.slash =1
                if self.window.sound == 0 and self.golem.center_x > self.view_left and self.golem.center_x < self.view_left + SCREEN_WIDTH:
                    arcade.sound.play_sound(self.golem_sound)
            if len(arcade.check_for_collision_with_list(golem, self.player_list)) > 0:
                if golem.pierwszeuderzenie ==0 and golem.slash ==1:
                    self.mocshield -= 1
                    golem.pierwszeuderzenie = 1
                    self.player_sprite.hit = True
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.tarcza_sound)
                    if self.mocshield==0:
                        self.shield.remove_from_sprite_lists()
                        if self.window.sound == 0 and self.koniec == 0:
                            arcade.sound.play_sound(self.strata_zycia_sound)
                        self.game_over()
            if golem.center_y < -100:
                golem.remove_from_sprite_lists()

        # sterowanie - co robi player
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
        #uaktualnienie fizyki
        self.physics_engine.step()

        # przesunięcie planszy w lewo
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        self.background.left = self.view_left - 10 - 0.0125*self.player_sprite.left
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            if self.view_left < -50:
                self.view_left = -50
            changed_viewport = True
        # przesunięcie planszy w prawo
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        self.background.left = self.view_left - 0.0125*self.player_sprite.left
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            if self.view_left > self.end_of_map-SCREEN_WIDTH +50:
                self.view_left=self.end_of_map-SCREEN_WIDTH +50
            changed_viewport = True
        # przesunięcie planszy w górę
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            if self.view_bottom > self.end_of_map_y - 2 * TOP_VIEWPORT_MARGIN:
                self.view_bottom = self.end_of_map_y - 2 * TOP_VIEWPORT_MARGIN
            changed_viewport = True
        # przesunięcie planszy w dół
        self.background.bottom = self.view_bottom - 10
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        #czy konieczność przesunięcia
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            if self.view_bottom < -50:
                self.view_bottom = -50
            changed_viewport = True
        if changed_viewport:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            # przesunięcie planszy
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        #uaktualnienie ruchomych sprite-ów
        for moving_sprite in self.moving_sprites_list:
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

        # ruchy obcych
        for xenemy_sprite in self.xenemy_sprites_list:
            x = xenemy_sprite.center_x
            y = xenemy_sprite.center_y
            if int(xenemy_sprite.properties['Points']) <100:
                self.strzal_enemy(x,y)
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
            #czy obcy dostał
            if len(arcade.check_for_collision_with_list(xenemy_sprite, self.bullet_list)) > 0:
                hit_list = arcade.check_for_collision_with_list(xenemy_sprite, self.bullet_list)
                for bullet in hit_list:
                    bullet.remove_from_sprite_lists()
                xenemy_sprite.zycie -=1
                predkosc = int(random.randrange(4))+1
                xenemy_sprite.change_y *= - predkosc/2
                if xenemy_sprite.change_y >6:
                    xenemy_sprite.change_y = 6
                if xenemy_sprite.change_y < -6:
                    xenemy_sprite.change_y = -6
                xenemy_sprite.change_x *= - predkosc/2
                if xenemy_sprite.change_x >6:
                    xenemy_sprite.change_x = 6
                if xenemy_sprite.change_x < -6:
                    xenemy_sprite.change_x = -6
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.xenemy_hurt_sound)
                if xenemy_sprite.zycie ==0:
                    points = int(xenemy_sprite.properties['Points'])
                    self.window.score += points
                    xenemy_sprite.remove_from_sprite_lists()
                    # Make an explosion
                    self.explosion.center_x = hit_list[0].center_x
                    self.explosion.center_y = hit_list[0].center_y
                    self.explosion.update()
                    # Add to a list of sprites that are explosions
                    self.explosions_list.append(self.explosion)
                    if self.window.sound == 0:
                        arcade.sound.play_sound(self.hit_sound)
        #kolizje sprite-ów cd
        for bomb in self.bomb_list:
            if len(arcade.check_for_collision_with_list(bomb, self.player_list)) > 0:
                self.mocshield -= 1
                self.player_sprite.hit = True
                bomb.czywybuch = 0
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.tarcza_sound)
                bomb.remove_from_sprite_lists()
                hit_list = arcade.check_for_collision_with_list(bomb, self.player_list)
                self.explosion.center_x = hit_list[0].center_x
                self.explosion.center_y = hit_list[0].center_y
                self.explosion.update()
                self.explosions_list.append(self.explosion)
                if self.mocshield==0:
                    self.shield.remove_from_sprite_lists()
                    if self.window.sound == 0 and self.koniec == 0:
                        arcade.sound.play_sound(self.strata_zycia_sound)
                    self.game_over()
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            if self.diamond_czas ==0:
                if self.window.sound== 0 and self.koniec == 0:
                    arcade.sound.play_sound(self.strata_zycia_sound)
                self.game_over()
            arcade.pause(0.02)
        for coin in self.coins_list:
            if len(arcade.check_for_collision_with_list(coin, self.player_list)) > 0:
                coin.remove_from_sprite_lists()
                points = int(coin.properties['Points'])
                self.window.score += points
                if self.window.sound == 0:
                    arcade.play_sound(self.coin_sound)
        for extra in self.extra_item_list:
            if len(arcade.check_for_collision_with_list(extra, self.player_list)) > 0:
                extra.remove_from_sprite_lists()
                if self.window.sound == 0:
                    arcade.play_sound(self.extrai_sound)
                if str(extra.properties['Ext']) == "heart":
                    self.mocshield += 1
                elif str(extra.properties['Ext']) == "key":
                    self.key += 1
                elif str(extra.properties['Ext']) == "diamond":
                    self.diamond += 1
                elif str(extra.properties['Ext']) == "gun1":
                    self.gun1 += 1
                elif str(extra.properties['Ext']) == "gun2":
                    self.gun2 += 1
                self.window.score += 1
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.xenemy_sprites_list):
            self.shield.remove_from_sprite_lists()
            if self.window.sound == 0 and self.koniec == 0:
                arcade.sound.play_sound(self.strata_zycia_sound)
            self.game_over()

        for bullet_enemy in self.bullet_enemy_list:
            if len(arcade.check_for_collision_with_list(bullet_enemy, self.player_list)) > 0:
                self.mocshield -= 1
                self.player_sprite.hit = True
                bullet_enemy.remove_from_sprite_lists()
                if self.window.sound == 0:
                    arcade.sound.play_sound(self.tarcza_sound)
                if self.mocshield==0:
                    self.shield.remove_from_sprite_lists()
                    if self.window.sound == 0 and self.koniec == 0:
                        arcade.sound.play_sound(self.strata_zycia_sound)
                    self.game_over()
            if len(arcade.check_for_collision_with_list(bullet_enemy, self.golem_list)) > 0:
                bullet_enemy.remove_from_sprite_lists()
        #aktualizacja pozostałych danych
        if self.koniec == 1:
            self.player_sprite.dead == 1
        if self.czas_gun >0:
            self.czas_gun -=1
            if self.czas_gun ==0:
                self.gun_active = 0
        if self.diamond_czas >0:
            self.diamond_czas -=1

    def on_draw(self):
        #Rysowanie wszystkiego
        arcade.start_render()
        self.background.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.moving_sprites_list.draw()
        self.bullet_list.draw()
        self.bullet_enemy_list.draw()
        self.extra_item_list.draw()
        self.golem_list.draw()
        self.player_list.draw()
        self.shield_list.draw()
        self.coins_list.draw ()
        self.item_list.draw()
        self.dont_touch_list.draw()
        self.xenemy_sprites_list.draw()
        self.bomb_list.draw()
        self.explosions_list.draw()
        self.background_list.draw ()
        self.wynik()

    def wynik(self):
        #wyświetlenie wyniku po game over
        if self.koniec == 1:
            self.zliczdead += 1
            if self.ilosczyc > 1:
                if self.ilosczyc > 2:
                    ko = 'a'
                else:
                    ko = 'e'
                score_text = "Jeszcze raz - masz jeszcze " + str(self.ilosczyc - 1) + " życi" + str(ko)
                przes = -300
                arcade.draw_text(score_text, SCREEN_WIDTH/2 + self.view_left, 2*SCREEN_HEIGHT/3 + self.view_bottom,
                                 arcade.csscolor.RED, 48,anchor_x="center",  font_name='comic')

                score_text1 = "twój wynik - "
                arcade.draw_text(score_text1 + str(self.window.score), SCREEN_WIDTH/2+ self.view_left, SCREEN_HEIGHT/2 + self.view_bottom,
                                 arcade.csscolor.RED, 64, anchor_x="center",font_name='comic')

            if self.zliczdead >= 100:
                arcade.pause(1)
                self.ilosczyc -= 1
                self.view_bottom = 0
                self.view_left = 0
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)
                if self.ilosczyc == 0:
                    self.wyw_gameover()
                self.setup()
        #aktualizacja informacji i punktów
        else:
            arcade.draw_rectangle_filled(10 + self.view_left, 0 + self.view_bottom, 1500, 100,
                                         arcade.csscolor.WHITE)
            if self.gun_active ==2:
                if self.czas_gun > 150:
                    arcade.draw_rectangle_filled(715 + self.view_left, 0 + self.view_bottom, 100, 100,arcade.csscolor.RED)
                else:
                    arcade.draw_rectangle_filled(715 + self.view_left, 0 + self.view_bottom, 100, 100,
                                                 arcade.csscolor.SLATE_GREY)
            if self.gun_active ==1:
                if self.czas_gun>150:
                    arcade.draw_rectangle_filled(625 + self.view_left, 0 + self.view_bottom, 79, 100,
                                             arcade.csscolor.PALE_VIOLET_RED)
                else:
                    arcade.draw_rectangle_filled(625 + self.view_left, 0 + self.view_bottom, 79, 100,
                                             arcade.csscolor.SLATE_GRAY)
            if self.diamond_czas >= 150:
                arcade.draw_rectangle_filled(515 + self.view_left, 0 + self.view_bottom, 79, 100,
                                             arcade.csscolor.MEDIUM_PURPLE)
            if self.diamond_czas <150 and self.diamond_czas >0 :
                arcade.draw_rectangle_filled(515 + self.view_left, 0 + self.view_bottom, 79, 100,
                                             arcade.csscolor.DARK_GREY)
            if self.key >=3:
                arcade.draw_rectangle_filled(415 + self.view_left, 0 + self.view_bottom, 79, 100,
                                             arcade.csscolor.ORANGE_RED)

            score_text = f"Score: {self.window.score}" + "    Moc:" + str(self.mocshield) + "   Live:" + str(self.ilosczyc)
            arcade.draw_text(score_text, 10 + self.view_left, 20 + self.view_bottom+10 ,
                             arcade.csscolor.BLACK, 16, font_name='comic')

            arcade.draw_scaled_texture_rectangle(400 + self.view_left, 40 + self.view_bottom, self.scr2, scale=0.5)
            arcade.draw_text(str(self.key), 425 + self.view_left, 30 + self.view_bottom,
                             arcade.csscolor.BLACK, 16, font_name='comic')

            arcade.draw_scaled_texture_rectangle(500 + self.view_left,40 + self.view_bottom, self.scr1, scale = 0.5)
            arcade.draw_text(str(self.diamond), 525 + self.view_left, 30 + self.view_bottom,
                             arcade.csscolor.BLACK, 16, font_name='comic')

            arcade.draw_scaled_texture_rectangle(600 + self.view_left, 40 + self.view_bottom, self.scr4, scale=0.25)
            arcade.draw_text(str(self.gun1), 620 + self.view_left, 30 + self.view_bottom,
                             arcade.csscolor.BLACK, 16, font_name='comic')

            arcade.draw_scaled_texture_rectangle(700 + self.view_left, 30 + self.view_bottom, self.scr3, scale=0.5)
            arcade.draw_text(str(self.gun2), 740 + self.view_left, 30 + self.view_bottom,
                             arcade.csscolor.BLACK, 16, font_name='comic')

    def game_over(self):
        #koniec życia
        if self.koniec == 0:
            self.koniec = 1
        if self.koniec == 1:
            self.player_sprite.dead = 1

    def wyw_gameover(self):
        #wywołanie końca gry - przegrana
        self.window.musicp.stop()
        arcade.cleanup_texture_cache()
        game_over_view = GameOverView()
        self.window.show_view(game_over_view)

def main():
    #głowna metoda
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen= full)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()