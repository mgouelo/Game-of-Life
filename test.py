import pygame

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)

# Taille de base des cellules
base_cell_size = 20
cell_size = base_cell_size  # Taille actuelle de la cellule

# Facteur de zoom (initialisé à 1, ce qui signifie aucun zoom)
zoom_factor = 1.0
zoom_speed = 0.1  # Vitesse du zoom

# Nombre de cellules dans chaque direction (en fonction de la taille de la fenêtre et de la taille des cellules)
cols = window_size[0] // cell_size
rows = window_size[1] // cell_size

# Grille pour stocker les cellules vivantes
cells = set()  # Utilisation d'un set pour garder uniquement les cellules vivantes

# Fonction pour dessiner la grille
def draw_grid():
    for x in range(0, window_size[0], cell_size):
        for y in range(0, window_size[1], cell_size):
            # Dessiner les lignes de la grille
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, cell_size, cell_size), 1)

# Fonction pour dessiner les cellules vivantes
def draw_cells():
    for (x, y) in cells:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

# Fonction pour ajuster les coordonnées avec zoom
def adjust_coordinates(mouse_x, mouse_y):
    # Appliquer le facteur de zoom pour obtenir les coordonnées logiques
    grid_x = mouse_x // cell_size
    grid_y = mouse_y // cell_size
    return grid_x, grid_y

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))  # Effacer l'écran avec du noir
    draw_grid()  # Dessiner la grille
    draw_cells()  # Dessiner les cellules vivantes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Quand l'utilisateur clique sur la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Si clic gauche
                # Récupérer les coordonnées de la souris en pixels
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Ajuster les coordonnées en fonction du zoom
                grid_x, grid_y = adjust_coordinates(mouse_x, mouse_y)

                # Ajouter la cellule vivante à la grille
                cells.add((grid_x, grid_y))

        # Zoom avec la molette de la souris
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Molette vers le haut (zoom avant)
                zoom_factor += zoom_speed
            elif event.y < 0:  # Molette vers le bas (zoom arrière)
                zoom_factor = max(zoom_factor - zoom_speed, zoom_speed)

            # Mettre à jour la taille des cellules en fonction du facteur de zoom
            cell_size = int(base_cell_size * zoom_factor)

    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()
