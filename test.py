import pygame
import math

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
window_size = (1920, 1080)
screen = pygame.display.set_mode(window_size)

# Taille des cellules
base_cell_size = 20
cell_size = base_cell_size

# Définir le centre de la grille comme (0, 0) au départ
grid_offset_x = window_size[0] // 2
grid_offset_y = window_size[1] // 2

# Facteur de zoom
zoom_factor = 1.0
zoom_speed = 0.1

# Grille pour stocker les cellules vivantes
cells = set()

# Variables pour gérer le déplacement
panning = False  # Indique si on est en train de déplacer la grille
last_mouse_pos = None  # Stocke la dernière position de la souris

def draw_grid():
    for x in range(-20, 21):  # Une portion de la grille
        for y in range(-20, 21):
            # Décaler les coordonnées pour que les lignes partent des centres des cases
            rect_x = round(grid_offset_x + x * cell_size)
            rect_y = round(grid_offset_y + y * cell_size)

            # Définition de l'épaisseur des lignes
            thin_line = 1  # Épaisseur normale
            thick_line = 2  # Épaisseur pour les lignes toutes les 10 cellules

            # Vérifier si c'est une ligne majeure (toutes les 10 cellules)
            if x % 10 == 0:
                pygame.draw.line(screen, (66, 66, 66), (rect_x, 0), (rect_x, screen.get_height()), thick_line)
            else:
                pygame.draw.line(screen, (66, 66, 66), (rect_x, 0), (rect_x, screen.get_height()), thin_line)

            if y % 10 == 0:
                pygame.draw.line(screen, (66, 66, 66), (0, rect_y), (screen.get_width(), rect_y), thick_line)
            else:
                pygame.draw.line(screen, (66, 66, 66), (0, rect_y), (screen.get_width(), rect_y), thin_line)


def draw_cells():
    grid_line_width = 1  # Épaisseur de la grille normale
    padding = 1  # Marge fine pour éviter les chevauchements

    # Calcul de la taille réelle de la cellule, en tenant compte de la grille
    adjusted_size = cell_size - grid_line_width - padding
    adjusted_size = max(adjusted_size, 1)  # Eviter les tailles trop petites

    for (x, y) in cells:
        # Calculer les coordonnées pour que le centre des cellules corresponde aux points d'intersection
        rect_x = grid_offset_x + x * cell_size
        rect_y = grid_offset_y + y * cell_size


        # Dessiner la cellule
        pygame.draw.rect(screen, (255, 255, 255), 
                         pygame.Rect(rect_x, rect_y, adjusted_size, adjusted_size))



def adjust_coordinates(mouse_x, mouse_y):
    # Convertir les coordonnées de la souris en coordonnées de la grille
    grid_x = (mouse_x - grid_offset_x) / cell_size
    grid_y = (mouse_y - grid_offset_y) / cell_size
    
    # Arrondir pour obtenir la cellule la plus proche
    grid_x = math.floor(grid_x)
    grid_y = math.floor(grid_y)
    
    # Limiter les coordonnées pour éviter des valeurs aberrantes
    grid_x = max(min(grid_x, 20), -20)  # Limite à la portion visible de la grille
    grid_y = max(min(grid_y, 20), -20)
    
    return grid_x, grid_y


running = True
while running:
    screen.fill((0, 0, 0))  # Erase screen
    draw_grid()
    draw_cells()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # left click -> add new living cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = adjust_coordinates(mouse_x, mouse_y)  # Utiliser la même méthode que le sélecteur
                cells.add((grid_x, grid_y))  # Ajouter la cellule au bon endroit


            elif event.button == 3:  # right click -> begin movement
                panning = True
                last_mouse_pos = pygame.mouse.get_pos()  # Save mouse pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # release right click
                panning = False
                last_mouse_pos = None

        if event.type == pygame.MOUSEMOTION:
            if panning and last_mouse_pos:
                # calculate mouse movements
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - last_mouse_pos[0]
                dy = mouse_y - last_mouse_pos[1]

                #  Apply displacement to the grid offset
                grid_offset_x += dx
                grid_offset_y += dy

                # Update latest mouse pos 
                last_mouse_pos = (mouse_x, mouse_y)

        if event.type == pygame.MOUSEWHEEL:
            # Sauvegarde de la position actuelle du curseur en coordonnées de grille avant le zoom
            mouse_x, mouse_y = pygame.mouse.get_pos()
            before_zoom_x = (mouse_x - grid_offset_x) / cell_size
            before_zoom_y = (mouse_y - grid_offset_y) / cell_size

            # Appliquer le zoom
            if event.y > 0:  # Zoom in
                new_zoom_factor = zoom_factor + zoom_speed
            elif event.y < 0:  # Zoom out
                new_zoom_factor = max(zoom_factor - zoom_speed, zoom_speed)

            # Mise à jour de la taille des cellules en fonction du zoom
            new_cell_size = int(base_cell_size * new_zoom_factor)

            # Correction : recalcul précis de l'offset en fonction du facteur de zoom
            grid_offset_x = mouse_x - before_zoom_x * new_cell_size
            grid_offset_y = mouse_y - before_zoom_y * new_cell_size

            # Appliquer le zoom uniquement après recalcul précis de l'offset
            zoom_factor = new_zoom_factor
            cell_size = new_cell_size



    #Show square for the selection
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = adjust_coordinates(mouse_x, mouse_y)
    rect_x = grid_offset_x + grid_x * cell_size
    rect_y = grid_offset_y + grid_y * cell_size
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rect_x, rect_y, cell_size, cell_size), 1)

    # Refresh screen
    pygame.display.flip()

pygame.quit()