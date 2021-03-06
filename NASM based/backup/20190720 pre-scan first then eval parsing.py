from pp_ops import *
import pp_globals as g
from pp_const import *
from collections import namedtuple

#Factory for named tuples
Token=namedtuple('Token','data type')

def GenPattern(mainlist):
    formatstr=''
    i=0;
    i_end=len(mainlist)
    found1=False
    found2=False
    parcountouter=0
    while i<i_end:
        if mainlist[i].type==BUFF_ALPHA:
            if mainlist[i].data.upper() in OP_LIST:
                if found1:
                    found1=False
                    formatstr+='*'
                formatstr+='O'
            elif mainlist[i].data.lower() in ['x','y']:
                if found1:
                    found1=False
                    formatstr+='*'
                formatstr+=mainlist[i].data.upper()
            else:
                if found1:
                    found1=False
                    formatstr+='*'
                formatstr+='A'
        elif mainlist[i].type==BUFF_HASH:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='#'
        elif mainlist[i].type==BUFF_EQUAL:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='='
        elif mainlist[i].type==BUFF_OPEN_PAR:
            parcountouter+=1
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='('
            parcount=1
            found2=False
            i+=1
            while i<i_end:
                if mainlist[i].type==BUFF_CLOSE_PAR: parcount-=1
                elif mainlist[i].type==BUFF_OPEN_PAR: parcount+=1
                elif mainlist[i].type==BUFF_ALPHA:
                    if parcount==1:
                        if mainlist[i].data.lower() in ['x','y']:
                            if found2:
                                formatstr+='*'
                                found2=False
                            formatstr+=mainlist[i].data.upper()
                elif mainlist[i].type==BUFF_COMMA:
                    if parcount==1:
                        if found2:
                            formatstr+='*'
                            found2=False
                        formatstr+=','
                else:
                    found2=True
                if parcount==0:
                    if found2:
                        formatstr+='*'
                        found2=False
                    formatstr+=')'
                    break
                i+=1
            if parcount<0:
                print('Error: closing parenthesis without opening parenthesis')
                g.errorhalt=True
                return False
            elif parcount>0:
                print('Error: opening parenthesis without closing parenthesis')
                g.errorhalt=True
                return False
        elif mainlist[i].type==BUFF_COMMA:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+=','
        else:
            found1=True
        i+=1
    if found1:
        formatstr+='*'
    return formatstr            

