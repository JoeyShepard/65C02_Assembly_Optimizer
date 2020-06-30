from const import *
from collections import namedtuple
import globals as g
import sys

#Factory for named tuples
Token=namedtuple('Token','data type')
Evalstring=namedtuple('Evalstring','Resolved DelayedLabel TokenList')
Funcstring=namedtuple('Funcstring','ArgCount TokenList')
Label=namedtuple('Label','Raw Parent Local Lines')
Localvar=namedtuple('Localvar','Name Parent Size Address')

#List of variables in assembly file to ignore when set
# IGNORE_LIST=['LOCAL_LABEL','FUNC_NAME','OPTIMIZER_BUILTIN',
#              'ASSIGN_LOCAL_BYTE','ASSIGN_GLOBAL_BYTE',
#             'ASSIGN_LOCAL_WORD','ASSIGN_GLOBAL_WORD']

def SimplifySource():
    parentlabel=""
    call_function=""
    call_local_counter=0

    g.passcount+=1
    print("Pass:",g.passcount,"- classifying symbols")
    #First pass: convert labels, classify lines (resolved, symbolic, etc)
    for i in range(len(g.proglist)):
        templist=g.proglist[i].TokenList

        #Strip out labels
        if len(templist)>=2:
            if templist[0].type==BUFF_ALPHA and templist[1].type==BUFF_COLON:
                templabel=templist[0].data

                #print("New label:",templabel)
                #Local label
                if templabel[0]==".":
                    locallabel=True
                    combinedlabel=parentlabel+templabel
                else:
                    parentlabel=templabel
                    locallabel=False
                    combinedlabel=templabel
                g.labellist[combinedlabel]=Label(templabel, parentlabel, locallabel, [])
                g.proglist[i].LabelName=g.proglist[i].TokenList.pop(0).data
                g.proglist[i].TokenList.pop(0)
                templist=g.proglist[i].TokenList
        #Assign lastlabel in all cases
        g.proglist[i].LastLabel=parentlabel

        #Mark EQU and SET (including those used by optimizer)
        #(length could be reduced if label removed, so check)
        if len(templist)>=2:
            if templist[0].type==BUFF_ALPHA:
                if templist[1].type==BUFF_EQUAL or templist[1].type==BUFF_SET:
                    if templist[0].data.upper()=='LOCALS_BEGIN':
                        if templist[2].type!=BUFF_NUM:
                            print('Error: non-integer assignment to beginning address of local variables.',g.proglist[i].RawStr)
                            g.errorhalt=True
                            return
                        else:
                            g.ZP_counter=templist[2].data
                            g.globals_begin=templist[2].data
                            g.proglist[i].Resolved=True
                            g.proglist[i].Ignore=True
                    elif templist[0].data.upper()=='LOCALS_END':
                        if templist[2].type!=BUFF_NUM:
                            print('Error: non-integer assignment to end address of local variables.',g.proglist[i].RawStr)
                            g.errorhalt=True
                            return
                        else:
                            g.locals_limit=templist[2].data
                            g.proglist[i].Resolved=True
                            g.proglist[i].Ignore=True
                    elif templist[0].data.upper()=='BEGIN_FUNC':
                        g.begin_func=templist[2].data
                        g.proglist[i].Resolved=True
                        g.proglist[i].Ignore=True
                    # elif templist[0].data.upper() in IGNORE_LIST:
                    #     g.proglist[i].Resolved=True
                    #     g.proglist[i].Ignore=True
                    # elif templist[0].data.upper() == 'CALL_FUNCTION':
                    #     if templist[2].type not in [BUFF_STR,BUFF_ALPHA]:
                    #         print('Error: non-string/alpha assignment to call function.', g.proglist[i].RawStr)
                    #         g.errorhalt = True
                    #         return
                    #     else:
                    #         call_function = templist[2].data
                    #         g.proglist[i].Resolved = True
                    #         g.proglist[i].Ignore = True
                    # elif templist[0].data.upper() == 'CALL_LOCAL_OFFSET':
                    #         g.proglist[i].Resolved = True
                    #         g.proglist[i].Ignore = True
                    # elif templist[0].data.upper() == 'CALL_TEMP_LOCAL':
                    #     g.proglist[i].Resolved = True
                    #     g.proglist[i].Ignore = True
                    # elif templist[0].data.upper() == '{CALL_TEMP_LOCAL}':
                    #     g.proglist[i].Resolved = True
                    #     g.proglist[i].Ignore = True
                    # elif templist[0].data.upper() == 'CALL_LOCAL_RESET':
                    #     call_local_counter=0
                    #     g.proglist[i].Resolved = True
                    #     g.proglist[i].Ignore = True
                    # elif templist[0].data.upper() == 'DELAYED_RESOLVE':
                    #     g.callparamlist+=[templist[2].data]
                    #     g.proglist[i].Resolved = True
                    #     g.proglist[i].Ignore = True
                    elif templist[2].type==BUFF_ALPHA:
                        if templist[2].data.upper()=='ASSIGN_LOCAL_BYTE':
                            g.locallist[parentlabel+"."+templist[0].data]=Localvar(templist[0].data,parentlabel,1,None)
                            g.proglist[i].Resolved=True
                            g.proglist[i].Ignore=True
                        elif templist[2].data.upper()=='ASSIGN_LOCAL_WORD':
                            g.locallist[parentlabel+"."+templist[0].data]=Localvar(templist[0].data,parentlabel,2,None)
                            g.proglist[i].Resolved=True
                            g.proglist[i].Ignore=True
                        elif templist[2].data.upper()=='ASSIGN_GLOBAL_BYTE':
                            #Keep global as simple SET statement (less overhead)
                            g.proglist[i].TokenList[2]=Token(g.ZP_counter,BUFF_NUM)
                            g.ZP_counter+=1
                            g.proglist[i].SymbolUpdate=True
                            #print('Assign global:',templist[0].data)
                            #print('  ',g.proglist[i].TokenList)
                        elif templist[2].data.upper() == 'ASSIGN_GLOBAL_WORD':
                            # Keep global as simple SET statement (less overhead)
                            g.proglist[i].TokenList[2] = Token(g.ZP_counter, BUFF_NUM)
                            g.ZP_counter+=2
                            g.proglist[i].SymbolUpdate = True
                            # print('Assign global:',templist[0].data)
                            # print('  ',g.proglist[i].TokenList)
                        # elif templist[2].data.upper() == 'CALL_LABEL_ONLY':
                        #     # Dummy line so assembler will accept label for passing arguments
                        #     g.proglist[i].Resolved = True
                        #     g.proglist[i].Ignore = True
                        else:
                            #Could throw error here if resetting existing EQU but will never happen
                            g.proglist[i].SymbolUpdate=True
                    else:
                        #Could throw error here if resetting existing EQU but will never happen
                        g.proglist[i].SymbolUpdate=True

        #Instructions
            #(moved to parsing section which now identifies in position, although should only be in first)
        # if len(templist)>=1:
        #     #(prevents redefining instructions but that should have happened already)
        #     if templist[0].type==BUFF_ALPHA:
        #         if templist[0].data.upper() in OP_LIST:
        #             g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data.upper(),BUFF_INSTRUCTION)
        #             templist=g.proglist[i].TokenList

        #Words used by the assembler
        if len(templist)>=1:
            if templist[0].type==BUFF_ALPHA:
                if templist[0].data.upper()=='DFS':
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_DFS)
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper()=='FCB':
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_FCB)
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper()=='FCC':
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_FCC)
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper()=='FDB':
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_FDB)
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper()=='SECTION':
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_SECTION)
                    #Just mark as resolved for now. Probably don't need at all until output stage
                    g.proglist[i].Resolved=True
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper() in ASM_LIST:
                    g.proglist[i].TokenList[0]=Token(g.proglist[i].TokenList[0].data,BUFF_ASMWORD)
                    templist=g.proglist[i].TokenList
                elif templist[0].data.upper() == 'MESSAGE':
                    #Disable for now since MESSAGE already printed
                    g.proglist[i].TokenList=[]
                    templist = []
            elif len(templist)>=2:
                if templist[0].type == BUFF_OP:
                    if templist[0].data=="%":
                        if templist[1].type == BUFF_ALPHA:
                            if templist[1].data.upper() == "LINE":
                                g.proglist[i].Ignore = True
                                g.proglist[i].Resolved = True

        #Labels (only works if label definition comes first! moved below)
        # for k,a in enumerate(templist):
        #     if a.type==BUFF_ALPHA:
        #         if a.data in g.labellist:
        #             g.proglist[i].TokenList[k]=Token(g.proglist[i].TokenList[k].data,BUFF_LABEL)
        #             templist=g.proglist[i].TokenList
        #             #print("Label access:",[b.data for b in templist])

        #Functions defined in assembly file
        #(could be label or just symbol)
        #(seems cannot be local to macro or redefined)
        if len(templist)>=1:
            if g.proglist[i].LabelName!="":
                if ((templist[0].type==BUFF_ALPHA) and (templist[0].data.upper()=="FUNCTION")):
                    g.proglist[i].TokenList.insert(0,Token(g.proglist[i].LabelName,BUFF_ALPHA))
                    templist=g.proglist[i].TokenList
                    del g.labellist[g.proglist[i].LabelName]
                    #print("Label removed:",g.proglist[i].LabelName)
        if len(templist)>=2:
            if templist[0].type==BUFF_BUILTIN and \
            ((templist[2].type==BUFF_ALPHA) and (templist[2].data.upper()=="CUSTOM")): #and \
            #((templist[4].type==BUFF_ALPHA) and (templist[4].data.upper()=="OPTIMIZER_BUILTIN")):
                #Macro for builtins defines as FUNCTION but don't add
                #Could add error here if trying to redefine a built in (now just allows)
                g.proglist[i].Ignore=True
                g.proglist[i].Resolved=True
            elif (templist[0].type==BUFF_ALPHA):
                if ((templist[1].type==BUFF_ALPHA) and (templist[1].data.upper()=="FUNCTION")):
                    temparglist=templist[2:]
                    FUNC_ARG_EXPECTED=0
                    FUNC_COMMA_EXPECTED=1
                    FUNC_COMMA_NOT_ALLOWED=2
                    func_search_state=FUNC_ARG_EXPECTED
                    func_arg_count=0
                    func_last_arg=""
                    func_name=templist[0].data
                    for j in range(len(temparglist)-    1):
                        if func_search_state==FUNC_ARG_EXPECTED:
                            func_last_arg=temparglist[j]
                            if temparglist[j].type==BUFF_ALPHA:
                                func_search_state=FUNC_COMMA_EXPECTED
                            elif temparglist[j].type==BUFF_COMMA:
                                print('Error: missing argument in function:',g.proglist[i].RawStr)
                                g.errorhalt=True
                                return
                            else:
                                #Something other than alpha after comma means function body
                                func_search_state=FUNC_COMMA_NOT_ALLOWED
                        elif func_search_state==FUNC_COMMA_EXPECTED:
                            if temparglist[j].type==BUFF_COMMA:
                                func_search_state=FUNC_ARG_EXPECTED
                                func_arg_count+=1
                            else:
                                #Function body has started
                                func_search_state=FUNC_COMMA_NOT_ALLOWED
                    tempfunclist=temparglist[func_arg_count*2:]
                    temparglist=[temparglist[a] for a in range(0,func_arg_count*2,2)]
                    for k,a in enumerate(tempfunclist):
                        #Should always be true. MA wouldn't allow otherwise.
                        if a.type==BUFF_ALPHA:
                            if a.data in [b.data for b in temparglist]:
                                tempfunclist[k]=Token([b.data for b in temparglist].index(a.data),BUFF_FUNCARG)

                    #g.funclist[func_name]=Funcstring(func_arg_count,[temparglist[a] for a in range(0,func_arg_count*2,2)],temparglist[func_arg_count*2:])
                    g.funclist[func_name]=Funcstring(func_arg_count,[Token("(",BUFF_OPEN_PAR)]+tempfunclist+[Token(")",BUFF_CLOSE_PAR)])
                    #print(g.proglist[i].RawStr)
                    #print("   Arg count:",g.funclist[func_name].ArgCount)
                    #print("   Function:",[a.data for a in g.funclist[func_name].TokenList])

                    #Added to function list so no need to keep processing
                    #(also, AS re-evaluates symbol *every time* function is invoked)
                    #Don't delete since label still exists
                    g.proglist[i].Ignore=True
                    g.proglist[i].Resolved=True

        # #Replace {CALL_TEMP_LOCAL} with constructed call variable name
        # if g.proglist[i].Ignore==False:
        #     for j,token in enumerate(g.proglist[i].TokenList):
        #         if token.type==BUFF_ALPHA:
        #             if token.data=="{CALL_TEMP_LOCAL}":
        #                 g.proglist[i].TokenList[j] = Token(f"{call_function}.local{call_local_counter}", BUFF_ARG)
        #                 templist = g.proglist[i].TokenList
        #                 call_local_counter+=1
        #                 #Somewhat dangerous to set this since line may contain unresolved symbols
        #                 #However, always generated by macro, so risk is small
        #                 g.proglist[i].Resolved = True

        #Generate format strings
        g.proglist[i].FormatStr=GenPattern(templist)
    print("   Done")

    #Second pass and above - resolve symbols and calculate
    passcount=1
    repass=True

    while repass:
        unresolved_count=0
        g.passcount+=1
        print("Pass:",g.passcount,"- resolving references")
        repass=False
        for i in range(len(g.proglist)):
            if g.proglist[i].Ignore:continue
            if g.proglist[i].Resolved:continue
            if g.proglist[i].DelayedLabel:continue
            templist=g.proglist[i].TokenList
            #SET or EQU
            if g.proglist[i].SymbolUpdate:
                #print('Symbol update')
                #print([a.data for a in templist])
                #print("Begin:",[a.data for a in templist])
                #if templist[0].data in g.evallist:
                    #print("  ",templist[0].data+":",[a.data for a in g.evallist[templist[0].data].TokenList])
                #else:
                    #print("  ",templist[0].data+": unresolved")
                containslabel,containslocal,allresolved,newtokens=ExpandLine(templist[2:],100,g.proglist[i])
                g.evallist[templist[0].data]=Evalstring(allresolved,containslabel,newtokens)
                #print("Reval:",containslabel)
                #if containslabel:
                    #print("SET or EQU containing label")
                #print("   newtokens:",[a.data for a in newtokens])
                g.proglist[i].TokenList=templist[:2]+newtokens
                g.proglist[i].Resolved=allresolved

                templist=g.proglist[i].TokenList
                if allresolved==False:
                    repass=True
                    unresolved_count+=1
                #print("   Resolved:",allresolved)
                #print("End:",[a.data for a in templist])
                #print()
            else:
                containslabel,containslocal,allresolved,newtokens=ExpandLine(templist,100,g.proglist[i])
                g.proglist[i].TokenList=newtokens
                g.proglist[i].Resolved=allresolved
                g.proglist[i].DelayedLabel=containslabel
                g.proglist[i].LocalVar=containslocal
                #print('Returned',containslabel,'\n')
                templist=g.proglist[i].TokenList
                if allresolved==False:
                    repass=True
                    unresolved_count+=1

        if unresolved_count==0:
            print("   Done")
        elif g.passcount==10:
            print("   unresolved references after 10 passes!")
            for a in [a for a in g.proglist if a.Resolved==False]:
                print("   Line",a.FileLine,a.RawStr)
            sys.exit()
        elif unresolved_count==1:
            print("  ",unresolved_count,"reference left")
        else:
            print("  ",unresolved_count,"references left")

