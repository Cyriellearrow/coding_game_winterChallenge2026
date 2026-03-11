import sys

# Constants & Setup
my_id = int(input())
width = int(input())
height = int(input())

# We store our snake IDs to know which ones to command
my_snake_ids = []
opp_snake_ids = []

def get_move(snake_id, head, power_sources):
    if not power_sources:
        return "WAIT"
    
    hx, hy = head
    # Find the closest power source using Manhattan distance
    target_x, target_y = min(power_sources, key=lambda p: abs(p[0]-hx) + abs(p[1]-hy))
    
    # Simple movement logic
    if target_x < hx: return "LEFT"
    if target_x > hx: return "RIGHT"
    if target_y < hy: return "UP"
    if target_y > hy: return "DOWN"
    return "WAIT"

# Initial Grid Map (if needed for collision later)
grid = [input() for _ in range(height)]

snakebots_per_player = int(input())
for _ in range(snakebots_per_player):
    my_snake_ids.append(int(input()))
for _ in range(snakebots_per_player):
    opp_snake_ids.append(int(input()))

# Game Loop
while True:
    all_power = []
    power_source_count = int(input())
    for _ in range(power_source_count):
        all_power.append(list(map(int, input().split())))

    snakebot_count = int(input())
    # Dictionary to store snake positions: { id: [(x, y), (x, y)] }
    snakes_data = {}
    
    for _ in range(snakebot_count):
        data = input().split()
        s_id = int(data[0])
        body_str = data[1]
        
        # Parse body "x,y:x,y" into list of tuples
        coords = []
        for segment in body_str.split(':'):
            x, y = map(int, segment.split(','))
            coords.append((x, y))
        snakes_data[s_id] = coords

    # Generate actions for all my snakes that are still alive
    turn_actions = []
    for s_id in my_snake_ids:
        if s_id in snakes_data:
            head = snakes_data[s_id][0]
            move = get_move(s_id, head, all_power)
            turn_actions.append(f"{s_id} {move}")

    # Print all actions for this turn separated by |
    if turn_actions:
        print(";".join(turn_actions))
    else:
        print("WAIT")