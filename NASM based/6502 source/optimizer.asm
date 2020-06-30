;Optimizer macros
;================
;Macros for optimizing source or setting flag for external optimizer


;Initialize macro variables
;==========================
;Optimizer options (set in main file)
	IFNDEF OPTIMIZER_CONSOLIDATE_LOCALS
OPTIMIZER_CONSOLIDATE_LOCALS set FALSE
	ENDIF

;For local variables
	IFNDEF LOCALS_BEGIN
LOCALS_BEGIN set $00
	ENDIF
	
	IFNDEF LOCALS_END
LOCALS_END set $FF
	ENDIF

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
LOCAL MACRO arg1, arg2
	IF OPTIMIZER_CONSOLIDATE_LOCALS
		IF ARGCOUNT=1
			LOCAL_CONSOLIDATE arg1, 1
		ELSE
			LOCAL_CONSOLIDATE arg1, arg2
		ENDIF
	ELSE
		IF ARGCOUNT=1
			LOCAL_NO_CONSOLIDATE arg1, 1
		ELSE
			LOCAL_NO_CONSOLIDATE arg1, arg2
		ENDIF
	ENDIF
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better in listing to set to this (ie cosmetic)
LOCAL_LABEL set 0
	ENDM

GLOBAL MACRO arg1, arg2
	IF OPTIMIZER_CONSOLIDATE_LOCALS
		IF ARGCOUNT=1
			GLOBAL_CONSOLIDATE arg1, 1
		ELSE
			GLOBAL_CONSOLIDATE arg1, arg2
		ENDIF
	ELSE
		IF ARGCOUNT=1
			GLOBAL_NO_CONSOLIDATE arg1, 1
		ELSE
			GLOBAL_NO_CONSOLIDATE arg1, arg2
		ENDIF
	ENDIF
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
	ENDM


;Local variable macros
;=====================
;(also used for globals since they are local to top scope)

;Wrapper picks between the following two
;Just assign addresses one after another
LOCAL_NO_CONSOLIDATE MACRO arg1, arg2
	PUBLIC LOCALS_INDEX:PARENT
	PUBLIC LOCALS_COUNT:PARENT
	IF LOCALS_INDEX>LOCALS_END
		ERROR "Out of locals memory (local arg1 in func \{FUNC_NAME})"
	ENDIF
arg1 set LOCALS_INDEX
	IF arg2=1
		IF CONSOLE_SHOW_LOCALS
			MESSAGE "   arg1 = \{LOCALS_INDEX}"
		ENDIF
LOCALS_INDEX set LOCALS_INDEX+1
LOCALS_COUNT set LOCALS_COUNT+1
	ELSE
		IF CONSOLE_SHOW_LOCALS
			MESSAGE "   arg1 = \{LOCALS_INDEX}, \{arg2} bytes"
		ENDIF
LOCALS_INDEX set LOCALS_INDEX+arg2
LOCALS_COUNT set LOCALS_COUNT+arg2
	ENDIF
	ENDM
		
;Don't assign addresses. Just mark and hand off to external optimizer
LOCAL_CONSOLIDATE MACRO arg1, arg2
	IF arg2=1
OPTIMIZER_LOCAL_SIZE set 1
	ELSE
OPTIMIZER_LOCAL_SIZE set arg2
	ENDIF
arg1 set ASSIGN_LOCAL
	ENDM
		
		
;Global variable macros
;======================
;Same as LOCAL macros without PUBLIC line since same scope as those symbols
GLOBAL_NO_CONSOLIDATE MACRO arg1, arg2
	;PUBLIC LOCALS_INDEX:PARENT
	;PUBLIC LOCALS_COUNT:PARENT
arg1 set LOCALS_INDEX
	IF arg2=1
		IF CONSOLE_SHOW_GLOBALS
			MESSAGE "   arg1 = \{LOCALS_INDEX}"
		ENDIF
LOCALS_INDEX set LOCALS_INDEX+1
	ELSE
		IF CONSOLE_SHOW_GLOBALS
			MESSAGE "   arg1 = \{LOCALS_INDEX}, \{arg2} bytes"
		ENDIF
LOCALS_INDEX set LOCALS_INDEX+arg2
	ENDIF
	ENDM

;Don't assign addresses. Just mark and hand off to external optimizer
GLOBAL_CONSOLIDATE MACRO arg1, arg2
	IF arg2=1
OPTIMIZER_GLOBAL_SIZE set 1
	ELSE
OPTIMIZER_GLOBAL_SIZE set arg2
	ENDIF
arg1 set ASSIGN_GLOBAL
	ENDM

	
;Function macros
;===============
;Attributes listed after FUNC
;(utility macro for FUNC not to be called by user)
FUNC_ATTRIB MACRO funcname, arg
	IF UPSTRING("arg")="BEGIN"
BEGIN_FUNC set "funcname"
	ENDIF
	ENDM

FUNC MACRO arg, a0, a1, a2, a3
;Beginning of arg funtion macro expansion
FUNC_NAME set "arg"
	FUNC_ATTRIB arg, a0
arg equ *
arg:
	IF CONSOLE_SHOW_FUNCS
		MESSAGE "arg:"
	ENDIF
LOCALS_COUNT set 0
	SECTION sect_arg
;Local labels take on prefix of last accessed symbol in listing (LOCALS_COUNT)
;Looks better to set to this (ie cosmetic)
LOCAL_LABEL set 0
;End of arg function macro expansion
	ENDM

ENDFUNC MACRO
	IF CONSOLE_SHOW_FUNCS
		IF CONSOLE_SHOW_LOCALS
			IF LOCALS_COUNT=0
				MESSAGE "   (none)"
			ENDIF
		ENDIF
	ENDIF
	ENDSECTION
	RTS
	ENDM
	
	
;Wrappers for functions built into optimizer
OPTIMIZER_BUILTIN set $FF
BUILTIN MACRO arg1, arg2
;Dummy value for external optimizer
;OPTIMIZER_BUILTIN set $FF
	IF ARGCOUNT=1
arg1 FUNCTION CUSTOM,OPTIMIZER_BUILTIN
	ELSEIF ARGCOUNT=2
		IF arg=1
arg1 FUNCTION CUSTOM,OPTIMIZER_BUILTIN
		ELSEIF arg=2
arg1 FUNCTION CUSTOM,a0,OPTIMIZER_BUILTIN
		ELSEIF arg=3
arg1 FUNCTION CUSTOM,a0,a1,OPTIMIZER_BUILTIN
		ELSEIF arg=4
arg1 FUNCTION CUSTOM,a0,a1,a2,OPTIMIZER_BUILTIN
		ENDIF
	ELSE
		ERROR "Builtin arg1: expand macro for more arguments"
	ENDIF
	ENDM
	
	
	
	
	
	