#TODO: clean up list use to make clear which are references and which are new lists
def ExpandLine(line,max_loops,lineobj):
    #print('Enter Expand')
    #print([a.data for a in line])
    reprocessline=True
    linecount=0
    while reprocessline:
        reprocessline=False
        linecount+=1
        if linecount>=max_loops:
            #Handle infinite loop here
            pass
        allresolved=True
        containslabel=False
        containslocal=False
        for j in range(len(line)):
            if line[j].type==BUFF_ALPHA or line[j].type==BUFF_LABEL:
                if line[j].data in g.builtin_dict:
                    #Should have been set in parse.py but just to be safe
                    line[j]=Token(line[j].data,BUFF_BUILTIN)
                    #print("   Builtin:",line[j].data)
                elif line[j].data in g.funclist:
                    line[j]=Token(line[j].data,BUFF_FUNC)
                    #print("   Function:",line[j].data)
                    #print("      Start: ",[a.data for a in line])
                    #Expand function
                    if line[j+1].type!=BUFF_OPEN_PAR:
                        print("Error: function without opening parenthesis.")
                        sys.exit()
                    func_paren_count=1
                    func_temp_arg=[]
                    func_arg_list=[]
                    func_final_list=[]
                    for k in range(j+2,len(line)):
                        #print("         ",k,"=",line[k].data)
                        if line[k].type==BUFF_OPEN_PAR:
                            func_paren_count+=1
                            func_temp_arg.append(line[k])
                        elif line[k].type==BUFF_CLOSE_PAR or line[k].type==BUFF_COMMA:
                            if func_paren_count==1:
                                #print("         Append:",[a.data for a in func_temp_arg])
                                func_arg_list.append([Token("(",BUFF_OPEN_PAR)]+func_temp_arg+[Token(")",BUFF_CLOSE_PAR)])
                                func_temp_arg=[]
                            else:
                                if line[k].type==BUFF_COMMA:
                                    func_temp_arg.append(line[k])
                        else:
                            func_temp_arg.append(line[k])
                        if line[k].type==BUFF_CLOSE_PAR:
                            func_paren_count-=1
                            if func_paren_count==0:
                                reprocessline=True
                                func_end_index=k+1
                                break
                            else:
                                func_temp_arg.append(line[k])
                    for a in g.funclist[line[j].data].TokenList:
                        if a.type!=BUFF_FUNCARG:
                            #print("         Not funcarg:",a.data)
                            func_final_list.append(a)
                        else:
                            #print("         Funcarg:",[a.data for a in func_arg_list[a.data]])
                            func_final_list+=func_arg_list[a.data]
                        #print("        ",[a.data for a in func_final_list])

                    #print("         First:",[a.data for a in line[:j]])
                    #print("         Second:",[a.data for a in func_final_list])
                    #print("         Third:",[a.data for a in line[func_end_index:]])
                    line=line[:j]+func_final_list+line[func_end_index:]
                    #print("      End: ",[a.data for a in line])
                elif line[j].data[0]=="." and lineobj.LastLabel+line[j].data in g.labellist:
                    line[j]=Token(line[j].data,BUFF_LABEL)
                    containslabel=True
                    #print('Local label referenced:',lineobj.LastLabel,line[j].data,lineobj.RawStr)
                elif line[j].data in g.labellist:
                    line[j]=Token(line[j].data,BUFF_LABEL)
                    containslabel=True
                    #print('Label referenced:',line[j].data,lineobj.RawStr)
                elif lineobj.LastLabel+"."+line[j].data in g.locallist:
                    line[j]=Token(line[j].data,BUFF_LOCAL)
                    containslocal=True
                    #print('Local variable reference:',lineobj.LastLabel+"."+line[j].data)
                #Should only be for passing parameters
                elif line[j].data in g.locallist:
                    line[j] = Token(line[j].data, BUFF_LOCAL)
                    containslocal = True
                elif line[j].data in g.evallist:
                    #print("   Set:",line[j].data)
                    if g.evallist[line[j].data].Resolved:
                        #print("      1:",[a.data for a in line[:j]])
                        #print("      2:",[a.data for a in g.evallist[line[j].data].TokenList])
                        #print("      3:",[a.data for a in line[j+1:]])
                        #print('Evaluation:',line[j].data)
                        if g.evallist[line[j].data].DelayedLabel:
                            #print("   Delayed label")
                            containslabel=True
                        #else:
                            #print("   No delayed label")
                        newtoken=g.evallist[line[j].data].TokenList
                        line=line[:j]+newtoken+line[j+1:]
                        for k in newtoken:
                            if k.type==BUFF_LOCAL:
                                containslocal = True
                    else:
                        #print("      unresolved")
                        allresolved=False
                else:
                    #Unresolved symbol!
                    allresolved=False
                    #print("   Unresolved:",line[j].data)
            if reprocessline: break
        #print('1.',containslabel)
        #print([a.data for a in line])
    #print('2.',containslabel)

    #Stop searching if contains label
    if containslabel or containslocal:
        allresolved=True

    #If all symbols resolved, do calculations
    #(must do calculations before substituting)
    if allresolved and containslabel==False and containslocal==False:
        #try:
        retobj=CalculateLine(line,lineobj)
        #except:
            #print("Error: unable to simplify -",line)
            #sys.exit()



        if retobj.Error==BUFF_ERR_FAIL:
            sys.exit()
        #TODO: stop using retobj since code has been refactored
        line=retobj.TokenList
    return containslabel,containslocal,allresolved,line

