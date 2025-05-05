import pygame
import math

pygame.init()

window_size = (1920, 1080)
screen = pygame.display.set_mode(window_size)
base_cell_size = 20
cell_size = base_cell_size


grid_offset_x = window_size[0] // 2
grid_offset_y = window_size[1] // 2

zoom_factor = 1.0
zoom_speed = 0.1
cells = set()

panning = False
last_mouse_pos = None

def draw_grid():
    """ Dessine la grille avec correction d'alignement """
    screen.fill((0, 0, 0))  # Efface l'écran

    # Trouver les bords de la grille visible
    start_x = int((0 - grid_offset_x) / cell_size) - 1
    end_x = int((window_size[0] - grid_offset_x) / cell_size) + 2
    start_y = int((0 - grid_offset_y) / cell_size) - 1
    end_y = int((window_size[1] - grid_offset_y) / cell_size) + 2

    for x in range(start_x, end_x):
        rect_x = round(grid_offset_x + x * cell_size)
        pygame.draw.line(screen, (66, 66, 66), (rect_x, 0), (rect_x, window_size[1]), 1)

    for y in range(start_y, end_y):
        rect_y = round(grid_offset_y + y * cell_size)
        pygame.draw.line(screen, (66, 66, 66), (0, rect_y), (window_size[0], rect_y), 1)

def draw_cells():
    """ Dessine les cellules vivantes """
    for (x, y) in cells:
        rect_x = round(grid_offset_x + x * cell_size)
        rect_y = round(grid_offset_y + y * cell_size)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(rect_x, rect_y, cell_size - 1, cell_size - 1))

def adjust_coordinates(mouse_x, mouse_y):
    grid_x = math.floor((mouse_x - grid_offset_x) / cell_size)
    grid_y = math.floor((mouse_y - grid_offset_y) / cell_size)
    return grid_x, grid_y

running = True
while running:
    screen.fill((0, 0, 0))  # Efface l'écran
    draw_grid()
    draw_cells()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche -> ajouter une cellule
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = adjust_coordinates(mouse_x, mouse_y)
                if (grid_x, grid_y) in cells:
                    cells.remove((grid_x, grid_y))
                else:
                    cells.add((grid_x, grid_y))

            elif event.button == 3:  # Clic droit -> début du déplacement
                panning = True
                last_mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Arrêter le déplacement
                panning = False
                last_mouse_pos = None

        if event.type == pygame.MOUSEMOTION:
            if panning and last_mouse_pos:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - last_mouse_pos[0]
                dy = mouse_y - last_mouse_pos[1]
                grid_offset_x += dx
                grid_offset_y += dy
                last_mouse_pos = (mouse_x, mouse_y)

        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            before_zoom_x = (mouse_x - grid_offset_x) / cell_size
            before_zoom_y = (mouse_y - grid_offset_y) / cell_size

            if event.y > 0:
                zoom_factor += zoom_speed
            elif event.y < 0:
                zoom_factor = max(zoom_factor - zoom_speed, zoom_speed)

            new_cell_size = int(base_cell_size * zoom_factor)
            grid_offset_x = mouse_x - before_zoom_x * new_cell_size
            grid_offset_y = mouse_y - before_zoom_y * new_cell_size
            cell_size = new_cell_size

    # Afficher la sélection
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = adjust_coordinates(mouse_x, mouse_y)
    rect_x = round(grid_offset_x + grid_x * cell_size)
    rect_y = round(grid_offset_y + grid_y * cell_size)
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(rect_x, rect_y, cell_size, cell_size), 1)

    pygame.display.flip()

pygame.quit()
