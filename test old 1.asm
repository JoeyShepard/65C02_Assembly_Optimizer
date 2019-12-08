		LDA ($1234+$567,X)
		LDA $1234+$567,X
		
loop:	LDA 21  +3.2   *587*(7-3)/234;comment
		LDA int(3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3)
		DS Right(left("hello"*(2+(3/1)),(7-6)*((2*6)-1)),(9-4))
		LDA (lo(5*(4+3*(2+1))),X)


high	FUNCTION x, x / 256
low		FUNCTION x, x % 256
		LDA high($1234)
		LDA low($5678)
value	equ $1234+foo
        DB $65, lo($1234)
        DB [20]0
        ADC hi($1234+5)
        ADC lo($1234+5)
        LDA $1234+2+$1234+2
        DB $65, lo(2+3)
        DB [20]0
        ADC hi(2+3+5)
        ADC lo(2+3+5)
        LDA 2+3+2+2+3+2
		LDA #5
		DS SUBSTR("Hello!",2,3)	
Label:
foo		equ 17
        DB $65, lo(VALUE)
foo		equ 18
		LDA lo(VALUE)
        DB [20]0
        ADC hi(VALUE+5)
        ADC lo(VALUE+5)
        LDA VALUE+2+VALUE+2
Bar:	ADC #5
		JMP Label
		
		DB lower("AbCdE")
		DB upper("AbCdE")
		LDA example(5,7)
		
		