def CalculateLine(line,lineobj):
    opstack=[]
    objstack=[]
    retobj=g.LineType()
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

    #print("   Calculate begin:",[a.data for a in line])

    for i in line:
        if i.type in (BUFF_INSTRUCTION, BUFF_XREG, BUFF_YREG, BUFF_NUM, BUFF_FLOAT, BUFF_CHAR, BUFF_STR, BUFF_HASH,
        BUFF_OPEN_BRACKET, BUFF_CLOSE_BRACKET, BUFF_PCSTAR, BUFF_ASMWORD, BUFF_DFS, BUFF_FCB, BUFF_FCC, BUFF_FDB, BUFF_BOOLEAN):
            objstack.append(i)
            #print("      Object:",i.data)
        elif i.type==BUFF_FUNC:
            opstack.append(i)
            #print("      Function:",i.data)
        elif i.type==BUFF_BUILTIN:
            opstack.append(i)
        elif i.type==BUFF_OP:
            if len(opstack)>0:
                while ((opstack[-1].type!=BUFF_OPEN_PAR) and
                        ((opstack[-1].type==BUFF_FUNC) or
                        (opstack[-1].type == BUFF_BUILTIN) or
                        (OOP[opstack[-1].data]<OOP[i.data]) or
                        ((opstack[-1].data!='^') and
                        (OOP[opstack[-1].data]==OOP[i.data])))):
                    objstack=AddOp(opstack.pop(),objstack)
                    if g.errorhalt:
                        break
                    elif len(opstack)==0:
                        break
            opstack.append(i)
            #print("      Op stack:",i.data)
        elif i.type==BUFF_COMMA:
            while len(opstack)>0 and opstack[-1].type!=BUFF_OPEN_PAR and opstack[-1].type!=BUFF_COMMA:
                objstack=AddOp(opstack.pop(),objstack)
                if g.errorhalt:
                    break
            objstack.append(i)
        elif i.type==BUFF_OPEN_PAR:
            opstack.append(i)
        elif i.type==BUFF_CLOSE_PAR:
            while opstack[-1].type!=BUFF_OPEN_PAR:
                objstack=AddOp(opstack.pop(),objstack)
                if g.errorhalt:
                    break
            opstack.pop()
        elif i.type==BUFF_COLON:
            print('Error: colon found outside label')
            g.errorhalt=True
        else:
            print('Error: unknown item type in calculation:',i.type)
            g.errorhalt=True

        if g.errorhalt:
            break
    if g.errorhalt:
        #sys.exit()
        print("Line",lineobj.FileLine,":",lineobj.RawStr)
        retobj.Error=BUFF_ERR_FAIL
        return retobj

    while (len(opstack)>0):
        objstack=AddOp(opstack.pop(),objstack)
        if g.errorhalt:
            break

    if g.errorhalt:
        #sys.exit()
        print("Line",lineobj.FileLine,":",lineobj.RawStr)
        retobj.Error=BUFF_ERR_FAIL
        return retobj

    #print("   Calculate done:",[a.data for a in objstack])

    retobj.TokenList=objstack
    return retobj


