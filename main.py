# =====Constantes e demais variáveis globais=====

WIDTH = 800
HEIGHT = 600
TITLE = "Juninho, a Capivara"
ICON = "images/icon.png"
WORLD_WIDTH = 2496
TILE_SIZE = 64
SPEED = 3
GRAVITY = 0.5

MENU_STATE = 0
GAME_STATE = 1

game_state = MENU_STATE
sound_enabled = True
mouse_pos = (0, 0)
camera_x = 0

solid_tiles = [ # x, y, tiles_num, tile_img
    (0, 536, 13, "ground_tile"),
    (832, 536, 13, "bridge_tile"),
    (1664, 536, 13, "ground_tile")
]

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

class Player(Actor):
    def __init__(self, x, y, vx=0, vy=0):
        super().__init__("player_0", (x, y))
        self.vx = vx
        self.vy = vy
        self.flipped_x = False

    def update(self):
        global camera_x
        self.vx = 0
        if keyboard.left:
            self.vx = -SPEED
            self.flipped_x = True
        if keyboard.right:
            self.vx = SPEED
            self.flipped_x = False
        
        #self.vy = GRAVITY

        new_x = self.x + self.vx
        if self.width/2 <= new_x < WORLD_WIDTH - self.width/2:
            self.x = new_x

        self.y += self.vy

        camera_x = self.x - WIDTH // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))

    def __get_image(self):
        return "player_flipped_0" if self.flipped_x else "player_0"

    def draw(self, camera_x):
        screen.blit(self.__get_image(), (self.x - camera_x - self.width/2, self.y - self.height/2))

# =====Instâncias de atores=====

menu_background = Actor("menu_background", (WIDTH // 2, HEIGHT // 2))

start_button = Button("button_background", WIDTH // 2, 170, "Começar")
sound_button = Button("button_background", WIDTH // 2, 250, "Desligar Som")
exit_button = Button("button_background", WIDTH // 2, 330, "Sair")
menu_buttons = [start_button, sound_button, exit_button]

player = Player(32, 504)

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

def update():
    if game_state == GAME_STATE:
        player.update()

def draw():
    screen.clear()

    if game_state == MENU_STATE:
        draw_menu()
    elif game_state == GAME_STATE:
        screen.fill((0, 0, 0))
        draw_tiles()
        player.draw(camera_x)

def draw_tiles():
    screen_left  = camera_x
    screen_right = camera_x + WIDTH

    for x, y, tiles_num, tile_img in solid_tiles:
        for i in range(tiles_num):
            tile_x = x + i * TILE_SIZE
            if tile_x + TILE_SIZE < screen_left:
                continue
            if tile_x > screen_right:
                continue

            screen.blit(tile_img, (tile_x - camera_x, y))

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
