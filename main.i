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
;Constants
;=========
;Hardware
RAM_BANK1 = 	$FFE0		;0x200- 0x3FFF
RAM_BANK2 = 	$FFE1		;0x4000-0x7FFF
RAM_BANK3 = 	$FFE2		;0x8000-0xBFFF
ROM_BANK =		$FFE3		;0xC000-0xFFFF
KB_INPUT =		$FFE4
TIMER_MS4 =		$FFE5		;Current milliseconds divided by 4
DEBUG =			$FFE6
DEBUG_HEX = 	$FFE7
DEBUG_DEC = 	$FFE8
DEBUG_DEC16 = 	$FFE9
DEBUG_TIMING =	$FFEA
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
;Functions missing from assembler
;================================
;(actually these two are defined in pp_ops.py, so not needed here)
;(would be fine to define like this if preferred)
;lo	FUNCTION arg, arg#256
;hi	FUNCTION arg, arg/256
;Banking macros
;==============
;Graphics macros
;===============
;Point bank 2 and 3 to grahics memory
;Pushes existing banks
;Restore banks 2 and 3 that were pushed	
;Console output macros
;=====================
CONSOLE_SHOW_GLOBALS =		FALSE
CONSOLE_SHOW_LOCALS =		FALSE
CONSOLE_SHOW_FUNCS =		FALSE
hexstr set ""
;Returns string in hexstr
;Optimizer macros
;================
;Macros for optimizing source or setting flag for external optimizer
;Initialize macro variables
;==========================
;Optimizer options (set in main file)
;For local variables
LOCALS_INDEX set LOCALS_BEGIN
LOCALS_COUNT set 0
;Dummy value that is filled in later by external optimizer
ASSIGN_LOCAL set $FF
;Dummy value that is filled in later by external optimizer
ASSIGN_GLOBAL set $FF
;For functions
FUNC_NAME set ""
;Wrapper macros
;==============
;(actual macro laid down depends on optimizer flags above)
;Local variable macros
;=====================
;(also used for globals since they are local to top scope)
;Wrapper picks between the following two
;Just assign addresses one after another
;Don't assign addresses. Just mark and hand off to external optimizer
;Global variable macros
;======================
;Same as LOCAL macros without PUBLIC line since same scope as those symbols
;Don't assign addresses. Just mark and hand off to external optimizer
;Function macros
;===============
;Attributes listed after FUNC
;(utility macro for FUNC not to be called by user)
;Wrappers for functions built into optimizer
OPTIMIZER_BUILTIN set $FF
;Names of custom functions added to optimizer
;============================================
;Names mentioned here to appease assembler
;Functions defined in pp_ops.py
;Add custom functions there and mention here
;Dummy value for external optimizer
;OPTIMIZER_BUILTIN set $FF
example FUNCTION CUSTOM,OPTIMIZER_BUILTIN
	;hi and lo are defined in pp_ops.py but could be
	;defined here like this instead if preferred:
;lo	FUNCTION arg, arg#256
;hi	FUNCTION arg, arg/256
	;DISABLE FOR NOW!
;Dummy value for external optimizer
;OPTIMIZER_BUILTIN set $FF
hi FUNCTION CUSTOM,OPTIMIZER_BUILTIN
;Dummy value for external optimizer
;OPTIMIZER_BUILTIN set $FF
lo FUNCTION CUSTOM,OPTIMIZER_BUILTIN
;Zero page variables
;===================
;Graphics
OPTIMIZER_GLOBAL_SIZE set 1
fg_color set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
bg_color set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
text_X set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
text_Y set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
text_draw_mode set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;Arg registers (not preserved btw calls)
OPTIMIZER_GLOBAL_SIZE set 1
a0 set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
a1 set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
a2 set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
a3 set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;Bank buffers
	;Just a copy since probably can't read from output latch for RAM
