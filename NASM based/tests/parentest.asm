		;Check parenthesis function
		LDA $5678
		LDA $5678+$1234
		LDA ($5678)+$1234
		LDA $5678+($1234)
		LDA ($5678)+($1234)
		
		LDA $5678,Y
		LDA $5678+$1234,Y
		LDA ($5678)+$1234,Y
		LDA $5678+($1234),Y
		LDA ($5678)+($1234),Y

		LDA ($5678,X)
		LDA ($5678+$1234,X)
		LDA (($5678)+$1234,X)
		LDA (($5678+$1234),X)
		LDA (($5678)+($1234),X)
		
		LDA ($5678),Y
		LDA ($5678+$1234),Y
		LDA (($5678)+$1234),Y
		LDA (($5678+$1234)),Y
		LDA (($5678)+($1234)),Y
		
		LDA #$5678
		LDA #$5678+$1234
		LDA #($5678)+$1234
		LDA #$5678+($1234)
		LDA #($5678)+($1234)
		