def AddOp(op, inlist):
    outlist=inlist[:]
    if op.type==BUFF_OP:
        #print("         AddOp: op",op.data)
        if op.data not in '~*+': #Ops work only on numbers, except * and +
            if len(outlist)<2:
                print('Error: evaluation error, '+op.data+' requires two arguments')
                g.errorhalt=True
                return
            arg1=outlist.pop()
            arg2=outlist.pop()
            numcount=0
            if arg1.type in [BUFF_NUM, BUFF_FLOAT, BUFF_CHAR]: numcount+=1
            if arg2.type in [BUFF_NUM, BUFF_FLOAT, BUFF_CHAR]: numcount+=1
            if numcount!=2:
                print('Error: evaluation error, '+op.data+' expects int or float')
                #print(arg1, arg2)
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
                    return outlist
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
            #print("         Arg types:",arg1.type,arg2.type)
            if arg1.type==BUFF_NUM or arg1.type==BUFF_FLOAT:
                numcount=1
                otherarg=arg2
            if arg2.type==BUFF_NUM or arg2.type==BUFF_FLOAT:
                if numcount==1:
                    tempval=arg1.data+arg2.data
                    if '.' in str(tempval): outlist.append(Token(tempval,BUFF_FLOAT))
                    else: outlist.append(Token(tempval,BUFF_NUM))
                    #print("         tempval:",tempval)
                    #print("         Sum:",[a.data for a in outlist])
                    return outlist
                else:
                    numcount=1
                    otherarg=arg1
            if numcount==1:
                if otherarg.type==BUFF_ALPHA:
                    outlist.append(Token(str(arg2.data)+str(arg1.data),BUFF_ALPHA))
                elif otherarg.type==BUFF_CHAR:
                    if arg1.type==BUFF_CHAR:
                        #outlist.append(Token(ord(arg1.data[0])+int(arg2.data),BUFF_NUM))
                        outlist.append(Token(arg1.data[0]+int(arg2.data),BUFF_NUM))
                    else:
                        #outlist.append(Token(ord(arg2.data[0])+int(arg1.data),BUFF_NUM))
                        outlist.append(Token(arg2.data+int(arg1.data),BUFF_NUM))
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
    elif op.type==BUFF_BUILTIN:
        #if op.data=='lo':
            #print([a for a in outlist])
        #print("         AddOp: builtin",op.data)
        argcount=g.builtin_dict[op.data][0]
        func=g.builtin_dict[op.data][1]
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
                #outlist.append(Token(str(retval),BUFF_CHAR))
                outlist.append(Token(chr(retval),BUFF_CHAR))
    #Expanded before calculation
    #THIS SHOULD NEVER RUN
    """
    elif op.type==BUFF_FUNC:
        print(op.data)
        argcount=g.funclist[op.data].ArgCount
        print("   Arg count:",argcount)
        if len(outlist)<(argcount*2-1):
            print('Error: '+op.data+' takes '+str(argcount)+' argments')
            g.errorhalt=True
            return
        arglist=[]
        for a in range(argcount):
            temparg=outlist.pop()
            outlist.pop()
            arglist.insert(0,temparg)
        print("   Arg list:",[a.data for a in arglist])
        tempfuncexpansion=[]
        for a in g.funclist[op.data].TokenList:
            if a.type==BUFF_FUNCARG:
                tempfuncexpansion.append(arglist[a.data])
            else:
                tempfuncexpansion.append(a)
        print("   Func list:",[a.data for a in tempfuncexpansion])
        #Dummy value for debugging
        outlist.append(Token(0,BUFF_NUM))
    #UNFINISHED
    """
    return outlist

