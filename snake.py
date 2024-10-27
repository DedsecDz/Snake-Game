import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
GAME_WIDTH, GAME_HEIGHT = 700, 500  # Dimensions initiales de la zone de jeu pour le Snake
GAME_OFFSET_X, GAME_OFFSET_Y = 50, 50  # Décalage initial de la zone de jeu sur la fenêtre principale
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
YELLOW_CUSTOM = (217, 171, 29)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

# Fontes
default_font = pygame.font.SysFont(None, 74) 
small_font = pygame.font.SysFont(None, 36)
title_menu_font = pygame.font.Font("Font/tehisa-font/Terasong-mLZ3a.ttf", 100)

# Variables du jeu
clock = pygame.time.Clock()
difficulty = "Medium"
mode = "Classic"
snake_speed = 15

# Image
background = "Image/Background.jpg"

# Classe pour gérer le jeu Snake
class SnakeGamePlay:
    def __init__(self):
        self.reset_game()
        self.update_game_surface()

    def update_game_surface(self):
        # Met à jour la surface de jeu en fonction des nouvelles dimensions
        global GAME_WIDTH, GAME_HEIGHT, GAME_OFFSET_X, GAME_OFFSET_Y
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    def generate_food(self):
        return [
            random.randrange(GAME_OFFSET_X, GAME_OFFSET_X + GAME_WIDTH, 10),
            random.randrange(GAME_OFFSET_Y, GAME_OFFSET_Y + GAME_HEIGHT, 10)
        ]

    def draw_elements(self):
        # Charger et afficher l'image de fond
        background_image = pygame.image.load(background)
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        win.blit(background_image, (0, 0))

        # Remplir la surface de jeu avec un fond noir
        self.game_surface.fill(BLACK)
        
        # Dessiner le cadre autour de l'aire de jeu
        pygame.draw.rect(win, GRAY, (GAME_OFFSET_X - 5, GAME_OFFSET_Y - 5, GAME_WIDTH + 10, GAME_HEIGHT + 10), 5)

        # Dessiner le serpent
        for pos in self.snake_pos:
            pygame.draw.rect(self.game_surface, GREEN, pygame.Rect(pos[0] - GAME_OFFSET_X, pos[1] - GAME_OFFSET_Y, 10, 10))

        # Dessiner la nourriture
        pygame.draw.rect(self.game_surface, RED, pygame.Rect(self.food_pos[0] - GAME_OFFSET_X, self.food_pos[1] - GAME_OFFSET_Y, 10, 10))

        # Copier la surface de jeu noire mise à jour dans la fenêtre principale
        win.blit(self.game_surface, (GAME_OFFSET_X, GAME_OFFSET_Y))

        # Afficher le score
        score_text = small_font.render(f"Score: {self.score}", True, WHITE)
        win.blit(score_text, [10, 10])

        pygame.display.update()

    def move_snake(self):
        if self.snake_direction == 'UP':
            new_head = [self.snake_pos[0][0], self.snake_pos[0][1] - 10]
        elif self.snake_direction == 'DOWN':
            new_head = [self.snake_pos[0][0], self.snake_pos[0][1] + 10]
        elif self.snake_direction == 'LEFT':
            new_head = [self.snake_pos[0][0] - 10, self.snake_pos[0][1]]
        elif self.snake_direction == 'RIGHT':
            new_head = [self.snake_pos[0][0] + 10, self.snake_pos[0][1]]

        # Ajoute la nouvelle tête au début du corps du serpent
        self.snake_pos.insert(0, new_head)

    def check_collisions(self):
        # Collision avec la nourriture
        if self.snake_pos[0] == self.food_pos:
            self.food_spawn = False
            self.score += 10
        else:
            self.snake_pos.pop() 

        if not self.food_spawn:
            self.food_pos = self.generate_food()
        self.food_spawn = True

        # Collision avec les murs de la zone de jeu
        if (self.snake_pos[0][0] < GAME_OFFSET_X or self.snake_pos[0][0] >= GAME_OFFSET_X + GAME_WIDTH or
                self.snake_pos[0][1] < GAME_OFFSET_Y or self.snake_pos[0][1] >= GAME_OFFSET_Y + GAME_HEIGHT):
            return True

        # Collision avec soi-même
        for block in self.snake_pos[1:]:
            if self.snake_pos[0] == block:
                return True

        return False

    def change_direction(self, event):
        if event.key == pygame.K_UP and self.snake_direction != 'DOWN':
            self.snake_direction = 'UP'
        if event.key == pygame.K_DOWN and self.snake_direction != 'UP':
            self.snake_direction = 'DOWN'
        if event.key == pygame.K_LEFT and self.snake_direction != 'RIGHT':
            self.snake_direction = 'LEFT'
        if event.key == pygame.K_RIGHT and self.snake_direction != 'LEFT':
            self.snake_direction = 'RIGHT'

    def reset_game(self):
        # Réinitialise la position du serpent et d'autres variables
        self.snake_pos = [[GAME_OFFSET_X + 100, GAME_OFFSET_Y + 50], [GAME_OFFSET_X + 90, GAME_OFFSET_Y + 50], [GAME_OFFSET_X + 80, GAME_OFFSET_Y + 50]]
        self.snake_direction = 'RIGHT'
        self.food_pos = self.generate_food()
        self.food_spawn = True
        self.score = 0

