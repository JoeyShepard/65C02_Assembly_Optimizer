;Main code
;=========
	;Unlimited lines per page in listing
	PAGE 0
	;Variables in zero page
	ORG $0000
	RB1_copy:
		DFS 1
	RB2_copy:
		DFS 1
	RB3_copy:
		DFS 1
	;Beginning of EEPROM code
	ORG $C000
CodeBegin:
;Constants
;=========
;Hardware
RAM_BANK1 = 	$FFE0		;0x200- 0x3FFF
RAM_BANK2 = 	$FFE1		;0x4000-0x7FFF
RAM_BANK3 = 	$FFE2		;0x8000-0xBFFF
ROM_BANK =		$FFE3		;0xC000-0xFFFF
KB_INPUT =		$FFE4
TIMER_MS4 =		$FFE5		;Current milliseconds divided by 4
TIMER_S =		$FFE6		;Current seconds
DEBUG =			$FFE7
DEBUG_HEX = 	$FFE8
DEBUG_DEC = 	$FFE9
DEBUG_DEC16 = 	$FFEA
DEBUG_TIMING =	$FFEB
;RAM/ROM bank indexes
BANK_GEN_RAM1 =	0
BANK_GEN_RAM2 =	1
BANK_GEN_RAM3 =	2
BANK_GEN_RAM4 =	3
BANK_GFX_RAM1 = 4
BANK_GFX_RAM2 = 5
BANK_GEN_ROM =	14
;RAM/ROM bank addresses
RB1 = 	$0200		;Address of RAM bank 1
RB2 = 	$4000		;Address of RAM bank 2
RB3 = 	$8000		;Address of RAM bank 3
ROMB = 	$C000		;Address of ROM bank
;Colors
R0 = 0
R1 = 1
R2 = 2
R3 = 3
G0 = 0
G1 = 4
G2 = 8
G3 = 12
B0 = 0
B1 = 16
B2 = 32
B3 = 48
COLOR_RED =			R3|G0|B0
COLOR_GREEN =		R0|G3|B0
COLOR_BLUE =		R0|G0|B3
COLOR_BLACK =		R0|G0|B0
COLOR_WHITE =		R3|G3|B3
COLOR_GRAY1 =		R1|G1|B1
COLOR_GRAY2 =		R2|G2|B2
COLOR_CUST_GRAY =	64
;Text mode
TEXT_COLUMNS =	42
TEXT_ROWS =		16
;Text mode draw mode flags
TEXT_MODE_OPAQUE = 0
TEXT_MODE_TRANSPARENT = 1
;Character codes
CHAR_ENTER =	13
;Banking macros
;==============
;Graphics macros
;===============
;Point bank 2 and 3 to grahics memory
;Pushes existing banks
;Restore banks 2 and 3 that were pushed	
hexstr set ""
;Returns string in hexstr
;debug_nl
;debug_puts
;Constants
;=========
;debug_puts
TIMING_INSTR_BEGIN =	1
TIMING_INSTR_END =		2
TIMING_INSTR_RESET =	3
TIMING_TIME_BEGIN =		4
TIMING_TIME_END =		5
TIMING_TIME_RESET =		6
TIMING_ECHO_ON =		7
TIMING_ECHO_OFF =		8
	debug_nl:
		LDA #'\\'
		STA DEBUG
		LDA #'n'
		STA DEBUG
		RTS
	debug_puts:
		;LOCAL dbg_ptr,2
		;PLA
		;STA dbg_ptr
		;PLA
		;STA dbg_ptr+1
		;LDY #1
		;.loop:
		;	LDA (dbg_ptr),Y
		;	BEQ .done
		;		INY
		;		STA DEBUG
		;BRA .loop
		;.done:
		;TYA
		;SEC
		;ADC dbg_ptr
		;STA dbg_ptr
		;LDA #0
		;ADC dbg_ptr+1
		;STA dbg_ptr+1
		;JMP (dbg_ptr)
		RTS
	main:
		LDA 0
		main_loop:
			INC A
		BRA main_loop
	setup:
		;Banks
        LDA #BANK_GEN_RAM1
        STA RAM_BANK1
        STA RB1_copy
        LDA #BANK_GEN_RAM2
        STA RAM_BANK2
        STA RB2_copy
        LDA #BANK_GEN_RAM3
        STA RAM_BANK3
        STA RB3_copy
		RTS
CodeEnd:
;Reset vector
	;.RES $FFFC-*
	ORG $FFFC
	FDB main
;Display memory usage in console
;===============================
	;Re-evaluate here since must be resolvable after first pass
CodeSize set CodeEnd-CodeBegin
	MESSAGE " "
	MESSAGE "Memory usage"
	MESSAGE "============"
counter set CodeSize
tens set 10000
outnum set 0
zeroyet set FALSE
hexstr set ""
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
counter set counter-tens
outnum set outnum+1
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
tempstr set hexstr
counter set 100*CodeSize/$4000
tens set 10000
outnum set 0
zeroyet set FALSE
hexstr set ""
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
tens set tens/10
outnum set 0
	MESSAGE "Code size: \{tempstr} bytes (\{hexstr}% of 16k bank)"
	;Tell script that prints assembler output to stop outputting
	;Eliminates double output (because of multiple passes???)
	MESSAGE "END"
