import random

# Define the desired number of positions for each list
num_positions_dblocks1 = 60
num_positions_dblocks2 = 40
num_positions_dblocks3 = 20

# Define the position lists
Dblocks_positions1 = [[(600, 780), (480, 240), (840, 660), (240, 660), (960, 720), (720, 660), (480, 240), (240, 660), (360, 240), (1080, 240), (1020, 660), (840, 360), (600, 780), (600, 420), (600, 300), (960, 420), (420, 300), (660, 660), (1080, 60), (240, 180), (660, 780), (300, 300), (780, 660), (960, 540), (360, 360), (540, 780), (1020, 300), (240, 180), (360, 480), (960, 780), (300, 60), (900, 180), (720, 780), (960, 360), (960, 420), (240, 240), (840, 660), (720, 720), (240, 480), (360, 180), (840, 300), (600, 720), (600, 600), (540, 780), (540, 660), (360, 600), (840, 780)]]
Dblocks_positions2 = [[(480, 60), (1080, 60), (840, 360), (420, 180), (900, 420), (840, 600), (720, 720), (240, 600), (300, 420), (240, 300), (720, 720), (720, 540), (240, 300), (480, 600), (420, 60), (360, 540), (360, 180), (480, 240), (600, 660), (1080, 420), (780, 660), (660, 420), (420, 300), (1080, 660), (420, 180), (600, 120), (240, 480), (960, 300), (300, 60), (960, 240), (600, 180), (720, 240), (420, 660), (240, 480), (660, 180), (960, 420), (720, 660), (240, 360), (720, 360), (720, 780), (600, 180), (300, 180), (360, 420), (1080, 180), (600, 480), (420, 300), (420, 780)]]
Dblocks_positions3 = [[(420, 420), (840, 720), (240, 180), (1080, 180), (360, 180), (780, 420), (960, 600), (660, 780), (960, 360), (660, 420), (480, 540), (600, 720), (900, 60), (600, 60), (360, 600), (240, 180), (600, 240), (720, 600), (1080, 660), (600, 660), (840, 600), (600, 660), (600, 360), (360, 360), (540, 300), (1080, 540), (240, 600), (900, 780), (360, 120), (360, 660), (600, 480), (1020, 660), (360, 600), (900, 180), (540, 660), (1020, 300), (360, 660), (1020, 60), (1020, 420), (600, 180), (960, 600), (1080, 780), (1080, 780), (480, 180), (1020, 660), (360, 420), (420, 180)]]

# Function to evenly distribute positions without repetition
def distribute_positions(positions, num_positions):
    distributed_positions = []
    total_positions = len(positions)
    if total_positions == 0 or num_positions == 0:
        return distributed_positions  # Return an empty list if no positions available or no positions requested
    
    random.shuffle(positions)  # Shuffle the positions list
    step_size = total_positions // num_positions
    for i in range(num_positions):
        index = i * step_size
        if index < total_positions:
            distributed_positions.append(positions[index])
    return distributed_positions

# Distribute positions for each list
dblocks1 = distribute_positions(Dblocks_positions1[0].copy(), num_positions_dblocks1)
dblocks2 = distribute_positions(Dblocks_positions2[0].copy(), num_positions_dblocks2)
dblocks3 = distribute_positions(Dblocks_positions3[0].copy(), num_positions_dblocks3)

# Define key positions and door positions
key_position1, key_position2, key_position3 = (360,180), (360,180), (360,180)
door_position1, door_position2, door_position3 = (360,300), (360,300), (360,300)

# Find new key positions satisfying the conditions
new_key_position1 = random.choice(dblocks1)
new_key_position2 = random.choice(dblocks2)
new_key_position3 = random.choice(dblocks3)

# Find new door positions satisfying the conditions
door_positions = [pos for pos in dblocks1 + dblocks2 + dblocks3 if pos != new_key_position1 and pos != new_key_position2 and pos != new_key_position3]
new_door_position1 = random.choice(door_positions)
door_positions.remove(new_door_position1)
new_door_position2 = random.choice(door_positions)
door_positions.remove(new_door_position2)
new_door_position3 = random.choice(door_positions)

# Print the new positions
print("New Key Position 1:", new_key_position1)
print("New Key Position 2:", new_key_position2)
print("New Key Position 3:", new_key_position3)
print("New Door Position 1:", new_door_position1)
print("New Door Position 2:", new_door_position2)
print("New Door Position 3:", new_door_position3)