# Classe pour créer et gérer les boutons
class Button:
    def __init__(self, text, x, y, w, h, inactive_color, active_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.clicked = False  

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Change de couleur en fonction de la position de la souris
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(surface, self.active_color, (self.x, self.y, self.width, self.height))
            
            # Vérifie si le bouton de la souris est enfoncé
            if click[0] == 1:
                self.clicked = True

            # Si le bouton a été enfoncé et est relâché, déclenche l'action
            if click[0] == 0 and self.clicked:
                self.clicked = False
                if self.action is not None:
                    self.action()
        else:
            pygame.draw.rect(surface, self.inactive_color, (self.x, self.y, self.width, self.height))
            self.clicked = False  

        # Affiche le texte centré sur le bouton
        draw_text(self.text, small_font, WHITE, surface, self.x + (self.width // 2), self.y + (self.height // 2))

    def update_position(self, new_x, new_y):
        # Mettre à jour la position du bouton
        self.x = new_x
        self.y = new_y


# Fonction pour dessiner du texte centré
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Fonction pour quitter le jeu proprement
def quit_game():
    pygame.quit()
    sys.exit()

# Classe pour gérer le menu
class Menu:
    def __init__(self, title=None, title_color=None, font=None, background_image=None, background_color=BLACK):
        self.buttons = []
        self.title = title
        self.title_color = title_color
        self.font = font if font else default_font
        self.background_image = None
        self.background_color = background_color

        # Charger l'image de fond si configurée
        if background_image:
            self.background_image = pygame.image.load(background_image)
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

    def update_size(self):
        global WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, GAME_OFFSET_X, GAME_OFFSET_Y
        
        # Mettre à jour les dimensions globales
        GAME_WIDTH = WIDTH - 100
        GAME_HEIGHT = HEIGHT - 100
        GAME_OFFSET_X = (WIDTH - GAME_WIDTH) // 2
        GAME_OFFSET_Y = (HEIGHT - GAME_HEIGHT) // 2

        # Recalculer les positions des boutons en fonction des nouvelles dimensions
        for index, button in enumerate(self.buttons):
            # Met à jour la position du bouton
            new_x = (WIDTH // 2) - (button.width // 2)
            new_y = (HEIGHT // 2 - 50) + (index * 60) 
            button.update_position(new_x, new_y)

        # Redimensionner l'image de fond si elle est présente
        if self.background_image:
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        # Mettre à jour la surface de jeu globale
        game.snake_gameplay.update_game_surface()

    def add_button(self, text, x, y, w, h, inactive_color, active_color, action):
        button = Button(text, x, y, w, h, inactive_color, active_color, action)
        self.buttons.append(button)
    
    def draw_title(self):
        if self.title:
            draw_text(self.title, self.font, self.title_color, win, WIDTH // 2, HEIGHT // 6)

    def display(self):
        if self.background_image:
            # Si background_image 
            scaled_background = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
            win.blit(scaled_background, (0, 0))
        else:
            # Background couleur uniforme
            win.fill(self.background_color)

        self.draw_title()
        for button in self.buttons:
            button.draw(win)
        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                elif event.type == pygame.VIDEORESIZE:
                    # Mettre à jour les dimensions globales
                    global WIDTH, HEIGHT
                    WIDTH, HEIGHT = event.w, event.h
                    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                    # Mettre à jour la taille du menu
                    self.update_size()

            # Afficher le menu mis à jour
            self.display()

# Classe principale du jeu Snake
class SnakeGame:
    def __init__(self):
        self.main_menu = Menu(title="Snake Game", title_color=YELLOW_CUSTOM, background_image=background, font=title_menu_font)
        self.mode_menu = Menu(title="Select Mode",  title_color=YELLOW_CUSTOM, background_image=background)
        self.difficulty_menu = Menu(title="Select Difficulty",  title_color=YELLOW_CUSTOM, background_image=background)
        self.game_over_menu = Menu(title="Game Over !", title_color=WHITE, font=title_menu_font)
        self.snake_gameplay = SnakeGamePlay()  

        self.setup_main_menu()
        self.setup_mode_menu()
        self.setup_difficulty_menu()
        self.setup_game_over_menu()

    def setup_main_menu(self):
        self.main_menu.add_button("Start", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GREEN, DARK_GREEN, self.show_mode_menu)
        self.main_menu.add_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GREEN, DARK_GREEN, quit_game)

    def setup_mode_menu(self):
        self.mode_menu.add_button("Classic", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GREEN, DARK_GREEN, lambda: self.set_mode("Classic"))
        self.mode_menu.add_button("In Progress...", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GREEN, DARK_GREEN, self.show_main_menu)
        self.mode_menu.add_button("Back", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50, GREEN, DARK_GREEN, self.show_main_menu)

    def setup_difficulty_menu(self):
        self.difficulty_menu.add_button("Easy", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GREEN, DARK_GREEN, lambda: self.set_difficulty("Easy"))
        self.difficulty_menu.add_button("Medium", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GREEN, DARK_GREEN, lambda: self.set_difficulty("Medium"))
        self.difficulty_menu.add_button("Hard", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GREEN, DARK_GREEN, lambda: self.set_difficulty("Hard"))
        self.difficulty_menu.add_button("Back", WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50, GREEN, DARK_GREEN, self.show_mode_menu)

    def setup_game_over_menu(self):
        self.game_over_menu.add_button("Restart", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, GREEN, DARK_GREEN, self.start_game)
        self.game_over_menu.add_button("Menu", WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50, GREEN, DARK_GREEN, self.show_main_menu)
        self.game_over_menu.add_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50, GREEN, RED, quit_game)

    def show_main_menu(self):
        self.main_menu.run()

    def show_mode_menu(self):
        self.mode_menu.run()

    def show_difficulty_menu(self):
        self.difficulty_menu.run()

    def show_game_over_menu(self):
        self.game_over_menu.run()

    def set_mode(self, selected_mode):
        global mode
        mode = selected_mode
        self.show_difficulty_menu()

    def set_difficulty(self, selected_difficulty):
        global difficulty, snake_speed
        difficulty = selected_difficulty

        # Changer la vitesse en fonction de la difficulté
        if difficulty == "Easy":
            snake_speed = 10
        elif difficulty == "Medium":
            snake_speed = 15
        elif difficulty == "Hard":
            snake_speed = 20

        self.start_game()

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.KEYDOWN:
                    self.snake_gameplay.change_direction(event)
                elif event.type == pygame.VIDEORESIZE:
                    # Mettre à jour les dimensions globales et ajuster la surface de jeu
                    global WIDTH, HEIGHT
                    WIDTH, HEIGHT = event.w, event.h
                    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                    # Utiliser la méthode update_size pour ajuster les dimensions
                    game.main_menu.update_size()
                    game.mode_menu.update_size()
                    game.difficulty_menu.update_size()
                    game.game_over_menu.update_size()

            # Déplacer le serpent
            self.snake_gameplay.move_snake()

            # Vérifier les collisions
            if self.snake_gameplay.check_collisions():
                running = False  # Fin de la partie si ya colision

            # Redessiner les éléments
            self.snake_gameplay.draw_elements()

            # Contrôle de la vitesse du jeu selon la difficulté
            clock.tick(snake_speed)

        # Affiche le score et propose de rejouer ou de retourner au menu
        self.snake_gameplay.reset_game()
        self.show_game_over_menu()


# Lancement du jeu
if __name__ == "__main__":
    game = SnakeGame()
    game.show_main_menu()
