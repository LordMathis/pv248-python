from sys import argv, exit
import utils

def check_position(pos_x, pos_y, width, height, dir, file):
    
    try:
        pos_x = int(pos_x)
        pos_y = int(pos_y)
    except:
        urils.report(file, 2, "Positions should be integers")
        return None, None, None
    
    if pos_x < 0 or pos_x > width - 1:
        utils.report(file, 2, "Starting position is outside of the world")
        return None, None, None
        
    if pos_y < 0 or pos_y > height - 1:
        utils.report(file, 2, "Starting position is outside of the world")
        return None, None, None
    
    if dir not in 'nesw':
        utils.report(file, 2, "Unexpected direction")
        return None, None, None
        
    return pos_x, pos_y, dir
    
def check_world_dims(width, height, file):
    
    try:
        width = int(width)
        height = int(height)
    except:
        utils.report(file, 2, "World dimensions should be integers")
        return None, None
        
    if width < 0 or height < 0:
        utils.report(file, 2, "World dimensions cannot be negative")
        return None, None
        
    return width, height

def check_world(world_file):

    world_data = utils.read_file(world_file).splitlines()

    if len(world_data[0].split()) != 2:
        utils.report(world_file, 1, "Line 1 should contain only width and height")
        return None

    if len(world_data[1].split()) != 3:
        utils.report(world_file, 2, "Line 2 should contain 3 items")
        return None

    width, height = world_data[0].split()
    width, height = check_world_dims(width, height, world_file)
    if width is None or height is None:
        return None 
    
    pos_x, pos_y, dir = world_data[1].split()    
    pos_x, pos_y, dir = check_position(pos_x, pos_y, width, height, dir, world_file)
    
    if pos_x is None or pos_y is None or dir is None:
        return None
    
    world = []

    for i, line in enumerate(world_data[2:]):

        world_line = []

        if len(line) != width:
            utils.report(world_file, i+3, "Unexpected number of items in line")
            return None

        for char in line:
            if char not in '0123456789 #':
                utils.report(world_file, i+3, "Unexpected character")
                return None

            if char == ' ':
                char = 0
            world_line.append(char)

        world.append(world_line)

        if i > height:
            utils.report(world_file, i+2, "Unexpected number of lines")
            return None

    if len(world) < height:
        utils.report(world_file, len(world_data)+1, "Unexpected number of lines")
        return None

    from karel import WorldMap
    return WorldMap(width, height, pos_x, pos_y, dir, world)

if __name__ == '__main__':

    file_path = argv[1]
    ret = check_world(file_path)
    if ret is None:
        exit(1)
    exit(0)
