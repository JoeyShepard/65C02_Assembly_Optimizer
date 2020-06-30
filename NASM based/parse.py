from ops import *
import globals as g
from const import *
from collections import namedtuple
import sys

#Factory for named tuples
Token=namedtuple('Token','data type')

def ParseLine(instr):
    templist=[]
    retobj=g.LineType()

    retobj.RawStr=instr

    def AddToList(item,itemtype):
        if itemtype==BUFF_ALPHA:
            #Not supported in AS assembler
            #if item.lower() in ('or','and','xor'):
                #templist.append(Token(item.lower(),BUFF_OP))
            #elif item.lower() in [a.lower() for (a,b,c) in commandlist]:

            if item in g.builtin_dict:
                templist.append(Token(item.lower(),BUFF_BUILTIN))
            elif item.upper()=="EQU":
                templist.append(Token(item.lower(),BUFF_EQUAL))
            elif item.upper()=="SET":
                templist.append(Token(item.lower(),BUFF_SET))
            elif item.upper() in OP_LIST:
                templist.append(Token(item.upper(),BUFF_INSTRUCTION))
            elif item=='TRUE':
                templist.append(Token(True,BUFF_BOOLEAN))
            elif item=='FALSE':
                templist.append(Token(False,BUFF_BOOLEAN))
            elif item.upper()=='X':
                templist.append(Token(item,BUFF_XREG))
            elif item.upper()=='Y':
                templist.append(Token(item,BUFF_YREG))
            elif item.upper()=='DFS':
                templist.append(Token(item,BUFF_DFS))
            elif item.upper()=='FCB':
                templist.append(Token(item,BUFF_FCB))
            elif item.upper()=='FCC':
                templist.append(Token(item,BUFF_FCC))
            elif item.upper()=='FDB':
                templist.append(Token(item,BUFF_FDB))
            else:
                templist.append(Token(item,itemtype))
        elif itemtype==BUFF_NUM:
            templist.append(Token(int(item),itemtype))
        elif itemtype==BUFF_FLOAT:
            templist.append(Token(float(item),itemtype))
        elif itemtype==BUFF_HEX:
            templist.append(Token(int(item,16),BUFF_NUM))
        elif itemtype==BUFF_CHAR:
            #' appended to end (why did I do this?)
            #templist.append(Token(item[0],itemtype))
            templist.append(Token(ord(item[0]),itemtype))
        elif itemtype==BUFF_STR:
            #" appended to end (why did I do this?)
            templist.append(Token(item[0:-1],itemtype))
        elif itemtype==BUFF_OP:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_HASH:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_COLON:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_COMMA:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_OPEN_PAR:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_CLOSE_PAR:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_EQUAL:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_OPEN_BRACKET:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_CLOSE_BRACKET:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_PCSTAR:
            templist.append(Token(item,itemtype))
        #These don't get classified until later so didn't make sense to have these here
        #elif itemtype==BUFF_ASMWORDS:
        #    templist.append(Token(item,itemtype))

        else:
            print("Error: unknown item type -",itemtype)
            sys.exit()
    
    #Buffer of characters in each item
    tempbuff=''
    #State of buffer
    buffstate=BUFF_EMPTY
    #Error code
    bufferror=BUFF_ERR_NONE
    #Sometimes need to repeat loop body
    loopcounter=0
    #Exit early if comment
    exitearly=False
    #Whether a minus sign has been encountered
    minussign=False

    instr+=' '
    
    for c in instr:
        loopcounter=1
        while loopcounter>0:
            loopcounter-=1
            if buffstate==BUFF_EMPTY:
                if c==' ' or c=='	':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                elif c.isalpha() or c in '@_.{':  # Can begin with "." but not contain it
                    tempbuff=c
                    buffstate=BUFF_ALPHA
                elif c.isdigit():
                    tempbuff=''
                    if minussign:
                        #print("adding minus")
                        tempbuff='-'
                        minussign=False
                    tempbuff+=c
                    buffstate=BUFF_NUM
                elif c=='$':
                    tempbuff=''
                    if minussign:
                        tempbuff='-'
                        minussign=False
                    buffstate=BUFF_HEX
                elif c=="'":
                    tempbuff=''
                    buffstate=BUFF_CHAR
                elif c=='"':
                    tempbuff=''
                    buffstate=BUFF_STR
                elif c== '#':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList('#',BUFF_HASH)
                elif c== '=':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList('=',BUFF_EQUAL)
                elif c in BUFF_OP_STR:
                    if c in '<>':
                        tempbuff=c
                        buffstate=BUFF_OP
                    elif c=='*':
                        ispcstar=False
                        #NOT SURE THIS WILL ALWAYS WORK CORRECTLY!
                        #Detect * as the symbol for current address
                        #If * is first in line, it's address (*=123)
                        if len(templist)==0:
                            ispcstar=True
                        elif templist[-1].type in [BUFF_OP,BUFF_HASH,BUFF_COLON,BUFF_OPEN_PAR,BUFF_EQUAL,BUFF_OPEN_BRACKET,BUFF_SET,BUFF_INSTRUCTION]:
                            ispcstar=True
                        buffstate=BUFF_EMPTY
                        if ispcstar:
                            AddToList(c,BUFF_PCSTAR)
                        else:
                            AddToList(c,BUFF_OP)
                    elif c=='-':
                        #print("minus found:",instr,"preceding type:",templist[-1].type)
                        buffstate=BUFF_EMPTY
                        #Treat - as negative sign only if preceded by #
                        #Could be other situations though!!! (ie FCB?)
                        if templist[-1].type in [BUFF_OP,BUFF_HASH,BUFF_COLON,BUFF_OPEN_PAR,BUFF_EQUAL,BUFF_OPEN_BRACKET,BUFF_SET,BUFF_INSTRUCTION]:
                            minussign=True
                            #print("   negative number")
                        else:
                            AddToList(c,BUFF_OP)
                    else:
                        buffstate=BUFF_EMPTY
                        AddToList(c,BUFF_OP)
                elif c==';':
                    exitearly=True
                elif c==':':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList(':',BUFF_COLON)
                elif c==',':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList(',',BUFF_COMMA)
                elif c=='(':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList('(',BUFF_OPEN_PAR)
                elif c==')':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList(')',BUFF_CLOSE_PAR)
                elif c=='[':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList('[',BUFF_OPEN_BRACKET)
                elif c==']':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                    AddToList(']',BUFF_CLOSE_BRACKET)
            elif buffstate==BUFF_ALPHA:
                #if c.isalpha() or c.isdigit() or c in '_{}':
                if c.isalpha() or c.isdigit() or c in '@._{}':
                    #NASM generates temp labels with @ in name but AS doesnt accept
                    if c=="@":
                        c="_"
                    tempbuff+=c
                elif c in BUFF_VALID_STR + BUFF_OP_STR + ':':
                    AddToList(tempbuff,buffstate)
                    buffstate=BUFF_EMPTY
                    loopcounter+=1
                else:
                    print("Error: illegal character in name "+tempbuff+c+"...")
                    bufferror=BUFF_ERR_FAIL
            elif buffstate==BUFF_NUM or buffstate==BUFF_FLOAT:
                if c.isdigit():
                    tempbuff+=c
                elif c=='.':
                    if buffstate==BUFF_NUM:
                        tempbuff+='.'
                        buffstate=BUFF_FLOAT
                    elif buffstate==BUFF_FLOAT:
                        print("Error: two decimals found in number "+tempbuff+"...")
                        bufferror=BUFF_ERR_FAIL
                elif c in BUFF_VALID_STR or c in BUFF_OP_STR:
                    AddToList(tempbuff,buffstate)
                    buffstate=BUFF_EMPTY
                    loopcounter+=1
                else:
                    print("Error: invalid character in number "+tempbuff+c+"...")
                    bufferror=BUFF_ERR_FAIL
            elif buffstate==BUFF_HEX:
                if c.isdigit() or c.upper() in 'ABCDEF':
                    tempbuff+=c
                elif c in BUFF_VALID_STR or c in BUFF_OP_STR:
                    AddToList(tempbuff,buffstate)
                    buffstate=BUFF_EMPTY
                    loopcounter+=1
                else:
                    print("Error: invalid character in hex "+tempbuff+c+"...")
                    bufferror=BUFF_ERR_FAIL
            elif buffstate==BUFF_CHAR:
                if tempbuff=='':
                    tempbuff+=c
                elif len(tempbuff)==1:
                    if c=="'":
                        #Why????
                        tempbuff+="'"
                    else:
                        #Double slash is escape for \
                        if tempbuff=="\\" and c=="\\":
                            pass
                        else:
                            print("Error: character length must be 1: '"+tempbuff+c+"...")
                            bufferror=BUFF_ERR_FAIL
                elif len(tempbuff)==2:
                    if c in BUFF_VALID_STR or c in BUFF_OP_STR:
                        AddToList(tempbuff,buffstate)
                        buffstate=BUFF_EMPTY
                        loopcounter+=1
                    else:
                        print("Error: invalid character "+tempbuff+c+"...")
                        bufferror=BUFF_ERR_FAIL
            elif buffstate==BUFF_STR:
                if tempbuff[-1:]=='"':
                    if c in BUFF_VALID_STR or c in BUFF_OP_STR: #or c=='"':
                        AddToList(tempbuff,buffstate)
                        buffstate=BUFF_EMPTY
                        loopcounter+=1
                    else:
                        print("Error: invalid character "+tempbuff+c+"...")
                        bufferror=BUFF_ERR_FAIL
                else:
                    tempbuff+=c
            elif buffstate==BUFF_OP:
                if c==tempbuff:
                    tempbuff+=c
                    AddToList(tempbuff,buffstate)
                    buffstate=BUFF_EMPTY
                else:
                    print("Error: invalid character "+tempbuff)
                    bufferror=BUFF_ERR_FAIL
            if bufferror!=BUFF_ERR_NONE:
                break
            elif exitearly:
                break
        if bufferror!=BUFF_ERR_NONE:
            break
        elif exitearly:
            break

    if bufferror==BUFF_ERR_FAIL:
        retobj.Error=BUFF_ERR_FAIL
        return retobj
    else:
        retobj.TokenList=templist
    return retobj

#lines is array of source code lines
def ParseSource(listlines):
    try:
        output_file=open("output.txt",mode="w")
    except:
        print("Error: unable to open output.txt ")
        sys.exit()

    for k,line in enumerate(listlines):
        if line.strip()!='':
            retval=ParseLine(line)
            #print(retval.RawStr)
            if retval.Error==BUFF_ERR_FAIL:
                sys.exit()
            elif len(retval.TokenList)!=0 or retval.LabelName!=None: #or retval.Org!=None:
                retval.FileLine=k+1
                g.proglist.append(retval)
                ##print(retval.RawStr)
                ##print([a.data for a in retval.TokenList])
                #print([a for (a,b) in retval.TokenList])
                #print([b for (a,b) in retval.TokenList])
                ##print(retval.FormatStr)
                #print()
                ##Also print to file
                ##print(retval.RawStr, file=output_file)
                #print([a for (a,b) in retval.TokenList], file=output_file)
                #print([b for (a,b) in retval.TokenList], file=output_file)
                ##print(retval.FormatStr,file=output_file)
                #print(file=output_file)
            else:
                #print(retval.TokenList)
                #print()
                pass


    output_file.close()
