
;Functions missing from assembler
;================================
;(actually these two are defined in pp_ops.py, so not needed here)
;(would be fine to define like this if preferred)
;lo	FUNCTION arg, arg#256
;hi	FUNCTION arg, arg/256


;Banking macros
;==============
BANK1	MACRO	arg
	LDA arg
	STA RAM_BANK1
	STA RB1_copy
	ENDM

BANK2	MACRO	arg
	LDA arg
	STA RAM_BANK2
	STA RB2_copy
	ENDM

BANK3	MACRO	arg
	LDA arg
	STA RAM_BANK3
	STA RB3_copy
	ENDM


;Graphics macros
;===============
;Point bank 2 and 3 to grahics memory
;Pushes existing banks
ENTER_GFX_PUSH	MACRO
	LDA RB2_copy
	PHA
	LDA RB3_copy
	PHA
	
	BANK2 #BANK_GFX_RAM1
	BANK3 #BANK_GFX_RAM2
	ENDM

;Restore banks 2 and 3 that were pushed	
EXIT_GFX_PULL MACRO
	PLA
	STA RAM_BANK3
	STA RB3_copy
	PLA
	STA RAM_BANK2
	STA RB2_copy
	ENDM
	

;Console output macros
;=====================
	IFNDEF CONSOLE_SHOW_GLOBALS
CONSOLE_SHOW_GLOBALS =		FALSE
	ENDIF
	
	IFNDEF CONSOLE_SHOW_LOCALS
CONSOLE_SHOW_LOCALS =		FALSE
	ENDIF
	
	IFNDEF CONSOLE_SHOW_FUNCS
CONSOLE_SHOW_FUNCS =		FALSE
	ENDIF
	
hexstr set ""

;Returns string in hexstr
HexToDec MACRO numarg
counter set numarg
tens set 10000
outnum set 0
zeroyet set FALSE
hexstr set ""
	WHILE tens>0
		REPT 10
			IF counter>=tens
counter set counter-tens
outnum set outnum+1
			ENDIF
		ENDM
		IF ((outnum<>0)||zeroyet)
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
			IF tens=1000
hexstr set hexstr+","
			ENDIF
		ENDIF
tens set tens/10
outnum set 0
	ENDM
	ENDM

