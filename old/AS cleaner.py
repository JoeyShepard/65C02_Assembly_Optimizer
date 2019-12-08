from enum import Enum
class line_kind(Enum):
    BLANK = 1
    OP = 2
    FCB = 3

class src_line():
    def __init__(self, kind, label, op, data)
        self.kind = kind
        self.label = label
        self.op = op
        self.data = data

def main():
    print("6502 AS Cleaner v0.1")
    print("===================")
    #from sys import argv
    import sys

    #set command line for testing
    sys.argv=[sys.argv[0],"temp.lst"]
    
    if len(sys.argv)==1:
        print("Usage:...")
        sys.exit();

    try:
        file=open(sys.argv[1],mode="r")
    except:
        print("Error: unable to open file -",sys.argv[1])
        sys.exit()

    line_list = []

    try:
        line_counter=0
        for line in file:
            line_counter+=1
            #Skip first 3 lines
            if line_counter>3:
                #Don't test lines that are too short
                if len(line)>=20:
                    #Check if line is beginning line
                    if line[18]==":":
                        data_section=line[20:38].strip()
                        if data_section=="":
                            temp_kind = line_kind.BLANK
                            #Blank line, check for label
                            op_section=line[40:-1].strip()
                            if op_section[-1:]==":":
                                temp="label"
                            else:
                                temp=""
                        elif data_section[0:1]=="=":
                            #Assignment (do nothing)
                            temp=""
                        elif data_section[0:6]=="(MACRO":
                            #Macro (do nothing)
                            temp=""
                        else:
                            temp=data_section
                        if temp!="": print(line_counter,temp)
    except:
        print("Error: problem reading file in")
        file.close()
        sys.exit()

    file.close()

    
if __name__=="__main__":
    main()