def AddOp(op, outlist):
    if op.type==BUFF_OP:
        if op.data not in '~*+': #Ops work only on numbers, except * and +
            if len(outlist)<2:
                print('Error: evaluation error, '+op.data+' requires two arguments')
                g.errorhalt=True
                return
            arg1=outlist.pop()
            arg2=outlist.pop()
            numcount=0
            if arg1.type==BUFF_NUM or arg1.type==BUFF_FLOAT: numcount+=1
            if arg1.type==BUFF_NUM or arg1.type==BUFF_FLOAT: numcount+=1
            if numcount!=2:
                print('Error: evaluation error, '+op.data+' expects int or float')
                print(arg1, arg2)
                g.errorhalt=True
                return
            if op.data=='^': tempop='**'
            elif op.data=='!': tempop='^'
            else: tempop=op.data
            #Added parentheses so -2^4 won't be -16
            tempval=eval("("+str(arg2.data)+")"+tempop+"("+str(arg1.data)+")")
            if '.' in str(tempval): outlist.append(Token(tempval,BUFF_FLOAT))
            else: outlist.append(Token(tempval,BUFF_NUM))
        elif op.data=='*':
            if len(outlist)<2:
                print('Error: evaluation error, * requires two arguments')
                g.errorhalt=True
                return
            arg1=outlist.pop()
            arg2=outlist.pop()
            numcount=0
            
            if arg1.type==BUFF_NUM or arg1.type==BUFF_FLOAT:
                numcount=1
                numarg=arg1.data
                otherarg=arg2
            if arg2.type==BUFF_NUM or arg2.type==BUFF_FLOAT:
                if numcount==1:
                    tempval=numarg*arg2.data
                    if '.' in str(tempval): outlist.append(Token(tempval,BUFF_FLOAT))
                    else: outlist.append(Token(tempval,BUFF_NUM))
                    return
                else:
                    numcount=1
                    numarg=arg2.data
                    otherarg=arg1
            if numcount==0:
                print('Error: multiplication expects at least one int or float')
                g.errorhalt=True
                return
            numarg=int(numarg)
            if otherarg.type==BUFF_ALPHA:
                outlist.append(Token(numarg*otherarg.data,BUFF_ALPHA))
            elif otherarg.type==BUFF_CHAR or otherarg.type==BUFF_STR:
                outlist.append(Token(numarg*otherarg.data,BUFF_STR))
            else:
                print('Error: cannot multiply '+numarg+' and '+otherarg.data)
                g.errorhalt=True
                return
        elif op.data=='+':
            if len(outlist)<2:
                print('Error: evaluation error, + requires two arguments')
                g.errorhalt=True
                return
            arg1=outlist.pop()
            arg2=outlist.pop()
            numcount=0
            
            if arg1.type==BUFF_NUM or arg1.type==BUFF_FLOAT:
                numcount=1
                otherarg=arg2
            if arg2.type==BUFF_NUM or arg2.type==BUFF_FLOAT:
                if numcount==1:
                    tempval=arg1.data+arg2.data
                    if '.' in str(tempval): outlist.append(Token(tempval,BUFF_FLOAT))
                    else: outlist.append(Token(tempval,BUFF_NUM))
                    return
                else:
                    numcount=1
                    otherarg=arg1
            if numcount==1:
                if otherarg.type==BUFF_ALPHA:
                    outlist.append(Token(str(arg2.data)+str(arg1.data),BUFF_ALPHA))
                elif otherarg.type==BUFF_CHAR:
                    if arg1.type==BUFF_CHAR:
                        outlist.append(Token(ord(arg1.data[0])+int(arg2.data),BUFF_NUM))
                    else:
                        outlist.append(Token(ord(arg2.data[0])+int(arg1.data),BUFF_NUM))
                elif otherarg.type==BUFF_STR:
                    outlist.append((str(arg2.data)+str(arg1.data),BUFF_STR))
                else:
                    print('Error: cannot add '+arg2.data+' and '+arg1.data)
                    g.errorhalt=True
                    return  
            elif numcount==0:
                alphacount=0
                strcount=0
                if arg1.type==BUFF_ALPHA: alphacount+=1
                if arg2.type==BUFF_ALPHA: alphacount+=1
                if arg1.type==BUFF_CHAR or arg1.type==BUFF_STR: strcount+=1
                if arg2.type==BUFF_CHAR or arg2.type==BUFF_STR: strcount+=1

                if alphacount==2:
                    outlist.append(Token(str(arg2.data)+str(arg1.data),BUFF_ALPHA))
                elif strcount==2:
                    outlist.append(Token(str(arg2.data)+str(arg1.data),BUFF_STR))
                else:
                    print('Error: cannot add '+arg2.data+' and '+arg1.data)
                    g.errorhalt=True
                    return
    elif op.type==BUFF_FUNC:
        argcount=g.commandlistnew[op.data][0]
        func=g.commandlistnew[op.data][1]
        if len(outlist)<(argcount*2-1):
            print('Error: '+op.data+' takes '+str(argcount)+' argments')
            g.errorhalt=True
            return
        arglist=[]
        for i in range(1,argcount*2):
            temparg=outlist.pop()
            if i & 1:
                if temparg.type in (BUFF_ALPHA, BUFF_NUM, BUFF_FLOAT, BUFF_CHAR, BUFF_STR):
                    #arglist.append(temparg[0])
                    arglist.insert(0,temparg)
                else:
                    print('Error: cannot pass '+temparg.data+' to '+op.data)
                    g.errorhalt=True
                    return
            else:
                if temparg.type!=BUFF_COMMA:
                    print('Error: expected comma in arguments to '+op.data+' but found '+temparg.data)
                    g.errorhalt=True
                    return

        rettype=None
        if op.data.lower()=='alpha':
            retval=str(arglist[0].data)
            rettype='alpha'
        elif op.data.lower()=='str':
            retval=str(arglist[0].data)
            rettype=str
        elif op.data.lower()=='char':
            if len(str(arglist[0].data))==1:
                rettype='char'
            else:
                rettype=str
        else:
            retval=func(*[str(a) for a,b in arglist])    
            if type(retval)==int: rettype=int
            elif type(retval)==float: rettype=float
            elif type(retval)==str:
                if len(arglist)==0:
                    #No input type so can't guess output
                    rettype=str
                else:
                    if arglist[0].type==BUFF_ALPHA: rettype='alpha'
                    elif arglist[0].type==BUFF_NUM: rettype=BUFF_NUM
                    elif arglist[0].type==BUFF_FLOAT: rettype=BUFF_FLOAT
                    elif arglist[0].type==BUFF_CHAR:
                        if len(str(retval))==1: rettype='char'
                        else: rettype=str
                    elif arglist[0].type==BUFF_STR: rettype=str
            else:
                rettype=None
        
        #if not (retval==None or (type(retval)==str and retval=='')): #Null strings???
        if rettype!=None:
            if rettype==int:
                outlist.append(Token(int(retval),BUFF_NUM))
            elif rettype==float:
                outlist.append(Token(float(retval),BUFF_FLOAT))
            elif rettype=='alpha':
                outlist.append(Token(str(retval),BUFF_ALPHA))
            elif rettype==str:
                outlist.append(Token(str(retval),BUFF_STR))
            elif rettype=='char':
                outlist.append(Token(str(retval),BUFF_CHAR))


