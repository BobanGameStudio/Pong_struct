import time
import os
import sys
import pygame
from pygame.locals import *
from pathlib import Path

pygame.init()

def quick_sort(list, descending = True):
    """ Quick sort for tuple, if optional argument is "True" then sort is descending, if "False" then ascending """
    if len(list) <= 1: #Jezeli na liscie do posortowania jest tylko jeden element zwroc go
        return list
    #Wybranie ostatniego elementu
    selected_item = ( list[ len(list)-1 ] )
    list = list[ 0:len(list)-1 ]#Usuniecie elementow z listy

    smaller = [ ]#Stworzenie list elementow mniejszych oraz wiekszych od wybranego
    bigger = [ ]
    
    for nr_elementu, element in enumerate(list):#Przydzielenie elementow do list w zaleznosci od tego czy sa smaller czy bigger od elementu wybranego
        if element < selected_item:
            smaller.append(list[nr_elementu])
        else:
            bigger.append(list[nr_elementu])
    
    smaller = quick_sort(smaller, descending)
    bigger = quick_sort(bigger, descending)

    if descending:
        result = bigger
        result.append(selected_item)
        result =  result + smaller
    else:
        result = smaller
        result.append(selected_item)
        result =  result + bigger
    
    return result

def display_caption(surface, text_to_display, font, position, background_color, font_color, refresh = True):
    """ Displaying caption (choosen text, choosen font, choosen position, choosen background and font color) on surface 
    optional option "refresh" if true: updates surface after display caption"""
    Caption = font.render(text_to_display, 1, font_color,background_color)
    surface.blit(Caption, position)
    if refresh:
        pygame.display.flip()

def if_cursor_on_the_surface( mouse_pos, surface_pos, surface, down = True):
    """ Function check if coursor is on surface, 
    if optional argument "down" is "True" then returns "True" if coursor is on surface and left mouse button is down and False otherwise
    if optional argument "down" is "False" then returns "True" if coursor is on surface and left mouse button is up and False otherwise"""
    if  mouse_pos[0] > surface_pos[0]:
        if mouse_pos[0] < surface_pos[0] + surface.get_width():
            if mouse_pos[1] > surface_pos[1]:
                if mouse_pos[1] < surface_pos[1] + surface.get_height():
                    if down:
                        if pygame.mouse.get_pressed()[0] == 1 :
                            return True
                        else:
                            return False  
                    else:
                        if pygame.mouse.get_pressed()[0] == 0 :
                            return True    
                        else:
                            return False  
    else:
        return False  

def unicode_from_number( number ):
    """ Give unicode from ascii for the chosen ones """
    if number == 0:# klawisz 
        return ("_")
    if number == 1:# klawisz 
        return ("")
    if number == 9:# klawisz 'TAB'
        return ("TAB")
    if number == 12:# klawisz 'ENTER'
        return ("ENTER")
    if number == 32:# klawisz 'SPACE'
        return ("SPACE")
    if number == 39:# klawisz '''
        return pygame.key.name( number )
    if number >= 44 and number <= 57:# klawisze ',' '-' '.' '/' '0 - 9'
        return pygame.key.name( number )
    if number == 59:# klawisz ';'
        return pygame.key.name( number )
    if number == 61:# klawisz '='
        return pygame.key.name( number )
    if number >= 97 and number <= 122:# klawisze 'a - z' i 'A - Z'
        return pygame.key.name( number )
    if number == 273:# klawisz 'UP'
        return ("UP")
    if number == 274:# klawisz 'DOWN'
        return ("DOWN")
    if number == 275:# klawisz 'RIGHT'
        return ("RIGHT")
    if number == 276:# klawisz 'LEFT'
        return ("LEFT")
    if number >= 282 and number <= 293:# klawisze 'F1 - F12'
        return ("F" + str( number - 281 ) )
    return ("_")

#region Inicjalizacja okna
infoObject = pygame.display.Info() #Pobranie informacji o obrazie (rowniez rozdzielczosc monitora)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( 0, 0 )#Początkowa pozycja okna na ekranie
window = pygame.display.set_mode(( infoObject.current_w, infoObject.current_h)) #stworzenie okna gry
pygame.display.set_caption("Gra Pong")

clock = pygame.time.Clock()

#region pobieranie obrazkow
button_start_PvP_up     = pygame.image.load("pictures/button_start_PvP_up.png").convert_alpha()
button_start_PvP_down   = pygame.image.load("pictures/button_start_PvP_down.png").convert_alpha()
button_start_PvE_up     = pygame.image.load("pictures/button_start_PvE_up.png").convert_alpha()
button_start_PvE_down   = pygame.image.load("pictures/button_start_PvE_down.png").convert_alpha()
button_options_up       = pygame.image.load("pictures/button_options_up.png").convert_alpha()
button_options_down     = pygame.image.load("pictures/button_options_down.png").convert_alpha()
button_high_score_up    = pygame.image.load("pictures/button_high_score_up.png").convert_alpha()
button_high_score_down  = pygame.image.load("pictures/button_high_score_down.png").convert_alpha()
button_contact_up       = pygame.image.load("pictures/button_contact_up.png").convert_alpha()
button_contact_down     = pygame.image.load("pictures/button_contact_down.png").convert_alpha()
button_exit_up          = pygame.image.load("pictures/button_exit_up.png").convert_alpha()
button_exit_down        = pygame.image.load("pictures/button_exit_down.png").convert_alpha()

button_right_up         = pygame.image.load("pictures/button_right_up2.png").convert_alpha()
button_right_down       = pygame.image.load("pictures/button_right_down2.png").convert_alpha()
button_left_up          = pygame.image.load("pictures/button_left_up2.png").convert_alpha()
button_left_down        = pygame.image.load("pictures/button_left_down2.png").convert_alpha()

small_stake             = pygame.image.load("pictures/small_stake.png").convert_alpha()
big_stake               = pygame.image.load("pictures/big_stake.png").convert_alpha()
#endregion

#region Stale
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

STRIP_W = 15
STRIP_H = 50
STRIP_DISTANCE = 40

PADDLE_W = 30
PADDLE_H = 120

BALL_SIZE = 15

with open( "options/options.txt" ) as file:
    options = file.read().splitlines()
file.close()

for option in options:
    if "Ball speed:" in option:
        ball_speed = int( option[ option.index(":") + 1: len(option) ] )
    if "Paddle speed:" in option:
        paddle_speed = int( option[ option.index(":") + 1: len(option) ] )
