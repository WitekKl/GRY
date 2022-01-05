import math
import random
from typing import Optional
import arcade

SCREEN_TITLE = "PAC MAN"
# wykorzystano:
# Paul Vincent Craven.
# https://arcade.academy/index.html
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# https://www.shadertoy.com/
# muzyka jest dostępna na licencji Creative Commons

SPRITE_IMAGE_SIZE = 128
global path, full
MOVEMENT_SPEED = 8
MUSIC_VOLUME = 0.1
path = "images/"
full = False

PLAYER_START_X = 1
PLAYER_START_Y = 1

#definicja stałych
width, height = arcade.get_display_size()
przelicz = 64
SPRITE_SCALING_PLAYER = przelicz/128
SPRITE_SCALING_TILES = przelicz/128
SPRITE_SIZE_MAP = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_TILES)
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
ASPECT=SCREEN_HEIGHT / SCREEN_WIDTH
#LEFT_VIEWPORT_MARGIN = 300
#RIGHT_VIEWPORT_MARGIN = 300
#BOTTOM_VIEWPORT_MARGIN = 200
#TOP_VIEWPORT_MARGIN = 200
DEAD_ZONE = 0.1
RIGHT_FACING = 1
LEFT_FACING = 0
UP_FACING=0
DOWN_FACING=0
DISTANCE_TO_CHANGE_TEXTURE = 8
GRAVITY = 0
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
        self.dead_textures = []
        for i in range (6):
            texture = arcade.load_texture_pair(f"{main_path}/Walk/Dead_{i}.png", hit_box_algorithm=hit_box_algorithm)
            self.dead_textures.append(texture)
        self.idle_textures = []
        for i in range(11):
            texture = arcade.load_texture_pair(f"{main_path}/idle/Idle_{i}.png",hit_box_algorithm=hit_box_algorithm)
            self.idle_textures.append(texture)
        self.walk_textures = []
        for i in range(20):
            texture = arcade.load_texture_pair(f"{main_path}/walk/walk_{i}.png")
            self.walk_textures.append(texture)
        self.character_face_direction = LEFT_FACING
        self.texture = self.walk_textures[0][RIGHT_FACING]
        self.hit_box = self.texture.hit_box_points
        self.texture = self.idle_textures[0][RIGHT_FACING]
        self.cur_texture = 0
        self.x_odometer = 0
        self.y_odometer = 0
        self.dx = 0
        self.dy = 0
        self.dead = False
        self.pocz_dead = True
        self.opoznienie_dead = 0

    def update(self,delta_time: float = 1 / 60):
        if self.change_x < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        if self.dead:
            if self.pocz_dead:
                self.cur_texture = 0
            self.texture = self.dead_textures[self.cur_texture][self.character_face_direction]
            self.pocz_dead =False
            self.opoznienie_dead +=1
            if self.opoznienie_dead ==5:
                self.cur_texture += 1
                self.opoznienie_dead = 0
                if self.cur_texture > 5:
                    self.cur_texture = 0
                    self.dead = False
                    self.pocz_dead = True
                    self.texture = self.idle_textures[0][self.character_face_direction]

            return

        self.x_odometer += self.change_x
        self.y_odometer += self.change_y
        self.dy = self.change_y
        self.dx = self.change_x
        if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.y_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 19:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(self.dx) <= DEAD_ZONE and abs(self.dy)<=DEAD_ZONE:
            self.cur_texture += 1
            if self.cur_texture > 10:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]
            return
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 19:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class Dodatki(arcade.Sprite):
    #wyświetlenie punktów - animacja
    def __init__(self, hit_box_algorithm):
        super().__init__()

        self.szybkosc=0
        self.czas=0
        self.co = 0
        self.scale = SPRITE_SCALING_TILES
        self.frozen_textures = []
        for i in range(4):
            texture = arcade.load_texture("images/frozen_"+ str(i) + ".png")
            self.frozen_textures.append(texture)
        self.speed_textures = []
        for i in range(4):
            texture = arcade.load_texture("images/speed_"+ str(i) + ".png")
            self.speed_textures.append(texture)
        self.heart_textures = []
        for i in range(4):
            texture = arcade.load_texture("images/heart_"+ str(i) + ".png")
            self.heart_textures.append(texture)
        self.shield_textures = []
        for i in range(4):
            texture = arcade.load_texture("images/shield_"+ str(i) + ".png")
            self.shield_textures.append(texture)

        self.cur_texture = 0
        self.texture = self.frozen_textures [self.cur_texture]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        self.szybkosc+= 1
        if self.co==1:
            if self.szybkosc ==5:
                self.texture = self.frozen_textures[self.cur_texture]
                self.cur_texture += 1
                self.czas += 1
                if self.cur_texture < len(self.frozen_textures):
                    self.szybkosc =0
                else:
                    self.cur_texture = 0
                    self.szybkosc = 0
        elif self.co==2:
            if self.szybkosc ==5:
                self.texture = self.speed_textures[self.cur_texture]
                self.cur_texture += 1
                self.czas += 1
                if self.cur_texture < len(self.speed_textures):
                    self.szybkosc =0
                else:
                    self.cur_texture = 0
                    self.szybkosc = 0
        elif self.co==3:
            if self.szybkosc ==5:
                self.texture = self.heart_textures[self.cur_texture]
                self.cur_texture += 1
                self.czas+=1
                if self.cur_texture < len(self.heart_textures):
                    self.szybkosc =0
                else:
                    self.cur_texture = 0
                    self.szybkosc = 0
        elif self.co==4:
            if self.szybkosc ==5:
                self.texture = self.shield_textures[self.cur_texture]
                self.cur_texture += 1
                self.czas += 1
                if self.cur_texture < len(self.shield_textures):
                    self.szybkosc =0
                else:
                    self.cur_texture = 0
                    self.szybkosc = 0
        if self.czas ==100:
            self.remove_from_sprite_lists()

