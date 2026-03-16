import sys

# ─── Lecture de la grille initiale ───
my_id = int(input())
width = int(input())
height = int(input())

my_snake_ids = []
opp_snake_ids = []
walls = set()

grid = [input().strip() for _ in range(height)]
for y in range(height):
    for x in range(width):
        if grid[y][x] == '#':
            walls.add((x, y))

# ─── Fonctions utilitaires ───

def manhattan(a, b):
    """Distance de Manhattan entre deux points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_snake_length(snake_id, snakes_data):
    """Retourne la longueur actuelle du serpent"""
    if snake_id not in snakes_data:
        return 0
    return len(snakes_data[snake_id])


def get_reachable_powers(snake_id, power_sources, snakes_data):
    """
    Retourne uniquement les power sources que le serpent peut atteindre
    avec sa longueur actuelle
    """
    length = get_snake_length(snake_id, snakes_data)
    reachable = []
    for px, py in power_sources:
        # Approximation : on considère qu'on peut manger si la distance ≤ longueur
        if manhattan((px, py), snakes_data[snake_id][0]) <= length + 5:  # marge
            reachable.append((px, py))
    return reachable


def get_safe_moves(head, collision, w, h):
    """Retourne les directions possibles et leur nouvelle position"""
    hx, hy = head
    candidates = {
        "LEFT":  (hx - 1, hy),
        "RIGHT": (hx + 1, hy),
        "UP":    (hx, hy - 1),
        "DOWN":  (hx, hy + 1)
    }

    safe = {}
    for direction, (nx, ny) in candidates.items():
        if (0 <= nx < w and 0 <= ny < h and (nx, ny) not in collision):
            safe[direction] = (nx, ny)
    
    return safe


def choose_best_move(snake_id, head, power_sources, collision, w, h, snakes_data):
    safe_moves = get_safe_moves(head, collision, w, h)
    
    if not safe_moves:
        return "WAIT"

    # On filtre les power sources atteignables
    targets = get_reachable_powers(snake_id, power_sources, snakes_data)
    
    if not targets:
        return list(safe_moves.keys())[0]

    # On choisit la cible la plus proche (Manhattan)
    closest_target = min(targets, key=lambda p: manhattan(head, p))
    tx, ty = closest_target

    # Parmi les mouvements sûrs, celui qui réduit le plus la distance
    best_dir = min(
        safe_moves.keys(),
        key=lambda d: manhattan(safe_moves[d], (tx, ty))
    )

    return best_dir


# ─── Lecture des identifiants de serpents ───
snakebots_per_player = int(input())
for _ in range(snakebots_per_player):
    my_snake_ids.append(int(input()))

for _ in range(snakebots_per_player):
    opp_snake_ids.append(int(input()))


# ─── Boucle de jeu ───
while True:
    power_sources = []
    snakes_data = {}
    collision = set(walls)          # on commence avec les murs

    # Power sources (nourriture / power-up)
    power_count = int(input())
    for _ in range(power_count):
        x, y = map(int, input().split())
        power_sources.append((x, y))

    # Tous les serpents (y compris le nôtre)
    snake_count = int(input())
    for _ in range(snake_count):
        line = input().split()
        sid = int(line[0])
        body_str = line[1]

        segments = []
        for part in body_str.split(':'):
            if part:  # évite les ':' en trop
                x, y = map(int, part.split(','))
                segments.append((x, y))

        snakes_data[sid] = segments
        
        # On ajoute TOUTES les parties du corps à la collision
        # (y compris la tête → évite les collisions frontales)
        collision.update(segments)

    # On enlève notre propre tête des collisions pour pouvoir bouger
    for sid in my_snake_ids:
        if sid in snakes_data and snakes_data[sid]:
            collision.discard(snakes_data[sid][0])

    # Génération des actions pour tous nos serpents
    actions = []
    for sid in my_snake_ids:
        if sid not in snakes_data or not snakes_data[sid]:
            continue
            
        head = snakes_data[sid][0]
        direction = choose_best_move(
            sid, head, power_sources, collision, width, height, snakes_data
        )
        
        if direction != "WAIT":
            actions.append(f"{sid} {direction}")

    # Sortie
    if actions:
        print(";".join(actions))
    else:
        print("WAIT") 