SPEED_MULTIPLIER = 2

OPTIONS_TEXT_BACKGROUND_W = 190
if infoObject.current_h > 800:
    OPTIONS_TEXT_BACKGROUND_H = 55
else:
    OPTIONS_TEXT_BACKGROUND_H = 35
#endregion

#region napisy

pygame.font.init()
#Czcionki
font_menu =             pygame.font.Font('fonts/casio-fx-702p.ttf', 70)# Font of text "PONG GAME" in menu
font_version =          pygame.font.Font('fonts/casio-fx-702p.ttf', 15)# Font of text showing program version in menu
font_pause =            pygame.font.Font('fonts/casio-fx-702p.ttf', 150)# Font of text showing "PAUSE" while game is paused
font_fps =              pygame.font.Font('fonts/casio-fx-702p.ttf', 15)# Font of showed FPS
font_options_title =    pygame.font.Font('fonts/casio-fx-702p.ttf', 80)# Font of text "OPTIONS" in options
font_points =           pygame.font.Font('fonts/casio-fx-702p.ttf', 50)# Font of points showed in game
font_ranking_title =    pygame.font.Font('fonts/casio-fx-702p.ttf', 60)# Font of "HIGH SCORES" in high scores

if infoObject.current_h > 800:
    font_options_names =       pygame.font.Font('fonts/casio-fx-702p.ttf', 40)# Font of all options names
    font_ranking_points =      pygame.font.Font('fonts/casio-fx-702p.ttf', 25)# Font of points in ranking
    font_ranking_description = pygame.font.Font('fonts/casio-fx-702p.ttf', 25)# Font of points in ranking
    font_contact_title =       pygame.font.Font('fonts/casio-fx-702p.ttf', 70)# Font of "CONTACT WITH ME" in contact
    font_contact_mail =        pygame.font.SysFont('Times new Roman', 50)# Font of mail in contact
else:
    font_options_names =        pygame.font.Font('fonts/casio-fx-702p.ttf', 20)# Font of all options names
    font_ranking_points =       pygame.font.Font('fonts/casio-fx-702p.ttf', 15)# Font of points in ranking
    font_ranking_description =  pygame.font.Font('fonts/casio-fx-702p.ttf', 15)# Font of points in ranking
    font_contact_title =        pygame.font.Font('fonts/casio-fx-702p.ttf', 50)# Font of "CONTACT WITH ME" in contact
    font_contact_mail =         pygame.font.SysFont('Times new Roman', 40)# Font of mail in contact

#tworzenie napisow
text_menu =               font_menu.render( "PONG GAME", 1, GRAY, BLACK )
text_version =            font_version.render( "V.1.0", 1, GRAY, BLACK )
text_pause =              font_pause.render( "PAUSE", 1, GRAY, BLACK )
text_options_title =      font_options_title.render( "OPTIONS", 1, GRAY, BLACK )
text_options_names =      [font_options_names.render( "Ball speed", 1, GRAY, BLACK ),
                          font_options_names.render( "Paddle speed", 1, GRAY, BLACK ),
                          font_options_names.render( "Difficulty level", 1, GRAY, BLACK ),
                          font_options_names.render( "Paddle up p.1", 1, GRAY, BLACK ),
                          font_options_names.render( "Paddle down p.1", 1, GRAY, BLACK ),
                          font_options_names.render( "Paddle up p.2", 1, GRAY, BLACK ),
                          font_options_names.render( "Paddle down p.2", 1, GRAY, BLACK ),
                          font_options_names.render( "Pause", 1, GRAY, BLACK ),
                          font_options_names.render( "Show fps", 1, GRAY, BLACK )]
text_options_diff_lvl_1 = font_options_names.render( "Easy", 1, GRAY, BLACK )
text_options_diff_lvl_2 = font_options_names.render( "Hard", 1, GRAY, BLACK )
text_ranking_title =      font_ranking_title.render( "High Scores:", 1, GRAY, BLACK )
text_ranking_description =font_ranking_description.render( "Only from PvE", 1, GRAY, BLACK )
text_contact_title =      font_contact_title.render( "Contact with me:", 1, GRAY, BLACK )
text_contact_mail =       font_contact_mail.render( "boban.skolimowski@gmail.com", 1, GRAY, BLACK )

TEXT_MENU_POS =           ( infoObject.current_w/2 - round( text_menu.get_width()/2 ), infoObject.current_h/20)
TEXT_PAUSE_POS =          ( infoObject.current_w/2 - round( text_pause.get_width()/2 ), infoObject.current_h/2 - round( text_pause.get_height()/2 ) )
TEXT_FPS_POS =            ( infoObject.current_w - 120, 5 )
TEXT_POINTS_1_POS =       ( infoObject.current_w/2 - 270, 50)
TEXT_POINTS_2_POS =       ( infoObject.current_w/2 + 200, 50)
if infoObject.current_h > 800:
    TEXT_VERSION_POS =         ( infoObject.current_w * 15/16, infoObject.current_h - text_version.get_height() - 5 )
    TEXT_OPTIONS_TITLE_POS =   ( infoObject.current_w/2 - round( text_options_title.get_width()/2), 50)
    TEXT_OPTIONS_DISTANCES =   65
    TEXT_OPTIONS_NAMES_POS =   ( infoObject.current_w/2 - round( text_options_title.get_width() ), 180)
    BACKGROUND_OPTIONS_POS =   ( infoObject.current_w/2 + round( text_options_title.get_width()/2 ), 180 + text_options_names[0].get_height()/2 - OPTIONS_TEXT_BACKGROUND_H/2)
    STAKE_1_POS =              ( infoObject.current_w/2 + round( text_options_title.get_width()/2 ), BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) )
    STAKE_2_POS =              ( infoObject.current_w/2 + round( text_options_title.get_width()/2 ), BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 + TEXT_OPTIONS_DISTANCES ) )
    STAKE_DISTANCES =          20
    TEXT_RANKING_DISTANCES =   55