class Shield(arcade.Sprite):
    #tarcza
    def __init__(self, hit_box_algorithm):
        super().__init__()

        self.ochron = []
        for i in range(4):
            texture = arcade.load_texture("images/shield" + str(i) + ".png")
            self.ochron.append(texture)
        self.scale = SPRITE_SCALING_TILES*0.75
        self.shieldon = 0
        self.szybkosc = 0
        self.cur_texture = 0
        self.texture = self.ochron[self.cur_texture]
        self.hit_box = self.texture.hit_box_points
        self.use_spatial_hash = True
    def update(self):
        self.szybkosc += 1
        if self.szybkosc >=5:
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
        self.tile_map = None
        self.scene = None
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.background = None
        self.max_level = 6
        self.krok=przelicz
        self.czyruch=False
        self.koniecpoziomu = False
        self.dodatki_czas=0
        self.czas_ruch=0
        self.strata_zycia_czas=0
        self.time=False

        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.level=1
        self.przenosiny = False
        self.shield_active= False
        self.shield1=0
        self.gameover = False
        self.przes_x=0
        self.setup()

    def setup(self):
        #definicja zmiennych
        self.camera = arcade.Camera(width, height)
        self.gui_camera = arcade.Camera(width, height)
        self.life=3

        # Odczyt map
        map_name = "pac_"+str(self.level) + ".json"

        self.my_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
        layer_options = {
            "wall": {
                "use_spatial_hash": True,
            },
            "enemy": {
                "use_spatial_hash": False,
            },
            "out": {
                "use_spatial_hash": True,
            }
        }


        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.background = arcade.load_texture("images/tlo_4.jpg")

        # Definicja pacman
        self.player_sprite = PlayerSprite( hit_box_algorithm="Simple")

        self.player_sprite.center_x = int(
            self.tile_map.tile_width * SPRITE_SCALING_PLAYER * PLAYER_START_X*1.5)
        self.player_sprite.center_y = int(
            self.tile_map.tile_height * SPRITE_SCALING_PLAYER * PLAYER_START_Y*1.5)

        self.scene.add_sprite("Player", self.player_sprite)

        #dodatki
        self.dodatki = Dodatki(hit_box_algorithm="Simple")
        self.scene.add_sprite("dodatki", self.dodatki)
        self.dodatki.remove_from_sprite_lists()

        #tarcza
        self.shield = Shield(hit_box_algorithm="Simple")
        self.scene.add_sprite("shield", self.shield)
        self.shield.remove_from_sprite_lists()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, [self.scene.name_mapping["wall"], self.scene.name_mapping["moving"]],GRAVITY
        )

        for element in self.scene.name_mapping["moving"]:
            if  "time" in element.properties:
                element.time = int(element.properties["time"])
            if  "move_x" in element.properties:
                element.move_x = int(element.properties["move_x"])
            if  "move_y" in element.properties:
                element.move_y = int(element.properties["move_y"])
        for enemy in self.scene.name_mapping["enemy"] :
            if abs(enemy.change_x)>0:
                enemy.predkosc=abs(enemy.change_x)
            else:
                enemy.predkosc=abs(enemy.change_y)
        for element in self.scene.name_mapping["out"]:
            if  "time" in element.properties:
                element.time = int(element.properties["time"])
                self.time=True
                self.time_odlicz=element.time
        self.live_sound = arcade.sound.load_sound("sound/live.wav")
        self.game_over_sound= arcade.sound.load_sound("sound/gameover.wav")
        self.eat_sound = arcade.sound.load_sound("sound/s_eat.wav")
        self.eat2_sound = arcade.load_sound("sound/s_eat2.wav")
        self.upgrade_sound = arcade.load_sound("sound/upgrade.wav")
        self.poj_upgrade_sound = arcade.load_sound("sound/secret2.wav")
        self.level_sound = arcade.load_sound("sound/level.wav")
        self.wolne_enemy= arcade.load_sound("sound/fall3.wav")
        self.pre_level_sound = arcade.load_sound("sound/wszystko.wav")

        self.tlo_sound = arcade.load_sound("sound/tlo.mp3")
        self.window.media_player =self.tlo_sound.play(MUSIC_VOLUME)

    def uzyjshield(self):
        #włączenie tarczy
        self.shield = Shield(hit_box_algorithm="Simple")
        self.shield.center_x = self.player_sprite.center_x
        self.shield.center_y = self.player_sprite.center_y
        self.shield.update()
        self.scene.add_sprite("shield", self.shield)
        self.shield_active = 1

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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_draw(self):
        arcade.start_render()
        arcade.load_font(font_name="ARCADECLASSIC.TTF")
        # Activate the game camera
        self.camera.use()

        arcade.draw_lrwh_rectangle_textured(self.screen_center_x-przelicz, self.screen_center_y-przelicz,
                                            SCREEN_WIDTH+przelicz*4, SCREEN_HEIGHT+przelicz*4,
                                            self.background)

        # Draw our Scene
        self.scene.draw()

        self.gui_camera.use()
        arcade.draw_rectangle_filled(SCREEN_WIDTH*0.8,SCREEN_HEIGHT, 550, 120,
                                     arcade.csscolor.WHITE)
        score_text = "Score:" + str(self.score) + "  Life:" + str(self.life) + "  Ile zjesc:" + str(len(self.scene.name_mapping["eat"]))+ "  Level: " + str(self.level)
        arcade.draw_text(
            score_text,
            SCREEN_WIDTH*0.61,
            SCREEN_HEIGHT-50,
            arcade.csscolor.FIREBRICK,
            18,font_name='ARCADECLASSIC')


        if self.koniecpoziomu:
            text = "KONIEC POZIOMU"
            arcade.draw_text(
                text,
                SCREEN_WIDTH * 0.5,
                SCREEN_HEIGHT * 0.5,
                arcade.csscolor.WHITE,
                50, anchor_x='center', font_name='ARCADECLASSIC')
        if self.gameover:
            text = "GAME OVER"
            arcade.draw_text(
                text,
                SCREEN_WIDTH * 0.5,
                SCREEN_HEIGHT * 0.5,
                arcade.csscolor.WHITE,
                50, anchor_x='center', font_name='ARCADECLASSIC')

    def center_camera_to_player(self, panning_fraction: float = 0.7):
        self.screen_center_x = self.player_sprite.center_x -width/8 - (self.camera.viewport_width / 2)
        self.screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if self.screen_center_x < -width/8:
            self.screen_center_x = -width/8
        if self.screen_center_y < 0:
            self.screen_center_y = 0
        player_centered = self.screen_center_x, self.screen_center_y

        self.camera.move_to(player_centered, panning_fraction)

    def postaw_dodatek(self, co):
        if co ==0 or co>4:
            self.dodatki_czas = 0
            return
        self.dodatki = Dodatki(hit_box_algorithm="Simple")
        self.dodatki.co=co
        if co ==1:
            self.dodatki.texture=self.dodatki.frozen_textures[0]
        elif co ==2:
            self.dodatki.texture = self.dodatki.speed_textures[0]
        elif co ==3:
            self.dodatki.texture = self.dodatki.heart_textures[0]
        elif co ==4:
            self.dodatki.texture = self.dodatki.shield_textures[0]

        self.dodatki.center_x=int(random.randrange(self.tile_map.width)*przelicz+przelicz/2)
        self.dodatki.center_y=int(random.randrange(self.tile_map.height)*przelicz+przelicz/2)
        self.scene.add_sprite("dodatki", self.dodatki)
        for dodatek in self.scene.name_mapping["dodatki"]:
            if len(arcade.check_for_collision_with_list (dodatek, self.scene.name_mapping["wall"]))>0:
                dodatek.remove_from_sprite_lists()
            else:
                self.dodatki_czas = 0
                arcade.sound.play_sound(self.poj_upgrade_sound)

    def zmien_predkosc (self, ruch):
        for element in self.scene.name_mapping["enemy"]:
            if element.change_x>0:
                element.change_x = element.predkosc + ruch
            elif element.change_x<0:
                element.change_x = -element.predkosc - ruch
            elif element.change_y>0:
                element.change_y = element.predkosc + ruch
            elif element.change_y<0:
                element.change_y = -element.predkosc - ruch

    def game_over(self ):
        arcade.sound.play_sound(self.game_over_sound)
        self.gameover = True
        self.czas_gameover = 250

    def on_update(self, delta_time: float = 1 / 60):
        if self.gameover:
            self.czas_gameover-=1
            if self.czas_gameover==0:
                self.gameover = False
                self.score = 0
                arcade.cleanup_texture_cache()
                self.setup()
            return
        if self.koniecpoziomu:
            self.czas_koniecpoziomu-=1
            if self.czas_koniecpoziomu==0:
                self.koniecpoziomu = False
                if self.max_level==self.level:
                    arcade.cleanup_texture_cache()
                    self.setup()
                else:
                    self.level+=1
                    arcade.cleanup_texture_cache()
                    self.setup()
        self.dodatki_czas+=1
        if self.time:
            self.time_odlicz-=1
            if self.time_odlicz==0:
                self.time = False
                for element in self.scene.name_mapping["out"]:
                    if "time" in element.properties:
                        element.remove_from_sprite_lists ()
                        arcade.play_sound(self.wolne_enemy)
        if self.czas_ruch>0:
            self.czas_ruch-=1
            if self.czas_ruch==0:
                self.zmien_predkosc(0)

        if self.strata_zycia_czas > 0:
            self.strata_zycia_czas-=1

        if self.dodatki_czas>=250:
            co=random.randrange(5)
            self.postaw_dodatek(co)

        self.physics_engine.update()
        self.player_sprite.update()
        self.scene.update(["enemy", "dodatki"])
        if self.shield1>0:
            self.scene.update(["shield"])
            self.shield.follow_sprite(self.player_sprite)

        zmien = False
        self.player_sprite.center_x = int(self.player_sprite.center_x)
        self.player_sprite.center_y = int(self.player_sprite.center_y)
        if self.czyruch:
            self.krok-=DISTANCE_TO_CHANGE_TEXTURE
            if self.krok ==0:
                self.czyruch= False
                self.krok=przelicz
                self.przes_x = int(self.player_sprite.center_x - przelicz/2) % przelicz
                self.przes_y = int(self.player_sprite.center_y - przelicz/2) % przelicz
                if self.przes_x != 0:
                    if self.przes_x > przelicz/2:
                        self.player_sprite.change_x = max(przelicz - self.przes_x, DISTANCE_TO_CHANGE_TEXTURE)
                    else:
                        self.player_sprite.change_x = -min(self.przes_x, DISTANCE_TO_CHANGE_TEXTURE)

                if self.przes_y != 0:
                    if self.przes_y > przelicz/2:
                        self.player_sprite.change_y = max(przelicz - self.przes_y, DISTANCE_TO_CHANGE_TEXTURE)
                    else:
                        self.player_sprite.change_y = -min(self.przes_y, DISTANCE_TO_CHANGE_TEXTURE)

        else:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

            if self.up_pressed and not self.down_pressed :
                self.player_sprite.change_y = MOVEMENT_SPEED
                self.krok -= DISTANCE_TO_CHANGE_TEXTURE
                self.player_sprite.kierunek=1
                self.czyruch=True
            elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_y = -MOVEMENT_SPEED
                self.krok -= DISTANCE_TO_CHANGE_TEXTURE
                self.player_sprite.kierunek=2
                self.czyruch = True
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -MOVEMENT_SPEED
                self.krok -= DISTANCE_TO_CHANGE_TEXTURE
                self.player_sprite.kierunek=3
                self.czyruch = True
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = MOVEMENT_SPEED
                self.krok -= DISTANCE_TO_CHANGE_TEXTURE
                self.player_sprite.kierunek=4
                self.czyruch = True

        for enemy in self.scene.name_mapping["enemy"] :
            if enemy.angle>0:
                enemy.angle+=5
                if enemy.angle==360:
                    enemy.angle=0
                    enemy.change_x = enemy.tym_x
                    enemy.change_y = enemy.tym_y
            else:

                if abs(enemy.change_x)>0:
                    predkosc=abs(enemy.change_x)
                else:
                    predkosc=abs(enemy.change_y)
                if len(arcade.check_for_collision_with_list (enemy, self.scene.name_mapping["zmiana"]))>0:
                    hit_list = arcade.check_for_collision_with_list(enemy, self.scene.name_mapping["zmiana"])
                    for zmiany in hit_list:
                        if abs(zmiany.center_x-enemy.center_x)<3 and abs(zmiany.center_y-enemy.center_y)<3:
                            x= int(random.randrange(4))
                            if x==0:
                                enemy.change_x=0
                                enemy.change_y= - predkosc
                                enemy.center_y-=predkosc
                                if len(arcade.check_for_collision_with_list(enemy, self.scene.name_mapping["wall"]))>0:
                                    x+=1
                                enemy.center_y+= predkosc
                            if x==1:
                                enemy.change_x=0
                                enemy.change_y=predkosc
                                enemy.center_y+= predkosc
                                if len(arcade.check_for_collision_with_list(enemy, self.scene.name_mapping["wall"]))>0:
                                    x+=1
                                enemy.center_y-=predkosc
                            if x==2:
                                enemy.change_x=predkosc
                                enemy.change_y=0
                                enemy.center_x +=predkosc
                                if len(arcade.check_for_collision_with_list(enemy, self.scene.name_mapping["wall"]))>0:
                                    x+=1
                                enemy.center_x -= predkosc
                            if x==3:
                                enemy.change_x=-predkosc
                                # odwrocenie ??
                                enemy.change_y=0
                                enemy.center_x -= predkosc
                                if len(arcade.check_for_collision_with_list(enemy, self.scene.name_mapping["wall"]))>0:
                                    enemy.change_x = 0
                                    enemy.change_y = - predkosc
                                enemy.center_x += predkosc

                            if abs(self.player_sprite.center_x-enemy.center_x)<3:
                                # sprawdzenie czy na tej samej pionowej ścieżce
                                if self.player_sprite.center_y>enemy.center_y:
                                    enemy.center_x=self.player_sprite.center_x
                                    enemy.change_y = predkosc
                                    enemy.change_x = 0
                                else:
                                    enemy.center_x = self.player_sprite.center_x
                                    enemy.change_y = -predkosc
                                    enemy.change_x = 0
                            if abs(self.player_sprite.center_y-enemy.center_y)<3:
                                # sprawdzenie czy na tej samej poziomej ścieżce
                                if self.player_sprite.center_x>enemy.center_x:
                                    enemy.center_y=self.player_sprite.center_y
                                    enemy.change_x = predkosc
                                    enemy.change_y = 0
                                else:
                                    enemy.center_y = self.player_sprite.center_y
                                    enemy.change_x = -predkosc
                                    enemy.change_y = 0
                            ###### środkowanie1
                            przes_x = int(enemy.center_x - przelicz / 2) % przelicz
                            przes_y = int(enemy.center_y - przelicz / 2) % przelicz
                            if przes_x != 0:
                                if przes_x > przelicz / 2:
                                    enemy.center_x += max(przelicz - przes_x, DISTANCE_TO_CHANGE_TEXTURE)
                                else:
                                    enemy.center_x -= min(przes_x, DISTANCE_TO_CHANGE_TEXTURE)
                            if przes_y != 0:
                                if przes_y > przelicz / 2:
                                    enemy.center_y += max(przelicz - przes_y, DISTANCE_TO_CHANGE_TEXTURE)
                                else:
                                    enemy.center_y -= min(przes_y, DISTANCE_TO_CHANGE_TEXTURE)
                if len(arcade.check_for_collision_with_list (enemy, self.scene.name_mapping["wall"]))>0:
                    ###### środkowanie
                    przes_x = int(enemy.center_x - przelicz / 2) % przelicz
                    przes_y = int(enemy.center_y - przelicz / 2) % przelicz
                    if przes_x != 0:
                        if przes_x > przelicz / 2:
                            enemy.center_x += max(przelicz - przes_x, DISTANCE_TO_CHANGE_TEXTURE)
                        else:
                            enemy.center_x -= min(przes_x, DISTANCE_TO_CHANGE_TEXTURE)
                    if przes_y != 0:
                        if przes_y > przelicz / 2:
                            enemy.center_y += max(przelicz - przes_y, DISTANCE_TO_CHANGE_TEXTURE)
                        else:
                            enemy.center_y -= min(przes_y, DISTANCE_TO_CHANGE_TEXTURE)
                    enemy.change_x = (-1)*enemy.change_x
                    enemy.change_y = (-1) * enemy.change_y
                    zmien = True
                if len(arcade.check_for_collision_with_list (enemy, self.scene.name_mapping["moving"]))>0:
                    enemy.change_x = (-1)*enemy.change_x
                    enemy.change_y = (-1) * enemy.change_y
                    zmien = True
                if len(arcade.check_for_collision_with_list (enemy, self.scene.name_mapping["shield"]))>0:
                    enemy.change_x = (-1)*enemy.change_x
                    enemy.change_y = (-1) * enemy.change_y
                    zmien = True
                if len(arcade.check_for_collision_with_list (enemy, self.scene.name_mapping["out"]))>0 and not zmien:
                    enemy.change_x = (-1)*enemy.change_x
                    enemy.change_y = (-1) * enemy.change_y

        if len(arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["eat"]))>0:
            hit_list = arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["eat"])
            for eata in hit_list:
                eata.remove_from_sprite_lists()
                arcade.sound.play_sound(self.eat_sound)
                self.score+=1
                if len(self.scene.name_mapping['eat']) ==0:
                    for element in self.scene.name_mapping["out"]:
                        if "blokada" in element.properties:
                            x=element.center_x
                            y=element.center_y
                            for usun in self.scene.name_mapping["wall"]:
                                if usun.center_x==x and usun.center_y==y:
                                    usun.remove_from_sprite_lists()
                                    arcade.sound.play_sound(self.pre_level_sound)
                                    #usunięcie ściany do wyjścia
        if len(arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["fruit"]))>0:
            hit_list = arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["fruit"])
            for fruity in hit_list:
                fruity.remove_from_sprite_lists()
                arcade.sound.play_sound(self.eat2_sound)
                self.score+=10
                self.dodatki_czas+=50
        if len(arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["exit"]))>0:
            hit_list = arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["exit"])
            for exity in hit_list:
                if self.player_sprite.center_x==exity.center_x and self.player_sprite.center_y==exity.center_y:
                    #koniec poziomu
                    if not self.koniecpoziomu:
                        arcade.sound.play_sound(self.level_sound)
                        self.koniecpoziomu=True
                        self.czas_koniecpoziomu = 100
        if len(arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["out"]))>0:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.name_mapping["out"])
            for element in hit_list:
                if abs(self.player_sprite.center_x-element.center_x)<4 and "move_x" in element.properties and not self.przenosiny:
                    alfa= int(element.properties["move_x"])
                    self.player_sprite.center_x+=alfa*przelicz
                    self.przenosiny = True
                if abs(self.player_sprite.center_y-element.center_y)<4 and "move_y" in element.properties and not self.przenosiny:
                    alfa= int(element.properties["move_y"])
                    self.player_sprite.center_y+=alfa*przelicz
                    self.przenosiny = True
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene.name_mapping["out"])) == 0:
            self.przenosiny = False
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene.name_mapping["dodatki"])) > 0:
            hit_list = arcade.check_for_collision_with_list (self.player_sprite, self.scene.name_mapping["dodatki"])
            for element in hit_list:
                element.remove_from_sprite_lists()
                arcade.sound.play_sound(self.upgrade_sound)
                self.score+=10
                self.dodatki_czas+=50
                if element.co == 1:
                    ruch=-2
                    self.zmien_predkosc(ruch)
                    self.czas_ruch=250
                elif element.co == 2:
                    ruch=2
                    self.zmien_predkosc(ruch)
                    self.czas_ruch = 250
                elif element.co == 3:
                    #extra life
                    self.life+=1
                elif element.co == 4:
                    #tarcza
                    self.shield1 += 1
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene.name_mapping["enemy"])) > 0:
            if self.strata_zycia_czas==0 and self.shield1==0:
                self.life -=1
                self.player_sprite.dead = True
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.name_mapping["enemy"])
                for enemy in hit_list:
                    if enemy.angle==0:
                        enemy.angle =5
                        enemy.tym_x= enemy.change_x
                        enemy.tym_y=enemy.change_y
                        enemy.change_x=0
                        enemy.change_y=0
                if self.life==0:
                    #koniec gry:
                    self.game_over()
                else:
                    self.strata_zycia_czas = 50
                    arcade.sound.play_sound(self.live_sound)

        if self.shield_active == 0 and self.shield1>0:
            self.uzyjshield()
        if self.shield_active > 0:
            self.shield_active += 1
            if self.shield_active >= 500:
                self.shield_active = 0
                self.shield1 -= 1
                self.shield.remove_from_sprite_lists()
        if self.player_sprite.right>self.tile_map.width*przelicz:
            self.player_sprite.right=self.tile_map.width*przelicz
            self.przenosiny = False
        if self.player_sprite.left<0:
            self.player_sprite.left=0
            self.przenosiny=False
        if self.player_sprite.top>self.tile_map.height*przelicz:
            self.player_sprite.top= self.tile_map.height * przelicz
            self.przenosiny = False
        if self.player_sprite.bottom<0:
            self.player_sprite.bottom=0
            self.przenosiny=False


        self.scene.update_animation (delta_time,["enemy", "fruit", "eat", "out"])
        #przesunięcia ring i ustawienie enemy
        for element in self.scene.name_mapping["moving"]:
            element.time -=1
            if element.time==0:
                if "move_x" in element.properties:
                    element.center_x+=element.move_x*przelicz
                    element.time = int(element.properties["time"])
                    element.move_x*=(-1)
                    if len(arcade.check_for_collision_with_list (element, self.scene.name_mapping["enemy"]))>0:
                        hitlist=arcade.check_for_collision_with_list (element, self.scene.name_mapping["enemy"])
                        for element1 in hitlist:
                            if element.move_x>0:
                                element1.center_x =element1.center_x+przelicz+2
                            else:
                                element1.center_x = element1.center_x - przelicz-2

                else:
                    element.center_y+=element.move_y*przelicz
                    element.time = int(element.properties["time"])
                    element.move_y*=(-1)
                    if len(arcade.check_for_collision_with_list (element, self.scene.name_mapping["enemy"]))>0:
                        hitlist=arcade.check_for_collision_with_list (element, self.scene.name_mapping["enemy"])
                        for element1 in hitlist:
                            if element.move_y > 0:
                                element1.center_y =element1.center_y+przelicz+2
                            else:
                                element1.center_y = element1.center_y -przelicz-2

        # Position the camera
        self.center_camera_to_player(panning_fraction=0.1)

def main():
    # Metoda główna
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT-32, SCREEN_TITLE, fullscreen= full)

    window.score = 0
    menu_view = GameView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()