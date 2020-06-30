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
	FUNC clrscr
		LOCAL ptr,2
		LOCAL line_counter
		PHA
		ENTER_GFX_PUSH
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
		
		EXIT_GFX_PULL
		PLA
		
		JSR test_funcA
		JSR test_funcB
	ENDFUNC

	FUNC putc
		LOCAL ptr,2
		LOCAL gptr,2
		LOCAL temp_mult
		LOCAL char_buff,8
		;PHA
		;LDA #TIMING_INSTR_BEGIN
		;STA DEBUG_TIMING
		;PLA
		PHA
		PHX
		PHY
		ENTER_GFX_PUSH
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
		EXIT_GFX_PULL
		PLY
		PLX
		PLA
		;AND #$FF	;If flags must be set
	ENDFUNC
		
	FUNC put_hex
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
	ENDFUNC

	FUNC put_int16
		LOCAL num,2
		LOCAL printed
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
	ENDFUNC	
	
	FUNC puts
		LOCAL ptr,2
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
	ENDFUNC
	
	