else:
    TEXT_VERSION_POS =         ( infoObject.current_w * 14/16, infoObject.current_h - text_version.get_height() - 5 )
    TEXT_OPTIONS_TITLE_POS =   ( infoObject.current_w/2 - round( text_options_title.get_width()/2), 50)
    TEXT_OPTIONS_DISTANCES =   45
    TEXT_OPTIONS_NAMES_POS =   ( infoObject.current_w/2 - round( text_options_title.get_width()*3/4), 180)
    BACKGROUND_OPTIONS_POS =   ( infoObject.current_w/2 + round( text_options_title.get_width()/4 ), 180 + text_options_names[0].get_height()/2 - OPTIONS_TEXT_BACKGROUND_H/2)
    STAKE_1_POS =              ( infoObject.current_w/2 + round( text_options_title.get_width()/4 ), BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) )
    STAKE_2_POS =              ( infoObject.current_w/2 + round( text_options_title.get_width()/4 ), BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 + TEXT_OPTIONS_DISTANCES ) )
    STAKE_DISTANCES =          20
    TEXT_RANKING_DISTANCES = 35
TEXT_OPTIONS_DIFF_1_POS = ( BACKGROUND_OPTIONS_POS[0] + round( OPTIONS_TEXT_BACKGROUND_W/2 - text_options_diff_lvl_1.get_width()/2 ), 180 - text_options_diff_lvl_1.get_height()/2 + OPTIONS_TEXT_BACKGROUND_H/2 + 2 * TEXT_OPTIONS_DISTANCES )
TEXT_OPTIONS_DIFF_2_POS = ( BACKGROUND_OPTIONS_POS[0] + round( OPTIONS_TEXT_BACKGROUND_W/2 - text_options_diff_lvl_2.get_width()/2 ), 180 - text_options_diff_lvl_2.get_height()/2 + OPTIONS_TEXT_BACKGROUND_H/2 + 2 * TEXT_OPTIONS_DISTANCES )
TEXT_RANKING_TITLE_POS =  ( infoObject.current_w/2 - round( text_ranking_title.get_width()/2 ), 60)
TEXT_RANKING_DESC_POS =   ( infoObject.current_w/2 - round( text_ranking_description.get_width()/2 ), 140)
TEXT_RANKING_POINTS_POS = ( infoObject.current_w/2 - round( text_ranking_title.get_width()/2 ), 190 )
TEXT_CONTACT_TITLE_POS =  ( infoObject.current_w/2 - round( text_contact_title.get_width()/2 ), 100)
TEXT_CONTACT_MAIL_POS =   ( infoObject.current_w/2 - round( text_contact_mail.get_width()/2 ), 300)
#endregion           

#region Przyciski
BUTTON_START_PVP_UP_XY          = ( infoObject.current_w/2 - button_start_PvP_up.get_width()/2, 4 * infoObject.current_h/20 )
BUTTON_START_PVE_UP_XY          = ( infoObject.current_w/2 - button_start_PvE_up.get_width()/2, 6 * infoObject.current_h/20 )
BUTTON_OPTIONS_UP_XY            = ( infoObject.current_w/2 - button_options_up.get_width()/2, 8 * infoObject.current_h/20 )
BUTTON_HIGH_SCORE_UP_XY         = ( infoObject.current_w/2 - button_high_score_up.get_width()/2, 10 * infoObject.current_h/20 )
BUTTON_CONTACT_UP_XY            = ( infoObject.current_w/2 - button_contact_up.get_width()/2, 12 * infoObject.current_h/20 )
BUTTON_EXIT_UP_XY               = ( infoObject.current_w/2 - button_exit_up.get_width()/2, 14 * infoObject.current_h/20 )

BUTTON_OPTIONS_LEFT_UP_1_XY     = ( BACKGROUND_OPTIONS_POS[0] - button_right_up.get_width() * 3/2, BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) - button_right_up.get_height()/2 )
BUTTON_OPTIONS_RIGHT_UP_1_XY    = ( BACKGROUND_OPTIONS_POS[0] + OPTIONS_TEXT_BACKGROUND_W + button_right_up.get_width() * 1/2, BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) - button_right_up.get_height()/2 )

BUTTON_START_PVP_DOWN_XY        = ( infoObject.current_w/2 - button_start_PvP_down.get_width()/2, 4 * infoObject.current_h/20 )
BUTTON_START_PVE_DOWN_XY        = ( infoObject.current_w/2 - button_start_PvE_down.get_width()/2, 6 * infoObject.current_h/20 )
BUTTON_OPTIONS_DOWN_XY          = ( infoObject.current_w/2 - button_options_down.get_width()/2, 8 * infoObject.current_h/20 )
BUTTON_HIGH_SCORE_DOWN_XY       = ( infoObject.current_w/2 - button_high_score_down.get_width()/2, 10 * infoObject.current_h/20 )
BUTTON_CONTACT_DOWN_XY          = ( infoObject.current_w/2 - button_contact_down.get_width()/2, 12 * infoObject.current_h/20 )
BUTTON_EXIT_DOWN_XY             = ( infoObject.current_w/2 - button_exit_up.get_width()/2, 14 * infoObject.current_h/20 )

BUTTON_OPTIONS_LEFT_DOWN_1_XY   = ( BACKGROUND_OPTIONS_POS[0] - button_right_down.get_width() * 3/2, BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) - button_right_down.get_height()/2)
BUTTON_OPTIONS_RIGHT_DOWN_1_XY  = ( BACKGROUND_OPTIONS_POS[0] + OPTIONS_TEXT_BACKGROUND_W + button_right_down.get_width() * 1/2, BACKGROUND_OPTIONS_POS[1] + round( OPTIONS_TEXT_BACKGROUND_H/2 ) - button_right_down.get_height()/2)

#endregion

#region Zmienne
paddle_1_start_x_pos = 30
paddle_1_start_y_pos =  round( infoObject.current_h/2 - PADDLE_H/2 )

paddle_2_start_x_pos = infoObject.current_w - 30 - PADDLE_W
paddle_2_start_y_pos =  round( infoObject.current_h/2 - PADDLE_H/2 )
 
ball_start_x_pos = round ( infoObject.current_w/2 - BALL_SIZE/2 ) 
ball_start_y_pos = round ( infoObject.current_h/2 - BALL_SIZE/2 )

ball_speed_x = ball_speed * SPEED_MULTIPLIER
ball_speed_y = ball_speed * SPEED_MULTIPLIER

ball_start_direction_x = True
ball_start_direction_y = True

window_menu = True
window_pvp = False
window_pve = False
window_options = False
window_highscore = False
window_contact = False

pause = False

data_loaded = False
game_started = False

button_start_pvp_pressed = False
button_start_pve_pressed = False
button_options_pressed = False
button_high_score_pressed = False
button_contact_pressed = False
button_exit_pressed = False

option_changed = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
option_flashing = False
change_option_counter = 0

show_fps = False

