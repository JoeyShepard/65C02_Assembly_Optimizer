	
	IF CONSOLE_SHOW_GLOBALS
		MESSAGE "Globals:"
	ENDIF

;Zero page variables
;===================

;Graphics
	GLOBAL fg_color
	GLOBAL bg_color
	GLOBAL text_X
	GLOBAL text_Y
	GLOBAL text_draw_mode

;Arg registers (not preserved btw calls)
	GLOBAL a0
	GLOBAL a1
	GLOBAL a2
	GLOBAL a3

;Bank buffers
	;Just a copy since probably can't read from output latch for RAM
	GLOBAL RB1_copy
	GLOBAL RB2_copy
	GLOBAL RB3_copy
	GLOBAL ROMB_copy