OPTIMIZER_GLOBAL_SIZE set 1
RB1_copy set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
RB2_copy set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
RB3_copy set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_GLOBAL_SIZE set 1
ROMB_copy set ASSIGN_GLOBAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
CharTable:
	;" "
	FCB 0, 0, 0, 0, 0, 0, 0, 0
	;"!"
	FCB 32, 32, 32, 32, 32, 0, 32, 0
	;"""
	FCB 80, 80, 80, 0, 0, 0, 0, 0
	;"#"
	FCB 80, 80, 248, 80, 248, 80, 80, 0
	;"$"
	FCB 32, 240, 40, 112, 160, 120, 32, 0
	;"%"
	FCB 24, 152, 64, 32, 16, 200, 192, 0
	;"&"
	FCB 48, 72, 40, 16, 168, 72, 176, 0
	;"'"
	FCB 24, 16, 8, 0, 0, 0, 0, 0
	;"("
	FCB 32, 16, 8, 8, 8, 16, 32, 0
	;")"
	FCB 32, 64, 128, 128, 128, 64, 32, 0
	;"*"
	FCB 0, 32, 168, 112, 168, 32, 0, 0
	;"+"
	FCB 0, 32, 32, 248, 32, 32, 0, 0
	;","
	FCB 0, 0, 0, 0, 0, 48, 32, 16
	;"-"
	FCB 0, 0, 0, 248, 0, 0, 0, 0
	;"."
	FCB 0, 0, 0, 0, 0, 48, 48, 0
	;"/"
	FCB 0, 128, 64, 32, 16, 8, 0, 0
	;"0"
	FCB 112, 136, 200, 168, 152, 136, 112, 0
	;"1"
	FCB 32, 48, 32, 32, 32, 32, 112, 0
	;"2"
	FCB 112, 136, 128, 64, 32, 16, 248, 0
	;"3"
	FCB 248, 64, 32, 64, 128, 136, 112, 0
	;"4"
	FCB 64, 96, 80, 72, 248, 64, 64, 0
	;"5"
	FCB 248, 8, 120, 128, 128, 136, 112, 0
	;"6"
	FCB 96, 16, 8, 120, 136, 136, 112, 0
	;"7"
	FCB 248, 128, 64, 32, 16, 16, 16, 0
	;"8"
	FCB 112, 136, 136, 112, 136, 136, 112, 0
	;"9"
	FCB 112, 136, 136, 240, 128, 64, 48, 0
	;":"
	FCB 0, 48, 48, 0, 48, 48, 0, 0
	;";"
	FCB 0, 48, 48, 0, 48, 32, 16, 0
	;"<"
	FCB 64, 32, 16, 8, 16, 32, 64, 0
	;"="
	FCB 0, 0, 248, 0, 248, 0, 0, 0
	;">"
	FCB 16, 32, 64, 128, 64, 32, 16, 0
	;"?"
	FCB 112, 136, 128, 64, 32, 0, 32, 0
	;"@"
	FCB 112, 136, 128, 176, 168, 168, 112, 0
	;"A"
	FCB 32, 80, 136, 136, 248, 136, 136, 0
	;"B"
	FCB 120, 136, 136, 248, 136, 136, 120, 0
	;"C"
	FCB 112, 136, 8, 8, 8, 136, 112, 0
	;"D"
	FCB 56, 72, 136, 136, 136, 72, 56, 0
	;"E"
	FCB 248, 8, 8, 120, 8, 8, 248, 0
	;"F"
	FCB 248, 8, 8, 120, 8, 8, 8, 0
	;"G"
	FCB 112, 136, 8, 232, 136, 136, 112, 0
	;"H"
	FCB 136, 136, 136, 248, 136, 136, 136, 0
	;"I"
	FCB 112, 32, 32, 32, 32, 32, 112, 0
	;"J"
	FCB 224, 64, 64, 64, 64, 72, 48, 0
	;"K"
	FCB 136, 72, 40, 24, 40, 72, 136, 0
	;"L"
	FCB 8, 8, 8, 8, 8, 8, 248, 0
	;"M"
	FCB 136, 216, 168, 168, 136, 136, 136, 0
	;"N"
	FCB 136, 136, 152, 168, 200, 136, 136, 0
	;"O"
	FCB 112, 136, 136, 136, 136, 136, 112, 0
	;"P"
	FCB 120, 136, 136, 120, 8, 8, 8, 0
	;"Q"
	FCB 112, 136, 136, 136, 168, 72, 176, 0
	;"R"
	FCB 120, 136, 136, 120, 40, 72, 136, 0
	;"S"
	FCB 112, 136, 8, 112, 128, 136, 112, 0
	;"T"
	FCB 248, 32, 32, 32, 32, 32, 32, 0
	;"U"
	FCB 136, 136, 136, 136, 136, 136, 112, 0
	;"V"
	FCB 136, 136, 136, 136, 136, 80, 32, 0
	;"W"
	FCB 136, 136, 136, 168, 168, 216, 136, 0
	;"X"
	FCB 136, 136, 80, 32, 80, 136, 136, 0
	;"Y"
	FCB 136, 136, 80, 32, 32, 32, 32, 0
	;"Z"
	FCB 248, 128, 64, 32, 16, 8, 248, 0
	;"["
	FCB 112, 16, 16, 16, 16, 16, 112, 0
	;"\"
	FCB 0, 8, 16, 32, 64, 128, 0, 0
	;"]"
	FCB 112, 64, 64, 64, 64, 64, 112, 0
	;"^"
	FCB 32, 80, 136, 0, 0, 0, 0, 0
	;"_"
	FCB 0, 0, 0, 0, 0, 0, 248, 0
	;"`"
	FCB 8, 16, 32, 0, 0, 0, 0, 0
	;"a"
	FCB 0, 0, 112, 128, 240, 136, 240, 0
	;"b"
	FCB 8, 8, 8, 120, 136, 136, 120, 0
	;"c"
	FCB 0, 0, 112, 136, 8, 136, 112, 0
	;"d"
	FCB 128, 128, 128, 240, 136, 136, 240, 0
	;"e"
	FCB 0, 0, 112, 136, 248, 8, 112, 0
	;"f"
	FCB 96, 144, 16, 56, 16, 16, 16, 0
	;"g"
	FCB 0, 0, 240, 136, 240, 128, 112, 0
	;"h"
	FCB 8, 8, 8, 120, 136, 136, 136, 0
	;"i"
	FCB 0, 32, 0, 48, 32, 32, 112, 0
	;"j"
	FCB 64, 0, 64, 64, 64, 72, 48, 0
	;"k"
	FCB 8, 8, 72, 40, 24, 40, 72, 0
	;"l"
	FCB 48, 32, 32, 32, 32, 32, 112, 0
	;"m"
	FCB 0, 0, 88, 168, 168, 136, 136, 0
	;"n"
	FCB 0, 0, 104, 152, 136, 136, 136, 0
	;"o"
	FCB 0, 0, 112, 136, 136, 136, 112, 0
	;"p"
	FCB 0, 0, 120, 136, 248, 8, 8, 0
	;"q"
	FCB 0, 0, 240, 136, 240, 128, 128, 0
	;"r"
	FCB 0, 0, 104, 152, 8, 8, 8, 0
	;"s"
	FCB 0, 0, 112, 8, 112, 128, 120, 0
	;"t"
	FCB 16, 16, 56, 16, 16, 144, 96, 0
	;"u"
	FCB 0, 0, 136, 136, 136, 200, 176, 0
	;"v"
	FCB 0, 0, 136, 136, 136, 80, 32, 0
	;"w"
	FCB 0, 0, 136, 168, 168, 168, 80, 0
	;"x"
	FCB 0, 0, 136, 80, 32, 80, 136, 0
	;"y"
	FCB 0, 0, 136, 136, 240, 128, 112, 0
	;"z"
	FCB 0, 0, 248, 64, 32, 16, 248, 0
	;"{"
	FCB 64, 32, 32, 16, 32, 32, 64, 0
	;"|"
	FCB 32, 32, 32, 0, 32, 32, 32, 0
	;"}"
	FCB 16, 32, 32, 64, 32, 32, 16, 0
	;"~"
	FCB 64, 168, 16, 0, 0, 0, 0, 0
	;""
	FCB 0, 0, 0, 0, 0, 0, 0, 0
;clrscr
	;color in A
;putc
	;character in A
;putc_hex
	;value in A
;puts
	;data follows after JSR
;put_int16
	;low byte in A, high byte in X
	;color in A
;Beginning of clrscr funtion macro expansion
FUNC_NAME set "clrscr"
clrscr equ *
clrscr:
LOCALS_COUNT set 0
        SECTION sect_clrscr
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of clrscr function macro expansion
OPTIMIZER_LOCAL_SIZE set 2
ptr set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
line_counter set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		PHA
        LDA RB2_copy
        PHA
        LDA RB3_copy
        PHA
        LDA #BANK_GFX_RAM1
        STA RAM_BANK2
        STA RB2_copy
        LDA #BANK_GFX_RAM2
        STA RAM_BANK3
        STA RB3_copy
		LDA #hi(RB2)
		STA ptr+1
		STZ ptr
		LDY #0
		LDA #128
		STA line_counter
		TSX
		LDA $103,X
		.loop:
			STA (ptr),Y
			INY
			BNE .loop
				INC ptr+1
				DEC line_counter
		BNE .loop
        PLA
        STA RAM_BANK3
        STA RB3_copy
        PLA
        STA RAM_BANK2
        STA RB2_copy
		PLA
		JSR test_funcA
		JSR test_funcB
        ENDSECTION
        RTS
;Beginning of putc funtion macro expansion
FUNC_NAME set "putc"
putc equ *
putc:
LOCALS_COUNT set 0
        SECTION sect_putc
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of putc function macro expansion
OPTIMIZER_LOCAL_SIZE set 2
ptr set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 2
gptr set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
temp_mult set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 8
char_buff set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		;PHA
		;LDA #TIMING_INSTR_BEGIN
		;STA DEBUG_TIMING
		;PLA
		PHA
		PHX
		PHY
        LDA RB2_copy
        PHA
        LDA RB3_copy
        PHA
        LDA #BANK_GFX_RAM1
        STA RAM_BANK2
        STA RB2_copy
        LDA #BANK_GFX_RAM2
        STA RAM_BANK3
        STA RB3_copy
		TSX
		LDA $105,X
		CMP #8
		BNE .not_backspace
			LDA text_X
			BNE .backspace
				JMP .putc_ret
		.backspace:
			DEC text_X
			LDA #' '
			BRA .passed_checks
		.not_backspace:
			CMP #13
			BNE .no_newline
				STZ text_X
				LDA text_Y
				CMP #TEXT_ROWS
				BNE .newline
					;text_Y is 16 so leave it
					;ie scrolling has been disabled
					BRK
					JMP .putc_ret
		.newline:
			INC text_Y
			LDA text_Y
			CMP #TEXT_ROWS
			BNE .newline_done
				JSR .putc_scroll
				DEC text_Y
		.newline_done:
			JMP .putc_ret
		.no_newline:
			CMP #' '						;first valid character
			BCC .failed_checks
				CMP #'~'+1					;last valid character
				BCS .failed_checks
					LDX text_X
					CPX #TEXT_COLUMNS
					BCS .failed_checks	;text_X out of range
						LDX text_Y
						CPX #TEXT_ROWS
						BCS .failed_checks	;text_Y out of range
							BRA .passed_checks
		.failed_checks:
		;set error code if needed
			JMP .putc_ret
		.passed_checks:
		SEC
		SBC #32
		LDX #lo(CharTable)
		STX ptr
		LDX #hi(CharTable)
		STX ptr+1
		LDX #0
		CLC
		ROL		;all under 126, so no need to carry
		ROL
		PHA
		TXA
		ADC #0
		ROL
		TAX
		PLA
		ROL
		PHA
		TXA
		ADC ptr+1
		STA ptr+1
		PLA
		;Carry should be clear
		ADC ptr
		STA ptr
		LDA ptr+1
		ADC #0
		STA ptr+1
		LDY #0
		LDX #8
		.loop:
			LDA (ptr),Y
			;BREAK
			STA char_buff-1,X		;offset -1 since start at 8 not 7
			INY
			DEX
		BNE .loop
		LDA text_X
		;New 6 pixel wide (including space)
		;Only works if max X is <43
		CLC
		ROL
		STA temp_mult
		ADC temp_mult
		ADC temp_mult
		CLC
		ADC #lo(RB2)
		STA ptr
		;Add carry though not needed if <RB2 is 0
		LDA #0
		ADC #hi(RB2)
		STA ptr+1
		LDA text_Y
		;Carry should be clear
		;Only works if max Y <32 (currently 15)
		ROL
		ROL
		ROL
		ADC ptr+1
		STA ptr+1
		LDY #0
		LDX #8
		.draw_loop:
		LDA char_buff-1,X
		PHX
		;LDX #8
		LDX #6
		ROR
		ROR
		.draw_loop_inner:
		;Carry in doesn't matter
			ROR
			PHA
			LDA fg_color
			BCS .use_fg_color
				LDA text_draw_mode
				AND #TEXT_MODE_TRANSPARENT
				BNE .bg_trans
					LDA bg_color
			.use_fg_color:
			STA (ptr),Y
			.bg_trans:
			PLA
			INY
			DEX
		BNE .draw_loop_inner
		PLX
		DEX
		BEQ .draw_done
			LDA ptr
			CLC
			ADC #250
			STA ptr
			LDA #0
			ADC ptr+1
			STA ptr+1
			JMP .draw_loop
		.draw_done:
		INC text_X
		LDA text_X
		CMP #TEXT_COLUMNS
		BNE .adjust_XY_done
			STZ text_X
			INC text_Y
			;Check text_Y here to support scrolling
			;Otherwise, text_Y=16 and next putc aborts
			LDA text_Y
			CMP #TEXT_ROWS
			BNE .adjust_XY_done
				JSR .putc_scroll
				DEC text_Y
		.adjust_XY_done:
			JMP .putc_ret
		;JSR to here from putc
		.putc_scroll:
		LDA #hi(RB2)
		STA ptr+1
		STZ ptr
		ADC #7
		STA gptr+1
		STZ gptr
		;Number of rows
		LDX #TEXT_ROWS*8-8
		LDY #0
		.scroll_loop:
			LDA (gptr),Y
			STA (ptr),Y
			INY 
			BNE .scroll_loop
				INC ptr+1
				INC gptr+1
				DEX
		BNE .scroll_loop
		LDX #8
		LDY #0
		LDA bg_color
		.scroll_blank:
			STA (ptr),Y
			INY 
			BNE .scroll_blank
				INC ptr+1
				DEX
		BNE .scroll_blank
		RTS
		.putc_ret:
		TSX
		LDA $105,X
		CMP #8
		BNE .no_backspace_correction
			LDA text_X
			BEQ .no_backspace_correction
				DEC text_X
		.no_backspace_correction:
        PLA
        STA RAM_BANK3
        STA RB3_copy
        PLA
        STA RAM_BANK2
        STA RB2_copy
		PLY
		PLX
		PLA
		;AND #$FF	;If flags must be set
        ENDSECTION
        RTS
;Beginning of put_hex funtion macro expansion
FUNC_NAME set "put_hex"
put_hex equ *
put_hex:
LOCALS_COUNT set 0
        SECTION sect_put_hex
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of put_hex function macro expansion
		PHA
		PHX
		TAX
		LSR
		LSR
		LSR
		LSR
		CMP #10
		BPL .letter1
			CLC
			ADC #'0'
			BRA .done1
		.letter1:
		CLC
		ADC #'A'-10
		.done1:
		JSR putc
		TXA
		AND #$F
		CMP #10
		BPL .letter2
			CLC
			ADC #'0'
			BRA .done2
		.letter2:
		CLC
		ADC #'A'-10
		.done2:
		JSR putc
		PLX
		PLA
        ENDSECTION
        RTS
;Beginning of put_int16 funtion macro expansion
FUNC_NAME set "put_int16"
put_int16 equ *
put_int16:
LOCALS_COUNT set 0
        SECTION sect_put_int16
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of put_int16 function macro expansion
OPTIMIZER_LOCAL_SIZE set 2
num set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
printed set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		STA num
		STX num+1
		STZ printed
		LDX #0	;Character to print
		LDY #8	;Index into 10^x table
		.loop:
			LDA num
			SEC
			SBC .table,Y
			PHA
			LDA num+1
			SBC .table+1,Y
			BCC .underflow
				STA num+1
				PLA
				STA num
				INX
				BRA .loop
			.underflow:
			PLA
			LDA printed
			BNE .print
				TXA
				BNE .print
					BRA .test
			.print:
			LDA #1
			STA printed
			TXA
			CLC
			ADC #'0'
			JSR putc
			.test:
			CPY #0
			BEQ .done
				DEY
				DEY
				LDX #0
				BRA .loop
		.done:
		RTS
		.table:
		FDB 1
		FDB 10
		FDB 100
		FDB 1000
		FDB 10000
        ENDSECTION
        RTS
;Beginning of puts funtion macro expansion
FUNC_NAME set "puts"
puts equ *
puts:
LOCALS_COUNT set 0
        SECTION sect_puts
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of puts function macro expansion
OPTIMIZER_LOCAL_SIZE set 2
ptr set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		PLA
		STA ptr
		PLA
		STA ptr+1
		LDY #1
		.loop:
			LDA (ptr),Y
			BEQ .done
				PHY
				JSR putc
				PLY
				INY
		BRA .loop
		.done:
		INY
		TYA
		CLC
		ADC ptr
		STA ptr
		LDA ptr+1
		ADC #0
		STA ptr+1
		JMP (ptr)
        ENDSECTION
        RTS
;getch
;gets
;Constants
;=========
;gets
CURSOR_TIME = 80
GETS_BUFF_LEN = 64
	getch:
		LDA KB_INPUT
		BEQ getch
		RTS
;Beginning of gets funtion macro expansion
FUNC_NAME set "gets"
gets equ *
gets:
LOCALS_COUNT set 0
        SECTION sect_gets
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of gets function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
start_X set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
goal set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
offset set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
state set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		LDA TIMER_MS4
		CLC
		ADC #CURSOR_TIME
		STZ goal
		STZ state
		LDA text_X
		STA start_X
		BRA .cursor_draw
		.loop:
			LDA KB_INPUT
			BEQ	.cursor
				;Process keys
				BRA .loop
			.cursor:
			LDA TIMER_MS4
			CLC
			ADC offset
			CMP goal
			BMI .loop
				;This triggers too many times
				STZ offset
				LDA goal
				CLC
				ADC #CURSOR_TIME
				STA goal
				BCC .no_offset
					CLC
					ADC #CURSOR_TIME
					STA goal
					LDA #CURSOR_TIME
					STA offset
				.no_offset:
				LDA state
				EOR #$FF
				STA state
				BNE .cursor_erase
				.cursor_draw:
					LDA #'_'
					BRA .cursor_do
				.cursor_erase:
					LDA #' '
				.cursor_do:
				JSR putc
				DEC text_X
				LDA #TIMING_INSTR_END
				STA DEBUG_TIMING
				LDA #TIMING_INSTR_BEGIN
				STA DEBUG_TIMING
				JSR debug_nl
		BRA .loop
        ENDSECTION
        RTS
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
;Beginning of debug_nl funtion macro expansion
FUNC_NAME set "debug_nl"
debug_nl equ *
debug_nl:
LOCALS_COUNT set 0
        SECTION sect_debug_nl
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of debug_nl function macro expansion
		LDA #'\\'
		STA DEBUG
		LDA #'n'
		STA DEBUG
		RTS
        ENDSECTION
        RTS
;Beginning of debug_puts funtion macro expansion
FUNC_NAME set "debug_puts"
debug_puts equ *
debug_puts:
LOCALS_COUNT set 0
        SECTION sect_debug_puts
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of debug_puts function macro expansion
OPTIMIZER_LOCAL_SIZE set 2
dbg_ptr set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		PLA
		STA dbg_ptr
		PLA
		STA dbg_ptr+1
		LDY #1
		.loop:
			LDA (dbg_ptr),Y
			BEQ .done
				INY
				STA DEBUG
		BRA .loop
		.done:
		TYA
		SEC
		ADC dbg_ptr
		STA dbg_ptr
		LDA #0
		ADC dbg_ptr+1
		STA dbg_ptr+1
		JMP (dbg_ptr)
        ENDSECTION
        RTS
;Beginning of main funtion macro expansion
FUNC_NAME set "main"
BEGIN_FUNC set "main"
main equ *
main:
LOCALS_COUNT set 0
        SECTION sect_main
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of main function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
foo set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
bar set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
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
        ENDSECTION
        RTS
;Beginning of setup funtion macro expansion
FUNC_NAME set "setup"
setup equ *
setup:
LOCALS_COUNT set 0
        SECTION sect_setup
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of setup function macro expansion
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
        ENDSECTION
        RTS
;Beginning of test_funcA funtion macro expansion
FUNC_NAME set "test_funcA"
test_funcA equ *
test_funcA:
LOCALS_COUNT set 0
        SECTION sect_test_funcA
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of test_funcA function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
test_var set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
        ENDSECTION
        RTS
;Beginning of test_funcB funtion macro expansion
FUNC_NAME set "test_funcB"
test_funcB equ *
test_funcB:
LOCALS_COUNT set 0
        SECTION sect_test_funcB
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of test_funcB function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
test_var1 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
test_var2 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		JSR test_funcC
		JSR test_funcD
        ENDSECTION
        RTS
;Beginning of test_funcC funtion macro expansion
FUNC_NAME set "test_funcC"
test_funcC equ *
test_funcC:
LOCALS_COUNT set 0
        SECTION sect_test_funcC
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of test_funcC function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
test_var1 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
test_var2 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
test_var3 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
        ENDSECTION
        RTS
;Beginning of test_funcD funtion macro expansion
FUNC_NAME set "test_funcD"
test_funcD equ *
test_funcD:
LOCALS_COUNT set 0
        SECTION sect_test_funcD
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of test_funcD function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
test_var1 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
OPTIMIZER_LOCAL_SIZE set 1
test_var2 set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
        ENDSECTION
        RTS
;Beginning of test_funcE funtion macro expansion
FUNC_NAME set "test_funcE"
test_funcE equ *
test_funcE:
LOCALS_COUNT set 0
        SECTION sect_test_funcE
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of test_funcE function macro expansion
OPTIMIZER_LOCAL_SIZE set 1
test_var set ASSIGN_LOCAL
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
		JSR test_funcC
        ENDSECTION
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
counter set counter-tens
outnum set outnum+1
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
hexstr set hexstr+","
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
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
counter set counter-tens
outnum set outnum+1
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
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
counter set counter-tens
outnum set outnum+1
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
zeroyet set TRUE
hexstr set hexstr+"\{outnum}"
tens set tens/10
outnum set 0
	MESSAGE "Code size: \{tempstr} bytes (\{hexstr}% of 16k bank)"
		MESSAGE "Locals size: optimizer will assign"
	;Tell script that prints assembler output to stop outputting
	;Eliminates double output (because of multiple passes???)
	MESSAGE "END"