button_left     = [ False, False, False]
button_right    = [ False, False, False]

keys_set = []
with open( "options/options.txt" ) as file:
    options = file.read().splitlines()# Przepisansie ustawien z pliku
file.close()
for option_num, option in enumerate( options ):
    if option_num > 2:
        keys_set.append( int( option[ option.index(":") + 1: len(option) ] ) )# Zapis klawiszy
    elif option_num == 2:
        if "0" in option:
            difficulty_level = "Easy"
        elif "1" in option:
            difficulty_level = "Hard"
        keys_set.append( 0 )
    else:
        keys_set.append( 0 )
#endregion

#region tworzenie powierzchni
menu_background = pygame.Surface( (infoObject.current_w, infoObject.current_h) )
menu_background.fill(BLACK)

game_background = pygame.Surface( (infoObject.current_w, infoObject.current_h) )
game_background.fill(BLACK)

paddle_1 = pygame.Surface([PADDLE_W, PADDLE_H])
paddle_1.fill(GRAY)

paddle_2 = pygame.Surface([PADDLE_W, PADDLE_H])
paddle_2.fill(GRAY)

ball = pygame.Surface( ( BALL_SIZE, BALL_SIZE ) )
ball.fill(GRAY)

stripe = pygame.Surface([STRIP_W, STRIP_H])
stripe.fill(GRAY)

options_background_stripe = pygame.Surface([OPTIONS_TEXT_BACKGROUND_W, OPTIONS_TEXT_BACKGROUND_H])
options_background_stripe.fill(DARK_GRAY)

contact_background = pygame.Surface( (infoObject.current_w, infoObject.current_h) )
contact_background.fill(BLACK)

highscores_background = pygame.Surface( (infoObject.current_w, infoObject.current_h) )
highscores_background.fill(BLACK)
#endregion

for i in range(0, round( infoObject.current_h / ( STRIP_H + STRIP_DISTANCE ))):
    game_background.blit( stripe, ( infoObject.current_w/2 - STRIP_W/2, i * (STRIP_H + STRIP_DISTANCE)) )

# uruchomienie glownej petli (mainloop) do obslugi zdarzen

