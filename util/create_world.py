from django.contrib.auth.models import User
from adventure.models import Player, Room
import random
Room.objects.all().delete()
adjectives = [
    "aggressive","alert","alive","ancient","anxious","arrow","attractive","average","bad","beautiful","beige","better","big","bitter","black","blue","brown","bumpy","busy","careful","cheap","chestnut","clear","cold","combative","cool","cotton","crazy","crooked","crystal","dangerous","dead","delicious","dim","drab","dry","dull","dusty","elderly","excited","expensive","fancy","fat","few","filthy","fresh","fuzzy","giant","good","graceful","granite","green","handsome","happy","hard","harsh","hollow","hot","huge","hungry","large","lazy","light","long","low","massive","mellow","melodic","modern","new","noisy","oak","octagonal","old","orange","oval","petite","pink","plain","plastic","poor","puny","purple","quiet","rainy","red","rich","right","round","sad","safe","salty","sane","scared","shallow","sharp","shiny","short","shrill","shy","skinny","small","soft","solid""sore","sour","square","steep","sticky","strong","superior","sweet","swift","tan","tart","teak","teeny","terrible","tiny","tired","tremendous","triangular","ugly","unusual","weak","weary","wet","whispering","white","wild","wooden","woolen","wrong","yellow","young"]
countryList = ["United States of merica","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas (the)","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia (Plurinational State of)","Bonaire, Sint Eustatius and Saba","Bosnia and Herzegovina","Botswana","Bouvet Island","Brazil","British Indian Ocean Territory (the)","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Cayman Islands (the)","Central African Republic (the)","Chad","Chile","China","Christmas Island","Cocos (Keeling) Islands (the)","Colombia","Comoros (the)","Congo (the Democratic Republic of the)","Congo (the)","Cook Islands (the)","Costa Rica","Croatia","Cuba","Curaçao","Cyprus","Czechia","Côte d'Ivoire","Denmark","Djibouti","Dominica","Dominican Republic (the)","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Falkland Islands (the) [Malvinas]","Faroe Islands (the)","Fiji","Finland","France","French Guiana","French Polynesia","French Southern Territories (the)","Gabon","Gambia (the)","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Holy See (the)","Honduras","Hong Kong","Hungary","Iceland"]
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
                countryList[room_count],
                f"This is a {random.choice(adjectives)} country",
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