#Generates a string representing the pattern found (LDA (5+2),Y = O(*),Y)
def GenPattern(mainlist):
    formatstr=''
    i=0;
    i_end=len(mainlist)
    found1=False
    found2=False
    parcountouter=0

    while i<i_end:
        if mainlist[i].type==BUFF_ALPHA:
            #if mainlist[i].data.upper() in OP_LIST:
                #if found1:
                    #found1=False
                    #formatstr+='*'
                #formatstr+='O'
            #elif mainlist[i].data.lower() in ['x','y']:
                #if found1:
                    #found1=False
                    #formatstr+='*'
                #formatstr+=mainlist[i].data.upper()
            #else:
                #if found1:
                    #found1=False
                    #formatstr+='*'
                #formatstr+='A'
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='A'
        elif mainlist[i].type==BUFF_INSTRUCTION:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='O'
        elif mainlist[i].type==BUFF_XREG:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='X'
        elif mainlist[i].type==BUFF_YREG:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='Y'
        elif mainlist[i].type==BUFF_HASH:
            if found1:
                found1=False
                formatstr+='*'
            formatstr+='#'
        elif mainlist[i].type==BUFF_EQUAL or mainlist[i].type==BUFF_SET:
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
                #elif mainlist[i].type==BUFF_ALPHA:
                    #if parcount==1:
                        #if mainlist[i].data.lower() in ['x','y']:
                            #if found2:
                                #formatstr+='*'
                                #found2=False
                            #formatstr+=mainlist[i].data.upper()
                elif mainlist[i].type==BUFF_XREG:
                    if parcount==1:
                        if found2:
                            formatstr+='*'
                            found2=False
                        formatstr+='X'
                elif mainlist[i].type==BUFF_YREG:
                    if parcount==1:
                        if found2:
                            formatstr+='*'
                            found2=False
                        formatstr+='Y'
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

