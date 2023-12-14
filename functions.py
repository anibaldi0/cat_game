
import pygame


def terminar():
    """
    Esta función no toma parametros.

    Parámetros:
    sale del juego.

    Devuelve:
    None.
    """
    pygame.quit()
    exit()

def wait_user():
    """
    Esta función no toma parametros.

    Parámetros:
    entra en bucle infinito para agregar una pausa al juego.

    Devuelve:
    return para salir del bucle
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminar()
                return
            
def show_paused_text(surface, texto, fuente, coordenadas, color_fuente):
    """
    Muestra un texto de pausa en la superficie especificada.

    Parametros:
    - surface: La superficie en la que se mostrara el texto de pausa.
    - texto: El texto que se mostrará.
    - fuente: El objeto de fuente utilizado para renderizar el texto.
    - coordenadas: La posición central donde se mostrará el texto.
    - color_fuente: El color del texto.

    No devuelve nada. Simplemente muestra el texto en la superficie especificada.
    """
    paused_text = fuente.render(texto, True, color_fuente)
    rect_paused_text = paused_text.get_rect()
    rect_paused_text.center = coordenadas
    surface.blit(paused_text, rect_paused_text)
    pygame.display.flip()

def save_score(player_name, best_score_number):
    """
    esta funcion recibe 2 parametros y guarda el nombre y mayor score.
    maneja 3 excepciones, uno para buscar y abrir el archivo donde se guardaran los datos, 
    otra para evaluar valores enteros y la otra para evaluar los indices de la lista 
    para acceder a los elementos del archivo.
    Por ultimo se compara el nuevo score con el previo y se guarda el nuevo si es mayor

    parametros: 
    - player_name: nombre del jugador
    - score: mayor score

    retorna None
    """
    try:
        with open("score.txt", "r") as file:
            line = file.readline()
            if line:
                previous_score_number = int(line.split()[1])
            else:
                previous_score_number = 0
    except (FileNotFoundError, ValueError, IndexError):
        previous_score_number = 0

    if best_score_number > previous_score_number:
        with open("score.txt", "w") as file:
            file.write("{0} {1}\n".format(player_name, best_score_number))


def load_score():
    try:
        with open("score.txt", "r") as file:
            line = file.readline()
            if line:
                values = line.split()
                if len(values) == 2:
                    player_name, best_score_number = values
                    return player_name, int(best_score_number)
                else:
                    print("Invalid data format in score.txt. Using default values.")
                    return None, 0
            else:
                return None, 0
    except FileNotFoundError:
        return None, 0






