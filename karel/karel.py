from sys import argv, exit
from chk_prog import check_prog
from chk_world import check_world
import utils

class WorldMap:

    def __init__(self,
                 width = None,
                 height = None,
                 pos_x = None,
                 pos_y = None,
                 dir = None,
                 map = None):

        self._width = width
        self._height = height
        self._init_pos_x = pos_x
        self._init_pos_y = pos_y
        self._init_dir = dir
        self._map = map
        
    def check_position(x, y):
        if self._map[x][y] == '#':
            return -1
        else:
            return self._map[x][y]
        
    def set_position(x, y, z):
        self._map[x][y] = z
        
class Program:
    
    def __init__(self, program):
        
        self.program = program
        
class Karel:
    
    def __init__(self, worldmap, program, prog_file):
        
        self._worldmap = worldmap
        self._program = program
        self._instruction_file = prog_file
        self._stack = []
        self._coins = 0
        self._pos_x = worldmap._init_pos_x
        self._pos_y = worldmap._init_pos_y
        self._dir = worldmap._init_dir
                
    def run(self):
        
        main = self._program['MAIN']
        self._push_procedure(main)
        
        while self._stack:
            
            instruction = self._stack.pop()
            ret = self._run_instruction(instruction)
            
            if ret != 0:
                return None
        
    def _push_procedure(procedure):
        
        self._stack.append((0, '__sub__'))
        
        for instruction in procedure[::-1]:
            self._stack.append(instruction)    
        
    def _run_instruction(self, instruction):
        
        line = instruction[0]
        
        if instruction[1] == 'SKIP' or instruction[1] == '__sub__':
            return 0
            
        elif instruction[1] == 'BREAK':
            next = self._stack.pop()
            while next[1] != '__sub__':
                next = self._stack.pop()
            
        elif instruction[1] == 'HALT':
            return -1
            
        elif instruction[1] == 'MOVE':
            cur_dir = self._dir
            next_pos_x = self._pos_x
            next_pos_y = self._pos_y
            
            if cur_dir == 'n':
                next_pos_y -= 1
            elif cur_dir == 'w':
                next_pos_x -= 1
            elif cur_dir == 's':
                next_pos_y += 1
            elif cur_dir == 'e':
                next_pos_x += 1
                
            if self._worldmap.check_position(next_pos_x, next_pos_y) >= 0:
                self._pos_x = next_pos_x
                self._pos_y = next_pos_y
                
                utils.report(prog_file, instruction[0],
                             "Runtime Error: Karel tried to move into a wall") 
            
        elif instruction[1] == 'LEFT':
            cur_dir = self._dir
            next_dir = cur_dir
            
            if cur_dir == 'n':
                next_dir = 'w'
            elif cur_dir == 'w':
                next_dir = 's'
            elif cur_dir == 's':
                next_dir = 'e'
            elif cur_dir == 'e':
                next_dir = 'n'  
                
            self._dir = next_dir
            
        elif instruction[1] == 'RIGHT':
            cur_dir = self._dir
            next_dir = cur_dir
            
            if cur_dir == 'n':
                next_dir = 'e'
            elif cur_dir == 'w':
                next_dir = 'n'
            elif cur_dir == 's':
                next_dir = 'w'
            elif cur_dir == 'e':
                next_dir = 's'  
                
            self._dir = next_dir
            
        elif instruction[1] == 'PICKUP':
            
            x = self._pos_x
            y = self._pos_y
            
            pos = self._worldmap.check_position(x, y)
                        
            if pos > 0:
                self._worldmap.set_position(x, y, pos-1)
                self._coins += 1
                return 0
            else:
                utils.report(self._instruction_file, instruction[0],
                             "Runtime Error: Trying to pickup mark from wrong place")
                return -1
            
        elif instruction[1] == 'PUTDOWN':
            
            x = self._pos_x
            y = self._pos_y
            
            pos = self._worldmap.check_position(x, y)
            
            if pos >= 0:
                if self._coins > 0:
                    self._coins -= 1
                    self._worldmap.set_position(x, y, pos+1)
                else:
                    utils.report(self._instruction_file, instruction[0],
                                 "Runtime Error: Trying to putdown mark with zero marks")
                    return -1
            else:
                utils.report(self._instruction_file, instruction[0],
                             "Runtime Error: Trying to putdown mark on a wall")
                return -1
                
            
        elif instruction[1] == 'IFWALL':
            pass
            
        elif instruction[1] == 'IFMARK':
            pass
            
        else:
            sub_proc = self._program[instruction[1]]
            self._push_procedure(sub_proc)
            
        return 0

if __name__ == '__main__':
    
    world_file = argv[1]
    prog_file = argv[2]
    
    ret_world = check_world(world_file)
    if ret_world is not None:
        
        ret_prog = check_prog(prog_file)
        if ret_prog is not None:
            karel = Karel(ret_world, ret_prog, prog_file)
            res = karel.run()
            
            if res is not None:
                exit(0)
            else:
                exit(1)            
            
        else:
            exit(1)
    else:
        exit(1)
    
    