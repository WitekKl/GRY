import arcade
import arcade.gui
import random
import os
import xlrd
from typing import Optional

# wykorzystano:
# https://arcade.academy/index.html
# https://www.kenney.nl/
# http://dig.ccmixter.org/
# muzyka jest dostępna na licencji Creative Commons

width, height = arcade.get_display_size()
stawka_y = height/11
stawka_x = stawka_y
gr_linii =2
start_x = 50
start_y = 4*stawka_y/5
PANEL1=0.65*width
przerwa =10
full = False
SCREEN_TITLE = "SUDOKU"
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
color_l = arcade.color.AERO_BLUE
color_gr=arcade.color.BLACK


class GameView(arcade.View):
    #główna część gry
    def __init__(self):
        super().__init__()
        self.poziom = 0
        self.ktory=0

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        arcade.load_font("comic.ttf")
        arcade.set_background_color(arcade.color.BLUE_YONDER)
        self.x = 0
        self.y=0
        self.kwadr_x=0
        self.kwadr_y=0
        self.ktr_x= 0
        self.ktr_y = 0
        self.czy_ustal_pole = False
        self.jakiznak = "Brak"
        self.czy_poj_znak = True
        self.stare_pole = [-1,-1]
        self.kolizja_sound = arcade.load_sound("sound/fall3.wav")
        self.wszystko_sound = arcade.load_sound("sound/level2.ogg")

        self.setup()

    def setup(self):

        self.tabela = []
        self.tabela_new = []
        self.tabela_cofnij = []
        for row in range(9):
            self.tabela.append([])
            for column in range(9):
                self.tabela[row].append('')
        for row in range(9):
            self.tabela_new.append([])
            for column in range(9):
                self.tabela_new[row].append('')
        for row in range(9):
            self.tabela_cofnij.append([])
            for column in range(9):
                self.tabela_cofnij[row].append('')
        self.tabela_pionpoziom =[]
        for element in range (18):
            self.tabela_pionpoziom.append('')



        red_style = {
            "font_name": ("calibri", "arial"),
            "font_size": int(stawka_y),
            "font_color": arcade.color.WHITE,
            "border_width": 3,
            "border_color": None,
            "bg_color": arcade.color.REDWOOD,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,  # also used when hovered
            "font_color_pressed": arcade.color.RED}


        blue_style = {
            "font_name": ("calibri", "arial"),
            "font_size": int(stawka_y/4),
            "font_color": arcade.color.WHITE_SMOKE,
            "border_width": 4,
            "border_color": None,
            "bg_color": arcade.color.RASPBERRY_ROSE,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,  # also used when hovered
            "font_color_pressed": arcade.color.BLUEBONNET}

        self.zaczyt_poz()

        self.button_1 = arcade.gui.UIFlatButton(text="1", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1, y = height-2*stawka_y-przerwa*2, style=red_style)
        self.manager.add(self.button_1)

        self.button_2 = arcade.gui.UIFlatButton(text="2", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+ stawka_x*1.5+ przerwa, y = height-2*stawka_y-przerwa*2, style=red_style)
        self.manager.add(self.button_2)

        self.button_3 = arcade.gui.UIFlatButton(text="3", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+ stawka_x*3 + przerwa*2 , y = height-2*stawka_y-przerwa*2, style=red_style)
        self.manager.add(self.button_3)

        self.button_4 = arcade.gui.UIFlatButton(text="4", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1, y = height-3.5*stawka_y-przerwa*3, style=red_style)
        self.manager.add(self.button_4)

        self.button_5 = arcade.gui.UIFlatButton(text="5", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+stawka_x*1.5+ przerwa, y = height-3.5*stawka_y-przerwa*3, style=red_style)
        self.manager.add(self.button_5)

        self.button_6 = arcade.gui.UIFlatButton(text="6", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+stawka_x*3+ przerwa*2, y = height-3.5*stawka_y-przerwa*3, style=red_style)
        self.manager.add(self.button_6)

        self.button_7 = arcade.gui.UIFlatButton(text="7", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1, y = height-5*stawka_y-przerwa*4, style=red_style)
        self.manager.add(self.button_7)

        self.button_8 = arcade.gui.UIFlatButton(text="8", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+stawka_x*1.5+ przerwa, y = height-5*stawka_y-przerwa*4, style=red_style)
        self.manager.add(self.button_8)

        self.button_9 = arcade.gui.UIFlatButton(text="9", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+ stawka_x*3 + przerwa*2, y = height-5*stawka_y-przerwa*4, style=red_style)
        self.manager.add(self.button_9)

        self.button_11 = arcade.gui.UIFlatButton(text="#", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1, y = height-6.5*stawka_y-przerwa*5, style=red_style)
        self.manager.add(self.button_11)

        #self.button_10 = arcade.gui.UIFlatButton(text="*", width=stawka_y*2, height = stawka_y*2, x= PANEL1+ stawka_x*2+ przerwa, y = height-8*stawka_y-przerwa*5, style=red_style)
        #self.manager.add(self.button_10)

        self.button_12 = arcade.gui.UIFlatButton(text="<", width=stawka_y*1.5, height = stawka_y*1.5, x= PANEL1+ stawka_x*3+ przerwa*2, y = height-6.5*stawka_y-przerwa*5, style=red_style)
        self.manager.add(self.button_12)

        #self.button_latwy
        #self.button_sredni
        #self.button_trudny
        self.button_latwy = arcade.gui.UIFlatButton(text="łatwy", width=stawka_y * 1.5, height=stawka_y * 1.5, x=PANEL1,
                                                 y=height - 8.5 * stawka_y - przerwa * 5, style=blue_style)
        self.manager.add(self.button_latwy)

        self.button_sredni = arcade.gui.UIFlatButton(text="średni", width=stawka_y * 1.5, height=stawka_y * 1.5, x= PANEL1+stawka_x*1.5+ przerwa,
                                                 y=height - 8.5 * stawka_y - przerwa * 5, style=blue_style)
        self.manager.add(self.button_sredni)

        self.button_trudny = arcade.gui.UIFlatButton(text="trudny", width=stawka_y * 1.5, height=stawka_y * 1.5, x= PANEL1+stawka_x*3+ przerwa*2,
                                                 y=height - 8.5 * stawka_y - przerwa * 5, style=blue_style)
        self.manager.add(self.button_trudny)

        @self.button_1.event("on_click")
        def on_click_button_1(event):
            self.jakiznak = 1
            self.wprowadz_znak()

        @self.button_2.event("on_click")
        def on_click_button_2(event):
            self.jakiznak = 2
            self.wprowadz_znak()

        @self.button_3.event("on_click")
        def on_click_button_3(event):
            self.jakiznak = 3
            self.wprowadz_znak ()

        @self.button_4.event("on_click")
        def on_click_button_4(event):
            self.jakiznak = 4
            self.wprowadz_znak()

        @self.button_5.event("on_click")
        def on_click_button_5(event):
            self.jakiznak = 5
            self.wprowadz_znak()

        @self.button_6.event("on_click")
        def on_click_button_6(event):
            self.jakiznak = 6
            self.wprowadz_znak()

        @self.button_7.event("on_click")
        def on_click_button_7(event):
            self.jakiznak = 7
            self.wprowadz_znak()

        @self.button_8.event("on_click")
        def on_click_button_8(event):
            self.jakiznak = 8
            self.wprowadz_znak()

        @self.button_9.event("on_click")
        def on_click_button_9(event):
            self.jakiznak = 9
            self.wprowadz_znak()

        @self.button_11.event("on_click")
        def on_click_button_11(event):
            if self.czy_poj_znak:
                self.jakiznak = 0
                self.wprowadz_znak()
                self.czy_poj_znak = False
            else:
                self.czy_poj_znak = True

        @self.button_12.event("on_click")
        def on_click_button_12(event):
            self.zamien_tabele()

        @self.button_latwy.event("on_click")
        def on_click_button_latwy(event):
            self.poziom=0
            self.setup()

        @self.button_sredni.event("on_click")
        def on_click_button_sredni(event):
            self.poziom=1
            self.setup()

        @self.button_trudny.event("on_click")
        def on_click_button_trudby(event):
            self.poziom=2
            self.setup()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:

            self.x=x
            self.y=y

            self.kwadr_x = int((x - start_x) / (stawka_x))
            self.kwadr_y = int((y - start_y) / (stawka_y))

            if self.kwadr_y<=9 and self.kwadr_x<=9:
                self.ktr_x = self.kwadr_x
                self.ktr_y = self.kwadr_y
                if self.stare_pole !=[self.ktr_x,self.ktr_y]:
                    self.czy_poj_znak = True
                    self.stare_pole = [self.ktr_x,self.ktr_y]

            if not self.czy_ustal_pole and self.jakiznak=='Brak':
                self.czy_ustal_pole = True

    def dodatkowe_pola(self):
        if self.ktr_x==9 and self.ktr_y==9:
            return
        if self.ktr_x==9:
            pole =9+self.ktr_y
        else:
            pole = self.ktr_x

        if self.czy_poj_znak and self.jakiznak!=0:
            if self.czy_ustal_pole and self.jakiznak!='Brak':
              self.tabela_pionpoziom[pole] = self.jakiznak
              self.jakiznak = 'Brak'

    def ustalenie_pola (self):
        #żółty prostokat
        if self.czy_ustal_pole and self.jakiznak=='Brak':
            arcade.draw_rectangle_filled(self.ktr_x * stawka_x + start_x + stawka_x / 2 - 1,
                                         self.ktr_y * stawka_y + start_y + stawka_y / 2 - 1,
                                         stawka_x - 4, stawka_y - 4, color=arcade.color.YELLOW)


    def wprowadz_znak(self):
        if self.ktr_x ==9 or self.ktr_y==9:
            self.dodatkowe_pola()
            self.jakiznak = 'Brak'
            return
        if self.czy_poj_znak:
            if self.czy_ustal_pole and self.jakiznak!='Brak':
                # tutaj sprawdzenie czy wszystkie może być ten znak
                self.sprawdzenie()
                if self.jakiznak =="":
                    self.jakiznak = 'Brak'
                    return
                self.kopiuj_tabele()
                self.tabela[self.ktr_x][self.ktr_y] = self.jakiznak
                self.jakiznak = 'Brak'
        else:
            #tutaj sprawdzenie czy nowy znak w małej tabeli jest ok
            #czy wywołać sprawdzenie
            self.sprawdzenie()
            if not (self.jakiznak =="" or self.jakiznak=="#"):
                if self.tabela[self.ktr_x][self.ktr_y]==[] or self.tabela[self.ktr_x][self.ktr_y]==0:
                    self.kopiuj_tabele()
                    self.tabela[self.ktr_x][self.ktr_y] = self.jakiznak
                    self.jakiznak = 'Brak'
                elif int(self.tabela[self.ktr_x][self.ktr_y])>0 and int(self.tabela[self.ktr_x][self.ktr_y])<1000:
                    wartosc = self.tabela[self.ktr_x][self.ktr_y]*10 + self.jakiznak
                    self.kopiuj_tabele()
                    self.tabela[self.ktr_x][self.ktr_y] = wartosc
                    self.jakiznak = 'Brak'
                else:
                    wartosc = str(self.tabela[self.ktr_x][self.ktr_y])
                    wartosc = int(wartosc[1:4])
                    wartosc = wartosc*10 + self.jakiznak
                    self.kopiuj_tabele()
                    self.tabela[self.ktr_x][self.ktr_y] = wartosc
                    self.jakiznak = 'Brak'
    def kopiuj_tabele(self):
        for row in range(9):
            for column in range(9):
                self.tabela_cofnij[row][column] = self.tabela[row][column]

    def zamien_tabele (self):
        for row in range(9):
            for column in range(9):
                self.tabela[row][column] = self.tabela_cofnij[row][column]

        arcade.play_sound(self.kolizja_sound)

    def on_draw(self):
        # Rysowanie wszystkiego
        # arcade.start_render()
        self.clear()
        self.ustalenie_pola()
        self.rysuj_pola()
        self.manager.draw()
        self.rysuj_siatke()
        self.ramka ()
        self.dodatkowe()
        self.napisy()
    def dodatkowe(self):
        #ramka

        #liczby
        for x  in range (9):
            wartosc = str(self.tabela_pionpoziom[x])
            arcade.draw_text(wartosc, x * stawka_x + start_x + stawka_x / 2,
                             9 * stawka_y + start_y + stawka_y / 3, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                             color=arcade.color.BLACK)
        for y in range(9):
            wartosc = str(self.tabela_pionpoziom[y+9])
            arcade.draw_text(wartosc, 9 * stawka_x + start_x + stawka_x / 2,
                             y * stawka_y + start_y + stawka_y / 3, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                             color=arcade.color.BLACK)



    def on_update(self, delta_time):
        # sprawdzenie czy wszystkie liczby sudoku
        #ile liczb
        ile = 0
        for row in range(9):
            for column in range(9):
                wartosc = self.tabela[row][column]
                if wartosc!="" and wartosc!="#":
                    wartosc =  (self.tabela[row][column])
                    if int(wartosc)<10 and int(wartosc)>0 and wartosc!="":
                        ile+=1
        if ile ==81:
            arcade.play_sound(self.wszystko_sound)
            self.rysuj_pola()
            arcade.pause(2)
            self.setup()

    def napisy (self):
        if self.poziom == 0:
            self.n1 = "łatwy"
        elif self.poziom==1:
            self.n1 = "średni"
        else:
            self.n1 = "trudny"

        arcade.draw_text(str(self.ktory) + "   " +self.n1,PANEL1+stawka_x*2, height-stawka_y/2, arcade.color.RED_BROWN,
                         font_size=stawka_y*0.4, anchor_x="center")
    def ramka (self):
        arcade.draw_line (start_x=PANEL1-przerwa,start_y=height - stawka_y * 7-przerwa*2,end_x= PANEL1+stawka_x * 4.5+przerwa*3,end_y=height - stawka_y * 7-przerwa*2,color = arcade.color.RED_BROWN, line_width=3 )
            #(center_x=  center_y= , width=, height=, )

    def sprawdzenie (self):
        # sprawdzenie danych poczatkowych
        if (self.tabela_new[self.ktr_x][self.ktr_y])!="":
            arcade.play_sound(self.kolizja_sound)
            self.jakiznak = ""
        # sprawdzenie rzędu
        for row in range(9):
            if self.tabela[row][self.ktr_y] == self.jakiznak:
                arcade.play_sound(self.kolizja_sound)
                self.jakiznak = ""
        # sprawdzenie kolumny
        for column in range(9):
            if self.tabela[self.ktr_x][column] == self.jakiznak:
                arcade.play_sound(self.kolizja_sound)
                self.jakiznak = ""
    # sprawdzenie małego kwadratu
        m_x = self.ktr_x//3
        m_y= self.ktr_y//3
        for row in range (3):
            for column in range(3):
                if self.tabela[m_x*3+row][m_y*3+column] == self.jakiznak:
                    arcade.play_sound(self.kolizja_sound)
                    self.jakiznak = ""


    def rysuj_pola(self):

        for row in range(9):
            for column in range(9):
                wartosc = (self.tabela[row][column])
                if wartosc!="":
                    wartosc =int (self.tabela[row][column])
                    if wartosc ==0:
                        l1 ="#"
                        arcade.draw_text(l1, row * stawka_x + start_x + stawka_x / 2,
                                         column * stawka_y + start_y + stawka_y / 3, font_size=40, anchor_x="center",
                                         font_name="Comic Sans MS",
                                         color=arcade.color.BLACK)

                        if not (self.ktr_x==row and self.ktr_y==column):
                            arcade.draw_rectangle_filled(row * stawka_x + start_x + stawka_x / 2 - 1,
                                                     column* stawka_y + start_y + stawka_y / 2 - 1,
                                                     stawka_x - 4, stawka_y - 4, color=arcade.color.BABY_PINK)
                    elif wartosc>10:
                        if not (self.ktr_x==row and self.ktr_y==column):
                            arcade.draw_rectangle_filled(row * stawka_x + start_x + stawka_x / 2 - 1,
                                                     column* stawka_y + start_y + stawka_y / 2 - 1,
                                                     stawka_x - 4, stawka_y - 4, color=arcade.color.BABY_PINK)
                        l1 = str(wartosc)
                        l0= l1[0:1]
                        arcade.draw_text(l0, row * stawka_x + start_x+stawka_x/4,
                                     column * stawka_y + start_y+stawka_y/6, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                                     color=arcade.color.BLACK)
                        l0 = l1[1:2]
                        arcade.draw_text(l0, row * stawka_x + start_x+3*stawka_x/4,
                                     column * stawka_y + start_y+2*stawka_y/3, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                                     color=arcade.color.BLACK)
                        l0 = l1[2:3]
                        arcade.draw_text(l0, row * stawka_x + start_x+3*stawka_x/4,
                                     column * stawka_y + start_y+stawka_y/6, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                                     color=arcade.color.BLACK)
                        l0 = l1[3:4]
                        arcade.draw_text(l0, row * stawka_x + start_x+stawka_x/4,
                                     column * stawka_y + start_y+2*stawka_y/3, font_size=24,anchor_x="center", font_name="Comic Sans MS",
                                     color=arcade.color.BLACK)

                        arcade.draw_line(row * stawka_x+ start_x+ stawka_x/8,column * stawka_y+start_y+ stawka_y/2,
                                         (row+1) * stawka_x + start_x -stawka_x/8,column * stawka_y+start_y+stawka_y/2, color = arcade.color.BEAU_BLUE,line_width= 2)
                        arcade.draw_line(row * stawka_x+ start_x+ stawka_x/2,column * stawka_y+start_y+ stawka_y/8,
                                         row * stawka_x + start_x +stawka_x/2,(column+1) * stawka_y+start_y-stawka_y/8, color = arcade.color.BEAU_BLUE,line_width= 2)

                    else:
                        if not (self.ktr_x == row and self.ktr_y == column):
                            if self.tabela[row][column]==self.tabela_new[row][column]:

                                arcade.draw_rectangle_filled(row * stawka_x + start_x + stawka_x / 2 - 1,
                                                         column* stawka_y + start_y + stawka_y / 2 - 1,
                                                         stawka_x - 4, stawka_y - 4, color=arcade.color.BLUE_BELL)
                            else:
                                arcade.draw_rectangle_filled(row * stawka_x + start_x + stawka_x / 2 - 1,
                                                         column* stawka_y + start_y + stawka_y / 2 - 1,
                                                         stawka_x - 4, stawka_y - 4, color=arcade.color.BLUE_GREEN)
                        arcade.draw_text(wartosc, row * stawka_x + start_x+stawka_x/2,
                                     column * stawka_y + start_y+stawka_y/3, font_size=40,anchor_x="center", font_name="Comic Sans MS",
                                     color=arcade.color.BLACK)



    def kordynacja (self):

        arcade.draw_text(str(self.kwadr_x) + "   " + str(self.kwadr_y)+ "    " + str(stawka_x),500, 500, arcade.color.RED_BROWN,
                         font_size=40, anchor_x="center")

    def rysuj_siatke(self):
        for column in range (10):
            if column % 3 ==0:
                arcade.draw_line(start_x, start_y+column*stawka_y,start_x+9*stawka_x, start_y+column*stawka_y, color_gr,gr_linii*3)
            else:
                arcade.draw_line(start_x, start_y + column * stawka_y, start_x + 9 * stawka_x,
                                 start_y + column * stawka_y, color_l, gr_linii)
        for row in range (10):
            if row % 3 == 0:
                arcade.draw_line(start_x+ row*stawka_x, start_y,start_x+ row*stawka_x, start_y+9*stawka_y, color_gr,gr_linii*3)
            else:
                arcade.draw_line(start_x + row * stawka_x, start_y, start_x + row * stawka_x, start_y + 9 * stawka_y,
                                 color_l, gr_linii)

    def zaczyt_poz (self):
        self.zerowanie()
        self.ktory = int(random.randrange(10))
        fname = 'sud.xls'
        self.xl_workbook = xlrd.open_workbook(fname)
        self.sheet_names = self.xl_workbook.sheet_names()
        self.xl_sheet = self.xl_workbook.sheet_by_name(self.sheet_names[self.poziom])

        for row in range(9):
            for column in range(9):
                co = int(self.xl_sheet.cell_value(row+self.ktory*10, column))
                if co>0:
                    self.ktr_x=column
                    self.ktr_y=row
                    self.jakiznak=co
                    self.sprawdzenie()
                    self.tabela[column][row] = co
                    self.tabela_new[column][row]= co
        self.ktr_x=0
        self.ktr_y=0
        self.jakiznak="Brak"

    def zerowanie(self):
        pass

def main():
    # główna metoda
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=full)
    menu_view = GameView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()