foo set 7
f   FUNCTION ax,ax*2
g   FUNCTION ax,ax*3
i   FUNCTION ax,ay,2*ax+ay*3
	LDA f(g(f(6)))+g(3)	  				;6*2*3*2=72+3*3=81
	LDA i(i(2,3),i(f(1+3),g(5))+foo)	;26+180+24=230
main:
foo set 5
value set 7+foo
	LDA value
foo set 9
	LDA value
derp:	FUNCTION arg, arg*2
bar		FUNCTION arg, arg+5
	LDA derp(6)
	LDA bar(7)
e set 5
d set e+4
c set d+3
b set c+2
ape set b+1
	LDA ape
	LDA derp(ape)
	LDA bar(ape)
	LDA e
;Works on mine but not here sunce multiple passes required
;ape set b+1
;b set c+2
;c set d+3
;d set e+4
;e set 5
	;BUILTIN lo, hi
;Dummy value for external optimizer
OPTIMIZER_BUILTIN set $FF
lo FUNCTION CUSTOM,OPTIMIZER_BUILTIN
;Dummy value for external optimizer
OPTIMIZER_BUILTIN set $FF
hi FUNCTION CUSTOM,OPTIMIZER_BUILTIN
	LDA lo($1234+foo)
	LDA hi($1234)
boo set 1+foo
	LDA boo*boo
argtest1	FUNCTION ax,ay,az,ax*2+ay*3+az*4+5
argtest2:	FUNCTION ax,ay,az,2*ax+3*ay+4*az+5
argtest3:	FUNCTION ax,ay,ax*ay+ax*ay
argtest4: 	FUNCTION ax, ax+boo
	LDA argtest1(1,2,3)   ;1*2+2*3+3*4+5 = 2+6+12+5 = 25
	LDA argtest2(2,3,4)   ;2*2+3*3+4*4+5 = 4+9+16+5 = 34
	LDA argtest1(1,2,3)*2 ;= 50 (30 is wrong!)
	LDA argtest2(2,3,4)*2 ;= 68 (39 is wrong!)
	LDA argtest3(5,7)	  ;= 70
	LDA argtest3(1+2,3+4) ;(1+2)*(3+4)+(1+2)*(3+4) = 42
						  ;1+2*3+4+1+2*3+4 = 1+6+5+6+4 = 22 is wrong!
	LDA argtest4(7)		  ;17
foo SET 15
	LDA argtest4(7)		  ;Still 17!
boo set 15
	LDA argtest4(7)		  ;22
f2	equ f(5)+boo	;10+15=25
	LDA f2			;25
boo set 10
	LDA f2			;25 not 20!
h   FUNCTION ax,ax*4+blob
	LDA h(7)		;Parse 2 - unresolved, then 33
blob set 5
	
	JMP main
	
	;BUILTIN example
	;LDA example(2,3)	;Should be 8 not 7
;Test that functions and builtins work
