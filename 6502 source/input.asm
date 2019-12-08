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

	FUNC gets
		LOCAL start_X
		LOCAL goal
		LOCAL offset
		LOCAL state
		
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
	ENDFUNC

