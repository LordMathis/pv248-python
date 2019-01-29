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
        
    def check_position(self, x, y):
        
        print(x, y)
        
        if x < 0 or x >= self._width:
            return -1
            
        if y < 0 or y >= self._height:
            return -1        
        
        if self._map[y][x] == '#':
            return -1
        
        return int(self._map[y][x])
        
    def set_position(self, x, y, z):
        self._map[y][x] = z
        
    def print_world(self):
        for row in self._map:
            print(''.join(str(row)))
        
        
class Program:
    
    def __init__(self, program):
        
        self.program = program
        
        
class Karel:
    
    def __init__(self, worldmap, program, prog_file):
        
        self._worldmap = worldmap
        self._program = program
        self._instruction_file = prog_file
        self._stack = []
        self._steps = 0
        self._pos_x = worldmap._init_pos_x
        self._pos_y = worldmap._init_pos_y
        self._dir = worldmap._init_dir
                
    def run(self):
        
        main = self._program.program['MAIN']
        self._push_procedure(main)
        inst_index = 0
        
        while self._stack:
            
            instruction = self._stack.pop()
            inst_index = instruction[0]
            ret = self._run_instruction(instruction)
            
            if ret != 0:
                return None
                
        ret = self.check_marks(inst_index)
        if ret != 0:
            return None
        
        self._worldmap.print_world()
        utils.eprint("program finished in {} steps".format(self._steps))          
        return ret
        
    def _push_procedure(self, procedure):
        
        self._stack.append((0, '__sub__'))
        
        for instruction in procedure[::-1]:
            self._stack.append(instruction)    
        
    def _run_instruction(self, instruction):
        
        print(self._steps, instruction)
        
        if instruction[1] == '__sub__':
            return 0
        
        self._steps += 1
        
        line = instruction[0]
        
        if instruction[1] == 'SKIP':
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
                self._worldmap.set_position(x, y, pos+1)
            else:
                utils.report(self._instruction_file, instruction[0],
                             "Runtime Error: Trying to putdown mark on a wall")
                return -1
                
            
        elif instruction[1] == 'IFWALL':
            
            next_pos_x = self._pos_x
            next_pos_y = self._pos_y
            
            if self._dir == 'n':
                next_pos_y = self._pos_y - 1
            elif self._dir == 'w':
                next_pos_x = self._pos_x - 1
            elif self._dir == 's':
                next_pos_y = self._pos_y + 1
            elif self._dir == 'e':
                next_pos_x = self._pos_x + 1
                
            if self._worldmap.check_position(next_pos_x, next_pos_y) == -1:
                return self._run_instruction((instruction[0], instruction[2]))
            else:
                return self._run_instruction((instruction[0] + 1, instruction[3]))
            
        elif instruction[1] == 'IFMARK':
            
            if self._worldmap.check_position(self._pos_x, self._pos_y) > 0:
                return self._run_instruction((instruction[0], instruction[2]))
            else:
                return self._run_instruction((instruction[0] + 1, instruction[3]))
            
        else:
            sub_proc = self._program.program[instruction[1]]
            self._push_procedure(sub_proc)
            
        return 0
        
    def check_marks(self, lineno):
        for row in self._worldmap._map:
            for cell in row:
                if cell != '#':
                    if int(cell) > 9:
                        utils.report(self._instruction_file, lineno, "Program ended with more than 9 marks in a ")
                        return -1
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
    
    