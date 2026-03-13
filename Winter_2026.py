import sys

# Constants & Setup
my_id = int(input())
width = int(input())
height = int(input())

my_snake_ids = []
opp_snake_ids = []
wall_position = set()

# ---  grille ---
grid = [input() for _ in range(height)]
for y in range(height):
    for x in range(width):
        if grid[y][x] == '#':
            wall_position.add((x, y))

# --- Fonction de mouvement PRENT EN COMPTE LES MUR ET LES SNAKE ADVERSE ---
def get_move(snake_id, head, power_sources, collision, width, height):
    hx, hy = head
    moves = {
        "LEFT": (hx - 1, hy),
        "RIGHT": (hx + 1, hy),
        "UP": (hx, hy - 1),
        "DOWN": (hx, hy + 1)
    }

    safe_moves = {name: pos for name, pos in moves.items() 
                  if 0 <= pos[0] < width and 0 <= pos[1] < height 
                  and pos not in collision}

    if not safe_moves:
        return "WAIT" 

    if power_sources:
        # Find closest food
        tx, ty = min(power_sources, key=lambda p: abs(p[0]-hx) + abs(p[1]-hy))
        # Choose the safe move that gets us closest to that food
        best_move = min(safe_moves.keys(), 
                        key=lambda m: abs(tx - safe_moves[m][0]) + abs(ty - safe_moves[m][1]))
        return best_move
    
    # Pas de save move alors Wait
    return list(safe_moves.keys())[0]

# --- start ---
snakebots_per_player = int(input())
for _ in range(snakebots_per_player):
    my_snake_ids.append(int(input()))
for _ in range(snakebots_per_player):
    opp_snake_ids.append(int(input()))

# Game Loop
while True:
    all_power = []
    snakes_data = {}
    turn_actions = []
    collision_map = set(wall_position)

    power_source_count = int(input())
    for _ in range(power_source_count):
        all_power.append(list(map(int, input().split())))

    snakebot_count = int(input())
    for _ in range(snakebot_count):
        data = input().split()
        s_id = int(data[0])
        body_str = data[1]
        
        coords = []
        for segment in body_str.split(':'):
            x, y = map(int, segment.split(','))
            coords.append((x, y))
        snakes_data[s_id] = coords
        
        # On ajoute tout les corps de snake aux collisions
        # Comme ça, on évite les adversaires et nous.
        collision_map.update(coords)

    # Generate actions
    for s_id in my_snake_ids:
        if s_id in snakes_data:
            head = snakes_data[s_id][0]
            move = get_move(s_id, head, all_power, collision_map, width, height)
            if move != "WAIT":
                turn_actions.append(f"{s_id} {move}")
            else:
                turn_actions.append(("WAIT"))

    if turn_actions:
        print(";".join(turn_actions))
