from parse import *
from simplify import *
from optimize import *
from output import *
import globals as g
from const import *
from pp_6502 import *
import sys

#TODO:
#complaint about LDA 'y'
#~ - still unsupported but xor works
#{} in Function expansion
#Support for && and || in Python
#Check macros and error if LOCAL outside FUNC
    #Technically any LOCAL after first FUNC is within a label since ENDFUNC doesn't mark end

def main():
    print("6502 Assembly Optimizer v0.1")
    print("============================")

    #Load info about 6502 instructions
    LoadInstructions()

    #Read in command list available to assembler: hi, lo, upper, etc
    for i in commandlist:
        g.builtin_dict[i[0]]=(i[1],i[2])

    #Set input filename for testing
    sys.argv.append('main.i')

    #Get input file from command line
    try:
        file=open(sys.argv[1],mode="r")
    except:
        print("Error: file not found - "+sys.argv[1])
        sys.exit()

    #Split lines up into tokens
    ParseSource(file.read().splitlines())
    file.close()
    #Simplify token lines by evaluating symbols and calculating
    SimplifySource()
    #Generate control flow graph
    GenerateCallGraph()
    #Generate addresses for local variables depending on optimization mode
    GenerateLocals(consolidate=True)
    #Apply generated addresses for local variables to source
    AssignLocals()
    #Recognize instructions and assign op code if don't contain unresolvable symbols
    AssignInstructions()

    #FURTHER OPTIMIZATIONS GO HERE

    #Generate addresses and evaluate labels and builtin functions
    #(must happen towards the end after any sort of optimization)
    GenerateAddresses()

    #Print source to file
    #(disabled for now until builtin functions taking label as argument can be resolved)
    #PrintSource('processed.asm')

    #Print instead to HTML file to show progress
    PrintSourceHTML('output\processed.html')

    print("\nExecution successful. See output folder for results.")

if __name__=="__main__":
    main()