def ParseLine(instr):
    templist=[]
    tempoutput=[]
    retobj=g.LineType()

    retobj.RawStr=instr

    def AddToList(item,itemtype):
        if itemtype==BUFF_ALPHA:
            #Not supported in AS assembler
            #if item.lower() in ('or','and','xor'):
                #templist.append(Token(item.lower(),BUFF_OP))
            #elif item.lower() in [a.lower() for (a,b,c) in commandlist]:
            if item.lower() in [a.lower() for (a,b,c) in commandlist]:
                templist.append(Token(item.lower(),BUFF_FUNC))
            else:
                templist.append(Token(item,itemtype))
        elif itemtype==BUFF_NUM:
            templist.append(Token(int(item),itemtype))
        elif itemtype==BUFF_FLOAT:
            templist.append(Token(float(item),itemtype))
        elif itemtype==BUFF_HEX:
            templist.append(Token(int(item,16),BUFF_NUM))
        elif itemtype==BUFF_CHAR:
            templist.append(Token(item[0],itemtype))
        elif itemtype==BUFF_STR:
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
        elif itemtype==BUFF_OPEN_BRACKET:
            templist.append(Token(item,itemtype))
        elif itemtype==BUFF_CLOSE_BRACKET:
            templist.append(Token(item,itemtype))
    
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

    instr+=' '
    
    for c in instr:
        loopcounter=1
        while loopcounter>0:
            loopcounter-=1
            if buffstate==BUFF_EMPTY:
                if c==' ' or c=='	':
                    tempbuff=''
                    buffstate=BUFF_EMPTY
                elif c.isalpha() or c in '_.': #Can begin with "." but not contain it
                    tempbuff=c
                    buffstate=BUFF_ALPHA
                elif c.isdigit():
                    tempbuff=c
                    buffstate=BUFF_NUM
                elif c=='$':
                    tempbuff=''
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
                if c.isalpha() or c.isdigit() or c in '_':
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
                        tempbuff+="'"
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

    #Always simplify input unless it is a function
    processinput=True

    if len(templist)>=2:
        if templist[0].type==BUFF_ALPHA and templist[1].type==BUFF_COLON:
            retobj.LabelName=templist.pop(0)
            templist.pop(0)
        elif templist[0].type==BUFF_ALPHA and templist[1].type==BUFF_ALPHA:
            if templist[1].data.upper()=='FUNCTION':
                #print('Function: '+templist[0][0])
                processinput=False
            elif templist[1].data.upper()=='EQU':
                g.noevallist[templist[0].data.upper()]=templist[2:]
                processinput=False
                
    #print('Tokenized:',[a for (a,b) in templist])
    #print('Format: ',MatchPattern(templist,''))
    
        
    if processinput and g.errorhalt==False:
        opstack=[]
        OOP={'^':1,
             '~':2,
             '*':3, '/':3, '%':3,
             '+':4, '-':4,
             '<<':5, '>>':5,
             #'and':6,
             #'xor':7,
             #'or':8
             '&':6,
             '!':7,
             '|':8
             }


        #Equ substitution before processing
        #if matches, need to restart
        #Actually, better to read all in then do this
        equ_recheck=True
        while equ_recheck:
            equ_recheck=False
            for i,j in enumerate(templist):
                if j.type==BUFF_ALPHA and j.data.upper() in g.noevallist:
                    print("EQU:")
                    print(templist)
                    templist=templist[:i]+g.noevallist[j.data.upper()]+templist[i+1:]
                    print(templist)
                    print()
                    equ_recheck=True
                    break
            
        retobj.FormatStr=GenPattern(templist)

        for i in templist:
            if i.type in (BUFF_ALPHA, BUFF_NUM, BUFF_FLOAT, BUFF_CHAR, BUFF_STR, BUFF_HASH, BUFF_OPEN_BRACKET, BUFF_CLOSE_BRACKET):
                tempoutput.append(i)
            elif i.type==BUFF_FUNC:
                opstack.append(i)
            elif i.type==BUFF_OP:
                if len(opstack)>0:
                    while ((opstack[-1].type!=BUFF_OPEN_PAR) and
                           ((opstack[-1].type==BUFF_FUNC) or
                           (OOP[opstack[-1].data]<OOP[i.data]) or
                           ((opstack[-1].data!='^') and
                            (OOP[opstack[-1].data]==OOP[i.data])))):
                        AddOp(opstack.pop(),tempoutput)
                        if g.errorhalt:
                            break
                        elif len(opstack)==0:
                            break
                opstack.append(i)
            elif i.type==BUFF_COMMA:
                while len(opstack)>0 and opstack[-1].type!=BUFF_OPEN_PAR and opstack[-1].type!=BUFF_COMMA:
                    AddOp(opstack.pop(),tempoutput)
                    if g.errorhalt:
                        break
                tempoutput.append(i)
            elif i.type==BUFF_OPEN_PAR:
                opstack.append(i)
            elif i.type==BUFF_CLOSE_PAR:
                while opstack[-1].type!=BUFF_OPEN_PAR:
                    AddOp(opstack.pop(),tempoutput)
                    if g.errorhalt:
                        break
                opstack.pop()
            elif i.type==BUFF_COLON:
                print('Error: colon found outside label')
                g.errorhalt=True
            
            if g.errorhalt:
                break
        if g.errorhalt:
            #sys.exit()
            retobj.Error=BUFF_ERR_FAIL
            return retobj

        while (len(opstack)>0):
            AddOp(opstack.pop(),tempoutput)
            if g.errorhalt:
                break

    if g.errorhalt:
        #sys.exit()
        retobj.Error=BUFF_ERR_FAIL
        return retobj
    
    retobj.TokenList=tempoutput
    return retobj
