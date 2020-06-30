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

	FUNC debug_nl
		LDA #'\\'
		STA DEBUG
		LDA #'n'
		STA DEBUG
		RTS
	ENDFUNC
	
	FUNC debug_puts
		LOCAL dbg_ptr,2
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
	ENDFUNC

	