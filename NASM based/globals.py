from const import *

#Global variables
#================
errorhalt=False
#List of functions built in to the assembler (lo, hi, upper,etc)
builtin_dict={}
#List of one line functions from source (not built in functions)
funclist={}
#List of symbols defined with EQU and SET
evallist={}
#List of program lines
proglist=[]
#List of op code data
oplist={}
#List of labels
labellist={}
#List of locals
locallist={}
#List of instruction data
instructionlist={}
#Different functions use the same count of passes
passcount=0
#List of functions and what functions they call
callgraph={}
#List of locals with address asigned by optimizer
optimizedlocals={}

#Memory usage just for status output
globals_begin=0
globals_end=0
locals_begin=0
locals_end=0
#Last assignable address in zero page (can be changed in source)
locals_limit=0xFF
#Zero page counter for globals and locals
ZP_counter=0
#Whether to consolidate local variables or just assign each to a different byte
consolidate_locals=False
#Function to begin call graph search with
begin_func=""

#Line of program
class LineType:
    LabelName=None          #Label name given on this line
    LastLabel=None          #Last non-temp label passed
    FormatStr=''            #Format of line (LDA (5+7),Y = O(*),Y)
    TokenList=[]            #List of tokens on the line
    Error=BUFF_ERR_NONE     #Error from processing if any
    RawStr=''               #Original line read in from file
    SymbolUpdate=False      #Whether line is SET/EQU or not
    Resolved=False          #Whether all symbols have been resolved
    Ignore=False            #Ignore because done processing
    FileLine=None           #Line in the original file
    DelayedLabel=False      #Skip evaluating label since don't have value yet
    JumpLine=False          #Whether line contains JMP or JSR
    GlobalSize=None         #May not be necessary. Go back and check!
    LocalSize=None          #May not be necessary. Go back and check!
    LocalVar=False          #Whether line contains a local variable
    Address=None            #Address assigned after resolving symbols
    Binary=[]               #Byte(s) of instruction
    Source=""               #Source generated for instructions
    Comment=''              #Comment assigned during optimization not original comment

class OpType:
    Hex=0
    OpCode_raw=''
    OpCode=''
    OpMode=None
    Size=0
    Cycles=0
    BCDcycle=0
    Repeatable=False
    Peephole=False
    ReliesOnA=False
    ReliesOnX=False
    ReliesOnY=False
    ReliesOnSP=False
    ReliesOnMem=False
    ReliesOnN=False
    ReliesOnV=False
    ReliesOnB=False
    ReliesOnD=False
    ReliesOnI=False
    ReliesOnZ=False
    ReliesOnC=False
    ModifiesA=False
    ModifiesX=False
    ModifiesY=False
    ModifiesSP=False
    ModifiesMem=False
    ModifiesN=False
    ModifiesV=False
    ModifiesB=False
    ModifiesD=False
    ModifiesI=False
    ModifiesZ=False
    ModifiesC=False    
    
class CallGraphNodeType:
    Leaves=[]
    Locals=[]
    TotalLocals=0
