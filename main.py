# =====Constantes e demais variáveis globais=====

WIDTH = 800
HEIGHT = 600
TITLE = "Juninho, a Capivara"
ICON = "images/icon.png"
WORLD_WIDTH = 2496
TILE_SIZE = 64
SPEED = 3
GRAVITY = 0.5
JUMP_FORCE = -10

MENU_STATE = 0
GAME_STATE = 1
WIN_STATE = 2
LOSE_STATE = 3

game_state = MENU_STATE
sound_enabled = True
mouse_pos = (0, 0)
camera_x = 0

solid_tiles = [ # x, y, tiles_num, tile_img
    (0, 536, 13, "ground_tile"),
    (832, 536, 13, "bridge_tile"),
    (1664, 536, 13, "ground_tile"),
    (200, 456, 2, "platform_tile")
]

non_solid_tiles = [
    (128, 472, 2, "grass_tile"),
    (320, 472, 3, "grass_tile"),
    (702, 472, 1, "flowers_tile"),
    (1728, 472, 2, "grass_tile"),
    (1856, 472, 1, "flowers_tile"),
    (2048, 472, 2, "grass_tile")
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
        super().__init__("player", (x, y))
        self.vx = vx
        self.vy = vy
        self.flipped_x = False
        self.on_ground = True
        self.animations = {
            "idle": ["player"],
            "jumping": ["player_jumping"],
            "walking": ["player", "player_walking"]
        }
        self.current_animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0

    def update_animation(self):
        previous = self.current_animation

        if not self.on_ground:
            self.current_animation = "jumping"
        elif self.vx != 0:
            self.current_animation = "walking"
        else:
            self.current_animation = "idle"

        if self.current_animation != previous:
            self.frame_index = 0
            self.frame_timer = 0

        self.frame_timer += 1
        if self.frame_timer > 8:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])

    def update(self):
        global camera_x
        self.vx = 0
        if keyboard.left:
            self.vx = -SPEED
            self.flipped_x = True
        if keyboard.right:
            self.vx = SPEED
            self.flipped_x = False

        new_x = self.x + self.vx
        if self.width/2 <= new_x < WORLD_WIDTH - self.width/2:
            self.x = new_x

        self.vy += GRAVITY
        self.y += self.vy

        self.on_ground = check_collision_with_ground(self)
        if self.on_ground:
            self.vy = 0

        if keyboard.space and self.on_ground:
            play_sound_if_enabled("jump")
            self.vy = JUMP_FORCE

        camera_x = self.x - WIDTH // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))

        self.update_animation()

    def __get_image(self):
        #return "player_flipped_0" if self.flipped_x else "player_0"
        image_name = self.animations[self.current_animation][self.frame_index]
        if self.flipped_x:
            image_name += "_flipped"
        return image_name

    def draw(self, camera_x):
        screen.blit(self.__get_image(), (self.x - camera_x - self.width/2, self.y - self.height/2))

class Enemy(Actor):
    def __init__(self, x, y, left_limit, right_limit, vx=0, vy=0, jumping=False):
        super().__init__("enemy_0", (x, y))
        self.vx = vx
        self.vy = vy
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.flipped_x = False
        self.direction = 1
        self.jumping = jumping

    def update(self):
        global camera_x
        self.vx = (SPEED / 2) * self.direction
        self.flipped_x = (self.direction == -1)

        new_x = self.x + self.vx
        half_w = self.width / 2

        if new_x > self.right_limit - half_w:
            self.x = self.right_limit - half_w
            self.direction = -1
            self.vx = (SPEED / 2) * self.direction
        elif new_x < self.left_limit + half_w:
            self.x = self.left_limit + half_w
            self.direction = 1
            self.vx = (SPEED / 2) * self.direction
        else:
            self.x = new_x

        self.x += self.vx

        self.vy += GRAVITY
        self.y += self.vy

        on_ground = check_collision_with_ground(self)
        if on_ground:
            self.vy = 0

        if self.jumping and on_ground:
            self.vy = JUMP_FORCE

    def __get_image(self):
        return "enemy_flipped_0" if self.flipped_x else "enemy_0"

    def draw(self, camera_x):
        screen.blit(self.__get_image(), (self.x - camera_x - self.width/2, self.y - self.height/2))

