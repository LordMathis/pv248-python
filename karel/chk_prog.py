from sys import argv, exit
import utils
from karel import Program

def process_procedure(procedures, key, file):
    
    procedure, k = procedures[key]
    instructions = []
            
    for i, line in enumerate(procedure):
        
        if line.startswith('#') or len(line) == 0:
            continue
        
        simple_inst = ['SKIP', 'BREAK', 'HALT', 'MOVE', 'LEFT', 'RIGHT', 'PICKUP', 'PUTDOWN']
        
        if line in simple_inst:
            instructions.append((k+i, line))
            
        elif line.startswith('IFWALL') or line.startswith('IFMARK'):
            
            split = line.split()
            if len(split) != 2:
                utils.report(file, k+i, "IFWALL and IFMARK expect exactly 1 parameter")
                return None
                
            if split[1] in simple_inst:
                instructions.append((k+i, split[0], split[1]))
            else:
                
                if not split[1].isalnum():
                    utils.report(file, k+i, "Illegal character")
                    return None
                    
                if split[1] not in procedures:
                    utils.report(file, k+i, "Undefined reference")
                    return None
                    
                instructions.append((k+i, split[0], split[1]))
        
        elif line.startswith('ELSE'):
            if instructions[-1][0] in ['IFWALL', 'IFMARK']:
                
                split = line.split()
                if len(split) != 2:
                    utils.report(file, k+i, "ELSE expects exactly 1 parameter")
                    return None           
                    
                instructions[-1] += split[1],
                
            else:
                utils.report(file, k+i, "ELSE must follow IFWALL or IFMARK")
                return None
                
        else:
            if not line.isalnum():
                utils.report(file, k+i, "Illegal character")
                return None
                    
            if line not in procedures:
                utils.report(file, k+i, "Undefined reference")
                return None
            
            instructions.append((k+i, line))
                
    return instructions     
        
def check_prog(file):
    
    lines = utils.read_file(file).splitlines()
    procedures = {}
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#') or len(line) == 0:
            i+=1
            continue
            
        if line.startswith('DEFINE'):
                        
            if len(line.split()) != 2:
                utils.report(file, i+1, "Procedures start with DEFINE [name]")
                return None
            
            proc_name = line.split()[1]
            procedure = []
            
            if not proc_name.isalnum():
                    utils.report(file, i+1, "Illegal character")
                    return None
            
            if proc_name in procedures:
                utils.report(file, i+1, "Procedure already exists")
                return None
            
            i += 1
            k = i
            
            while i < len(lines) and lines[i] != 'END':
                
                line = lines[i]
                
                if line.startswith('DEFINE'):
                    utils.report(file, i+1, "Missing END")
                    return None
                                                
                procedure.append(line.strip())
                i += 1
                
            if i == len(lines):
                utils.report(file, i+1, "Missing END")
                return None
    
            procedures[proc_name] = (procedure, k+1)            
            procedure = []
                        
        else:
            utils.report(file, i+1, "Instruction outside of procedure")
            return None
            
        i += 1
        
    for key in procedures:
        res = process_procedure(procedures, key, file)
        if res is None:
            return None
        procedures[key] = res
        
    if 'MAIN' not in procedures:
        utils.report(file, i+1, 'MAIN method not found')
        return None
        
    print(procedures)
    return Program(procedures)
    

if __name__ == '__main__':

    file_path = argv[1]
    ret = check_prog(file_path)
    if ret is None:
        exit(1)
    exit(0)