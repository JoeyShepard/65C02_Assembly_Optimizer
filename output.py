import globals as g
from const import *
import sys
from collections import namedtuple

Token=namedtuple('Token','data type')
space_tokens=[BUFF_ALPHA,BUFF_NUM,BUFF_FLOAT,BUFF_HEX,BUFF_CHAR,BUFF_HASH,BUFF_SET,
            BUFF_INSTRUCTION,BUFF_XREG,BUFF_YREG,BUFF_BUILTIN,BUFF_LABEL,BUFF_ASMWORD,BUFF_FCB,BUFF_FDB,
            BUFF_SECTION,BUFF_BOOLEAN,BUFF_GLOBAL,BUFF_LOCAL]

def PrintSource(filename):
    file=open(filename,'w')
    for a in g.proglist:
        tokenlast=Token('',BUFF_EMPTY)
        templine=''
        if a.LabelName!=None:
            templine+=a.RawStr[:len(a.RawStr)-len(a.RawStr.lstrip())]
            if a.LabelName[0]!='.': templine+='\n'
            templine+=a.LabelName+':'
            if a.TokenList!=[]: templine+='\n'
        if a.Ignore==False and a.SymbolUpdate==False:
            if a.TokenList!=[]:
                templine+=a.RawStr[:len(a.RawStr)-len(a.RawStr.lstrip())]
            for token in a.TokenList:
                #TODO: condense this if statement when behavior is settled on
                if token.type==BUFF_ALPHA:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_NUM:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+='$'+hex(token.data)[2:].upper()
                elif token.type==BUFF_FLOAT:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=str(token.data)
                elif token.type==BUFF_HEX:
                    print('Error: token marked hex in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_CHAR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+="'"+chr(token.data)+"'"
                elif token.type==BUFF_STR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+='"'+token.data+'"'
                elif token.type==BUFF_OP:
                    templine+=token.data
                elif token.type==BUFF_HASH:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_COLON:
                    templine+=token.data
                elif token.type==BUFF_COMMA:
                    templine+=token.data
                elif token.type==BUFF_OPEN_PAR:
                    templine+=token.data
                elif token.type==BUFF_CLOSE_PAR:
                    templine+=token.data
                elif token.type==BUFF_EQUAL:
                    # #Don't output EQU statements that conflict with label names
                    # #(these are necessary at beginning to get macros to work,
                    # #but conflict after expansion and won't assemble.)
                    # if tokenlast.type==BUFF_ALPHA:
                    #     #Only searches for top level labels, not local labels
                    #     #since macros never assign to local label with EQU
                    #     if tokenlast.data in g.labellist:
                    #         print("EQU assign to label name",tokenlast.data)
                    if token.data!='=':templine+=' '
                    templine+=token.data
                elif token.type==BUFF_OPEN_BRACKET:
                    templine+=token.data
                elif token.type==BUFF_CLOSE_BRACKET:
                    templine+=token.data
                elif token.type==BUFF_SET:
                    templine+=' '
                    templine+=token.data
                elif token.type==BUFF_INSTRUCTION:
                    templine+=token.data
                elif token.type==BUFF_XREG:
                    templine+=token.data
                elif token.type==BUFF_YREG:
                    templine+=token.data
                elif token.type==BUFF_FUNC:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_BUILTIN:
                    print('Error: token marked builtin in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_FUNCARG:
                    print('Error: token marked funcarg in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LABEL:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_PCSTAR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_ASMWORD:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_FCB:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_FDB:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_SECTION:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_BOOLEAN:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    if token.data:
                        templine+='TRUE'
                    else:
                        templine+='FALSE'
                elif token.type==BUFF_GLOBAL_SIZE:
                    print('Error: token marked global size in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_GLOBAL:
                    print('Error: token marked global in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LOCAL_SIZE:
                    print('Error: token marked local size in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LOCAL:
                    print('Error: token marked local in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                else:
                    print('Error: unknown token type in output:',a.type)
                    #g.errorhalt=True
                    #break
                tokenlast=token
            if g.errorhalt:
                break
            file.write(templine+'\n')
    file.close()
    if g.errorhalt:
        sys.exit()

def PrintSourceHTML(filename):
    file=open(filename,'w')

    file.write('<!DOCTYPE html><html><body>')
    file.write('<table border="1"><tr><td><b>Line</b></td><td><b>Original</b></td><td><b>Processed</b></td><td><b>Binary</b></td><td><b>Status</b></td></tr>')

    for linenumber,a in enumerate(g.proglist):
        linestatus=''
        tokenlast=Token('',BUFF_EMPTY)
        templine=''
        if a.LabelName!=None:
            templine+=a.RawStr[:len(a.RawStr)-len(a.RawStr.lstrip())]
            if a.LabelName[0]!='.': templine+='\n'
            templine+=a.LabelName+':'
            if a.TokenList!=[]: templine+='\n'
        if a.Ignore==False and a.SymbolUpdate==False:
            if a.TokenList!=[]:
                templine+=a.RawStr[:len(a.RawStr)-len(a.RawStr.lstrip())]
            for token in a.TokenList:
                #TODO: condense this if statement when behavior is settled on
                if token.type==BUFF_ALPHA:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_NUM:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+='$'+hex(token.data)[2:].upper()
                elif token.type==BUFF_FLOAT:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=str(token.data)
                elif token.type==BUFF_HEX:
                    print('Error: token marked hex in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_CHAR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+="'"+chr(token.data)+"'"
                elif token.type==BUFF_STR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+='"'+token.data+'"'
                elif token.type==BUFF_OP:
                    templine+=token.data
                elif token.type==BUFF_HASH:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_COLON:
                    templine+=token.data
                elif token.type==BUFF_COMMA:
                    templine+=token.data
                elif token.type==BUFF_OPEN_PAR:
                    templine+=token.data
                elif token.type==BUFF_CLOSE_PAR:
                    templine+=token.data
                elif token.type==BUFF_EQUAL:
                    # #Don't output EQU statements that conflict with label names
                    # #(these are necessary at beginning to get macros to work,
                    # #but conflict after expansion and won't assemble.)
                    # if tokenlast.type==BUFF_ALPHA:
                    #     #Only searches for top level labels, not local labels
                    #     #since macros never assign to local label with EQU
                    #     if tokenlast.data in g.labellist:
                    #         print("EQU assign to label name",tokenlast.data)
                    if token.data!='=':templine+=' '
                    templine+=token.data
                elif token.type==BUFF_OPEN_BRACKET:
                    templine+=token.data
                elif token.type==BUFF_CLOSE_BRACKET:
                    templine+=token.data
                elif token.type==BUFF_SET:
                    templine+=' '
                    templine+=token.data
                elif token.type==BUFF_INSTRUCTION:
                    templine+=token.data
                elif token.type==BUFF_XREG:
                    templine+=token.data
                elif token.type==BUFF_YREG:
                    templine+=token.data
                elif token.type==BUFF_FUNC:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_BUILTIN:
                    #Code does not exist yet to handle this situation
                    #print('Error: token marked global in file output. Something went wrong in simplification:',a.RawStr)
                    #g.errorhalt=True
                    #break

                    #Mark as unresolved
                    templine+=token.data
                    linestatus='Unresolved function!'
                elif token.type==BUFF_FUNCARG:
                    print('Error: token marked funcarg in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LABEL:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_PCSTAR:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_ASMWORD:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_FCB:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_FDB:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_SECTION:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    templine+=token.data
                elif token.type==BUFF_BOOLEAN:
                    if tokenlast.type in space_tokens: templine+=' '
                    elif tokenlast.type==BUFF_EQUAL and tokenlast.data.upper()=='EQU': templine+=' '
                    if token.data:
                        templine+='TRUE'
                    else:
                        templine+='FALSE'
                elif token.type==BUFF_GLOBAL_SIZE:
                    print('Error: token marked global size in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_GLOBAL:
                    print('Error: token marked global in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LOCAL_SIZE:
                    print('Error: token marked local size in file output. Something went wrong in simplification:',a.RawStr)
                    g.errorhalt=True
                    break
                elif token.type==BUFF_LOCAL:
                    if tokenlast.type in space_tokens: templine+=' '
                    templine+=token.data
                    linestatus='Unused local!'
                    #print('Error: token marked local in file output. Something went wrong in simplification:',a.RawStr)
                    #g.errorhalt=True
                    #break
                else:
                    print('Error: unknown token type in output:',a.type)
                    #g.errorhalt=True
                    #break
                tokenlast=token
            if g.errorhalt:
                break

            file.write('<tr><td>'+str(linenumber)+'</td><td>'+a.RawStr+'</td><td>'+templine+'</td>')
            if a.Binary!=[]:
                tempstr='<td>'
                for byte in a.Binary:
                    tempstr+="$"+hex(byte)[2:].upper()+" "
                file.write(tempstr+'</td>')
            else:
                file.write('<td></td>')
            if linestatus=='':
                if a.DelayedLabel:
                    file.write('<td bgcolor="green">Resolved (symbollic)</td>')
                else:
                    file.write('<td bgcolor="green">Resolved</td>')
            else:
                if linestatus=='Unused local!':
                    file.write('<td bgcolor="yellow">'+linestatus+'</td>')
                else:
                    file.write('<td bgcolor="red">'+linestatus+'</td>')
            file.write('</tr>')
    file.write('</table></html>')
    file.close()
    if g.errorhalt:
        sys.exit()
