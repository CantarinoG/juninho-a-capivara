# =====Constantes e demais variáveis globais=====

WIDTH = 800
HEIGHT = 600
TITLE = "Juninho, a Capivara"
ICON = "images/icon.png"

MENU_STATE = 0
GAME_STATE = 1

game_state = MENU_STATE
sound_enabled = True
mouse_pos = (0, 0)

music.play("scent_of_forest")

# =====Classes=====

class Button: 
    def __init__(self, image_name, x, y, text, on_click=None):
        self.actor = Actor(image_name, (x, y))
        self.text = text
        self.hovered = False
        self.on_click = on_click

    def draw(self):
        self.hovered = self.actor.collidepoint(mouse_pos)
        self.actor.draw()
        color = "#f0df51" if self.hovered else "white"
        screen.draw.text(self.text, center=self.actor.center, color=color, fontsize=34, fontname="jacquard_regular")
        
    def click(self):
        if self.on_click:
            self.on_click()

# =====Instâncias de atores=====

menu_background = Actor("menu_background", (WIDTH // 2, HEIGHT // 2))

start_button = Button("button_background", WIDTH // 2, 170, "Começar")
sound_button = Button("button_background", WIDTH // 2, 250, "Desligar Som")
exit_button = Button("button_background", WIDTH // 2, 330, "Sair")
menu_buttons = [start_button, sound_button, exit_button]

# =====Funções principais=====

def start_game():
    global game_state
    game_state = GAME_STATE

def toggle_sound():
    global sound_enabled, sound_button
    sound_enabled = not sound_enabled
    text = "Desligar Som" if sound_enabled else "Ligar Som"
    sound_button.text = text
    play_music_if_enabled("scent_of_forest")

def exit_game():
    exit()

start_button.on_click = start_game
sound_button.on_click = toggle_sound
exit_button.on_click = exit_game

def play_music_if_enabled(name, volume=1):
    music.stop()
    if sound_enabled:
        music.set_volume = volume
        music.play(name)

def draw():
    screen.clear()

    if game_state == MENU_STATE:
        draw_menu()
    else:
        screen.fill((0, 0, 0))

def draw_menu():
    menu_background.draw()
    for btn in menu_buttons:
        btn.draw()

def on_mouse_move(pos, rel, buttons):
    global mouse_pos
    mouse_pos = pos

def on_mouse_down(pos, button):
    if game_state == MENU_STATE:
        for btn in menu_buttons:
            if btn.actor.collidepoint(pos):
                btn.click()
