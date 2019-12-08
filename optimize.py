import globals as g
from const import *
from collections import namedtuple
from simplify import *
import turtle

Localvar=namedtuple('Localvar','Name Parent Size Address')
Token=namedtuple('Token','data type')

#Generate local addresses and assign to locallist
def GenerateLocals(consolidate):
    if consolidate:
        #Assigned in GenerateCallGraph
        #TODO: move generation code from there to here to make more clear
        g.globals_end=g.ZP_counter
        g.locals_begin=g.ZP_counter
        g.locals_end=max([a.Address+a.Size for a in g.locallist.values() if a.Address!=None])
        #print([a.Address+a.Size for a in g.locallist.values() if a.Address!=None])

    else:
        g.globals_end=g.ZP_counter
        g.locals_begin=g.ZP_counter
        for k in g.locallist.keys():
            local=g.locallist[k]
            g.locallist[k]=Localvar(local.Name, local.Parent, local.Size, g.ZP_counter)
            g.ZP_counter+=local.Size
        g.locals_end=g.ZP_counter
    if g.locals_end-1>g.locals_limit:
        print("Error: out of zero page memory. Range can be adjusted in source with LOCALS_BEGIN and LOCALS_END.")
        print("   Allowed range: $"+hex(g.globals_begin).upper()[2:]+"-$"+hex(g.locals_limit).upper()[2:]+" ("+str(g.locals_limit-g.globals_begin+1)+" bytes)")
        print("   Requested memory:",g.locals_end-g.globals_begin),"bytes"
        sys.exit()

#Assign locals to the value contained in locallist
def AssignLocals():
    g.passcount+=1
    print("Pass:",g.passcount,"- assigning variables")
    for k,line in enumerate(g.proglist):
        if line.LocalVar:
            calculate=False
            for j,symbol in enumerate(line.TokenList):
                if symbol.type==BUFF_LOCAL:
                    if g.locallist[line.LastLabel+"."+symbol.data].Address==None:
                        calculate=False
                    else:
                        g.proglist[k].TokenList[j]=Token(g.locallist[line.LastLabel+"."+symbol.data].Address,BUFF_NUM)
                        calculate=True
                    #print('Local:',symbol.data)
                    #print('  ',g.locallist[line.LastLabel+"."+symbol.data])
            if calculate:
                #print("   Before:",[a.data for a in line.TokenList])
                retobj=CalculateLine(line.TokenList,line)
                if retobj.Error==BUFF_ERR_FAIL:
                    sys.exit()
                g.proglist[k].TokenList=retobj.TokenList
                #line=g.proglist[k]
                #print("   After:",[a.data for a in line.TokenList])
                #print()
    if g.globals_end-g.globals_begin==0:
        print("   Globals: 0 bytes")
    else:
        print("   Globals:","$"+hex(g.globals_begin).upper()[2:]+"-$"+hex(g.globals_end-1).upper()[2:],"("+str(g.globals_end-g.globals_begin),"bytes)")
    if g.locals_end-g.locals_begin==0:
        print("   Locals: 0 bytes")
    else:
        print("   Locals:","$"+hex(g.locals_begin).upper()[2:]+"-$"+hex(g.locals_end-1).upper()[2:],"("+str(g.locals_end-g.locals_begin),"bytes)")
    print("   Total:",g.locals_end-g.globals_begin,"bytes ("+str(int(100*(g.locals_end-g.globals_begin)/(g.locals_limit-g.globals_begin+1)))+"% of",g.locals_limit-g.globals_begin+1,"allocated bytes)")