#Old version expecting only 8 bit literals
#(new version directly below
# def TwosComplement(number,rawstr):
#     if number>0:
#         return number
#     else:
#         number=-number
#         if number>128:
#             #Negative numbers are only valid for 8 bit length numbers
#             #(may want to add support for other sizes for FDB)
#             print("Error: negative value out of range.",rawstr.lstrip())
#             sys.exit()
#         else:
#             return 0x100-number

def TwosComplement(number,rawstr):
    retval=[]
    minsize=0

    if type(number)==float:
        number=int(number)

    if type(number)!=int:
        print("Error: invalid value for TwosComplement -",number,"from",rawstr)
        sys.exit()

    if number==None:
        retval=[0xFF,0]
        minsize=1
    elif number>=0 and number<256:
        retval=[number,0]
        minsize=1
    elif number>=256 and number<2**16:
        retval=[number&0xFF,(number>>8)]
        minsize=2
    elif number>=2**16:
        print("Error: overflow in value in instruction.",rawstr.strip())
        sys.exit()
    elif number<=-(2**16):
        print("Error: negative overflow in value in instruction.",rawstr.strip())
        sys.exit()
    else:
        #Negative number
        number=0x10000+number
        retval=[number&0xFF,(number>>8)]
        if retval[1]==0xFF:
            minsize=1
        else:
            minsize=2
    return minsize,retval

