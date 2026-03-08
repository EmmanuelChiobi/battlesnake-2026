# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Shadow Wizard Money Gang",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def flood_fill(coordinate: typing.Dict, occupied_squares: typing.Dict, filled_squares: typing.Dict, width, height):
    # base case: x coordinate is < 0
    if(coordinate['x'] < 0):
        return
    # base case: x coordinate is > width of board
    if(coordinate['x'] > width):
        return
    # base case: y coordinate is < 0
    if(coordinate['y'] < 0):
        return
    # base case: y coordinate is > height of board
    if(coordinate['y'] > height):
        return
    # base case: we are in an occupied square, skip it.
    for dict in occupied_squares:
        if (coordinate['x'] in dict['x']) and (coordinate['y'] in dict['y']):
            return
    # base case, we're in a filled square, skip it.
    for dict in filled_squares:
        if (coordinate['x'] in dict['x']) and (coordinate['y'] in dict['y']):
            return
    
    # append the current coordinate to the filled_squares list.
    new_coordinate_to_be_filled = {
        "x": -1,
        "y": -1
    }
    new_coordinate_to_be_filled['x'] = coordinate['x']
    new_coordinate_to_be_filled['y'] = coordinate['y']
    filled_squares.append(new_coordinate_to_be_filled)

    next_left = {
        "x": coordinate['x'] - 1,
        "y": coordinate['y']
    }
    next_left = typed.Dict(next_left)
    next_up = {
        "x": coordinate['x'],
        "y": coordinate['y'] + 1
    }
    next_up = typed.Dict(next_up)
    next_right = {
        "x": coordinate['x'] + 1,
        "y": coordinate['y']
    }
    next_right = typed.Dict(next_right)
    next_down = {
        "x": coordinate['x'],
        "y": coordinate['y'] - 1
    }
    next_down = typed.Dict(next_down)
    #
    # recursively fill the squares in the cardinal directions.
    #
    flood_fill(next_left, occupied_squares, filled_squares, width, height)
    flood_fill(next_up, occupied_squares, filled_squares, width, height)
    flood_fill(next_right, occupied_squares, filled_squares, width, height)
    flood_fill(next_down, occupied_squares, filled_squares, width, height)

def flood_fill_game_state(game_state: typing.Dict) -> typing.Dict:
    # first get the width and height of the board from game state.
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    empty_square_found = False
    coordinate = {
        "x": -1,
        "y": -1
    }
    #
    # This contains where all snake body parts are
    #
    occupied_squares = {}
    occupied_squares = typing.Dict(occupied_squares)

    #
    # This dictionary will contain which squares get filled.
    #
    filled_squares = {}
    filled_squares = typing.Dict(filled_squares)

    # check for any empty squares on the corners, best to start the flood-fill analysis there.
    # if a snake occupies one corner
    for dict in game_state['snakes']:
        occupied_squares.append(dict["body"])
        if dict['head']['x'] != 0:
            coordinate['x'] = 0
            if dict['head']['y'] != 0:
                empty_square_found = True
                break
            if dict['head']['y'] != board_height:
                empty_square_found = True
                break
        elif dict['head']['x'] != board_width:
            coordinate['x'] = board_width
            if dict['head']['y'] != 0:
                empty_square_found = True
                break
            if dict['head']['y'] != board_height:
                empty_square_found = True
                break
    if empty_square_found == True:
        # Easy case, start the flood fill from the corners.
        flood_fill(coordinate, occupied_squares, filled_squares, board_width, board_height)
    else:
        # Use the first food tile if the corners are unavailable.
        coordinate['x'] = game_state['board']['food'][0]['x']
        coordinate['y'] = game_state['board']['food'][0]['y']
        flood_fill(coordinate, occupied_squares, filled_squares, board_width, board_height)
    
    return filled_squares



#
# High-level strategy:
# - 

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    # this array is saying "is this move going to end in a collision or not"
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    filled_squares = {}
    filled_squares = typing.Dict(filled_squares)
    opponents = game_state['board']['snakes']
    num_snakes = len(opponents)

    current_heuristic = 0 # 0 = defense, 1 = offense
    is_recovering_health = False

    if game_state["you"]["health"] < 30:
        # below 30 health, start seeking food
        is_recovering_health = True
    
    if (num_opponents == 2):
        current_heuristic = 1 # switch to offense for the two-snake case


    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    if (my_head["x"] == 0):
        # implies that the head is right at the left edge of the board
        is_move_safe["left"] = False
    if (my_head["x"] == board_width):
        # implies that the head is at the right edge of the board
        is_move_safe["right"] = False
    if (my_head["y"] == 0):
        # implies the head is at the bottom of the board
        is_move_safe["down"] = False
    if (my_head["y"] == board_height):
        # implies the head is at the top of the board
        is_move_safe["up"] = False


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body'] # the part immediately after the neck
    for i in range(1, game_state['you']['length']-1):
        # last part of length is the tail itself, which always recedes so do not count the tail in the segments we are checking.
        if ((my_head["y"] - 1) == my_body[i]["y"]):
            # implies that a part of the snake body is right below the head
            is_move_safe["down"] = False
        if ((my_head["y"] + 1) == my_body[i]["y"]):
            # implies that a part of the snake body is right above the head
            is_move_safe["up"] = False
        if ((my_head["x"] - 1) == my_body[i]["x"]):
            # implies that a part of the snake body is to the left the head
            is_move_safe["left"] = False
        if ((my_head["x"] + 1) == my_body[i]["x"]):
            # implies that a part of the snake body is to the right the head
            is_move_safe["right"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    for opponent in opponents:
        for i in range(0, opponent['length']-1):
            # last part of length is the tail itself, which always recedes so do not count the tail in the segments we are checking.
            if ((my_head["y"] - 1) == opponent["body"][i]["y"]):
                # implies that a part of the snake body is right below the head
                is_move_safe["down"] = False
            if ((my_head["y"] + 1) == opponent["body"][i]["y"]):
                # implies that a part of the snake body is right above the head
                is_move_safe["up"] = False
            if ((my_head["x"] - 1) == opponent["body"][i]["x"]):
                # implies that a part of the snake body is to the left the head
                is_move_safe["left"] = False
            if ((my_head["x"] + 1) == opponent["body"][i]["x"]):
                # implies that a part of the snake body is to the right the head
                is_move_safe["right"] = False


    filled_squares = flood_fill_game_state(game_state)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        # Any move that isn't safe will automatically be game over for us.
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    #
    # Original code commented out, if we have safe moves to pick from, 
    # do a decision analysis based on Monte Carlo tree searching of what opponent moves
    # are going to be most optimal.
    #

    # 
    next_move = random.choice(safe_moves) # default to picking a random move

    if (is_recovering_health == True):
        # if we're looking for food, use A-star on each of the food points to find the closest.
        food = game_state['board']['food']

        # TODO: set next_move here based on closest food point
    else:
        if (current_heuristic == 0):
            # get to open space.

        elif (current_heuristic == 1):
            # get to a snake head.


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