while True:
    if window_menu:
        for event in pygame.event.get():
            # jesli kliknieto w przycisk zamykajacy window to konczymy program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit( menu_background, (0,0) )

        window.blit(text_menu, ( TEXT_MENU_POS[0], TEXT_MENU_POS[1] ) )

        mouse_pos = pygame.mouse.get_pos()

        #Przycisk start PVP
        if if_cursor_on_the_surface(mouse_pos, BUTTON_START_PVP_UP_XY, button_start_PvP_up, True ):
            window.blit( button_start_PvP_down, BUTTON_START_PVP_DOWN_XY )
            button_start_pvp_pressed = True 
        elif button_start_pvp_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_START_PVP_UP_XY, button_start_PvP_up, False ):
            window_pvp = True
            window_menu = False
            button_start_pvp_pressed = False
        else:
            window.blit( button_start_PvP_up, BUTTON_START_PVP_UP_XY )
            button_start_pvp_pressed = False

        #Przycisk start PVE
        if if_cursor_on_the_surface(mouse_pos, BUTTON_START_PVE_UP_XY, button_start_PvE_up, True ):
            window.blit( button_start_PvE_down, BUTTON_START_PVE_DOWN_XY )
            button_start_pve_pressed = True
        elif button_start_pve_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_START_PVE_UP_XY, button_start_PvE_up, False ):
            window_pve = True
            window_menu = False
            button_start_pve_pressed = False
        else:
            window.blit( button_start_PvE_up, BUTTON_START_PVE_UP_XY )
            button_start_pve_pressed = False

        #Przycisk window_options
        if if_cursor_on_the_surface(mouse_pos, BUTTON_OPTIONS_UP_XY, button_options_up, True ):
            window.blit( button_options_down, BUTTON_OPTIONS_DOWN_XY )
            button_options_pressed = True
        elif button_options_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_OPTIONS_UP_XY, button_options_up, False ):
            window_options = True
            window_menu = False
            button_options_pressed = False
        else:
            window.blit( button_options_up, BUTTON_OPTIONS_UP_XY )
            button_options_pressed = False

        #Przycisk high score
        if if_cursor_on_the_surface(mouse_pos, BUTTON_HIGH_SCORE_UP_XY, button_high_score_up, True ):
            window.blit( button_high_score_down, BUTTON_HIGH_SCORE_DOWN_XY )
            button_high_score_pressed = True
        elif button_high_score_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_HIGH_SCORE_UP_XY, button_high_score_up, False ):
            window_highscore = True
            window_menu = False
            button_high_score_pressed = False
        else:
            window.blit( button_high_score_up, BUTTON_HIGH_SCORE_UP_XY )
            button_high_score_pressed = False

        #Przycisk contact
        if if_cursor_on_the_surface(mouse_pos, BUTTON_CONTACT_UP_XY, button_contact_up, True ):
            window.blit( button_contact_down, BUTTON_CONTACT_DOWN_XY )
            button_contact_pressed = True
        elif button_contact_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_CONTACT_UP_XY, button_contact_up, False ):
            window_contact = True
            window_menu = False
            button_contact_pressed = False
        else:
            window.blit( button_contact_up, BUTTON_CONTACT_UP_XY )
            button_contact_pressed = False

        #Przycisk exit
        if if_cursor_on_the_surface(mouse_pos, BUTTON_EXIT_UP_XY, button_exit_up, True ):
            window.blit( button_exit_down, BUTTON_EXIT_DOWN_XY )
            button_exit_pressed = True
        elif button_exit_pressed and if_cursor_on_the_surface(mouse_pos, BUTTON_EXIT_UP_XY, button_exit_up, False ):
            window.blit( button_exit_up, BUTTON_EXIT_DOWN_XY )
            button_exit_pressed = False
            pygame.quit()
            sys.exit()
        else:
            window.blit( button_exit_up, BUTTON_EXIT_UP_XY )
            button_exit_pressed = False

        window.blit( text_version, TEXT_VERSION_POS )

        pygame.display.flip()

    if window_pvp:
        if game_started == False:
            paddle_1_x_pos = paddle_1_start_x_pos
            paddle_1_y_pos = paddle_1_start_y_pos
            paddle_2_x_pos = paddle_2_start_x_pos
            paddle_2_y_pos = paddle_2_start_y_pos

            ball_direction_x = ball_start_direction_x
            ball_direction_y = ball_start_direction_y

            points_1 = 0 
            points_2 = 0

            ball_x_pos = ball_start_x_pos
            ball_y_pos = ball_start_y_pos

            game_started = True
        # pobieranie kolejnych zdarzen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_pvp = False
                    window_menu = True
                    game_started = False
                    pause = False
                if event.key == keys_set[7]:
                    pause = not pause
                    window.blit(text_pause, ( TEXT_PAUSE_POS[0], TEXT_PAUSE_POS[1] ) )
                if event.key == keys_set[8]:
                    show_fps = not show_fps

            # jesli kliknieto w przycisk zamykajacy window to konczymy program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                game_started = False
            pygame.display.flip()

        if pause == False:
        
            pressed = pygame.key.get_pressed() 
            
            if pressed[ keys_set[3] ]:
                paddle_1_y_pos -= paddle_speed * SPEED_MULTIPLIER
                if paddle_1_y_pos < 0:
                    paddle_1_y_pos = 0
            if pressed[ keys_set[4] ]:
                paddle_1_y_pos += paddle_speed * SPEED_MULTIPLIER
                if paddle_1_y_pos > infoObject.current_h - PADDLE_H:
                    paddle_1_y_pos = infoObject.current_h - PADDLE_H
            if pressed[ keys_set[5] ]:
                paddle_2_y_pos -= paddle_speed * SPEED_MULTIPLIER
                if paddle_2_y_pos < 0:
                    paddle_2_y_pos = 0
            if pressed[ keys_set[6] ]:
                paddle_2_y_pos += paddle_speed * SPEED_MULTIPLIER
                if paddle_2_y_pos > infoObject.current_h - PADDLE_H:
                    paddle_2_y_pos = infoObject.current_h - PADDLE_H

            if ball_direction_x == True:#Obsluga ruchu pilki
                ball_x_pos += ball_speed_x
            else:
                ball_x_pos -= ball_speed_x
            if ball_direction_y == True:
                ball_y_pos += ball_speed_y
            else: 
                ball_y_pos -= ball_speed_y

            #region Obsluga zderzen
            #Paletka prawa
            if ball_x_pos >= paddle_2_x_pos - BALL_SIZE:
                if ball_x_pos <= paddle_2_x_pos - BALL_SIZE + ball_speed_x:
                    if ball_y_pos >= paddle_2_y_pos - BALL_SIZE:
                        if ball_y_pos <= paddle_2_y_pos + PADDLE_H:
                            ball_x_pos = paddle_2_x_pos - BALL_SIZE
                            ball_direction_x = not ball_direction_x
                            ball_speed_x = round ( ( 1 - abs( (ball_y_pos + BALL_SIZE/2) - (paddle_2_y_pos + PADDLE_H/2) )/(PADDLE_H/2 + 2 * BALL_SIZE)) * (ball_speed * SPEED_MULTIPLIER * 2))
                            ball_speed_y = round ( abs( (ball_y_pos + BALL_SIZE/2) - (paddle_2_y_pos + PADDLE_H/2) ) /(PADDLE_H/2 + 2 * BALL_SIZE) * (ball_speed * SPEED_MULTIPLIER * 2) )
                            print(ball_speed_x, ball_speed_y)
                            if ball_speed_x < 2:
                                ball_speed_x = 2
            if ball_x_pos > infoObject.current_w: 
                ball_x_pos = ball_start_x_pos
                ball_y_pos = ball_start_y_pos
                ball_direction_x = not ball_direction_x
                ball_direction_y = not ball_direction_y
                points_1 += 1
                ball_speed_x = ball_speed * SPEED_MULTIPLIER
                ball_speed_y = ball_speed * SPEED_MULTIPLIER
            #Paletka lewa
            if ball_x_pos <= paddle_1_x_pos + PADDLE_W:
                if ball_x_pos >= paddle_1_x_pos + PADDLE_W - ball_speed_x:
                    if ball_y_pos >= paddle_1_y_pos - BALL_SIZE:
                        if ball_y_pos <= paddle_1_y_pos + PADDLE_H:
                            ball_x_pos = paddle_1_x_pos + PADDLE_W
                            ball_direction_x = not ball_direction_x
                            ball_speed_x = round ( ( 1 - abs( (ball_y_pos + BALL_SIZE/2) - (paddle_1_y_pos + PADDLE_H/2) )/(PADDLE_H/2 + 2 * BALL_SIZE)) * (ball_speed * SPEED_MULTIPLIER * 2))
                            ball_speed_y = round ( abs( (ball_y_pos + BALL_SIZE/2) - (paddle_1_y_pos + PADDLE_H/2) ) /(PADDLE_H/2 + 2 * BALL_SIZE) * (ball_speed * SPEED_MULTIPLIER * 2) )
                            if ball_speed_x < 2:
                                ball_speed_x = 2
            if ball_x_pos < 0: 
                ball_x_pos = ball_start_x_pos
                ball_y_pos = ball_start_y_pos
                ball_direction_x = not ball_direction_x
                ball_direction_y = not ball_direction_y
                points_2 += 1
                ball_speed_x = ball_speed * SPEED_MULTIPLIER
                ball_speed_y = ball_speed * SPEED_MULTIPLIER
            #Granica dolna
            if ball_y_pos > infoObject.current_h - BALL_SIZE:
                ball_y_pos = infoObject.current_h - BALL_SIZE
                ball_direction_y = not ball_direction_y
            #Granica gorna
            if ball_y_pos < 0:
                ball_y_pos = 0
                ball_direction_y = not ball_direction_y
            #endregion

            window.blit( game_background, (0,0) )

            if show_fps:
                display_caption(window, "FPS: %.f " %( clock.get_fps() ), font_fps, TEXT_FPS_POS, BLACK, GRAY, False )

            display_caption(window, "%.f " %( points_1 ), font_points, TEXT_POINTS_1_POS, BLACK, GRAY, False)
            display_caption(window, "%.f " %( points_2 ), font_points, TEXT_POINTS_2_POS, BLACK, GRAY, False)

            window.blit( ball, ( ball_x_pos , ball_y_pos ) )
            window.blit( paddle_1, ( paddle_1_x_pos , paddle_1_y_pos ) )
            window.blit( paddle_2, ( paddle_2_x_pos, paddle_2_y_pos ) )
            
            #Ograniczenie do 60 klatek na sekunde
            clock.tick(60)

            #pygame.display.update()
            pygame.display.flip()

    if window_pve:
        if game_started == False:
            paddle_1_x_pos = paddle_1_start_x_pos
            paddle_1_y_pos = paddle_1_start_y_pos
            paddle_2_x_pos = paddle_2_start_x_pos
            paddle_2_y_pos = paddle_2_start_y_pos

            ball_direction_x = ball_start_direction_x
            ball_direction_y = ball_start_direction_y

            points_1 = 0 
            points_2 = 0

            ball_x_pos = ball_start_x_pos
            ball_y_pos = ball_start_y_pos

            if difficulty_level == "Easy":
                converter = 1
            if difficulty_level == "Hard":
                converter = 1.1

            game_started = True
        # pobieranie kolejnych zdarzen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_pve = False
                    window_menu = True
                    pause = False
                    
                    results = []
                    with open( "highscores/High Scores.txt" ) as file:
                        for i, wiersz in enumerate( file ):
                            results.append( int( wiersz ) )
                    file.close()

                    results.append( points_1 )
                    results = quick_sort( results )

                    with open( "highscores/High Scores.txt", "w" ) as file:
                        for i in range( 0, len(results)-1 ):
                            file.write( str( results[i] ) + "\n" )

                    game_started = False
                if event.key == keys_set[7]:
                    pause = not pause
                    window.blit(text_pause, ( TEXT_PAUSE_POS[0], TEXT_PAUSE_POS[1] ) )
                if event.key == keys_set[8]:
                    show_fps = not show_fps
            # jesli kliknieto w przycisk zamykajacy window to konczymy program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                game_started = False
            pygame.display.flip()

        if pause == False:
        
            pressed = pygame.key.get_pressed() 
            
            if pressed[ keys_set[3] ]:
                paddle_1_y_pos -= paddle_speed * SPEED_MULTIPLIER
                if paddle_1_y_pos < 0:
                    paddle_1_y_pos = 0
            if pressed[ keys_set[4] ]:
                paddle_1_y_pos += paddle_speed * SPEED_MULTIPLIER
                if paddle_1_y_pos > infoObject.current_h - PADDLE_H:
                    paddle_1_y_pos = infoObject.current_h - PADDLE_H
            
            # Ruch paletki komputera
            if ball_direction_x == True:
                if ball_x_pos < infoObject.current_w * 1/2:
                    if ball_y_pos < paddle_2_y_pos and paddle_2_y_pos > infoObject.current_h * 2/3 :
                        paddle_2_y_pos -= round( paddle_speed * SPEED_MULTIPLIER * converter )
                    elif ball_y_pos + BALL_SIZE > paddle_2_y_pos + PADDLE_H and paddle_2_y_pos < infoObject.current_h * 1/3:
                        paddle_2_y_pos += round( paddle_speed * SPEED_MULTIPLIER * converter )
                else:
                    if ball_y_pos < paddle_2_y_pos + PADDLE_H * 1/4 :
                        paddle_2_y_pos -= round( paddle_speed * SPEED_MULTIPLIER * converter )
                    elif ball_y_pos > paddle_2_y_pos + PADDLE_H * 3/4 :
                        paddle_2_y_pos += round( paddle_speed * SPEED_MULTIPLIER * converter )

                if paddle_2_y_pos < 0:
                    paddle_2_y_pos = 0
                elif infoObject.current_h - PADDLE_H < paddle_2_y_pos:
                    paddle_2_y_pos = infoObject.current_h - PADDLE_H 
                    #print(paddle_2_y_pos)

            if ball_direction_x == True:#Obsluga ruchu pilki
                ball_x_pos += ball_speed_x
            else:
                ball_x_pos -= ball_speed_x
            if ball_direction_y == True:
                ball_y_pos += ball_speed_y
            else: 
                ball_y_pos -= ball_speed_y

            #region Obsluga zderzen
            #Paletka prawa
            if ball_x_pos >= paddle_2_x_pos - BALL_SIZE:
                if ball_x_pos <= paddle_2_x_pos - BALL_SIZE + ball_speed_x:
                    if ball_y_pos >= paddle_2_y_pos - BALL_SIZE:
                        if ball_y_pos <= paddle_2_y_pos + PADDLE_H:
                            ball_x_pos = paddle_2_x_pos - BALL_SIZE
                            ball_direction_x = not ball_direction_x
                            ball_speed_x = round ( ( 1 - abs( (ball_y_pos + BALL_SIZE/2) - (paddle_2_y_pos + PADDLE_H/2) )/(PADDLE_H/2 + 2 * BALL_SIZE)) * (ball_speed * SPEED_MULTIPLIER * 2))
                            ball_speed_y = round ( abs( (ball_y_pos + BALL_SIZE/2) - (paddle_2_y_pos + PADDLE_H/2) ) /(PADDLE_H/2 + 2 * BALL_SIZE) * (ball_speed * SPEED_MULTIPLIER * 2) )
                            print(ball_speed_x , " ", ball_speed_y)
                            if ball_speed_x < 2:
                                ball_speed_x = 2
            if ball_x_pos > infoObject.current_w: 
                ball_x_pos = ball_start_x_pos
                ball_y_pos = ball_start_y_pos
                ball_direction_x = not ball_direction_x
                ball_direction_y = not ball_direction_y
                points_1 += 1
                ball_speed_x = ball_speed * SPEED_MULTIPLIER
                ball_speed_y = ball_speed * SPEED_MULTIPLIER
            #Paletka lewa
            if ball_x_pos <= paddle_1_x_pos + PADDLE_W:
                if ball_x_pos >= paddle_1_x_pos + PADDLE_W - ball_speed_x:
                    if ball_y_pos >= paddle_1_y_pos - BALL_SIZE:
                        if ball_y_pos <= paddle_1_y_pos + PADDLE_H:
                            ball_x_pos = paddle_1_x_pos + PADDLE_W
                            ball_direction_x = not ball_direction_x
                            ball_speed_x = round ( ( 1 - abs( (ball_y_pos + BALL_SIZE/2) - (paddle_1_y_pos + PADDLE_H/2) )/(PADDLE_H/2 + 2 * BALL_SIZE)) * (ball_speed * SPEED_MULTIPLIER * 2))
                            ball_speed_y = round ( abs( (ball_y_pos + BALL_SIZE/2) - (paddle_1_y_pos + PADDLE_H/2) ) /(PADDLE_H/2 + 2 * BALL_SIZE) * (ball_speed * SPEED_MULTIPLIER * 2) )
                            if ball_speed_x < 2:
                                ball_speed_x = 2
            if ball_x_pos < 0: 
                ball_x_pos = ball_start_x_pos
                ball_y_pos = ball_start_y_pos
                ball_direction_x = not ball_direction_x
                ball_direction_y = not ball_direction_y
                points_2 += 1
                ball_speed_x = ball_speed * SPEED_MULTIPLIER
                ball_speed_y = ball_speed * SPEED_MULTIPLIER
            #Granica dolna
            if ball_y_pos > infoObject.current_h - BALL_SIZE:
                ball_y_pos = infoObject.current_h - BALL_SIZE
                ball_direction_y = not ball_direction_y
            #Granica gorna
            if ball_y_pos < 0:
                ball_y_pos = 0
                ball_direction_y = not ball_direction_y
            #endregion

            window.blit( game_background, (0,0) )

            if show_fps:
                display_caption(window, "FPS: %.f " %( clock.get_fps() ), font_fps, TEXT_FPS_POS, BLACK, GRAY, False )

            display_caption(window, "%.f " %( points_1 ), font_points, TEXT_POINTS_1_POS, BLACK, GRAY, False)
            display_caption(window, "%.f " %( points_2 ), font_points, TEXT_POINTS_2_POS, BLACK, GRAY, False)

            window.blit( ball, ( ball_x_pos , ball_y_pos ) )
            window.blit( paddle_1, ( paddle_1_x_pos , paddle_1_y_pos ) )
            window.blit( paddle_2, ( paddle_2_x_pos, paddle_2_y_pos ) )
            
            #Ograniczenie do 60 klatek na sekunde
            clock.tick(60)

            #pygame.display.update()
            pygame.display.flip()

    if window_options:
        if data_loaded == False:
            keys_set = []
            with open( "options/options.txt" ) as file:
                options = file.read().splitlines()# Przepisanie ustawien z pliku
            file.close()
            for option_num, option in enumerate( options ):
                if option_num > 2:
                    keys_set.append( int( option[ option.index(":") + 1: len(option) ] ) )# Zapis klawiszy
                else:
                    keys_set.append( 0 )
            data_loaded = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_options = False
                    window_menu = True
                    data_loaded = False
                    option_changed = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                    ball_speed_x = ball_speed * SPEED_MULTIPLIER
                    ball_speed_y = ball_speed * SPEED_MULTIPLIER
                if sum( option_changed ) > 0 and option_changed.index(1) > 2: 
                    options[ option_changed.index(1) ] = options[ option_changed.index(1) ][ 0:options[ option_changed.index(1) ].index(":") + 1 ] + str( event.key )
                    keys_set[ option_changed.index(1) ] = 0 # Reset klawisza którego zmiana ma zajść
                    if event.key == 9 or event.key == 12 or event.key == 32 or event.key == 39 or ( event.key >= 44 and event.key <= 57 ) or event.key == 59  or event.key == 61 or ( event.key >= 97 and event.key <= 122 ) or ( event.key >= 273 and event.key <= 276 ) or ( event.key >= 282 and event.key <= 293 ):
                        if event.key not in keys_set:
                            file = open('options/options.txt','w')
                            for option_num, option in enumerate( options ):
                                file.write( option + "\n")
                                if option_num == option_changed.index(1) :
                                    keys_set[ option_changed.index(1) ] = int( event.key )
                            file.close()     
                            option_changed = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.blit( contact_background, (0,0) )

        window.blit(text_options_title, ( TEXT_OPTIONS_TITLE_POS[0], TEXT_OPTIONS_TITLE_POS[1] ) )

        mouse_pos = pygame.mouse.get_pos()
        for i in range( 0, 9 ):
            if i == 1:
                if difficulty_level == "Easy":
                    window.blit( text_options_diff_lvl_1, ( TEXT_OPTIONS_DIFF_1_POS[0], TEXT_OPTIONS_DIFF_1_POS[1] ) )#Wyswietlanie tla obok napisow
                elif difficulty_level == "Hard":
                    window.blit( text_options_diff_lvl_2, ( TEXT_OPTIONS_DIFF_2_POS[0], TEXT_OPTIONS_DIFF_2_POS[1] ) )#Wyswietlanie tla obok napisow
            if i > 2:
                window.blit( options_background_stripe, ( BACKGROUND_OPTIONS_POS[0], BACKGROUND_OPTIONS_POS[1] + i * TEXT_OPTIONS_DISTANCES ) )#Wyswietlanie tla obok napisow
                
                #Wykrywanie czy wcisnieta zostala zmiana klawisza
                if if_cursor_on_the_surface( mouse_pos, (BACKGROUND_OPTIONS_POS[0], (i) * TEXT_OPTIONS_DISTANCES + BACKGROUND_OPTIONS_POS[1]), options_background_stripe ):
                    if option_changed[i] == 0:
                        option_changed = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                        option_changed[i] = 1
                        with open( "options/options.txt" ) as file:
                            options = file.read().splitlines()
                        file.close()
                        change_option_counter = 0
            window.blit(text_options_names[i], ( TEXT_OPTIONS_NAMES_POS[0], TEXT_OPTIONS_NAMES_POS[1] + i * TEXT_OPTIONS_DISTANCES ) )#Wyswietlanie napisow opcji
        for option_num, option in enumerate( options ):# Wyswietlanie klawiszy opcji
            if "Gora gracz 1:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 3 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
            if "Dol gracz 1:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 4 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
            if "Gora gracz 2:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 5 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
            if "Dol gracz 2:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 6 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
            if "Pauza:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 7 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
            if "ShowFps:" in option:
                caption = font_options_names.render( unicode_from_number( int( option[ option.index(":") + 1: len(option) ] ) ), 1, GRAY, DARK_GRAY )
                window.blit(caption, ( BACKGROUND_OPTIONS_POS[0] + ( OPTIONS_TEXT_BACKGROUND_W - caption.get_width() )/2, BACKGROUND_OPTIONS_POS[1] + 8 * TEXT_OPTIONS_DISTANCES + ( OPTIONS_TEXT_BACKGROUND_H - caption.get_height() )/2 ) )
        
        for option_num, option in enumerate( option_changed ):# Miganie kreski
            if option == 1 and option_flashing == True:
                change_option_counter += 1
                options[ option_num ] = options[ option_num ][ 0:options[ option_num ].index(":") + 1 ] + "0"
                if change_option_counter == 100:
                    change_option_counter = 0
                    option_flashing = not option_flashing
                    options[ option_num ] = options[ option_num ][ 0:options[ option_num ].index(":") + 1 ] + "1"
            if option == 1 and option_flashing == False:
                change_option_counter += 1
                options[ option_num ] = options[ option_num ][ 0:options[ option_num ].index(":") + 1 ] + "1"
                if change_option_counter == 100:
                    change_option_counter = 0
                    option_flashing = not option_flashing
                    options[ option_num ] = options[ option_num ][ 0:options[ option_num ].index(":") + 1 ] + "0"

        for i in range( 0, 10 ):# Wyswietlanie slupkow
            if i < ball_speed:
                window.blit( big_stake, ( STAKE_1_POS[0] + i * STAKE_DISTANCES, STAKE_1_POS[1] - round( big_stake.get_height()/2 )) )
            else:
                window.blit( small_stake, ( STAKE_1_POS[0] + i * STAKE_DISTANCES, STAKE_1_POS[1] - round( small_stake.get_height()/2 )) )
            if i < paddle_speed:
                window.blit( big_stake, ( STAKE_2_POS[0] + i * STAKE_DISTANCES, STAKE_2_POS[1] - round( big_stake.get_height()/2 )) )
            else:
                window.blit( small_stake, ( STAKE_2_POS[0] + i * STAKE_DISTANCES, STAKE_2_POS[1] - round( small_stake.get_height()/2 )) )
        
        for i in range( 0, 3 ):#Rysowanie klawiszy prawo/lewo i wykrywanie czy sa wcisniete i czy zostaly puszczone
            # Klawisze lewo
            if if_cursor_on_the_surface( mouse_pos, ( BUTTON_OPTIONS_LEFT_UP_1_XY[0], BUTTON_OPTIONS_LEFT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES), button_left_up ):
                window.blit( button_left_down, ( BUTTON_OPTIONS_LEFT_DOWN_1_XY[0], BUTTON_OPTIONS_LEFT_DOWN_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES) )
                button_left[i] = True
            elif button_left[i] == True and if_cursor_on_the_surface( mouse_pos, ( BUTTON_OPTIONS_LEFT_UP_1_XY[0], BUTTON_OPTIONS_LEFT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES), button_left_up, False ):
                if i == 0 and ball_speed > 1:
                    ball_speed -= 1
                    option_changed[0] = 1
                    
                if i == 1 and paddle_speed > 1 :
                    paddle_speed -= 1
                    option_changed[1] = 1

                if i == 2 and difficulty_level == "Hard":
                    difficulty_level = "Easy"
                    option_changed[2] = 1
                    options[ 2 ] = options[ 2 ][ 0:options[ 2 ].index(":") + 1 ] + str( 0 )

                button_left[i] = False
            else:
                window.blit( button_left_up, ( BUTTON_OPTIONS_LEFT_UP_1_XY[0], BUTTON_OPTIONS_LEFT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES) )
                button_left[i] = False
            # Klawisze prawo
            if if_cursor_on_the_surface( mouse_pos, ( BUTTON_OPTIONS_RIGHT_UP_1_XY[0], BUTTON_OPTIONS_RIGHT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES), button_right_up ):
                window.blit( button_right_down, ( BUTTON_OPTIONS_RIGHT_DOWN_1_XY[0], BUTTON_OPTIONS_RIGHT_DOWN_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES) )
                button_right[i] = True
            elif button_right[i] == True and if_cursor_on_the_surface( mouse_pos, ( BUTTON_OPTIONS_RIGHT_UP_1_XY[0], BUTTON_OPTIONS_RIGHT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES), button_right_up, False ):
                if i == 0 and ball_speed < 10:
                    ball_speed += 1
                    option_changed[0] = 1

                if i == 1 and paddle_speed < 10:
                    paddle_speed += 1
                    option_changed[1] = 1

                if i == 2 and difficulty_level == "Easy":
                    difficulty_level = "Hard"
                    option_changed[2] = 1
                    options[ 2 ] = options[ 2 ][ 0:options[ 2 ].index(":") + 1 ] + str( 1 )

                button_right[i] = False
            else:
                window.blit( button_right_up, ( BUTTON_OPTIONS_RIGHT_UP_1_XY[0], BUTTON_OPTIONS_RIGHT_UP_1_XY[1] + i *  TEXT_OPTIONS_DISTANCES) )
                button_right[i] = False

            if option_changed[0] == 1:
                options[ 0 ] = options[ 0 ][ 0:options[ 0 ].index(":") + 1 ] + str( ball_speed )
            elif option_changed[1] == 1:
                options[ 1 ] = options[ 1 ][ 0:options[ 1 ].index(":") + 1 ] + str( paddle_speed )

            if option_changed[0] == 1 or option_changed[1] == 1 or option_changed[2] == 1:
                file = open('options/options.txt','w')
                for option_num, option in enumerate( options ):
                    file.write( option + "\n")
                file.close()
                option_changed = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        pygame.display.flip()

    if window_highscore:
        if data_loaded == False:
            results = []

            window.blit( highscores_background, (0,0) )

            window.blit( text_ranking_title, ( TEXT_RANKING_TITLE_POS[0], TEXT_RANKING_TITLE_POS[1] ) )
            window.blit( text_ranking_description, ( TEXT_RANKING_DESC_POS[0], TEXT_RANKING_DESC_POS[1] ) )
            
 
            with open( "highscores/High Scores.txt" ) as file:
                for i, wiersz in enumerate( file ):
                    points = font_ranking_points.render( "%.f" %( int( wiersz ) ), 1, GRAY, BLACK )
                    window.blit( points, ( TEXT_RANKING_POINTS_POS[0], TEXT_RANKING_POINTS_POS[1] + i * TEXT_RANKING_DISTANCES ) )
            
            file.close()

            data_loaded = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_highscore = False
                    window_menu = True
                    data_loaded = False
            # jesli kliknieto w przycisk zamykajacy window to konczymy program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    if window_contact:
        # pobieranie kolejnych zdarzen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_contact = False
                    window_menu = True
            # jesli kliknieto w przycisk zamykajacy window to konczymy program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit( contact_background, (0,0) )

        window.blit( text_contact_title, ( TEXT_CONTACT_TITLE_POS[0], TEXT_CONTACT_TITLE_POS[1] ) )
        window.blit( text_contact_mail, ( TEXT_CONTACT_MAIL_POS[0], TEXT_CONTACT_MAIL_POS[1] ) )
            

        pygame.display.flip()

pygame.quit()