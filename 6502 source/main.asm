
;Main code
;=========
	;Unlimited lines per page in listing
	PAGE 0
	
	;Assembler console output options (off by default)
;CONSOLE_SHOW_GLOBALS =		TRUE
;CONSOLE_SHOW_LOCALS =		TRUE
;CONSOLE_SHOW_FUNCS =		TRUE

	;Optimizer options (off by default)
OPTIMIZER_CONSOLIDATE_LOCALS =	TRUE

	;Locals usage
LOCALS_BEGIN =			$20
LOCALS_END =			$7F

	;Begin of EEPROM code
	ORG $C000

	;Test assembler
		;Nothing for now

CodeBegin:
	include const.asm
	include macros.asm
	include optimizer.asm
	include builtin.asm
	include globals.asm
CharTable:
	include chartable.asm
	include output.asm
	include input.asm
	include debug.asm
		
	FUNC main, begin
		LOCAL foo
		LOCAL bar
		JSR test_funcB
		JSR test_funcE
		
		JSR setup	
		LDA #R0|G0|B1
		JSR clrscr

		JSR puts
		FCB "6502 Calculator v0.1",13,0
		JSR puts
		FCB "====================",13,0
		LDA #COLOR_WHITE
		STA fg_color
		JSR puts
		FCB "RAM free: ",0
		LDA #COLOR_GREEN
		STA fg_color
		JSR puts
		FCB "???k",13,0
		LDA #COLOR_WHITE
		STA fg_color
		JSR puts
		FCB "Code size: ",0
		LDA #COLOR_GREEN
		STA fg_color

		;code size
CodeSize set CodeEnd-CodeBegin
		;LDA #lo(CodeSize)
		;LDX #hi(CodeSize)
		LDA #$0F
		LDX #$27
		JSR put_int16
		
		LDA #COLOR_WHITE
		STA fg_color
		JSR puts
		FCB " bytes",13,13,"Ready:",0
		LDA #COLOR_GRAY2
		STA fg_color
		
		;@input_loop:
		;	JSR getch
		;	JSR putc
		;BRA @input_loop
		JSR gets
	ENDFUNC


	FUNC setup
		;Banks
		BANK1 #BANK_GEN_RAM1
		BANK2 #BANK_GEN_RAM2
		BANK3 #BANK_GEN_RAM3
		
		;Graphics
		STZ text_X
		STZ text_Y
		LDA #R0|G0|B1
		STA bg_color
		LDA #R1|G2|B3
		STA fg_color
		LDA #TEXT_MODE_OPAQUE
		STA text_draw_mode
		
		JSR test_funcE
		JSR test_funcB
	ENDFUNC

	FUNC test_funcA
		LOCAL test_var
	ENDFUNC
	
	FUNC test_funcB
		LOCAL test_var1
		LOCAL test_var2
		JSR test_funcC
		JSR test_funcD
	ENDFUNC	

	FUNC test_funcC
		LOCAL test_var1
		LOCAL test_var2
		LOCAL test_var3
	ENDFUNC	

	FUNC test_funcD
		LOCAL test_var1
		LOCAL test_var2
	ENDFUNC	
	
	FUNC test_funcE
		LOCAL test_var
		JSR test_funcC
	ENDFUNC	
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
	HexToDec CodeSize
tempstr set hexstr
	HexToDec 100*CodeSize/$4000
	MESSAGE "Code size: \{tempstr} bytes (\{hexstr}% of 16k bank)"
	IF OPTIMIZER_CONSOLIDATE_LOCALS
		MESSAGE "Locals size: optimizer will assign"
	ELSE
		HexToDec (LOCALS_INDEX-LOCALS_BEGIN)
tempstr set hexstr
		HexToDec (100*(LOCALS_INDEX-LOCALS_BEGIN))/(LOCALS_END-LOCALS_BEGIN+1)
tempstr2 set hexstr
		HexToDec (LOCALS_END-LOCALS_BEGIN+1)
		MESSAGE "Locals size: \{tempstr} bytes (\{tempstr2}% of \{hexstr} bytes)"
	ENDIF

	;Tell script that prints assembler output to stop outputting
	;Eliminates double output (because of multiple passes???)
	MESSAGE "END"

