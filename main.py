# =====Constantes e demais variáveis globais=====

WIDTH = 800
HEIGHT = 600
TITLE = "Juninho, a Capivara"
ICON = "images/icon.png"

MENU_STATE = 0

game_state = MENU_STATE
sound_enabled = True
mouse_pos = (0, 0)

# =====Classes=====

class Button: 
    def __init__(self, image_name, x, y, text):
        self.actor = Actor(image_name, (x, y))
        self.text = text
        self.hovered = False

    def draw(self):
        self.hovered = self.actor.collidepoint(mouse_pos)
        self.actor.draw()
        if self.hovered:
            screen.draw.text(self.text, center=self.actor.center, color="yellow", fontsize=34, fontname="jacquard_regular")
        else:
            screen.draw.text(self.text, center=self.actor.center, color="white", fontsize=34, fontname="jacquard_regular")
        

# =====Instâncias de atores=====

menu_background = Actor("menu_background", (WIDTH // 2, HEIGHT // 2))
start_button = Button("button_background", WIDTH // 2, 170, "Começar")
sound_button = Button("button_background", WIDTH // 2, 250, "Desligar Som")
exit_button = Button("button_background", WIDTH // 2, 330, "Sair")

# =====Funções=====

def draw():
    screen.clear()

    if game_state == MENU_STATE:
        draw_menu()

def draw_menu():
    menu_background.draw()
    start_button.draw()
    sound_button.draw()
    exit_button.draw()

def on_mouse_move(pos, rel, buttons):
    global mouse_pos
    mouse_pos = pos
