from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# print(player.current_room)
reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}


def generate_path(visited_rooms=[]):
    directions_store = []

    # get all exit directions from current room
    for direction in player.current_room.get_exits():

        # move in a direction
        player.travel(direction)
        # print('moving', direction)

        # if the room hasn't already been visited:
        if player.current_room.id not in visited_rooms:

            # add the room to the list of visited rooms
            visited_rooms.append(player.current_room.id)
            print(visited_rooms, player.current_room.id)
            directions_store.append(direction)
            # print('1st store',directions_store, player.current_room.id)

            directions_store += generate_path(visited_rooms)
            # print('2nd store',directions_store, player.current_room.id)

            player.travel(reverse[direction])
            directions_store.append(reverse[direction])
            # print('3rd store',directions_store, player.current_room.id)

        # if the room is in the visited list, moves the reverse direction of the previous move
        else:
            # print('moving back', reverse[direction])
            player.travel(reverse[direction])

    return directions_store


traversal_path = generate_path()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
