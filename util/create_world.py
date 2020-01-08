from django.contrib.auth.models import User
from adventure.models import Player, Room

Room.objects.all().delete()
# Create world class
class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x
        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:
            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1
            # Create a room in the given direction
            room = Room(
                room_count,
                "A Generic Room",
                "This is a generic room.",
                x,
                y)
            # Note that in Django, you'll need to save the room after you
            # create it
            room.save()
            # Save the room in the World grid
            self.grid[y][x] = room
            # Connect the new room to the previous room
            opposite = {"w": "e", "e": "w", "s": "n", "n": "s"}
            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)
                room.connectRooms(previous_room,opposite[room_direction])
            # Update iteration variables
            previous_room = room
            room_count += 1

w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
starting_room = w.grid[0][0]
players = Player.objects.all()
for p in players:
    p.currentRoom = starting_room.id
    p.save()
