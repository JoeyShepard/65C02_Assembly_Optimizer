from enum import Enum, auto

OP_LIST=['BRK', 'ORA', 'NOP', 'TSB', 'ASL', 'RMB0', 'PHP', 'BBR0', 'BPL',
        'TRB', 'RMB1', 'CLC', 'INC', 'BBR1', 'JSR', 'AND', 'BIT', 'ROL',
        'RMB2', 'PLP', 'BBR2', 'BMI', 'RMB3', 'SEC', 'DEC', 'BBR3', 'RTI',
        'EOR', 'LSR', 'RMB4', 'PHA', 'JMP', 'BBR4', 'BVC', 'RMB5', 'CLI',
        'PHY', 'BBR5', 'RTS', 'ADC', 'STZ', 'ROR', 'RMB6', 'PLA', 'BBR6',
        'BVS', 'RMB7', 'SEI', 'PLY', 'BBR7', 'BRA', 'STA', 'STY', 'STX',
        'SMB0', 'DEY', 'TXA', 'BBS0', 'BCC', 'SMB1', 'TYA', 'TXS', 'BBS1',
        'LDY', 'LDA', 'LDX', 'SMB2', 'TAY', 'TAX', 'BBS2', 'BCS', 'SMB3',
        'CLV', 'TSX', 'BBS3', 'CPY', 'CMP', 'SMB4', 'INY', 'DEX', 'WAI',
        'BBS4', 'BNE', 'SMB5', 'CLD', 'PHX', 'STP', 'BBS5', 'CPX', 'SBC',
        'SMB6', 'INX', 'BBS6', 'BEQ', 'SMB7', 'SED', 'PLX', 'BBS7', ]
#OP_LIST_INDIRECT =['ORA', 'AND', 'EOR', 'ADC', 'STA', 'LDA', 'CMP', 'SBC']
  #What was I doing here?

OP_LIST_JUMPS=['JMP','JSR','BRA','BEQ','BNE','BMI','BPL','BCS','BCC','BVC','BVS']

#Can take 8 bit or 16 bit argument
#Have to use instruction constants here, not just name of instruction since LDA/LDA,X
OP_LIST_DUAL=[]
#ZP, ZP,X, ABS, ABS,X
    #ADC
    #AND
    #CMP
    #DEC
    #EOR
    #INC
    #LDA
    #LDY
    #LSR
    #ORA
    #ROL
    #ROR
    #SBC
    #STA
    #STZ

#ZP, ZP,Y, ABS, ABS,Y
    #LDX

#ZP, ABS
    #ASL
    #CPX
    #CPY
    #STX
    #STY
    #TRB
    #TSB





#ASM_LIST=["ENDSECTION","ORG","PAGE","MESSAGE"]
#filter MESSAGE out
ASM_LIST=["ENDSECTION","ORG","org","PAGE","OUTRADIX"]

#Constants for state of buffer
BUFF_EMPTY=10
BUFF_ALPHA=20
BUFF_NUM=30
BUFF_FLOAT=40
BUFF_HEX=50
BUFF_CHAR=60
BUFF_STR=70
#BUFF_VALID=80
BUFF_OP=90
BUFF_HASH=100
BUFF_COLON=110
BUFF_COMMA=120
BUFF_OPEN_PAR=130
BUFF_CLOSE_PAR=140
BUFF_EQUAL=160
BUFF_OPEN_BRACKET=170
BUFF_CLOSE_BRACKET=180
BUFF_SET=190
BUFF_INSTRUCTION=200
BUFF_XREG=210
BUFF_YREG=220
#Function defined in assembly file
BUFF_FUNC=230
#Python function from pp_ops.py
BUFF_BUILTIN=240
BUFF_FUNCARG=250
BUFF_LABEL=260
BUFF_PCSTAR=270
BUFF_ASMWORD=280
BUFF_DFS=285
BUFF_FCB=290
BUFF_FCC=295
BUFF_FDB=300
#Own code since introduces symbol (ignored for now)
BUFF_SECTION=310
BUFF_BOOLEAN=320
BUFF_GLOBAL_SIZE=330
BUFF_GLOBAL=340
BUFF_LOCAL_SIZE=350
BUFF_LOCAL=360
BUFF_COMMENT=370
BUFF_ARG=380
BUFF_DELAYED=390

#Constant error codes
BUFF_ERR_NONE=10
BUFF_ERR_WARN=20
BUFF_ERR_FAIL=30

#Characters that end sequence
BUFF_VALID_STR=' ()[],;	'
#% is not valid in AS assembler
#BUFF_OP_STR='+-/*%~<>^'
#Also, uses symbols for logic
BUFF_OP_STR='+-/*%~<>^|&!'

#Addressing modes for op codes
class MODE(Enum):
  IMPLICIT=auto()           #CLC
  IMMED=auto()              #LDA #5
  ZP=auto()                 #LDA $12
  ZP_X=auto()               #LDA $12,X
  ZP_Y=auto()               #LDA $12,Y
  REL=auto()                #BNE Label
  ABS=auto()                #LDA $1234
  ABS_X=auto()              #LDA #1234,X
  ABS_Y=auto()              #LDA #1234,Y
  INDIRECT=auto()           #JMP (ADDRESS)
  INDIRECT_ZP=auto()        #LDA($12)
  INDIRECT_X=auto()         #LDA ($12,X)
  INDIRECT_Y=auto()         #LDA ($12),Y
  INDIRECT_ABS_X=auto()     #JMP (ADDRESS,X)
  BB=auto()                 #BBR0 $12,ADDRESS
  ARG_UNKNOWN=auto()    #ABS, ZP, INDIRECT, or INDIRECT_ZP
  ARG_UNKNOWN_X=auto()  #ABS_X, ZP_X, INDIRECT_X, INDIRECT_ABS
  ARG_UNKNOWN_Y=auto()  #ABS_Y, ZP_Y, INDIRECT_Y



