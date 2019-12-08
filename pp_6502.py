import sys
import csv
import globals as g
from const import *


def LoadInstructions():
    try:
        op_csv=open('6502 Optimizer - Instructions.csv','r')
        csv_reader = csv.reader(op_csv,delimiter=',')
    except Exception as e:
        print("Error: file not found - 6502 Optimizer - Instructions.csv")
        print("   ",str(e))
        sys.exit()

    for i in range(2):
        next(csv_reader)
    for i,row in enumerate(csv_reader):
        tempop=g.OpType()
        tempop.Hex=int(row[0],16)
        tempop.OpCode_raw=row[1]
        tempop.OpCode=row[1][:3]
        if tempop.OpCode in ["BBR","BBS","RMB","SMB"]:
            tempop.OpCode=row[1][:4]

        if len(tempop.OpCode_raw)==3:
            #print("Implicit assigned:",tempop.OpCode_raw)
            tempop.OpMode=MODE.IMPLICIT
        elif tempop.OpCode_raw[-5:]==" #$00":
            tempop.OpMode=MODE.IMMED
        elif tempop.OpCode_raw[-4:]==" $00":
            tempop.OpMode=MODE.ZP
        elif tempop.OpCode_raw[-6:]==" $00,X":
            tempop.OpMode=MODE.ZP_X
        elif tempop.OpCode_raw[-6:]==" $00,Y":
            tempop.OpMode=MODE.ZP_Y
        elif tempop.OpCode_raw[-6:]==" $0000":
            if tempop.OpCode_raw[:3] in ["BPL","BMI","BVC","BVS","BCC","BCS","BNE","BEQ","BRA"]:
                tempop.OpMode=MODE.REL
            else:
                tempop.OpMode=MODE.ABS
        elif tempop.OpCode_raw[-8:]==" $0000,X":
            tempop.OpMode=MODE.ABS_X
        elif tempop.OpCode_raw[-8:]==" $0000,Y":
            tempop.OpMode=MODE.ABS_Y
        elif tempop.OpCode_raw[-8:]==" ($0000)":
            tempop.OpMode=MODE.INDIRECT
        elif tempop.OpCode_raw[-6:]==" ($00)":
            tempop.OpMode=MODE.INDIRECT_ZP
        elif tempop.OpCode_raw[-8:]==" ($00,X)":
            tempop.OpMode=MODE.INDIRECT_X
        elif tempop.OpCode_raw[-8:]==" ($00),Y":
            tempop.OpMode=MODE.INDIRECT_Y
        elif tempop.OpCode_raw[-10:]==" ($0000,X)":
            tempop.OpMode=MODE.INDIRECT_ABS_X
        elif tempop.OpCode_raw[-10:]==" $00,$0000":
            tempop.OpMode=MODE.BB
        else:
            print("Error: instruction not recognized -",tempop.OpCode_raw)
            sys.exit()

        tempop.Size=int(row[2])
        tempop.Cycles=int(row[3])
        tempop.BCDcycle=1 if row[4]=="Yes" else 0
        tempop.Repeatable=True if row[5]=="Yes" else False
        tempop.Peephole=True if row[6]=="Yes" else False
        tempop.ReliesOnA=True if row[7]=="Y" else False
        tempop.ReliesOnX=True if row[8]=="Y" else False
        tempop.ReliesOnY=True if row[9]=="Y" else False
        tempop.ReliesOnSP=True if row[10]=="Y" else False
        tempop.ReliesOnMem=True if row[11]=="Y" else False
        tempop.ReliesOnN=True if row[12]=="Y" else False
        tempop.ReliesOnV=True if row[13]=="Y" else False
        tempop.ReliesOnB=True if row[14]=="Y" else False
        tempop.ReliesOnD=True if row[15]=="Y" else False
        tempop.ReliesOnI=True if row[16]=="Y" else False
        tempop.ReliesOnZ=True if row[17]=="Y" else False
        tempop.ReliesOnC=True if row[18]=="Y" else False
        tempop.ModifiesA=True if row[19]=="Y" else False
        tempop.ModifiesX=True if row[20]=="Y" else False
        tempop.ModifiesY=True if row[21]=="Y" else False
        tempop.ModifiesSP=True if row[22]=="Y" else False
        tempop.ModifiesMem=True if row[23]=="Y" else False
        if row[24]=="Y": tempop.ModifiesN=True
        elif row[24]=="1": tempop.ModifiesN=1
        elif row[24]=="0": tempop.ModifiesN=0
        else: tempop.ModifiesN=False
        if row[25]=="Y": tempop.ModifiesV=True
        elif row[25]=="1": tempop.ModifiesV=1
        elif row[25]=="0": tempop.ModifiesV=0
        else: tempop.ModifiesV=False
        if row[26]=="Y": tempop.ModifiesB=True
        elif row[26]=="1": tempop.ModifiesB=1
        elif row[26]=="0": tempop.ModifiesB=0
        else: tempop.ModifiesB=False
        if row[27]=="Y": tempop.ModifiesD=True
        elif row[27]=="1": tempop.ModifiesD=1
        elif row[27]=="0": tempop.ModifiesD=0
        else: tempop.ModifiesD=False
        if row[28]=="Y": tempop.ModifiesI=True
        elif row[28]=="1": tempop.ModifiesI=1
        elif row[28]=="0": tempop.ModifiesI=0
        else: tempop.ModifiesI=False
        if row[29]=="Y": tempop.ModifiesZ=True
        elif row[29]=="1": tempop.ModifiesZ=1
        elif row[29]=="0": tempop.ModifiesZ=0
        else: tempop.ModifiesZ=False
        if row[30]=="Y": tempop.ModifiesC=True
        elif row[30]=="1": tempop.ModifiesC=1
        elif row[30]=="0": tempop.ModifiesC=0
        else: tempop.ModifiesC=False

        g.instructionlist[tempop.Hex]=tempop
    op_csv.close()
    #sys.exit()