def GenerateCallGraph():
#TODO: combine some of the below loops if possible
    g.passcount+=1
    print("Pass:",g.passcount,"- generating call graph")
    currentfunc=""
    calllist=[]
    for i,line in enumerate(g.proglist):
        if line.LastLabel!=currentfunc:
            g.callgraph[currentfunc]=g.CallGraphNodeType()
            g.callgraph[currentfunc].Leaves=calllist
            calllist=[]
            currentfunc=line.LastLabel
            #print(currentfunc)
        if len(line.TokenList)>=2:
            if line.TokenList[0].type==BUFF_INSTRUCTION and line.TokenList[0].data=="JSR":
                if line.TokenList[1].type!=BUFF_LABEL:
                    print("Error: JSR must use labels, not static addresses, for optimization to proceed.")
                    sys.exit()
                #print("   JSR",line.TokenList[1].data,line.TokenList[1].type)
                if line.TokenList[1].data[0]!='.':
                    if line.TokenList[1].data not in calllist:
                        calllist.append(line.TokenList[1].data)
                        #print("       added")
    g.callgraph[currentfunc]=g.CallGraphNodeType()
    g.callgraph[currentfunc].Leaves=calllist

    for k,v in g.callgraph.items():
        templocallist=[]
        totalbytes=0
        for k2,v2 in g.locallist.items():
            if v2.Parent==k:
                templocallist.append(v2)
                totalbytes+=v2.Size
        g.callgraph[k].Locals=templocallist
        g.callgraph[k].TotalSize=totalbytes

    # for k,v in g.callgraph.items():
    #     print(k+":",[a for a in v.Leaves])
    #     for a in v.Locals:
    #         print("  ",a.Name,a.Size)

    #Brute force search
    #Consider more efficient algorithm if this is bottleneck
    if g.begin_func not in g.callgraph:
        print("Error: beginning function",g.begin_func,"not found.")
        sys.exit()
    CallLeaf=namedtuple('CallLeaf','Name Iterator ID ParentID')
    ID_counter=0
    tempgraph=[CallLeaf(g.begin_func,iter(g.callgraph[g.begin_func].Leaves),ID_counter,None)]
    ID_counter+=1
    lastdropped=False
    treedraw=[]
    max_depth=0
    max_local_count=0
    max_local_index=None
    while tempgraph!=[]:
        try:
            templeaf=next(tempgraph[-1].Iterator)
            tempgraph.append(CallLeaf(templeaf,iter(g.callgraph[templeaf].Leaves),ID_counter,tempgraph[-1].ID))
            ID_counter+=1
            lastdropped=False
        except:
            if lastdropped==False:
                treedraw.append(tempgraph[:])
                #for i in tempgraph:
                #    print(i.Name,end=" ")
                #print("done")
                temp_local_count=0
                for i in tempgraph:
                    temp_local_count+=g.callgraph[i.Name].TotalSize
                    #print("   ",i.Name,temp_local_count)
                if temp_local_count>max_local_count:
                    max_local_index=len(treedraw)-1
                    max_local_count=temp_local_count
                if len(tempgraph)>max_depth: max_depth=len(tempgraph)
            del tempgraph[-1]
            lastdropped=True

    #print("Max index:", max_local_index, ",", max_local_count, "bytes")

    #OLD - Python turtles, see below for HTML output instead
    #(keeping layout code for turtles to use with HTML)

    #Width of tree
    # turtle.setup(width=1500,height=600,startx=0,starty=0)
    # turtle.setworldcoordinates(0,600,1500,0)
    # turtle.speed(0)
    # turtle.hideturtle()
    gb_width=100
    gb_height=50
    gb_border_width=10
    gb_border_height=30
    DrawInfo=namedtuple("DrawInfo","Title Xpos Ypos ID ParentID")
    drawlist=[]

    for i in range(max_depth):
        lastID=None
        lastindex=None
        lastfunc=None
        lastwidth=0
        for j,branch in enumerate(treedraw):
            addbox=False
            if len(branch)>i:
                if lastID==None:
                    addbox=True
                    nextindex=j
                elif lastID==branch[i].ID:
                    lastwidth+=1
                    if j==len(treedraw)-1:
                        addbox=True
                        nextindex=None
                else:
                    addbox=True
                    nextindex=j
            else:
                addbox=True
                nextindex=None

            if addbox:
                if lastID!=None:
                    drawlist.append(DrawInfo(lastfunc,lastindex+(lastwidth-1)/2,i,lastID,lastParentID))
                if nextindex!=None:
                    #print("  ",i)
                    lastID=branch[i].ID
                    lastParentID=branch[i].ParentID
                    lastindex=j
                    lastfunc=branch[i].Name
                    lastwidth=1
                    if j==len(treedraw)-1:
                        drawlist.append(DrawInfo(lastfunc,lastindex+(lastwidth-1)/2,i,lastID,lastParentID))
                else:
                    lastID=None

    #OLD - Python turtles version
    # linelist={}
    # for gb in drawlist:
    #     GraphBox(gb.Xpos*(gb_width+gb_border_width),gb.Ypos*(gb_height+gb_border_height),gb_width,gb_height,gb.Title,str(g.callgraph[gb.Title].TotalSize)+" bytes")
    #     linelist[gb.ID]=(gb.Xpos*(gb_width+gb_border_width)+gb_width/2,gb.Ypos*(gb_height+gb_border_height))
    # for gb in drawlist:
    #     if gb.ParentID!=None:
    #         turtle.penup()
    #         turtle.goto(linelist[gb.ID][0],linelist[gb.ID][1])
    #         turtle.pendown()
    #         turtle.goto(linelist[gb.ParentID][0],linelist[gb.ParentID][1]+gb_height)
    #         turtle.penup()

    #OLD DEBUG - draw each path through graph without consolidating
    # for i,branch in enumerate(treedraw):
    #     for j,leaf in enumerate(branch):
    #         GraphBox(i*(gb_width+gb_border_width),j*(gb_height+gb_border_height)+300,gb_width,gb_height,leaf.Name,leaf.ID)

    #OLD - turtles version. See HTML version above
    #turtle.exitonclick()

    #NEW - output graph to html file instead of turtles in Python
    linelist={}
    HTML_data="boxlist=[];\nlinelist=[];\n"
    for gb in drawlist:
        HTML_data+="boxlist.push(["+str(gb.Xpos)+","+str(gb.Ypos)+",'"+gb.Title+"','"+str(g.callgraph[gb.Title].TotalSize)+" bytes']);\n"
        linelist[gb.ID]=(gb.Xpos,gb.Ypos)
    for gb in drawlist:
        if gb.ParentID!=None:
            HTML_data+="linelist.push(["+str(linelist[gb.ID][0])+","+str(linelist[gb.ID][1])+","+str(linelist[gb.ParentID][0])+","+str(linelist[gb.ParentID][1])+"]);\n"
    HTML_data+="graphwidth="+str(len(treedraw))+";\n"
    HTML_data+="graphheight="+str(max_depth)+";\n"

    #Unique list of functions
    func_call_list={}
    #List of functions with variables left to assign
    funcs_left=set()
    for treebranch in treedraw:
        for leaf in treebranch:
            if leaf.Name not in func_call_list:
                #Note set not dict!
                func_call_list[leaf.Name]={leaf.Name}
                funcs_left.add(leaf.Name)

    #List of functions each function calls or is called by
    for treebranch in treedraw:
        for leaf in treebranch:
            func_call_list[leaf.Name]|=set([a.Name for a in treebranch])
    #print(func_call_list)

    #List of local variables to be assigned
    class LocalInfo:
        def __init__(self,Name,Func,Size,Index=0):
            self.Name=Name
            self.Func=Func
            self.Size=Size
            self.Index=Index
    # assigned_locals=[]
    mem_list=[]
    #First, put longest path in memory list
    for func in treedraw[max_local_index]:
        funcs_left.remove(func.Name)
        for local in g.callgraph[func.Name].Locals:
            g.locallist[func.Name+"."+local.Name]=Localvar(local.Name,func.Name,local.Size,len(mem_list)+g.ZP_counter)
            #print(func.Name+"."+local.Name+":"+str(len(mem_list)+g.locals_begin))
            if local.Size==1:
                mem_list.append([LocalInfo(local.Name,func.Name,1)])
            else:
                for i in range(local.Size):
                    mem_list.append([LocalInfo(local.Name,func.Name,local.Size,i)])

    #Assign remaining variables
    #TODO: find faster allocation algorithm!
    for func in funcs_left:
        for local in g.callgraph[func].Locals:
            #print("Allocating",func+"."+local.Name)
            byte_progress=0
            address_found=False
            potential_address=0
            for i,addresslist in enumerate(mem_list):
                #Is there a variable from the current function already at that location?
                if func not in [a.Func for a in addresslist]:
                    #Do any of the functions using this memory conflict with this function?
                    conflictfound=False
                    for func2 in func_call_list[func]:
                        if func2 in [a.Func for a in addresslist]:
                            conflictfound=True
                            byte_progress=0
                            potential_address=i+1
                            #print("   ",func,"not in initial but related",func2,"in",[a.Func for a in addresslist])
                            break
                    if conflictfound==False:
                        byte_progress+=1
                        if byte_progress==local.Size:
                            g.locallist[func+"."+local.Name]=Localvar(local.Name,func,local.Size,potential_address+g.ZP_counter)
                            #print(func+"."+local.Name+":"+str(potential_address+g.locals_begin))
                            for byte in range(local.Size):
                                mem_list[potential_address+byte].append(LocalInfo(local.Name,func,local.Size,byte))
                            address_found=True
                            #print("       Assigned to",potential_address)
                            break
                else:
                    byte_progress=0
                    potential_address=i+1
                    #print("   ",func," in",[a.Func for a in addresslist])
            if address_found==False:
                g.locallist[func+"."+local.Name]=Localvar(local.Name,func,local.Size,potential_address+g.ZP_counter)
                #print(func+"."+local.Name+":"+str(potential_address+g.locals_begin))
                for byte in range(local.Size):
                    mem_list[potential_address+byte].append(LocalInfo(local.Name,func,local.Size,byte))
                    address_found=True
                    #print("       No room found! Assigning to ",potential_address)

    max_row_length=0
    for row in mem_list:
        if len(row)>max_row_length:max_row_length=len(row)
        HTML_data+="tabledata.push(["
        for var in row:
            if HTML_data[-1]=="]": HTML_data+=","
            HTML_data+="['"+str(var.Func)+"','"+str(var.Name)+"',"+str(var.Size)+","+str(var.Index)+"]"
        HTML_data+="]);\n"
    HTML_data+="max_row_length="+str(max_row_length)+";\n"

    try:
        fptr=open("debug\\template.html",mode="r")
    except:
        print("Error: unable to open debug template.")
        sys.exit()
    templatelines=fptr.read().splitlines()
    fptr.close()
    outputlines=[]
    for line in templatelines:
        if line.strip()=="//PAYLOAD GOES HERE":
            outputlines.append(HTML_data)
        else:
            outputlines.append(line+"\n")
    try:
        fptr=open("output\\callgraph.html",mode="w")
        fptr.writelines(outputlines)
        fptr.close()
    except:
        print("Error: unable to open debug file for output.")
        sys.exit()


    # for i,localvar in enumerate(mem_list):
    #     for j in localvar:
    #         if j.Size==1:
    #             print("{:30}".format("{}. {} {}".format(i,j.Func,j.Name)),end=" | ")
    #         else:
    #             print("{:30}".format("{}. {} {} {}/{}".format(i,j.Func,j.Name,j.Index+1,j.Size)), end=" | ")
    #     print()



    print("   Done")

# #OLD - box drawing with turtles
# def GraphBox(xpos, ypos, width, height, title, title2=""):
#     turtle.penup()
#     turtle.setpos(xpos,ypos)
#     turtle.pendown()
#     turtle.seth(0)
#     turtle.fd(width)
#     turtle.left(90)
#     turtle.fd(height)
#     turtle.left(90)
#     turtle.fd(width)
#     turtle.left(90)
#     turtle.fd(height)
#     turtle.penup()
#     turtle.setpos(xpos+width/2,ypos+height/2)
#     turtle.pendown()
#     turtle.write(title,align="center",font=("Arial",12,"bold"))
#     turtle.penup()
#     turtle.setpos(xpos+width/2,ypos+height/2+16)
#     turtle.pendown()
#     turtle.write(title2,align="center",font=("Arial",12,"normal"))
#     turtle.penup()