#Branch instructions should all be symbollic and unresolved, so this should skip them
#Also skips BBR/BBS since must also use symbollic addresses
def AssignInstructions():
    #One pass. Don't worry yet if labels or builtin functions are unresolvable
    g.passcount+=1
    print("Pass:",g.passcount,"- assigning instructions")
    #print("   Total lines:",len(g.proglist))
    for i,line in enumerate(g.proglist):
        if line.TokenList!=[] and line.Binary==[] and BUFF_LOCAL not in [a.type for a in line.TokenList]:
            if BUFF_ARG not in [a.type for a in line.TokenList]:
                if line.TokenList[0].type==BUFF_INSTRUCTION:
                    #print(i,"Instruction:",line.RawStr.lstrip())
                    searchmode=None
                    if line.DelayedLabel:
                        #print("   DELAYED EXPANSION:",line.RawStr.lstrip())
                        pass
                    else:
                        if len(line.TokenList)==1:
                            searchmode=MODE.IMPLICIT
                        elif len(line.TokenList)==2:
                            searchmode=MODE.ARG_UNKNOWN
                        elif len(line.TokenList)==3:
                            if line.TokenList[1].type!=BUFF_HASH:
                                print("Error: invalid instruction format:",line.RawStr.strip())
                                sys.exit()
                            else:
                                searchmode=MODE.IMMED
                        #How about BBRO $00,$0000???
                        #Skip for now since always uses address which is not yet resolved
                        elif len(line.TokenList)==4:
                            if line.TokenList[2].type==BUFF_COMMA and line.TokenList[3].type==BUFF_XREG:
                                searchmode=MODE.ARG_UNKNOWN_X
                            elif line.TokenList[2].type==BUFF_COMMA and line.TokenList[3].type==BUFF_YREG:
                                searchmode=MODE.ARG_UNKNOWN_Y
                            else:
                                print("Error: invalid instruction format:",line.RawStr.strip())
                                #print("   ",[a.data for a in line.TokenList])
                                sys.exit()

                        if searchmode==MODE.IMPLICIT:
                            op_data=[]
                            #print("   Implicit:",end=" ")
                        elif searchmode in [MODE.ZP, MODE.ABS, MODE.INDIRECT, MODE.INDIRECT_ZP, MODE.ARG_UNKNOWN]:
                            op_size,op_data=TwosComplement(line.TokenList[1].data,line.RawStr)
                            if op_size==2 and (searchmode==MODE.ZP or searchmode==MODE.INDIRECT_ZP):
                                print("Error: instruction expects zero page address:",line.RawStr.strip())
                                sys.exit()
                            if searchmode==MODE.ARG_UNKNOWN:
                                if line.TokenList[0].data=="JSR":
                                    #Could throw error here since must use labels with JSR
                                    searchmode=MODE.ABS
                                elif line.TokenList[0].data=="JMP":
                                    if line.FormatStr=="O(*)": searchmode=MODE.INDIRECT
                                    else:
                                        #Could throw error here since must use labels to jump
                                        searchmode=MODE.ABS
                                elif op_size==1:
                                    if line.FormatStr=="O(*)": searchmode=MODE.INDIRECT_ZP
                                    else: searchmode=MODE.ZP
                                else:
                                    if line.FormatStr=="O(*)": searchmode=MODE.INDIRECT
                                    else: searchmode=MODE.ABS
                            if searchmode in [MODE.ZP,MODE.INDIRECT_ZP]:
                                op_data=[op_data[0]]
                                #print("   ZP/(ZP):",end=" ")
                            #else:
                                #print("   ABS/(ABS):",end=" ")
                        elif searchmode==MODE.IMMED:
                            op_size,op_data=TwosComplement(line.TokenList[2].data,line.RawStr)
                            if op_size!=1:
                                print("Error: immediate value out of range:",line.RawStr.strip())
                                sys.exit()
                            op_data=[op_data[0]]
                            #print("   Immed:",end=" ")
                        elif searchmode in [MODE.ZP_X, MODE.ABS_X, MODE.INDIRECT_X, MODE.INDIRECT_ABS_X, MODE.ARG_UNKNOWN_X]:
                            op_size,op_data=TwosComplement(line.TokenList[1].data,line.RawStr)
                            if searchmode==MODE.ARG_UNKNOWN_X:
                                if line.TokenList[0].data=="JMP":
                                    if line.FormatStr=="O(*,X)":
                                        searchmode=MODE.INDIRECT_ABS_X
                                    else:
                                        print("Error: invalid instruction format:",line.RawStr.strip())
                                        sys.exit()
                                elif op_size==1:
                                    if line.FormatStr=="O(*,X)": searchmode=MODE.INDIRECT_X
                                    else: searchmode=MODE.ZP_X
                                else:
                                    searchmode=MODE.ABS_X
                            if searchmode in [MODE.ZP_X,MODE.INDIRECT_X]:
                                op_data=[op_data[0]]
                                #print("   ZP,X/(ZP,X):",end=" ")
                            #elif searchmode in [MODE.ABS_X]:
                                #print("   ABS,X:",end=" ")
                            #elif searchmode in [MODE.INDIRECT_ABS_X]:
                                #print("   (ABS,X):",end=" ")
                        elif searchmode in [MODE.ABS_Y, MODE.ZP_Y, MODE.INDIRECT_Y, MODE.ARG_UNKNOWN_Y]:
                            op_size,op_data=TwosComplement(line.TokenList[1].data,line.RawStr)
                            if searchmode==MODE.ARG_UNKNOWN_Y:
                                if op_size==1:
                                    if line.FormatStr=="O(*),Y": searchmode=MODE.INDIRECT_Y
                                    else: searchmode=MODE.ZP_Y
                                else:
                                    searchmode=MODE.ABS_Y
                            if searchmode in [MODE.ZP_Y,MODE.INDIRECT_Y]:
                                op_data=[op_data[0]]
                                #print("   ZP,Y/(ZP),Y:",end=" ")
                            #elif searchmode in [MODE.ABS_Y]:
                                #print("   ABS,Y:",end=" ")
                        else:
                            print("Error: invalid instruction format",line.RawStr.strip())
                            sys.exit()

                        if line.TokenList[0].data in [a.OpCode for a in g.instructionlist.values() if a.OpMode==searchmode]:
                            temphex=[k for k,v in g.instructionlist.items() if line.TokenList[0].data==v.OpCode and v.OpMode==searchmode]
                            g.proglist[i].Binary=temphex+op_data

                            if g.instructionlist[temphex[0]].OpMode==MODE.ABS:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source+="$"+hex(op_data[0]+(op_data[1]<<8))[2:].upper()
                            elif g.instructionlist[temphex[0]].OpMode==MODE.ABS_X:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source+="$"+hex(op_data[0] + (op_data[1] << 8))[2:].upper()+",X"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.ABS_Y:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source+="$"+hex(op_data[0]+(op_data[1]<<8))[2:].upper()+",Y"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.BB:
                                pass
                            elif g.instructionlist[temphex[0]].OpMode == MODE.IMMED:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source+="#$"+hex(op_data[0])[2:].upper()
                            elif g.instructionlist[temphex[0]].OpMode == MODE.IMPLICIT:
                                g.proglist[i].Source = " "+line.TokenList[0].data
                            elif g.instructionlist[temphex[0]].OpMode == MODE.INDIRECT:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source+="($"+hex(op_data[0] + (op_data[1] << 8))[2:].upper()+")"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.INDIRECT_ABS_X:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "($" + hex(op_data[0] + (op_data[1] << 8))[2:].upper() + ",X)"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.INDIRECT_X:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "($" + hex(op_data[0])[2:].upper()+",X)"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.INDIRECT_Y:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "($" + hex(op_data[0])[2:].upper()+"),Y"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.INDIRECT_ZP:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "($" + hex(op_data[0])[2:].upper()+")"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.REL:
                                pass
                            elif g.instructionlist[temphex[0]].OpMode == MODE.ZP:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "$" + hex(op_data[0])[2:].upper()
                            elif g.instructionlist[temphex[0]].OpMode == MODE.ZP_X:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "$" + hex(op_data[0])[2:].upper()+",X"
                            elif g.instructionlist[temphex[0]].OpMode == MODE.ZP_Y:
                                g.proglist[i].Source = " "+line.TokenList[0].data + " "
                                g.proglist[i].Source += "$" + hex(op_data[0])[2:].upper()+",Y"
                            else:
                                print("Error: invalid op mode", line.RawStr.strip())
                                sys.exit()
                        else:
                            print("Error: invalid instruction format",line.RawStr.strip())
                            sys.exit()

    #print('End of function')
    #for i,line in enumerate(g.proglist):
    #    if line.TokenList!=[] and line.Binary!=[]:
    #        print(line.RawStr.strip(),line.Binary)

    print("   Done")

def GenerateAddresses():
    for line in g.proglist:
        #if BUFF_LABEL in [a.type for a in line.TokenList]:
        if line.DelayedLabel:
            #print(line.RawStr,[b for b in line.TokenList])
            pass