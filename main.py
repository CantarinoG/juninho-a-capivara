class Button: 
    def __init__(self, image_name, x, y, text):
        self.actor = Actor(image_name, (x, y))
        self.text = text

    def draw(self):
        self.actor.draw()
        screen.draw.text(self.text, center=self.actor.center, color="white", fontsize=34, fontname="jacquard_regular")

WIDTH = 800
HEIGHT = 600
TITLE = "Juninho, a Capivara"
ICON = "images/icon.png"

MENU_STATE = 0

game_state = MENU_STATE
sound_enabled = True

menu_background = Actor("menu_background", (WIDTH // 2, HEIGHT // 2))
start_button = Button("button_background", WIDTH // 2, 170, "Começar")
sound_button = Button("button_background", WIDTH // 2, 250, "Desligar Som")
exit_button = Button("button_background", WIDTH // 2, 330, "Sair")

def draw():
    screen.clear()

    if game_state == MENU_STATE:
        draw_menu()

def draw_menu():
    menu_background.draw()
    start_button.draw()
    sound_button.draw()
    exit_button.draw()