class Flag(Actor):
    def __init__(self, x, y):
        super().__init__("flag", (x, y))

    def draw(self, camera_x):
        screen.blit(self.image, (self.x - camera_x - self.width/2, self.y - self.height/2))

# =====Instâncias de atores=====

menu_background = Actor("menu_background", (WIDTH // 2, HEIGHT // 2))
game_background = Actor("game_background", (WIDTH // 2, HEIGHT // 2))
win_background = Actor("win_background", (WIDTH // 2, HEIGHT // 2))
lose_background = Actor("lose_background", (WIDTH // 2, HEIGHT // 2))

back_button = Button("button_background", WIDTH // 2, 300, "Voltar")
start_button = Button("button_background", WIDTH // 2, 170, "Começar")
sound_button = Button("button_background", WIDTH // 2, 250, "Desligar Som")
exit_button = Button("button_background", WIDTH // 2, 330, "Sair")
menu_buttons = [start_button, sound_button, exit_button]

player = Player(32, 504)
enemy = Enemy(100, 504, 100, 500, jumping=True)
flag = Flag(2400, 504)

# =====Funções principais=====

def back_to_menu():
    global game_state
    game_state = MENU_STATE

def start_game():
    global game_state, player, enemy
    game_state = GAME_STATE
    player.x = 32
    player.y = 504
    player.vy = 0
    enemy.x = 100
    enemy.y = 504
    enemy.vy = 0

def toggle_sound():
    global sound_enabled, sound_button
    sound_enabled = not sound_enabled
    text = "Desligar Som" if sound_enabled else "Ligar Som"
    sound_button.text = text
    play_music_if_enabled("scent_of_forest")

def exit_game():
    exit()

back_button.on_click = back_to_menu
start_button.on_click = start_game
sound_button.on_click = toggle_sound
exit_button.on_click = exit_game

def check_collision_with_ground(actor):
    actor_bottom = actor.y + actor.height/2

    for x, y, tiles_num, tile_img in solid_tiles:
        for i in range(tiles_num):
            tile_x = x + i * TILE_SIZE
            tile_y = y
            tile_rect = Rect((tile_x, tile_y), (TILE_SIZE, TILE_SIZE))

            if (actor.x + actor.width/2 > tile_rect.left and
                actor.x - actor.width/2 < tile_rect.right):
                if actor_bottom >= tile_rect.top and actor_bottom <= tile_rect.top + actor.vy:
                    actor.y = tile_rect.top - actor.height/2
                    return True
    return False

def play_music_if_enabled(name, volume=1):
    music.stop()
    if sound_enabled:
        music.set_volume = volume
        music.play(name)

def play_sound_if_enabled(name):
    if sound_enabled:
        sound = getattr(sounds, name, None)
        if sound:
            sound.play()

def update():
    global game_state
    if game_state == GAME_STATE:
        player.update()
        enemy.update()
        if player.colliderect(enemy):
            play_sound_if_enabled("lose")
            game_state = LOSE_STATE
        elif player.colliderect(flag):
            play_sound_if_enabled("win")
            game_state = WIN_STATE

def draw():
    screen.clear()

    if game_state == MENU_STATE:
        draw_menu()
    elif game_state == GAME_STATE:
        game_background.draw()
        draw_tiles()
        player.draw(camera_x)
        enemy.draw(camera_x)
        flag.draw(camera_x)
    elif game_state == WIN_STATE:
        win_background.draw()
        back_button.draw()
    elif game_state == LOSE_STATE:
        lose_background.draw()
        back_button.draw()

def draw_tiles():
    screen_left  = camera_x
    screen_right = camera_x + WIDTH

    all_tiles = non_solid_tiles + solid_tiles

    for x, y, tiles_num, tile_img in all_tiles:
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
    if game_state == WIN_STATE or game_state == LOSE_STATE:
        if back_button.actor.collidepoint(pos):
            back_button.click()
