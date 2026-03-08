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

def AStar(goal, my_head,board_height, board_width,is_move_safe):
    
    Bx = board_width
    By = board_height
    curX = my_head["x"]
    curY = my_head["y"]
    total = Bx*By
    result = 0

    Path = [total]
    visited = [total]

    for i in total:  #goes through every node
        Path[i] = 1001  #Pretend this is infiine distance
        visited[i] = 0  # 0 = not visited 1 = visited

    curpos = (curX-1)*(curY-1)
    Path[curpos] = 0 
    for i in total:    
        for j in total:
            if Path[j] == 1001:
                 curpos = i
                 break
        for j in total:
            if visited[j] == 0 & (Path[j] < Path[curpos]):
                curpos = j
        
        visited[curpos] = 1
        if Path[curpos] == 1001:
            result = -1


        Next = []

        if is_move_safe["up"]==True:
            Next.append(curpos-By)
        if is_move_safe["down"]==True:
            Next.append(curpos+By)
        if is_move_safe["left"]==True:
            Next.append(curpos-1)
        if is_move_safe["right"]==True:
            Next.append(curpos+1)
        for j in Next:
            w = Next[j]
            if Path[w] > Path[curpos]:
                o = Path[curpos]
                Path[w] = o + 1
                
    result = Path[goal-1]
    return result


#
# High-level strategy:
# - 

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

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
    
    #
    # Flood-fill the board here, we need to know which squares are open and which are occupied near our current position
    #

    #
    # Can we use pre-existing game state?
    #


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']


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
    #next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
