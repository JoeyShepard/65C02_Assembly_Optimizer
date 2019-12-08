#arg1, arg2, etc are passed as str and must be cast to be used as a number.
#The main program has type info for the arguments but does not pass them
#here. You can change the main program to do that if you like.
#Return values of int and float are automatically converted. For alpha,
#string, and char, the return type is the same as the first argument
#passed, but can be cast with the built in functions alpha, str, and char.

def left(arg1,arg2): return arg1[0:int(arg2)]

def right(arg1,arg2): return arg1[-int(arg2):]

def hi(arg1): return (int(arg1)>>8)&0xFF

def lo(arg1): return int(arg1)&0xFF

def concat(arg1,arg2): return arg1+arg2

def substr(arg1,arg2,arg3): return arg1[int(arg2):int(arg3)]

def lower(arg1): return arg1.lower()

def upper(arg1): return arg1.upper()

def to_int(arg1): return int(float(arg1))

#cl=namedtuple('Command list entry','name argcount function')
  #left off to make manipulating this file easier

#text name of function, number of arguments, function
commandlist=[('left',2,left),
            ('right',2,right),
            ('hi',1,hi),
            ('lo',1,lo),
            ('concat',2,concat),
            ('substr',3,substr),
            #('lower',1,lower),
            #Alternately, define the function inline
            ('lower',1,lambda arg1: arg1.lower()),
            ('upper',1,upper),
            #Built in functions
            ('int',1,to_int),
            ('float',1,float),
            #These change type and need to be handled in the main program
            ('alpha',1,0),
            ('str',1,0),
            ('char',1,0),

            #ADD CUSTOM FUNCTIONS HERE:
            #Also, add "BUILTIN example" to your source
            ('example',2,lambda x,y:int(x)+int(y)*2)]
